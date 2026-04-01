from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
import sys

class RoxUI(QLabel):

    def __init__(self):

        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.movie = QMovie("idle.gif")
        self.setMovie(self.movie)
        self.movie.start()

        self.resize(300,300)

    def set_state(self, state):

        if state == "idle":
            self.movie.setFileName("idle.gif")

        if state == "listen":
            self.movie.setFileName("listen.gif")

        if state == "talk":
            self.movie.setFileName("talk.gif")

        self.movie.start()


def start_ui():

    app = QApplication(sys.argv)
    ui = RoxUI()
    ui.show()

    sys.exit(app.exec_())