from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QFont, QFontDatabase
from PyQt6.QtWidgets import QWidget, QApplication, QGridLayout, QLabel
import sys

class MarqueeLabel(QWidget):
    def __init__(self, font=None):
        super().__init__()
        self._text = ""
        self._offset = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(30)
        self._timer.timeout.connect(self._tick)
        self._label_font = font
        self._fm = self.fontMetrics()
        self._speed= max(1, 100)
        self._timer.start()

    def setText(self, text: str):
        self._text = text or ""
        self._offset = 0.0
        print(self._fm.horizontalAdvance(self._text))
        self.update()

    def _tick(self):
        if not self._text:
            return
        text_width = self._fm.horizontalAdvance(self._text)
        if text_width*2 <= self.width():
            if self._offset != 0.0:
                self._offset = 0.0
                self.update()
            return

        dt = self._timer.interval() / 1000.0
        step = self._speed * dt
        self._offset += step
        if self._offset >= text_width*1.8:
            self._offset -= text_width*1.8
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(self._label_font)

        y = (self.height() + self._fm.ascent() - self._fm.descent()) // 2
        x = -self._offset

        grad = QLinearGradient(0, 0, self.width(), 0)
        grad.setColorAt(0.0, QColor("#ffffff"))
        grad.setColorAt(0.5, QColor("#ffd86b"))
        grad.setColorAt(1.0, QColor("#ff6b6b"))

        if not self._text:
            return

        painter.drawText(QPointF(x, y), self._text)
        painter.setPen(QColor(255, 255, 255))

class Display(QWidget):
    def __init__(self):
        super().__init__()
        lay = QGridLayout(self)
        font_id = QFontDatabase.addApplicationFont('jd-lcd-rounded-font/JdLcdRoundedRegular-vXwE.ttf')
        families = QFontDatabase.applicationFontFamilies(font_id)

        title_font = QFont(families[0], 30)
        self.marquee = MarqueeLabel(title_font)
        self.marquee.setText('Hola mundo, cómo están? este es un string muy largo')
        lay.addWidget(self.marquee,0,0,1,2)

        time_label = QLabel(self, text='00:00')
        time_label.setFont(QFont(families, 35))
        time_label.setStyleSheet('color: rgb(240, 250, 250);')
        lay.addWidget(time_label,0,2, Qt.AlignmentFlag.AlignCenter)

        bitrate_label = QLabel(self, text='bitrate')
        sample_rate = QLabel(self, text='samplerate')
        channel_num = QLabel(self, text='Channels')
        
        i=0
        for lbl in (bitrate_label, sample_rate, channel_num):
            lbl.setFont(QFont(families, 15))
            lbl.setStyleSheet('color: rgb(240, 250, 250);')
            lay.addWidget(lbl,1,i,Qt.AlignmentFlag.AlignLeft) 
            i += 1
        