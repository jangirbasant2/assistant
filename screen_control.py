import pyautogui


def click_image(image):

    location = pyautogui.locateCenterOnScreen(image,confidence=0.8)

    if location:

        pyautogui.click(location)

        return True

    return False