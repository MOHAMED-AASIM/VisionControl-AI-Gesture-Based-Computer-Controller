# 🖐️ VisionControl — AI Gesture-Based Computer Controller

> **Control your computer mouse using real-time hand gestures through your webcam.**

VisionControl is an AI-powered, webcam-based computer control system that uses **MediaPipe**, **OpenCV**, and **PyAutoGUI** to recognize hand gestures and translate them into mouse actions.

The project provides both a **desktop OpenCV application** and an interactive **Streamlit web dashboard** for monitoring gestures, FPS, control status, and configuration settings.

---

## ✨ Features

* 🎥 Real-time webcam hand tracking
* 🖐️ Single-hand gesture recognition
* 🖱️ Gesture-based mouse movement
* 👆 Index finger cursor control
* 🤏 Pinch gesture for left click
* ✌️ Two-finger gesture for right click
* ✊ Closed fist to pause control
* 🖐️ Open palm to resume control
* 🎯 Configurable active control zone
* ⚡ Cursor smoothing for stable movement
* ⏱️ Click cooldown/debouncing
* 📊 Real-time FPS monitoring
* 🔍 MediaPipe hand landmark visualization
* 🌐 Streamlit interactive dashboard
* 🛡️ PyAutoGUI corner failsafe
* 🧪 Unit tests for gesture recognition and controller logic
* 💻 Windows, macOS, and Linux setup support
* 🔒 Local processing with no default cloud upload or telemetry

---

## 🎯 Project Overview

VisionControl creates a computer interaction layer between a webcam and the operating system.

The basic pipeline is:

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hand Tracking
   ↓
Hand Landmarks
   ↓
Gesture Recognition
   ↓
Mouse Controller
   ↓
Computer Cursor / Click Actions
```

The system detects hand landmarks from the webcam feed and analyzes their positions to determine the user's intended gesture.

---

## 🖐️ Supported Gestures

| Gesture                   | Action                |
| ------------------------- | --------------------- |
| ☝️ Index finger extended  | Move cursor           |
| 🤏 Thumb + index pinch    | Left click            |
| ✌️ Index + middle fingers | Right click           |
| ✊ Closed fist             | Pause cursor control  |
| 🖐️ Open palm             | Resume cursor control |

### Gesture Workflow

```text
☝️ Index Finger
      ↓
Move Mouse Cursor

🤏 Pinch
      ↓
Left Click

✌️ Two Fingers
      ↓
Right Click

✊ Fist
      ↓
Pause Control

🖐️ Open Palm
      ↓
Resume Control
```

---

## 🛠️ Technologies Used

| Technology    | Purpose                              |
| ------------- | ------------------------------------ |
| **Python**    | Main programming language            |
| **OpenCV**    | Webcam capture and image processing  |
| **MediaPipe** | Real-time hand landmark detection    |
| **PyAutoGUI** | Mouse automation                     |
| **NumPy**     | Numerical and geometric calculations |
| **Streamlit** | Interactive web dashboard            |
| **WebRTC**    | Real-time browser camera streaming   |
| **Pytest**    | Automated testing                    |

---

## 📂 Project Structure

```text
VisionControl-AI-Gesture-Based-Computer-Controller/
│
├── .cache/
│   └── hand_landmarker.task
│
├── .streamlit/
│   └── config.toml
│
├── tests/
│   ├── test_controller.py
│   ├── test_gesture_recognizer.py
│   └── test_hand_tracker.py
│
├── config.py
├── controller.py
├── dashboard.py
├── gesture_recognizer.py
├── hand_tracker.py
├── main.py
├── styles.py
│
├── requirements.txt
├── .env.example
├── .gitignore
│
├── setup_windows.bat
├── setup_unix.sh
│
├── plan.md
├── implement.md
│
├── VisionControl_PRD.pdf
└── README.md
```

---

# 💻 System Requirements

### Minimum Requirements

* Python **3.9 – 3.12**
* Standard webcam
* Windows, macOS, or Linux
* Working graphical desktop environment
* Internet connection for initial MediaPipe model download if the model is not already available

> **Important:** Python 3.13/3.14 may cause compatibility problems with some computer-vision dependencies. Python **3.10 or 3.11** is recommended for a smoother setup.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/MOHAMED-AASIM/VisionControl-AI-Gesture-Based-Computer-Controller.git
```

Move into the project directory:

```bash
cd VisionControl-AI-Gesture-Based-Computer-Controller
```

---

# 🪟 Windows Setup

### Option 1 — Automatic Setup

Run:

```powershell
setup_windows.bat
```

The setup script prepares the Python environment and installs the required dependencies.

### Option 2 — Manual Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# 🍎 macOS / 🐧 Linux Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Or use the provided setup script:

```bash
chmod +x setup_unix.sh
./setup_unix.sh
```

---

