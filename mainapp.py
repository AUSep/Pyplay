from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QPushButton, QMainWindow,
QStyle, QGridLayout, QWidget, QGraphicsDropShadowEffect,
QSizePolicy, QSlider, QLabel)
from file_browser import Browser
from marquee_label import Display
from player import OutStream
import sys
from pymediainfo import MediaInfo
    
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
        self.filePath = None
        self.output_stream = None
        self.play_pos = 0

    def play(self):
        self.output_stream = OutStream(self.filePath, self.play_pos)
        self.audio_thread =QThread()

        self.output_stream.moveToThread(self.audio_thread)
        self.audio_thread.started.connect(self.output_stream.run)
        self.output_stream.finished.connect(self.audio_thread.quit)
        self.output_stream.finished.connect(self.output_stream.deleteLater)
        self.audio_thread.finished.connect(self.audio_thread.deleteLater)

        self.audio_thread.start()
    def previous(self):
        pass

    def pause(self):
        self.play_pos = self.output_stream.getPos()
        self.output_stream.stop()

    def next(self):
        pass

    def stop(self):
        self.output_stream.stop()
        self.output_stream = None
        self.play_pos = 0

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
        self.setGeometry(100, 100, 377, 144)
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
        glow.setColor(QColor(210, 250, 250, 200)) 
        glow.setOffset(0, 0)
        self.display.setGraphicsEffect(glow)

        self.browser = Browser()
        self.browser.file_data.connect(self.getFileData)
        layout.addWidget(self.browser, 3, 0)

        self.player_btns = PlayerButtons()
        self.player_btns.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.player_btns,1,0)

        self.show()
    
    def getFileData(self, file_dir : str) -> None:
        media_info = MediaInfo.parse(file_dir)
        for track in media_info.general_tracks:
            data_dict = track.to_data()
        for track in media_info.audio_tracks:
            data_dict.update(track.to_data())
        self.display.setDisplay(data_dict)
        self.player_btns.filePath = data_dict['complete_name']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    sys.exit(app.exec())