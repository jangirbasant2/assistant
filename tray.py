import pystray
from PIL import Image
import threading
import sys


def create_tray(start_fn, stop_fn):

    def start(icon,item):
        threading.Thread(target=start_fn).start()

    def stop(icon,item):
        stop_fn()

    def quit_app(icon,item):
        icon.stop()
        sys.exit()

    icon = pystray.Icon("ROS")

    icon.menu = pystray.Menu(
        pystray.MenuItem("Start ROS", start),
        pystray.MenuItem("Stop ROS", stop),
        pystray.MenuItem("Quit", quit_app)
    )

    icon.run()