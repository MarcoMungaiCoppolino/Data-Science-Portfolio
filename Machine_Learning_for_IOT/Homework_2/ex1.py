import redis
from time import sleep, time
import adafruit_dht
import uuid
from datetime import datetime
from board import D4
import numpy as np
import sounddevice as sd
import tensorflow as tf
from scipy.signal import resample_poly
import argparse
import zipfile

MODEL_FILE_PATH = 'model2.tflite.zip'

class Spectrogram:
    def __init__(self, sampling_rate, frame_length_in_s, frame_step_in_s):
        self.frame_length = int(frame_length_in_s * sampling_rate)
        self.frame_step = int(frame_step_in_s * sampling_rate)

    def get_spectrogram(self, audio):
        if audio.dtype != tf.float32:  # Ensure input is float32
            audio = tf.cast(audio, tf.float32)
        stft = tf.signal.stft(
            audio,
            frame_length=self.frame_length,
            frame_step=self.frame_step,
            fft_length=self.frame_length
        )
        spectrogram = tf.abs(stft)
        return spectrogram

class VAD:
    def __init__(self, sampling_rate, frame_length_in_s, frame_step_in_s, dBthres, duration_thres):
        self.frame_length_in_s = frame_length_in_s
        self.frame_step_in_s = frame_step_in_s
        self.spec_processor = Spectrogram(sampling_rate, frame_length_in_s, frame_step_in_s)
        self.dBthres = dBthres
        self.duration_thres = duration_thres

    def is_silence(self, audio):
        spectrogram = self.spec_processor.get_spectrogram(audio)
        dB = 20 * tf.math.log(spectrogram + 1.e-6)
        energy = tf.math.reduce_mean(dB, axis=1)
        min_energy = tf.reduce_min(energy)
        rel_energy = energy - min_energy
        non_silence = rel_energy > self.dBthres
        non_silence_frames = tf.math.reduce_sum(tf.cast(non_silence, tf.float32))
        non_silence_duration = self.frame_length_in_s + self.frame_step_in_s * (non_silence_frames - 1)
        return non_silence_duration <= self.duration_thres

class Preprocessing: # contains padding and normalization
    def __init__(self, bit_depth=tf.int16):
        self.input_rate = 48000
        self.target_rate = 16000
        self.downsampling_factor = self.input_rate / self.target_rate
        self.max_range = bit_depth.max  # Maximum value for the given bit depth (e.g., 32767 for int16)
   
    def preprocess_audio(self, audio):
        audio_float32 = tf.cast(audio, tf.float32)
        audio_resampled = resample_poly(audio_float32, up=1, down=int(self.downsampling_factor))
        audio_tensor = tf.convert_to_tensor(audio_resampled)
        audio_tensor = tf.squeeze(audio_tensor)
        audio_normalized = audio_tensor / self.max_range
        return audio_normalized

class MFCC:
    def __init__(
        self,
        sampling_rate,
        frame_length_in_s,
        frame_step_in_s,
        num_mel_bins,
        lower_frequency,
        upper_frequency,
        num_coefficients
    ):
        self.spectrogram_processor = Spectrogram(sampling_rate, frame_length_in_s, frame_step_in_s)
        num_spectrogram_bins = self.spectrogram_processor.frame_length // 2 + 1

        self.linear_to_mel_weight_matrix = tf.signal.linear_to_mel_weight_matrix(
            num_mel_bins=num_mel_bins,
            num_spectrogram_bins=num_spectrogram_bins,
            sample_rate=sampling_rate,
            lower_edge_hertz=lower_frequency,
            upper_edge_hertz=upper_frequency
        )
        self.num_coefficients = num_coefficients

    def get_mfccs(self, audio):
        spectrogram = self.spectrogram_processor.get_spectrogram(audio)
        mel_spectrogram = tf.matmul(spectrogram, self.linear_to_mel_weight_matrix)
        log_mel_spectrogram = tf.math.log(mel_spectrogram + 1.e-6)
        mfccs = tf.signal.mfccs_from_log_mel_spectrograms(log_mel_spectrogram)
        mfccs = mfccs[..., :self.num_coefficients]
        return mfccs

# argparse is used so that the script can be run from the command line with these inputs
parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, required=True)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--user', type=str, required=True)
parser.add_argument('--password', type=str, required=True)

args = parser.parse_args()

REDIS_HOST = args.host
REDIS_PORT = args.port
REDIS_USERNAME = args.user
REDIS_PASSWORD = args.password

