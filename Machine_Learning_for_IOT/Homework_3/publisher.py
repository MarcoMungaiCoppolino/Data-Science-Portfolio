import adafruit_dht
import uuid
import time
from datetime import datetime
from board import D4
import json
import paho.mqtt.client as mqtt

mac_address = hex(uuid.getnode())

dht_device = adafruit_dht.DHT11(D4)

# Create a new MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
try:
    client.connect('mqtt.eclipseprojects.io', 1883, keepalive=60)
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    time.sleep(5)  # Wait and retry
    

while True:
    timestamp = time.time()
    formatted_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')

    try: 
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        print(f'{formatted_time} - {mac_address}: temperature = {temperature}')
        print(f'{formatted_time} - {mac_address}: humidity = {humidity}')
        dht_device
    except:
        print(f'{formatted_time} - sensor failure')
        dht_device.exit()
        dht_device = adafruit_dht.DHT11(D4)
    
    obj = {
        "mac_address": mac_address,
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity
    }
    
    message = json.dumps(obj)
    
    client.publish('s332203', f'{message}')

    time.sleep(2)





