# 📡 Machine Learning for IoT - Course Reports  

This repository contains reports from the *Machine Learning for IoT* course at **Politecnico di Torino**. The reports focus on various aspects of **machine learning and data management in IoT systems**, covering topics such as sensor data processing, embedded ML model optimization, and IoT communication protocols.  

## 📑 Contents  

### 🔹 Homework 1: Time Series Processing & Voice Activity Detection  
This assignment explores the efficient management of IoT sensor data and optimization of voice activity detection for low-power devices.  

- **Time Series Memory Optimization**  
  - Calculated storage requirements for large-scale IoT sensor data.  
  - Applied data aggregation and compression techniques to reduce memory usage.  

- **Voice Activity Detection (VAD) Optimization**  
  - Tuned hyperparameters (frame length, step, dB threshold) to improve speech detection.  
  - Evaluated the trade-off between accuracy and latency in constrained environments.  

📄 [Read Full Report](Machine_Learning_for_IOT/Homework_1/ML4IoT_HW1_Report.pdf)  

---

### 🔹 Homework 2: Keyword Spotting with TinyML  
This homework focuses on **developing a compact, efficient keyword spotting model** suitable for deployment on low-power embedded devices.  

- **Model Training & Optimization**  
  - Used **MFCCs** for feature extraction from speech signals.  
  - Designed a **lightweight CNN model** optimized for IoT constraints.  

- **TinyML Techniques**  
  - Applied **Depthwise Separable CNNs (DSCNNs)** to reduce model size.  
  - Used **structured pruning** to minimize storage while maintaining accuracy.  

📄 [Read Full Report](Machine_Learning_for_IOT/Homework_2)  

---

### 🔹 Homework 3: IoT Data Collection & Visualization  
This report covers **real-time sensor data collection, storage, and visualization** using IoT communication protocols.  

- **MQTT-Based Data Collection**  
  - Implemented real-time data streaming from a **DHT-11 sensor** on a **Raspberry Pi**.  
  - Published sensor readings to an **MQTT broker** in structured JSON format.  

- **Data Storage & API Development**  
  - Stored sensor data using **Redis TimeSeries** for efficient retrieval.  
  - Developed a **REST API** to access historical sensor data.  
  - Implemented a **REST client** for data visualization using Deepnote.  

- **MQTT vs REST for IoT**  
  - Analyzed the trade-offs between **MQTT (low-latency, publish/subscribe model)** and **REST (request-response model)** for IoT applications.  

📄 [Read Full Report](Machine_Learning_for_IOT/Homework_3)  

---

## 🚀 Technologies Used  
- **IoT & Data Communication**: MQTT, REST APIs, Raspberry Pi  
- **Machine Learning & Optimization**: TensorFlow Lite, CNNs, VAD, keyword spotting  
- **Data Storage & Processing**: Redis TimeSeries, Deepnote  
- **Embedded Systems & TinyML**: Model compression, structured pruning  
- **Programming**: Python, Jupyter Notebooks  

## 📌 About  
These reports document practical applications of **machine learning for IoT**, focusing on:  
✅ **Efficient sensor data management**  
✅ **Deploying ML models on resource-constrained devices**  
✅ **Optimizing communication protocols for real-time data streaming**  

Feel free to explore the reports and reach out for discussions or collaborations! 🚀  