# ⚙️ Environment Configuration

The project includes:

```text
.env.example
```

Create your local environment configuration from the example:

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

You can adjust configuration values such as:

* Camera index
* Cursor smoothing
* Gesture thresholds
* Click cooldown
* Active-zone settings

---

# ▶️ Run the Desktop Application

After activating the virtual environment:

```bash
python main.py
```

The application opens the webcam and starts real-time hand tracking.

You should see information such as:

```text
Gesture: MOVE
Control: ENABLED
FPS: 30.0
```

### Exit

Press:

```text
Q
```

to close the application.

---

# 🌐 Run the Streamlit Dashboard

VisionControl also includes an interactive Streamlit dashboard.

Run:

```bash
streamlit run dashboard.py
```

The dashboard provides:

* 📹 Real-time camera stream
* 🖐️ Current gesture
* 📊 FPS
* 🟢 Control status
* 🎯 Active control zone
* ⚙️ Cursor smoothing settings
* 🤏 Pinch threshold
* ⏱️ Click cooldown
* 🔍 Landmark visibility
* 🔄 Reset settings

The dashboard keeps cursor control paused until it is explicitly enabled.

---

# 🎛️ Dashboard Settings

The dashboard includes several configurable controls.

### Cursor Smoothing

Controls how smoothly the cursor follows the detected fingertip.

Higher smoothing values can make cursor movement feel more responsive while lower values can provide a slower movement response.

### Pinch Threshold

Controls the maximum distance between the thumb and index finger for detecting a pinch.

### Click Cooldown

Prevents repeated clicks from being generated too quickly from one gesture.

### Active Zone Margin

Defines the usable area of the camera frame for cursor control.

### Show Landmarks

Displays MediaPipe hand landmarks on the camera feed.

### Enable Cursor Control

Enables or disables actual mouse control.

---

# 🧠 How Gesture Recognition Works

VisionControl uses hand landmarks detected by MediaPipe.

The system analyzes landmark positions and geometric relationships between fingers.

For example:

```text
Camera Frame
      ↓
Hand Detection
      ↓
21 Hand Landmarks
      ↓
Finger Position Analysis
      ↓
Gesture Classification
      ↓
Mouse Action
```

The recognized gesture is converted into an internal gesture state such as:

```text
MOVE
LEFT_CLICK
RIGHT_CLICK
PAUSE
RESUME
NO_HAND
UNKNOWN
```

---

# 🖱️ Mouse Control

The mouse controller maps the detected fingertip coordinates from the webcam frame to the computer screen.

The system includes:

### Active-Zone Mapping

Only a configured region of the webcam frame is used for cursor control.

### Cursor Smoothing

Reduces unwanted cursor jitter caused by small hand movements.

### Click Cooldown

Prevents multiple unintended clicks from a single gesture.

### Pause / Resume

The user can stop mouse control with a closed fist and resume it using an open palm.

---

# 🛡️ Safety Features

VisionControl includes PyAutoGUI's built-in corner failsafe.

If cursor automation behaves unexpectedly:

> Move the physical mouse to a corner of the screen.

This can trigger the PyAutoGUI failsafe and stop automated mouse actions.

### Recommended Usage

Before enabling cursor control:

1. Make sure your hand is visible.
2. Keep the camera frame clear.
3. Keep the physical mouse accessible.
4. Test gestures carefully.
5. Keep the PyAutoGUI failsafe enabled.

---

# 📷 Camera Recommendations

For better recognition:

* Use good lighting.
* Keep your hand clearly visible.
* Avoid strong backlighting.
* Use a simple background where possible.
* Keep your hand inside the active zone.
* Position the webcam at approximately eye level or slightly below.
* Avoid placing your hand too close to the camera.
* Avoid excessive motion.

---

# 🔐 Privacy

VisionControl is designed for local processing.

By default, the application:

* Does not upload camera frames.
* Does not record video.
* Does not store gesture history permanently.
* Does not require a user account.
* Does not send gesture telemetry to a cloud service.

The webcam feed is processed locally by the application.

---

# 🧪 Testing

The project contains automated tests under:

```text
tests/
```

Run the test suite:

```bash
python -m pytest
```

Run a Python syntax/compile check:

```bash
python -m compileall .
```

The tests focus on areas such as:

* Gesture recognition
* Gesture thresholds
* Controller behavior
* Hand-tracking related logic

---

# 🧩 Troubleshooting

## Camera Not Opening

Check that:

* Your webcam is connected.
* Another application is not using the webcam.
* Camera permissions are enabled.
* The configured camera index is correct.

You can change the camera configuration through the project settings.

---

## MediaPipe Model Error

The project uses the MediaPipe Tasks API and may require:

```text
hand_landmarker.task
```

The model can be stored in:

```text
.cache/hand_landmarker.task
```

