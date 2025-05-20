import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui  # For scrolling

# Volume control (Windows only)
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Volume setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Webcam parameters
wcam, hcam = 640, 480
frameR = 100
smoothening = 5

plocX, plocY = 0, 0
clocX, clocY = 0, 0

scroll_mode = False
volume_mode = False
initial_y = None
scroll_threshold = 50
scroll_speed = 30

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

pTime = 0

while True:
    success, img = cap.read()
    if not success or img is None:
        print("❌ Failed to capture frame")
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if lmList:
        x1, y1 = lmList[8][1:]  # Index finger tip
        fingers = detector.fingersUp()

        # Gesture detection
        little_up = fingers[4] == 1
        thumb_up = fingers[0] == 1

        if little_up and thumb_up:
            if not volume_mode:
                volume_mode = True
                scroll_mode = False
                initial_y = lmList[0][2]
                print("🔊 Volume mode ON")

            current_y = lmList[0][2]
            delta_y = current_y - initial_y

            if delta_y > scroll_threshold:
                new_vol = max(volume.GetMasterVolumeLevelScalar() - 0.01, 0.0)
                volume.SetMasterVolumeLevelScalar(new_vol, None)
                print("🔉 Volume Down")

            elif delta_y < -scroll_threshold:
                new_vol = min(volume.GetMasterVolumeLevelScalar() + 0.01, 1.0)
                volume.SetMasterVolumeLevelScalar(new_vol, None)
                print("🔊 Volume Up")

        elif little_up and not thumb_up:
            if not scroll_mode:
                scroll_mode = True
                volume_mode = False
                initial_y = lmList[0][2]
                print("🟢 Scroll mode ON")

            current_y = lmList[0][2]
            delta_y = current_y - initial_y

            if delta_y > scroll_threshold:
                pyautogui.scroll(-scroll_speed)
                print("⬇️ Scrolling Down")
            elif delta_y < -scroll_threshold:
                pyautogui.scroll(scroll_speed)
                print("⬆️ Scrolling Up")

        else:
            if scroll_mode or volume_mode:
                scroll_mode = volume_mode = False
                initial_y = None
                print("🔴 Mode OFF")

        # Move mouse with closed fist
        if fingers == [0, 0, 0, 0, 0]:
            x3 = np.interp(x1, (frameR, wcam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hcam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            flippedX = np.clip(wScr - clocX, 0, wScr - 1)
            clocY = np.clip(clocY, 0, hScr - 1)

            try:
                autopy.mouse.move(flippedX, clocY)
            except ValueError as e:
                print(f"⚠️ Mouse move out of bounds: ({flippedX}, {clocY}) – {e}")

            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Left click: index finger only
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            autopy.mouse.click(button=autopy.mouse.Button.LEFT)
            time.sleep(0.1)

        # Right click: thumb only
        if fingers[0] == 1 and all(f == 0 for f in fingers[1:]):
            autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
            time.sleep(0.1)

    # FPS display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (70, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("[INFO] Clean exit")
