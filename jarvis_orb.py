import sys
import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer, Qt
import sys
import numpy as np
import sounddevice as sd
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer, Qt


class JarvisOrb(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.radius = 70
        self.volume = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_orb)
        self.timer.start(40)

        self.resize(200,200)
        self.move_to_corner()

        sd.InputStream(callback=self.audio_callback).start()


    def move_to_corner(self):

        screen = QApplication.primaryScreen().geometry()

        x = screen.width() - 220
        y = 20

        self.move(x,y)


    def audio_callback(self,indata,frames,time,status):

        volume_norm = np.linalg.norm(indata)*10
        self.volume = volume_norm


    def update_orb(self):

        self.radius = 70 + int(self.volume*10)
        self.update()


    def paintEvent(self,event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        glow = QColor(0,200,255,120)
        core = QColor(0,200,255)

        painter.setBrush(glow)
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(100-self.radius,100-self.radius,
                            self.radius*2,self.radius*2)

        painter.setBrush(core)
        painter.drawEllipse(100-30,100-30,60,60)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    orb = JarvisOrb()
    orb.show()
    sys.exit(app.exec_())


class JarvisOrb(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.radius = 70

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(40)

        self.resize(200,200)

        self.move_to_corner()

    def move_to_corner(self):

        from PyQt5.QtWidgets import QApplication

        screen = QApplication.primaryScreen().geometry()

        x = screen.width() - 220
        y = 20

        self.move(x,y)

    def animate(self):

        self.radius = 70 + random.randint(-6,6)

        self.update()

    def paintEvent(self,event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        glow = QColor(0,200,255,120)
        core = QColor(0,200,255)

        painter.setBrush(glow)
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(100-self.radius,100-self.radius,
                            self.radius*2,self.radius*2)

        painter.setBrush(core)

        painter.drawEllipse(100-30,100-30,60,60)