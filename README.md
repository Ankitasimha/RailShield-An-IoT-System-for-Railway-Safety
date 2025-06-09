# RailShield-An-IoT-System-for-Railway-Safety
RailShield is a real-time railway safety monitoring system built using IoT devices, edge computing, and deep learning. The system is designed to detect track-side obstacles, fire/smoke incidents, and environmental anomalies—aiming to reduce accidents and improve the reliability of railway operations.

Key Features:
🔥 Fire and Smoke Detection using a Pi Camera and lightweight CNN model (MobileNetV2).

📡 Real-Time Alerting via email notifications to railway authorities.

🌡️ Temperature & Humidity Monitoring using DHT11 sensors.

🚧 Obstacle Detection with IR sensors to detect objects on or near the tracks.

🧠 On-Device Inference using Raspberry Pi for edge processing.

🛎️ Emergency Panic Button for manual hazard alerts.

📨 Chose email alerts over SMS due to better security, traceability, and ease of implementation.

Tech Stack:
Hardware: Raspberry Pi 4 (8GB), DHT11, IR Sensor, Pi Camera, Buzzer, Push Button

Software: Python 3.9, Thonny IDE, OpenCV, TensorFlow/Keras, RPi.GPIO

Alert System: SMTP (Email) Integration and GSM module used for buzzer alerts.

Model: MobileNetV2 (trained for fire/smoke image classification)

Results:
Achieved high accuracy in fire/smoke classification.

Real-time email alerts sent within seconds of anomaly detection.

Tested in lab and semi-outdoor conditions with consistent performance.