If the model is not available, ensure the application has network access during the initial setup.

---

## Cursor Does Not Move

Check that:

1. Cursor control is enabled.
2. Your hand is visible.
3. Your index finger is correctly detected.
4. You are inside the active zone.
5. The application has the required OS permissions.
6. The PyAutoGUI failsafe has not been triggered.

---

## macOS Permissions

macOS may require permissions for:

* Camera
* Accessibility
* Screen Recording

Check:

```text
System Settings
→ Privacy & Security
```

and provide the required permissions to the terminal/Python application.

---

## Linux Permissions

Linux systems may require:

* An active graphical desktop session
* Camera access
* Input permissions

Wayland/X11 behavior may also vary depending on the desktop environment.

---

# ⚠️ Known Limitations

Current version focuses on single-hand mouse control.

The project does not currently provide:

* Keyboard replacement
* Text input
* Multi-hand gesture control
* Voice control
* Eye tracking
* Air drawing
* Mobile/tablet support
* Cloud synchronization
* Gesture customization UI
* Packaged installers

---

# 🔮 Future Improvements

Possible future versions could include:

* 🖱️ Scroll gestures
* 🔊 Voice commands
* ⌨️ Gesture-based keyboard control
* ✋ Multi-hand interaction
* 🎮 Gesture-controlled media controls
* 📱 Mobile support
* 🎨 Custom gesture mapping
* 📈 Advanced performance analytics
* 🤖 Additional AI-based gesture recognition
* 📦 Windows executable installer
* 🧠 Personalized gesture calibration

---

# 📊 Project Architecture

```text
                    ┌─────────────────┐
                    │     Webcam      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     OpenCV      │
                    │ Frame Capture    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    MediaPipe    │
                    │ Hand Landmarks  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Gesture      │
                    │   Recognizer    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Mouse Controller│
                    │    PyAutoGUI    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Computer Mouse  │
                    │  / Click Action │
                    └─────────────────┘
```

---

# 📁 Main Components

### `hand_tracker.py`

Responsible for:

* Webcam hand tracking
* MediaPipe processing
* Landmark extraction
* Landmark visualization
* Handling missing hands

### `gesture_recognizer.py`

Responsible for:

* Finger-state analysis
* Pinch detection
* Gesture classification
* Recognition thresholds

### `controller.py`

Responsible for:

* Cursor movement
* Screen coordinate mapping
* Left/right clicks
* Cursor smoothing
* Pause/resume behavior
* Click cooldown
* Safety handling

### `main.py`

Main desktop application entry point.

It connects:

```text
Tracker → Recognizer → Controller
```

### `dashboard.py`

Provides the Streamlit interface with:

* Camera stream
* Gesture information
* FPS
* Settings
* Control status
* Landmark display

### `config.py`

Central configuration module for project parameters and thresholds.

---

# 📜 Development Status

### Completed

* [x] Project foundation
* [x] Python configuration
* [x] Hand tracking
* [x] Gesture recognition
* [x] Mouse controller
* [x] Cursor smoothing
* [x] Click cooldown
* [x] Pause/resume gestures
* [x] Desktop application
* [x] Streamlit dashboard
* [x] Unit test structure
* [x] Windows setup script
* [x] Unix setup script
* [x] Documentation

### Validation

* [x] Core implementation completed
* [x] Syntax/import checking performed
* [ ] Full automated test run
* [ ] Full webcam validation
* [ ] Manual gesture validation on target hardware
* [ ] Full cross-platform validation

---

# 📚 Project Documentation

Additional project documents are included in the repository:

```text
VisionControl_PRD.pdf
CodeToCrack OpenCV Visual Roadmap.pdf
plan.md
implement.md
```

These documents describe the project requirements, implementation approach, development plan, and verification checklist.

---

# 🤝 Contributing

Contributions are welcome.

To contribute:

```bash
git clone https://github.com/MOHAMED-AASIM/VisionControl-AI-Gesture-Based-Computer-Controller.git
```

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Make your changes and test them:

```bash
python -m pytest
python -m compileall .
```

Commit your changes:

```bash
git add .
git commit -m "Add your feature"
```

Push the branch:

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 👨‍💻 Author

**Mohamed Aasim**

Cloud Computing Undergraduate
SLTC Research University, Sri Lanka

### GitHub

https://github.com/MOHAMED-AASIM

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

Add your preferred open-source license to the repository before publishing the final release.

---

## 🚀 Quick Start

For experienced users:

```bash
git clone https://github.com/MOHAMED-AASIM/VisionControl-AI-Gesture-Based-Computer-Controller.git

cd VisionControl-AI-Gesture-Based-Computer-Controller

python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Streamlit Dashboard

```bash
streamlit run dashboard.py
```

---

**VisionControl — Turning hand gestures into computer control. 🖐️💻**