# Print the loaded arguments to verify they are correctly loaded
print("Arguments loaded successfully:")
print(f"REDIS_HOST: {REDIS_HOST}")
print(f"REDIS_PORT: {REDIS_PORT}")
print(f"REDIS_USERNAME: {REDIS_USERNAME}")
print(f"REDIS_PASSWORD: {REDIS_PASSWORD}")


redis_client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD
)

is_connected = redis_client.ping()
print('Redis Connected:', is_connected)

mac_address = hex(uuid.getnode())
dht_device = adafruit_dht.DHT11(D4)

# VAD Parameters
vad_processor = VAD(16000, 0.032, 0.016, 10, 0.15)

# Preprocessing instance
preprocessing = Preprocessing(tf.int16)
mfcc_processor = MFCC(
    sampling_rate=16000,
    frame_length_in_s=0.016,
    frame_step_in_s=0.008,
    num_mel_bins=10,
    lower_frequency=40,
    upper_frequency=4000,
    num_coefficients=10
)

if MODEL_FILE_PATH.endswith('.zip'):
    with zipfile.ZipFile(MODEL_FILE_PATH, 'r') as fp:
        fp.extractall('/tmp/')
        model_filename = fp.namelist()[0]
        MODEL_FILE_PATH = '/tmp/' + model_filename

# Load the "up/down" classification model provided
LABELS = ['down', 'up']
interpreter = tf.lite.Interpreter(model_path = MODEL_FILE_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Function to classify audio data using the TFLite model
def classify_audio(audio_data):
    mfcc_spectrogram = mfcc_processor.get_mfccs(audio_data)

    # Expand dimensions for batch and channel
    x_features = tf.expand_dims(mfcc_spectrogram, 0)  # Add batch dimension
    x_features = tf.expand_dims(x_features, -1)  # Add channel dimension

    # Set tensor and invoke the model
    interpreter.set_tensor(input_details[0]['index'], x_features)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])

    # Extract the predicted label and its probability
    top_index = np.argmax(output[0])
    predicted_label = LABELS[top_index]
    probability = output[0][top_index]
    return predicted_label, probability

# Global variables
data_collection_enabled = False
sampling_rate = 48000
recording_duration = 1
blocksize = recording_duration * sampling_rate
stop_checking_timer = 0

# Function to collect temperature and humidity
def collect_data():
    global dht_device  

    current_time = time()
    timestamp_ms = int(current_time * 1000)
    data_collection_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S.%f')

    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        redis_client.ts().add(f'{mac_address}:temperature', timestamp_ms, temperature)
        redis_client.ts().add(f'{mac_address}:humidity', timestamp_ms, humidity)

        print(f'{data_collection_time} - {mac_address}: temperature = {temperature}, humidity = {humidity}')
    except RuntimeError as e:
        print(f'{data_collection_time} - Sensor failure: {e}')
        # Reinitialize the sensor if there is a read error
        try:
            dht_device.exit()
        except Exception as exit_error:
            print(f"Error exiting DHT device: {exit_error}")
        dht_device = adafruit_dht.DHT11(D4)

    # Calculate dynamic sleep time to ensure consistent 2-second intervals
    elapsed_time = time() - current_time
    sleep_time = max(0, 2 - elapsed_time)  # Ensures exactly 2 seconds between reads
    sleep(sleep_time)


# Audio processing callback
def audio_callback(indata, frames, callback_time, status):
    global data_collection_enabled

    # Preprocess the audio input
    audio_preprocessed = preprocessing.preprocess_audio(indata)

    # Use VAD to check silence
    is_silenced = vad_processor.is_silence(audio_preprocessed)

    if is_silenced:
        print("Silence detected")
    else:
        print("Non-silence detected")

        # Classify the processed audio
        predicted_label, probability = classify_audio(audio_preprocessed)

        print(f"Keyword: {predicted_label}, Probability: {probability}")
        if predicted_label == 'up' and probability > 0.99:
            if data_collection_enabled:
                print("Data collection remains enabled")
            else:
                data_collection_enabled = True
                print("Data collection enabled.")
        elif predicted_label == 'down' and probability > 0.99:
            if data_collection_enabled:
                data_collection_enabled = False
                print("Data collection disabled.")
            else: 
                print("Data collection remains disabled")


# Start audio processing
with sd.InputStream(
    device=1,
    channels=1,
    dtype='int16',
    samplerate=sampling_rate,
    blocksize=blocksize,
    callback=audio_callback):
    while True:
        if data_collection_enabled:
            collect_data()
