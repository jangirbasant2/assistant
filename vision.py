import mss
from PIL import Image
import pytesseract


def capture_screen():

    with mss.mss() as sct:

        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        return img


def read_screen_text():

    img = capture_screen()

    text = pytesseract.image_to_string(img)

    return text