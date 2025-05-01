# Hand Gesture-Based Volume and Brightness Control

This project enables control of **system volume** and **screen brightness** using **hand gestures** detected via webcam using MediaPipe and OpenCV. 

- 👋 Left Hand = Volume Control  
- 👉 Right Hand = Brightness Control  
- 🤏 Thumb and Index finger distance = Level  
- 🧠 Pinky up/down = Enable/Disable adjustment  pinky finger needs to be below the index finger for changes to occur

## 🔧 Technologies Used
- [Python](https://www.python.org/)
- [MediaPipe](https://mediapipe.dev/)
- [OpenCV](https://opencv.org/)
- [pycaw](https://github.com/AndreMiras/pycaw) – for audio control (Windows only)
- [screen-brightness-control](https://pypi.org/project/screen-brightness-control/) – for controlling screen brightness

## 🎥 How It Works
- Detects left vs right hand using landmark positions.
- Calculates distance between thumb and index fingers.
- Converts that distance to either:
  - a system volume level (using `pycaw`)
  - a brightness level (using `screen-brightness-control`)
- Real-time visual feedback shown on the screen via OpenCV.


## 🚀 How to Run

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/hand-gesture-volume-brightness-control
   cd hand-gesture-volume-brightness-control
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python gest_control.py
   ```
## Author - Yusuf Solomon (Badasz)
  
