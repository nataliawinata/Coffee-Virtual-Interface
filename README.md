# ☕ Coffee Machine Virtual Interface  
### Gesture-Based Ordering System Using Computer Vision

---

## 📌 Background

Traditional coffee machines often rely on physical buttons or touchscreens as user interfaces. While effective, these methods raise concerns about hygiene and user experience—particularly in public places like cafés or restaurants. Touch-based systems can transmit germs and may overwhelm users with too many options.

This project introduces a **contactless virtual coffee ordering interface** using **hand gesture recognition** powered by **MediaPipe Hands** and **CVZone**. Users can select coffee and pastry packages with simple hand movements in front of a webcam—no physical touch required.

---

## 🎯 Project Objectives

- Build a gesture-based coffee ordering system using a webcam.
- Detect finger gestures in real time with **MediaPipe Hands**.
- Implement an intuitive menu navigation based on gesture sequences.

---

## ❓ Problem Statements

- How to create a virtual interface that recognizes hand gestures via camera?
- How to design gesture-based menu navigation with proper sequence control?

---

## ✅ Benefits

- Improves hygiene through touchless interaction.
- Introduces a more natural and intuitive user experience.
- Opens new possibilities in vending, food service, and public digital interfaces.

---

## 🧠 Technologies Used

| Component           | Description                                      |
|--------------------|--------------------------------------------------|
| **Python 3**        | Main programming language                        |
| **OpenCV**          | Image processing and webcam capture              |
| **MediaPipe Hands** | Pre-trained model for hand & finger tracking     |
| **CVZone**          | Wrapper for simplified implementation of vision  |
| **Custom Icons**    | Images used for menu interface and feedback      |

---

## 🔰 Prerequisites

Make sure you have the following installed:
- Python 3.7–3.10
- A working webcam (internal or external)

## 🛠️ Installation

### 💻 1. Clone the Repository
git bash
git clone https://github.com/nataliawinata/Coffee_Virtual_Interface.git
cd Coffee_Virtual_Interface

### 🧪 2. Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

### 📦 3. Install Dependencies
pip install opencv-python
pip install mediapipe
pip install cvzone

### ▶️ 4. Run the Application
python main.py

---

## 📄 License & Attribution

This project is inspired by the tutorial from **Computer Vision Zone** on YouTube:  
[🔗 Virtual Coffee Machine using Hand Tracking](https://youtu.be/trIwJ17YmsI)

All rights and original concepts related to the video belong to the respective author.  
This project is a **non-commercial educational adaptation** developed for learning and research purposes only.

## 🙌 Acknowledgements

- [Computer Vision Zone](https://www.computervision.zone/) for the base tutorial and explanation.
- Open-source communities that maintain libraries like **OpenCV**, **MediaPipe**, and **CVZone**.

---

> ✨ Feel free to fork this project and improve it further for academic or experimental use!
