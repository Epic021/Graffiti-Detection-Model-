Graffiti Detection Model

A computer vision-powered model to detect graffiti by monitoring changes in a reference frame over time. This project uses deep learning to classify whether new content (e.g., markings or changes) in an environment qualifies as graffiti and sends alerts accordingly.

---
Project Overview

Urban environments often struggle with unauthorized graffiti. This model offers an automated solution that:
- Detects changes in a static scene.
- Classifies those changes using a deep learning model.
- Sends alerts if graffiti is detected.

Built using OpenCV for image processing and TensorFlow/Keras for graffiti classification.

---
Features

- Change Detection: Monitors live or static feeds to detect alterations from a reference frame.
- Graffiti Classification: Uses a trained CNN model to determine if the detected change is graffiti.
- SMS Alert System: Sends real-time notifications via Twilio if graffiti is detected.
- Test Suite: Easily test new frames using stored images and model predictions.

---

Tech Stack

- Language: Python
- Libraries: 
  - OpenCV
  - TensorFlow / Keras
  - NumPy
  - Twilio (for notifications)
- Model Type: Convolutional Neural Network (CNN)
