from PyQt6.QtCore import QDir, QTimer, QItemSelection, Qt, QPropertyAnimation, QEasingCurve,\
QSize
from PyQt6.QtGui import QFileSystemModel, QFont, QPainter, QColor,\
QBrush, QLinearGradient
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow,\
QStyle, QGridLayout, QWidget, QTreeView, QGraphicsDropShadowEffect,\
QScrollArea, QFrame, QSizePolicy
import sys

class MarqueeLabel(QWidget):
    def __init__(self, parent=None, font=None, speed_px_per_sec=80, gap=40):
        super().__init__(parent)
        self._text = ""
        self._offset = 0.0
        self._gap = gap
        self._timer = QTimer(self)
        self._timer.setInterval(30)  # ms
        self._timer.timeout.connect(self._tick)
        self._label_font = font
        self._speed_px_per_sec = max(1, speed_px_per_sec)
        self.setMinimumHeight(48)
        self._timer.start()

    def setText(self, text: str):
        self._text = text or ""
        self._offset = 0.0
        self.update()

    def setSpeed(self, px_per_second: int):
        self._speed_px_per_sec = max(1, px_per_second)

    def resizeEvent(self, event):
        self._offset = 0.0
        super().resizeEvent(event)

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
        step = self._speed_px_per_sec * dt
        self._offset += step
        wrap_at = text_width + self._gap
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
        gap = self._gap

        painter.setPen(QColor(30, 30, 30, 160))
        painter.drawText(int(x_start) + 2, y + 2, self._text)
        painter.drawText(int(x_start + text_width + gap) + 2, y + 2, self._text)

        # aplicar gradiente frontal usando brush
        painter.setPen(QColor(255, 255, 255))
        painter.setBrush(QBrush(grad))
        painter.drawText(int(x_start), y, self._text)
        painter.drawText(int(x_start + text_width + gap), y, self._text)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return self.fontMetrics().boundingRect("M" * 20).size()

class PlayerButtons(QWidget):
    def __init__(self, file_path : str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filePath = file_path
        self.btn_layout = QGridLayout()
        self.setLayout(self.btn_layout)

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

class ExpandableTab(QWidget):
    def __init__(self, content_widget : QWidget, title : str, expanded : bool = False):
        super().__init__()
        self.pad_list = []
        self.lay = QGridLayout(self)
        self.expand_anim_duration = 220

        #Tab button setting
        self.header_btn = QPushButton(title)
        self.header_btn.setCheckable(True)
        self.header_btn.setChecked(expanded)
        self.header_btn.setStyleSheet("text-align: left; padding: 8px;")
        self.header_btn.clicked.connect(self.toggle)

        # Content area en QScrollArea
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_area.setFrameShape(QFrame.Shape.NoFrame)
        self.content_area.setWidget(content_widget)

        # Forzamos políticas para que el contenido tenga height fijo cuando colapsado/expandido
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # calcular altura objetivo del contenido
        self._content_height = content_widget.sizeHint().height()
        if expanded:
            self.content_area.setMaximumHeight(self._content_height)
        else:
            self.content_area.setMaximumHeight(0)

        # animación de maximumHeight del content_area
        self._anim = QPropertyAnimation(self.content_area, b"maximumHeight", self)
        self._anim.setDuration(self.expand_anim_duration)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._anim.finished.connect(self._on_anim_finished)

        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.header_btn)
        self.lay.addWidget(self.content_area)

    def toggle(self):
        checked = self.header_btn.isChecked()
        start = self.content_area.maximumHeight()
        end = self._content_height if checked else 0

        # detener animaciones previas
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.stop()
        if getattr(self, "_top_anim", None) and self._top_anim.state() == QPropertyAnimation.State.Running:
            self._top_anim.stop()

        # animar content_area
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)

        # animar ventana principal para acompañar el cambio de altura
        top = self.window()
        if top is not None:
            # calcular delta de altura
            delta = end - start
            self._top_anim = QPropertyAnimation(top, b"size", self)
            self._top_anim.setDuration(self.expand_anim_duration)
            self._top_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self._top_anim.setStartValue(top.size())
            new_size = QSize(top.width(), max(1, top.height() + delta))
            self._top_anim.setEndValue(new_size)
            # mantener referencia hasta que termine
            self._top_anim.start()

        self._anim.start()

    def setExpanded(self, expand: bool):
        if self.header_btn.isChecked() == expand:
            return
        self.header_btn.setChecked(expand)
        self.toggle()

    def _on_anim_finished(self):
        # asegurar que maximumHeight coincida exactamente al final
        if self.header_btn.isChecked():
            self.content_area.setMaximumHeight(self._content_height)
        else:
            self.content_area.setMaximumHeight(0)
        # ajustar tamaño final de la ventana por si small differences
        w = self.window()
        if w:
            w.adjustSize()

class TabsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_list : list[ExpandableTab] = []
        self.lay = QGridLayout(self)

    def new_tab(self, tab : ExpandableTab):
        self.lay.addWidget(tab, 0, self.lay.count())
        self.tab_list.append(tab)
        tab.header_btn.clicked.connect(lambda checked, t=tab: self)
    
    def _on_section_toggled(self, toggled_tab : ExpandableTab):
        if toggled_tab.header_btn.isChecked():
            for s in self.tab_list:
                if s is not toggled_tab and s.header_btn.isChecked():
                    s.setExpanded(False)

class MainWin(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Ventana principal')
        self.setGeometry(100, 100, 500, 300)
        mainwdgt = QWidget(self)
        layout = QGridLayout()
        mainwdgt.setLayout(layout)
        self.setCentralWidget(mainwdgt)

        #File browser and directory entry
        self.file_model= QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.file_model)
        self.tree_view.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self.tree_view.setSelectionMode(QTreeView.SelectionMode.SingleSelection)
        self.tree_view.setRootIndex(self.file_model.index(QDir.homePath()))
        self.tree_view.selectionModel().selectionChanged.connect(self.getFile)

        self.tab_panel = TabsPanel()
        self_browser_tab = ExpandableTab(self.tree_view, "Browse files..")
        self.tab_panel.new_tab(self_browser_tab)
        layout.addWidget(self.tab_panel, 3, 0)

        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.5)

        self.marquee = MarqueeLabel(font=title_font, speed_px_per_sec=80, gap=40)
        self.marquee.setStyleSheet("background: transparent;")
        layout.addWidget(self.marquee,0,0)

        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(22)
        glow.setColor(QColor(255, 200, 120, 200))
        glow.setOffset(0, 0)
        self.marquee.setGraphicsEffect(glow)

        #Player layout
        player_btns = PlayerButtons(self.marquee, self.tree_view)
        layout.addWidget(player_btns,1,0)

        self.show()

    def getFile(self, selected : QItemSelection, deselected : QItemSelection):
        sel = selected.indexes()
        index = sel[0]
        if isinstance(self.file_model, QFileSystemModel):
            path = self.file_model.filePath(index)
            self.marquee.setText(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    sys.exit(app.exec())
