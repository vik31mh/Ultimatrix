import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import HandTrackingModule as htm
import autopy
import pyautogui
import time
import wmi
from PIL import Image, ImageTk
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

class VirtualMouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Virtual Mouse Controller")
        self.root.geometry("1200x650")
        self.root.configure(bg="#2c3e50")

        # Variables
        self.wcam, self.hcam = 640, 480
        self.frameR = 100
        self.smoothening = 5
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        self.scroll_mode = False
        self.volume_mode = False
        self.brightness_mode = False
        self.initial_y = None
        self.scroll_threshold = 50
        self.scroll_speed = 30
        self.is_running = False

        # Setup audio and brightness
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = interface.QueryInterface(IAudioEndpointVolume)
        except:
            self.volume = None

        try:
            self.c = wmi.WMI(namespace='wmi')
            self.brightness_methods = self.c.WmiMonitorBrightnessMethods()[0]
        except:
            self.brightness_methods = None

        self.create_widgets()

    def create_widgets(self):
        container = tk.Frame(self.root, bg="#2c3e50")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel
        left = tk.Frame(container, bg="#34495e", width=400)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        title = tk.Label(left, text="AI Virtual Mouse", font=("Arial", 18, "bold"), fg="white", bg="#34495e")
        title.pack(pady=10)

        self.status = tk.Label(left, text="Status: Stopped", font=("Arial", 12, "bold"), fg="white", bg="#34495e")
        self.status.pack(pady=5)

        # Control buttons
        control = tk.Frame(left, bg="#34495e")
        control.pack(pady=10)

        self.start_btn = tk.Button(control, text="START", font=("Arial", 14, "bold"),
                                   bg="#27ae60", fg="white", width=12, height=2,
                                   command=self.start_mouse)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = tk.Button(control, text="STOP", font=("Arial", 14, "bold"),
                                  bg="#e74c3c", fg="white", width=12, height=2,
                                  command=self.stop_mouse, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # Instructions
        instr_title = tk.Label(left, text="Hand Gestures", font=("Arial", 14, "bold"), fg="white", bg="#34495e")
        instr_title.pack(pady=5)

        instr_text = """
MOUSE MOVEMENT:
• Closed Fist → Move cursor

CLICKING:
• Index finger only → Left click
• Thumb only → Right click

SPECIAL MODES:
• Pinky only → Scroll mode
• Pinky + Thumb → Volume control
• Pinky + Index → Brightness control

HOW TO USE MODES:
• Move hand up and hold to increase
• Move hand down and hold to decrease
• Move hand back to center to stop adjusting
"""
        instr = tk.Label(left, text=instr_text, font=("Arial", 9), fg="white", bg="#34495e", justify="left", wraplength=350)
        instr.pack(pady=5, padx=5, fill="both", expand=True)

        # Right panel
        right = tk.Frame(container, bg="#2c3e50")
        right.pack(side="right", fill="both", expand=True)

        cam_title = tk.Label(right, text="Camera Feed", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        cam_title.pack(pady=10)

        self.cam_label = tk.Label(right, text="Click START to begin", font=("Arial", 18), fg="white", bg="#2c3e50",
                                  width=60, height=25)
        self.cam_label.pack(expand=True, fill="both")

    def start_mouse(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wcam)
        self.cap.set(4, self.hcam)
        self.detector = htm.handDetector(maxHands=1)
        self.wScr, self.hScr = autopy.screen.size()
        self.is_running = True
        self.status.config(text="Status: Running")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.process_video()

    def stop_mouse(self):
        self.is_running = False
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
        self.status.config(text="Status: Stopped")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.cam_label.config(image="", text="Click START to begin")

    def process_video(self):
        if not self.is_running:
            return

        success, img = self.cap.read()
        if not success:
            self.root.after(10, self.process_video)
            return

        img = self.detector.findHands(img)
        lmList, _ = self.detector.findPosition(img)

        if lmList:
            x1, y1 = lmList[8][1:]
            fingers = self.detector.fingersUp()
            little_up, thumb_up, index_up = fingers[4], fingers[0], fingers[1]

            # Volume mode: pinky + thumb
            if little_up and thumb_up and not index_up:
                if not self.volume_mode:
                    self.volume_mode = True
                    self.scroll_mode = self.brightness_mode = False
                    self.initial_y = lmList[0][2]

                delta = lmList[0][2] - self.initial_y
                if self.volume:
                    if delta > self.scroll_threshold:
                        new_vol = max(self.volume.GetMasterVolumeLevelScalar() - 0.01, 0)
                        self.volume.SetMasterVolumeLevelScalar(new_vol, None)
                    elif delta < -self.scroll_threshold:
                        new_vol = min(self.volume.GetMasterVolumeLevelScalar() + 0.01, 1)
                        self.volume.SetMasterVolumeLevelScalar(new_vol, None)

            # Scroll mode: pinky only
            elif little_up and not thumb_up and not index_up:
                if not self.scroll_mode:
                    self.scroll_mode = True
                    self.volume_mode = self.brightness_mode = False
                    self.initial_y = lmList[0][2]

                delta = lmList[0][2] - self.initial_y
                if delta > self.scroll_threshold:
                    pyautogui.scroll(-self.scroll_speed)
                elif delta < -self.scroll_threshold:
                    pyautogui.scroll(self.scroll_speed)

            # Brightness mode: pinky + index
            elif little_up and index_up and not thumb_up and fingers[2]==0 and fingers[3]==0:
                if not self.brightness_mode:
                    self.brightness_mode = True
                    self.scroll_mode = self.volume_mode = False
                    self.initial_y = lmList[0][2]

                delta = lmList[0][2] - self.initial_y
                if self.brightness_methods:
                    try:
                        brightness = self.c.WmiMonitorBrightness()[0].CurrentBrightness
                        if delta > self.scroll_threshold:
                            new_brightness = max(brightness - 1, 0)
                            self.brightness_methods.WmiSetBrightness(new_brightness, 0)
                        elif delta < -self.scroll_threshold:
                            new_brightness = min(brightness + 1, 100)
                            self.brightness_methods.WmiSetBrightness(new_brightness, 0)
                    except:
                        pass

            else:
                # Exit all modes if no matching gesture
                self.scroll_mode = self.volume_mode = self.brightness_mode = False
                self.initial_y = None

            # Mouse movement: closed fist
            if fingers == [0,0,0,0,0]:
                x3 = np.interp(x1, (self.frameR, self.wcam - self.frameR), (0, self.wScr))
                y3 = np.interp(y1, (self.frameR, self.hcam - self.frameR), (0, self.hScr))
                self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
                self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening
                try:
                    autopy.mouse.move(self.wScr - self.clocX, self.clocY)
                except:
                    pass
                self.plocX, self.plocY = self.clocX, self.clocY

            # Left click: index only
            if fingers==[0,1,0,0,0]:
                autopy.mouse.click()
                time.sleep(0.1)
            # Right click: thumb only
            if fingers==[1,0,0,0,0]:
                autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
                time.sleep(0.1)

        self.display_frame(img)
        self.root.after(10, self.process_video)

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame).resize((750, 500))
        img_tk = ImageTk.PhotoImage(img_pil)
        self.cam_label.config(image=img_tk, text="")
        self.cam_label.image = img_tk

    def on_close(self):
        self.stop_mouse()
        self.root.destroy()

if __name__=="__main__":
    root = tk.Tk()
    app = VirtualMouseApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
