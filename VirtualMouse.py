import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui  # For scrolling

# Webcam parameters
wcam, hcam = 640, 480
frameR = 100  # Frame reduction
smoothening = 5

# Initialize previous and current location
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Scroll tracking
scroll_mode = False
initial_scroll_y = None
scroll_threshold = 50  # Increased threshold for more stable scroll

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

# Initialize hand detector
detector = htm.handDetector(maxHands=1)

# Get screen size
wScr, hScr = autopy.screen.size()
print("Screen Size:", wScr, hScr)

pTime = 0

# Scrolling speed multiplier
scroll_speed = 30  # Increased scroll speed

while True:
    success, img = cap.read()
    if not success or img is None:
        print("❌ Failed to capture frame")
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if lmList:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[4][1:]  # Thumb tip

        fingers = detector.fingersUp()

        # 🖱 Move mouse if fist is closed
        if fingers == [0, 0, 0, 0, 0]:
            x3 = np.interp(x1, (frameR, wcam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hcam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Clamp the coordinates within screen bounds
            clocX = np.clip(clocX, 0, wScr - 1)
            clocY = np.clip(clocY, 0, hScr - 1)

            autopy.mouse.move(wScr - clocX, clocY)

            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            plocX, plocY = clocX, clocY


        # 🖱 Left-click: only index finger up
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            autopy.mouse.click(button=autopy.mouse.Button.LEFT)
            time.sleep(0.1)

        # 🖱 Right-click: only thumb up
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
            time.sleep(0.1)

        # 🔃 Scroll mode: little finger up
        if fingers[4] == 1:
            if not scroll_mode:
                scroll_mode = True
                initial_scroll_y = lmList[0][2]  # Wrist Y
                print("🟢 Scroll mode ON")

            current_y = lmList[0][2]
            delta_y = current_y - initial_scroll_y

            if delta_y > scroll_threshold:
                pyautogui.scroll(-scroll_speed)  # Scroll down (faster speed)
            elif delta_y < -scroll_threshold:
                pyautogui.scroll(scroll_speed)   # Scroll up (faster speed)

        else:
            if scroll_mode:
                scroll_mode = False
                initial_scroll_y = None
                print("🔴 Scroll mode OFF")

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (70, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Show image
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("[INFO] Clean exit")
