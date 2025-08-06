# Ultimatrix - AI Virtual Mouse Controller

An advanced hand gesture-based virtual mouse system that allows you to control your computer using hand movements and gestures captured through your webcam.

## 🌟 Features

### Mouse Control
- **Cursor Movement**: Move your cursor by making a closed fist
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
- **GUI Interface**: Professional interface with live camera feed
- **Screenshot Capture**: Automatic screenshot saving to Pictures/Screenshots folder

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
   pip install opencv-python mediapipe numpy autopy pyautogui pycaw comtypes wmi pillow
   ```

### Usage

#### Option 1: GUI Interface (Recommended)
```bash
python MouseController.py
```
- Opens a professional GUI with controls and instructions
- Click START to begin hand tracking
- Live camera feed displayed on the right
- Click STOP to end session

#### Option 2: Direct Execution
```bash
python VirtualMouse.py
```
- Starts immediately with camera window
- Press 'q' to quit

## 🎮 Hand Gestures Guide

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
- Screenshots are automatically saved to `Pictures/Screenshots` folder
- Includes timestamp in filename for organization
- Visual confirmation popup appears briefly after capture

## 🛠️ Technical Details

### Architecture
- **Hand Detection**: MediaPipe Hands solution
- **Computer Vision**: OpenCV for image processing
- **Mouse Control**: AutoPy for cross-platform mouse operations
- **Audio Control**: pycaw for Windows audio management
- **Brightness Control**: WMI for Windows brightness adjustment
- **GUI Framework**: Tkinter with modern styling

### Key Components
- `HandTrackingModule.py` - Core hand detection and tracking
- `VirtualMouse.py` - Main virtual mouse functionality
- `MouseController.py` - GUI interface and controller

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
├── VirtualMouse.py          # Core virtual mouse functionality
├── MouseController.py       # GUI controller interface
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── venv/                   # Virtual environment
├── build/                  # Build files
└── dist/                   # Distribution files
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
- Ensure you have write permissions to Pictures folder
- Check if Screenshots folder is created automatically
- Verify PyAutoGUI is properly installed

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

- [ ] Multi-hand gesture support
- [ ] Custom gesture configuration
- [ ] Voice command integration
- [ ] Cross-platform brightness control
- [ ] Gesture recording and playback
- [ ] Eye tracking integration
- [ ] Mobile app companion

---

⭐ If you found this project helpful, please give it a star!

📧 For questions or suggestions, feel free to open an issue or contact the author.