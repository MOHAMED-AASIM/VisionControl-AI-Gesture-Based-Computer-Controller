# VisionControl

VisionControl is a local, webcam-based mouse controller for Windows, macOS, and Linux. It uses OpenCV and MediaPipe to recognize a small set of hand gestures and PyAutoGUI to move and click the system cursor.

## Requirements

- Python 3.9-3.12
- A standard webcam

## Setup

The default `.env` file contains the camera and gesture settings. Copy `.env.example` when creating a fresh setup, then adjust values such as `CAMERA_INDEX` or `SMOOTHING_FACTOR` if needed.

On Windows, run `setup_windows.bat`. On macOS/Linux, run:

```sh
chmod +x setup_unix.sh
./setup_unix.sh
```

Start the application from the project directory:

```sh
python main.py
```

To use the Streamlit dashboard:

```sh
streamlit run dashboard.py
```

The dashboard uses a real-time browser camera stream, processes frames locally with OpenCV and MediaPipe, shows gesture and FPS telemetry, and keeps cursor control paused until you enable it from the sidebar.

On newer Python versions, MediaPipe uses the Tasks API. The first camera start downloads `hand_landmarker.task` into `.cache` when network access is available, then loads the model from memory so non-ASCII project paths work. If downloads are blocked, download that file from the URL in `hand_tracker.py` and place it at `.cache/hand_landmarker.task`.

Press `Q` in the camera window to exit. PyAutoGUI's corner failsafe remains enabled: move the physical mouse to any screen corner to abort cursor automation.

## Gestures

| Gesture | Action |
| --- | --- |
| Index finger extended | Move cursor |
| Thumb and index pinched | Left click |
| Index and middle fingers extended | Right click |
| Closed fist | Pause control |
| Open palm | Resume control |

Keep your hand well lit and inside the displayed active zone. The camera should be at eye level or slightly below, with a plain background where possible.

## Platform permissions

macOS may require Accessibility permission for the terminal or Python interpreter, plus Camera and Screen Recording permission depending on the system configuration. Linux desktop environments may require an active graphical session and input permissions. Windows generally needs no additional permission, though endpoint security software can block simulated input.

## Development

```sh
python -m pytest
python -m compileall .
```

All processing is local. The application does not upload, record, persist, or transmit camera frames or gesture data.