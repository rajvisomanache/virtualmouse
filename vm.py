import cv2
import mouse 
import numpy as np
import threading
import time
import win32api
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import mediapipe as mp
import screen_brightness_control as sbc
import math
import pyautogui

pyautogui.FAILSAFE = False

# Adjust the volume using ctypes
def set_volume(vol):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(vol, None)

# functionfor returning fingers
def fingers_up(lmList):
    fingers = []

    # Thumb
    if lmList[4][1] > lmList[3][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index finger to little finger
    for i in range(1, 5):
        if lmList[4 + i*4][2] < lmList[4 + i*4 - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# Function to get the current system volume level
def get_volume():
    return int(win32api.GetSystemMetrics(0) * 100 / 65535)

# Finger tracking function
def finger_tracking(img, lmList):
    x1, y1 = lmList[4][1], lmList[4][2]
    x2, y2 = lmList[8][1], lmList[8][2]
   
    # Marking Thumb and Index finger
    cv2.circle(img, (x1, y1), 15, (255, 255, 255))
    cv2.circle(img, (x2, y2), 15, (255, 255, 255))
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
    length = math.hypot(x2 - x1, y2 - y1)
    if length < 50:
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

    return length

# Create HandDetector instance
detector = mp.solutions.hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Volume Control Library Usage 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol, volBar, volPer = volRange[0], volRange[1], 400, 0

# Webcam Setup
wCam, hCam = 640, 480
cam = cv2.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)
d_delay=0
l_delay=0
r_delay=0

frameR = 100  
minBright = 0  # Minimum brightness level
maxBright = 100  # Maximum brightness level

def d_clk_delay():
    global d_delay
    global d_clk_thread
    time.sleep(2)
    d_delay = 0

def l_clk_delay():
    global l_delay
    global l_clk_thread
    time.sleep(2)
    l_delay = 0

def r_clk_delay():
    global r_delay
    global r_clk_thread
    time.sleep(2)
    r_delay = 0

hand_detected = False

while cam.isOpened():
    success, image = cam.read()
    if not success:
        print("Camera not working!")
        break

    image = cv2.flip(image, 1)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    

# Hand detection and landmark extraction
    results = detector.process(imageRGB)
    lmList = []

    if results.multi_hand_landmarks:
    # Choose to process only the first hand detected
        hand_landmarks = results.multi_hand_landmarks[0]

        mp.solutions.drawing_utils.draw_landmarks(
        image,
        hand_landmarks,
        mp.solutions.hands.HAND_CONNECTIONS,
        mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
        mp.solutions.drawing_styles.get_default_hand_connections_style()
    )
    
        for id, lm in enumerate(hand_landmarks.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])

    
    #print fingers
    if len(lmList) != 0:
        fingers = fingers_up(lmList)
        print(fingers)
        ind_x, ind_y = lmList[8][1], lmList[8][2]
        mid_x, mid_y = lmList[12][1], lmList[12][2]

        #mouse movement 
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1:
            conv_x = int(np.interp(ind_x, (frameR, wCam - frameR), (0, 1920)))
            conv_y = int(np.interp(ind_y, (frameR, hCam - frameR), (0, 1080)))
            mouse.move(conv_x, conv_y)
        

        # Double click
        if fingers[1] == 0 and fingers[2] == 0 and fingers[0] == 0 and fingers[4] == 0 and d_delay == 0:
            mouse.double_click(button="left")
            d_delay = 2
            threading.Thread(target=d_clk_delay).start()

        # Left click
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
            if abs(ind_x - mid_x) < 25:
                if fingers[4] == 0 and l_delay == 0:
                    mouse.click(button="left")
                    l_delay = 2
                    threading.Thread(target=l_clk_delay).start()

        # Right click
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
            if abs(ind_x - mid_x) < 25:
                if fingers[4] == 1 and r_delay == 0:
                    mouse.click(button="right")
                    r_delay = 2
                    threading.Thread(target=r_clk_delay).start()
    
        # volume up down
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and   fingers[0] == 0 and fingers[4] == 0:
            length = finger_tracking(image, lmList)
            vol = np.interp(length, [50, 220], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            volBar = np.interp(length, [50, 220], [400, 150])
            volPer = np.interp(length, [50, 220], [0, 100])
            # Volume Bar
            cv2.rectangle(image, (50, 150), (85, 400), (0, 0, 0), 3)
            cv2.rectangle(image, (50, int(volBar)), (85, 400), (0, 0, 0), cv2.FILLED)
            cv2.putText(image, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
        
        # Brightness up down
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and   fingers[0] == 0 and fingers[4] == 1:
            length = finger_tracking(image, lmList)
            brightness = np.interp(length, [50, 220], [minBright, maxBright])
            sbc.set_brightness(int(brightness))
            Bbar = np.interp(length, [50, 220], [400, 150])
            Bper = np.interp(length, [50, 220], [0, 100])
            # brightness Bar
            cv2.rectangle(image, (50, 150), (85, 400), (0, 0, 0), 3)
            cv2.rectangle(image, (50, int(Bbar)), (85, 400), (0, 0, 0), cv2.FILLED)
            cv2.putText(image, f'{int(Bper)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
        
        # UP scrolling   
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 and fingers[4] == 1 and fingers[3] == 1:
            pyautogui.scroll(50)
        
        # Down scrolling   
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 and fingers[4] == 0 and fingers[3] == 0:
            pyautogui.scroll(-50)

    cv2.imshow('Hand Detection and Finger Tracking', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
