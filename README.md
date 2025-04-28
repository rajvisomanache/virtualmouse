# Virtual Mouse
This project implements a **Virtual Mouse** system **using hand gestures detected via webcam**.  
By simply showing different finger patterns to the camera, users can **control their computer** without touching the mouse, keyboard, or any physical button.

---

## Features

- 🖱️ **Virtual Mouse Movement** — Control your mouse pointer by moving your index finger.
- 🖱️ **Left Click, Right Click, and Double Click** — Specific finger patterns allow for different clicks.
- 🔊 **Volume Control** — Adjust system volume by changing the distance between your thumb and index finger.
- 💡 **Brightness Control** — Adjust the screen brightness using specific finger gestures.
- 📜 **Scroll Up and Down** — Use four-finger or three-finger gestures to scroll pages up or down.

---

## How It Works

- **Hand Detection** is powered by **MediaPipe**.
- **Mouse Control** is handled using the `mouse` and `pyautogui` libraries.
- **Volume Control** is achieved with the `pycaw` and `win32api` libraries.
- **Brightness Control** is managed using `screen-brightness-control`.
- The webcam captures the video feed, detects hand landmarks, and maps specific finger positions to actions.

## Requirements

*   **Hardware:** A webcam.
*   **Operating System:** Windows (due to `pycaw`, `win32api`, `comtypes` usage).
*   **Software:** Python 3.x
*   Install the required packages:

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pycaw
pip install pyautogui
pip install mouse
pip install screen-brightness-control
pip install pywin32

```

## Installation

1. Clone the repository or download the `vm.py` file.
2. Install dependencies.
3. Run the script:
   ``` bash
   vm.py
   ```

## Usage

1.  Ensure your webcam is connected and working.
2.  Navigate to the directory containing `vm.py` in your terminal or command prompt.
3.  Run the script:
    ```bash
    python vm.py
    ```
4.  A window titled 'Hand Detection and Finger Tracking' will open, showing your webcam feed.
5.  Position your hand clearly in the frame. The script will detect your hand and draw landmarks on it.
6.  Perform the gestures described below to control your computer.
7.  Press 'q' while the OpenCV window is active to quit the application.

## Gestures

The script identifies gestures based on which fingers are raised. The fingers are counted as follows:
*   `[Thumb, Index, Middle, Ring, Little]`
*   `1` means the finger is up, `0` means it's down.
*   For thumb it is reverse.

Here are the implemented controls:

1.  **Mouse Movement:** (`[1, 1, 0, 0, 0]`)
    *   **Gesture:** Index finger up, other fingers down.
    *   **Action:** Moves the mouse cursor based on the position of your index finger tip. `frameR` variable in the code defines the active area border.

2.  **Left Click:** (`[1, 1, 1, 0, 0]` - with Index/Middle close)
    *   **Gesture:** Index and Middle fingers up. Index and Middle fingers must be close together (distance < 25 pixels).
    *   **Action:** Performs a single left mouse click. There's a 2-second delay before another left click can be registered.

3.  **Right Click:** (`[1, 1, 1, 0, 1]` - with Index/Middle close)
    *   **Gesture:** Index and Middle fingers up. Index and Middle fingers must be close together (distance < 25 pixels). Little finger **must** be up.
    *   **Action:** Performs a single right mouse click. There's a 2-second delay before another right click can be registered.

4.  **Double Click:** (`[0, 0, 0, 0, 0]`)
    *   **Gesture:** Thumb must be open. Index, Middle, Ring and Little fingers down.
    *   **Action:** Performs a left mouse double-click. There's a 2-second delay before another double click can be registered.

5.  **Volume Control:** (`[0, 1, 1, 0, 0]`)
    *   **Gesture:** Thumb, Index and Middle fingers up, others down.
    *   **Action:** Adjusts system volume. The distance between the tips of your Thumb and Index finger controls the level. A volume bar is shown on the screen.

6.  **Brightness Control:** (`[0, 1, 0, 0, 1]`)
    *   **Gesture:** Thumb, Index and Little fingers up, others down.
    *   **Action:** Adjusts screen brightness. The distance between the tips of your Thumb and Index finger controls the level. A brightness bar is shown on the screen.

7.  **Scroll Up:** (`[1, 1, 1, 1, 1]`)
    *   **Gesture:** All fingers except Thumb up.
    *   **Action:** Scrolls the active window upwards.

8.  **Scroll Down:** (`[1, 1, 1, 1, 0]`)
    *   **Gesture:** Index and Middle fingers up, Thumb, Ring and Little fingers down.
    *   **Action:** Scrolls the active window downwards.

## Notes and Limitations

*   **Windows Only:** This script relies on Windows-specific libraries (`pycaw`, `win32api`) for volume and potentially other system interactions, so it won't work on macOS or Linux without modifications.
*   **Lighting and Background:** Performance depends heavily on good lighting conditions and a non-cluttered background for accurate hand detection.
*   **Gesture Sensitivity:** Some gestures might require practice to perform consistently. The closeness check for clicks (Index/Middle fingers) might need tuning (`abs(ind_x - mid_x) < 25`).
*   **Click Delay:** Left, Right, and Double clicks have a hardcoded 2-second delay to prevent accidental rapid clicks.
*   **Single Hand:** The script currently only processes the first detected hand if multiple hands are in the frame.
*   **PyAutoGUI Failsafe:** `pyautogui.FAILSAFE = False` is set. This disables the safety feature where moving the mouse cursor quickly to a corner stops the script. Be cautious, especially during development or if the script behaves unexpectedly. You can stop it by pressing 'q' in the window or using Ctrl+C in the terminal.

## Future Improvements
* Add multi-hand support.
* Add gesture training for customizable actions.
* Make it cross-platform.

---
Feel free to modify or add sections as needed!


