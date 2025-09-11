from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor, QBrush, QLinearGradient
from PyQt6.QtWidgets import QWidget

class MarqueeLabel(QWidget):
    def __init__(self, parent=None, font=None):
        super().__init__(parent)
        self._text = ""
        self._offset = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(30)
        self._timer.timeout.connect(self._tick)
        self._label_font = font
        self._speed= max(1, 80)
        self.setMinimumHeight(48)
        self._timer.start()

    def setText(self, text: str):
        self._text = text or ""
        self._offset = 0.0
        self.update()

    def _tick(self):
        if not self._text:
            return
        fm = self.fontMetrics()
        text_width = fm.horizontalAdvance(self._text)
        if text_width <= self.width():
            if self._offset != 0.0:
                self._offset = 0.0
                self.update()
            return

        dt = self._timer.interval() / 1000.0
        step = self._speed * dt
        self._offset += step
        wrap_at = text_width
        if self._offset >= wrap_at:
            self._offset -= wrap_at
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(self._label_font)

        fm = painter.fontMetrics()
        text_width = fm.horizontalAdvance(self._text)
        y = (self.height() + fm.ascent() - fm.descent()) // 2

        grad = QLinearGradient(0, 0, self.width(), 0)
        grad.setColorAt(0.0, QColor("#ffffff"))
        grad.setColorAt(0.5, QColor("#ffd86b"))
        grad.setColorAt(1.0, QColor("#ff6b6b"))

        if text_width == 0:
            return

        if text_width <= self.width():
            x = (self.width() - text_width) // 2
            painter.setPen(QColor(30, 30, 30, 160))
            painter.drawText(x + 2, y + 2, self._text)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(x, y, self._text)
            return

        x_start = -self._offset

        painter.setPen(QColor(30, 30, 30, 160))
        painter.drawText(int(x_start) + 2, y + 2, self._text)
        painter.drawText(int(x_start + text_width) + 2, y + 2, self._text)

        # aplicar gradiente frontal usando brush
        painter.setPen(QColor(255, 255, 255))
        painter.setBrush(QBrush(grad))
        painter.drawText(int(x_start), y, self._text)
        painter.drawText(int(x_start + text_width), y, self._text)