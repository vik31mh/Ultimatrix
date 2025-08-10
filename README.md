# Ultimatrix - AI Virtual Mouse Controller

An advanced hand gesture-based virtual mouse system that allows you to control your computer using hand movements and gestures captured through your webcam. This project features a modern GUI interface built with Tkinter and provides intuitive gesture controls for mouse operations.

## 🌟 Features

### Mouse Control
- **Cursor Movement**: Navigate your cursor using hand movements
- **Left Click**: Point with your index finger only
- **Right Click**: Point with your thumb only
- **Screenshot**: Open all five fingers to capture a screenshot

### Special Control Modes
- **Scroll Mode**: Raise your pinky finger to enter scroll mode
- **Volume Control**: Raise pinky + thumb for volume adjustment
- **Brightness Control**: Raise pinky + index finger for screen brightness

### Advanced Capabilities
- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand detection
- **Smooth Mouse Movement**: Built-in smoothening algorithm for precise control
- **Multiple Gesture Recognition**: Simultaneous detection of complex hand gestures
- **Modern GUI Interface**: Professional Tkinter interface with live camera feed and controls
- **Screenshot Capture**: Automatic screenshot saving with visual confirmation
- **Cross-platform Support**: Works on Windows with full feature support

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam/Camera
- Windows OS (for volume and brightness control)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vik31mh/Ultimatrix.git
   cd Ultimatrix
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install tk opencv-python numpy mediapipe autopy pyautogui wmi Pillow pycaw comtypes
   ```

### Usage

Run the application:
```bash
python VirtualMouse.py
```

- Opens a professional GUI with controls and live camera feed
- Click "Start Camera" to begin hand tracking
- Use the gesture controls as described below
- Click "Stop Camera" to end session
- Press 'q' in the camera window to quit

## 🎮 Hand Gestures Guide

### GUI Interface Features
- **Start/Stop Camera**: Control camera activation through GUI buttons
- **Live Camera Feed**: Real-time video display in the application window
- **Status Indicators**: Visual feedback for active modes and gestures
- **File Dialogs**: Easy screenshot folder selection
- **Modern Design**: Professional dark-themed interface

### Basic Controls
| Gesture | Action |
|---------|--------|
| ![Closed Fist](docs/fist.png) | **Move Cursor** - Navigate around screen |
| ![Index Finger](docs/index.png) | **Left Click** - Single finger pointing |
| ![Thumb](docs/thumb.png) | **Right Click** - Thumb up gesture |
| ![Open Hand](docs/open-hand.png) | **Screenshot** - All five fingers open |

### Special Modes
| Gesture | Mode | Action |
|---------|------|--------|
| ![Pinky](docs/pinky.png) | **Scroll Mode** | Move hand up/down to scroll |
| ![Pinky + Thumb](docs/pinky-thumb.png) | **Volume Control** | Move hand up/down to adjust volume |
| ![Pinky + Index](docs/pinky-index.png) | **Brightness Control** | Move hand up/down to adjust brightness |

### How to Use Special Modes
1. Make the gesture to enter the mode
2. Move your hand **up** to increase (volume/brightness/scroll up)
3. Move your hand **down** to decrease (volume/brightness/scroll down)
4. Change to a different gesture to exit the mode

### Screenshot Feature
- **Open all five fingers** to capture a screenshot
- Screenshots are saved with timestamp filenames
- Visual confirmation appears after capture
- Temporary lock prevents multiple screenshots from single gesture

## 🛠️ Technical Details

### Architecture
- **Hand Detection**: MediaPipe Hands solution for robust hand tracking
- **Computer Vision**: OpenCV for image processing and camera handling
- **Mouse Control**: AutoPy and PyAutoGUI for cross-platform mouse operations
- **Audio Control**: pycaw for Windows audio management
- **Brightness Control**: WMI for Windows brightness adjustment
- **GUI Framework**: Tkinter with modern dark theme styling
- **Image Processing**: PIL (Pillow) for image manipulation and display

### Key Components
- `HandTrackingModule.py` - Core hand detection and tracking functionality
- `VirtualMouse.py` - Main application with GUI interface and virtual mouse functionality
- `requirements.txt` - Python dependencies list
- `icon.ico` - Application icon

### Performance Features
- **Optimized Frame Processing**: 30+ FPS real-time tracking
- **Smoothening Algorithm**: Reduces jitter in cursor movement
- **Gesture Debouncing**: Prevents accidental multiple clicks
- **Memory Efficient**: Minimal resource usage
- **Screenshot Lock**: Prevents multiple screenshots from single gesture

## 📁 Project Structure

```
Ultimatrix/
├── HandTrackingModule.py    # Hand detection and tracking module
├── VirtualMouse.py          # Main application with GUI and virtual mouse functionality
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── icon.ico               # Application icon
├── VirtualMouse.spec      # PyInstaller specification file
├── .gitignore            # Git ignore file
└── __pycache__/          # Python cache files
```

## 🔧 Configuration

### Adjustable Parameters
- **Camera Resolution**: 640x480 (default)
- **Smoothening Factor**: 5 (adjustable for cursor smoothness)
- **Scroll Speed**: 30 (scroll sensitivity)
- **Gesture Threshold**: 50 pixels (movement sensitivity)

### Customization
You can modify these parameters in the code:
```python
wcam, hcam = 640, 480        # Camera resolution
smoothening = 5              # Mouse smoothening
scroll_threshold = 50        # Gesture sensitivity
scroll_speed = 30           # Scroll speed
```

## 📦 Building Executable

The project includes a PyInstaller specification file for creating a standalone executable:

```bash
pip install pyinstaller
pyinstaller VirtualMouse.spec
```

This will create a distributable executable in the `dist/` folder that can run without requiring Python installation.

## 🚨 Troubleshooting

### Common Issues

**Camera not detected**
- Ensure webcam is connected and not used by other applications
- Try changing camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

**Hand tracking not working**
- Ensure good lighting conditions
- Keep hand within camera frame
- Avoid busy backgrounds

**Brightness control not working**
- Ensure you're running on Windows
- Some laptops may not support WMI brightness control
- Try updating display drivers

**Screenshot feature not working**
- Ensure the application has permission to save files in the selected directory
- Check if PyAutoGUI is properly installed
- Verify that the screenshot folder path is accessible

**Volume control not working**
- Ensure Windows audio service is running
- Check if pycaw is properly installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Vikas** - [vik31mh](https://github.com/vik31mh)

## 🙏 Acknowledgments

- **MediaPipe** - For providing excellent hand tracking solutions
- **OpenCV** - For computer vision capabilities
- **AutoPy** - For cross-platform mouse control
- **pycaw** - For Windows audio control

## 📈 Future Enhancements

- [ ] Multi-hand gesture support for advanced controls
- [ ] Customizable gesture configuration through GUI
- [ ] Gesture sensitivity adjustment settings
- [ ] Cross-platform brightness control (macOS, Linux)
- [ ] Gesture recording and macro playback
- [ ] Additional mouse gestures (double-click, drag & drop)
- [ ] Configuration file for persistent settings
- [ ] Multi-monitor support and calibration

---

⭐ If you found this project helpful, please give it a star!

📧 For questions or suggestions, feel free to open an issue or contact the author.