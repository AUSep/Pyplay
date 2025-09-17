from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (QApplication, QPushButton, QMainWindow,
QStyle, QGridLayout, QWidget, QGraphicsDropShadowEffect,
QSizePolicy, QSlider, QLabel)
from file_browser import Browser
from marquee_label import Display
import sys
    
class VolumeSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.lay = QGridLayout(self)
        self.lay.setContentsMargins(5,5,5,5)
        self.lay.setSpacing(5)
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0,100)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.setVolume)
        self.lay.addWidget(self.slider, 0, 0, 1, 4)

        pixmapi = QStyle.StandardPixmap.SP_MediaVolume
        icon = self.style().standardIcon(pixmapi)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(icon.pixmap(24,24))
        self.lay.addWidget(icon_lbl, 0, 5)
    
    def setVolume(self):
        pass

class PlayerButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.filePath = None
        self.btn_layout = QGridLayout()
        self.setLayout(self.btn_layout)
        self.btn_layout.setContentsMargins(0,0,0,0)
        self.btn_layout.setSpacing(0)

        icon_dict={
            "Play" : QStyle.StandardPixmap.SP_MediaPlay,
            "Previous" : QStyle.StandardPixmap.SP_MediaSkipBackward,
            "Pause" : QStyle.StandardPixmap.SP_MediaPause,
            "Next" : QStyle.StandardPixmap.SP_MediaSkipForward,
            "Stop" : QStyle.StandardPixmap.SP_MediaStop,
        }

        btn_dict = self.build_player_buttons(icon_dict)

        self.__play_btn = btn_dict["Play"]
        self.__play_btn.clicked.connect(self.play)
        self.__prev_btn = btn_dict["Previous"]
        self.__prev_btn.clicked.connect(self.previous)
        self.__pause_btn = btn_dict["Pause"]
        self.__pause_btn.clicked.connect(self.pause)
        self.__pause_btn = btn_dict["Next"]
        self.__pause_btn.clicked.connect(self.next)
        self.__pause_btn = btn_dict["Stop"]
        self.__pause_btn.clicked.connect(self.stop)

        self.__volume_slider = VolumeSlider()
        self.btn_layout.addWidget(self.__volume_slider, 0, 6, 1, 2)

    def play(self):
        pass
    
    def previous(self):
        pass

    def pause(self):
        pass
    
    def next(self):
        pass

    def stop(self):
        pass

    def build_player_buttons(self, icon_dict: dict[str, QStyle.StandardPixmap]) -> dict[str, QPushButton]:
        i = 0
        btn_dct={}
        for btn_str in icon_dict:
            pixmapi = icon_dict[btn_str]
            icon = self.style().standardIcon(pixmapi)
            btn = QPushButton(self, icon=icon)
            self.btn_layout.addWidget(btn,0,i)
            btn_dct[btn_str] = btn
            i += 1
        return btn_dct

class MainWin(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Ventana principal')
        self.setGeometry(100, 100, 300, 150)
        mainwdgt = QWidget(self)
        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        mainwdgt.setLayout(layout)
        self.setCentralWidget(mainwdgt)

        self.display = Display()
        self.display.setStyleSheet("background: transparent;")
        layout.addWidget(self.display,0,0)
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(22)
        glow.setColor(QColor(255, 200, 120, 200))
        glow.setOffset(0, 0)
        self.display.setGraphicsEffect(glow)


        #File browser and directory entry
        self.browser = Browser()
        self.browser.file_data.connect(self.display.marquee.setText)
        layout.addWidget(self.browser, 3, 0)

        #Player layout
        player_btns = PlayerButtons()
        player_btns.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(player_btns,1,0)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    sys.exit(app.exec())
