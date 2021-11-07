import pyautogui

screenWidth, screenHeight = pyautogui.size()

while True:
    try:
        pyautogui.move(-3,3)

    except KeyboardInterrupt:
        print('Finish with Ctrl+C')
        break