from PyQt6.QtWidgets import (QWidget, QApplication, QGridLayout, QPushButton, QTreeView)
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir, QItemSelection, pyqtSignal
from pymediainfo import MediaInfo
import sys

class Browser(QWidget):
    file_data = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.lay = QGridLayout(self)
        self.lay.setContentsMargins(0,0,0,0)
        self.lay.setSpacing(0)

        browser_btn = QPushButton(self, text = 'Browse files...')
        gallery_btn = QPushButton(self, text = 'Media gallery')
        playlist_btn = QPushButton(self, text = 'Playlist')
        self.btns : list[QPushButton] = [browser_btn, gallery_btn, playlist_btn]
        self.views : list[QTreeView] = []

        self.view_hold = QWidget(self)
        self.hold_lay = QGridLayout(self.view_hold)
        self.view_hold.setVisible(False)
        self.lay.addWidget(self.view_hold, 1, 0, 1, 3)

        i = 0
        for btn in self.btns:
            btn.setCheckable(True)
            self.lay.addWidget(btn,0,i)
            btn.released.connect(lambda b = i: self.slot(b))
            tree_view = QTreeView(self.view_hold)
            tree_view.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
            tree_view.setSelectionMode(QTreeView.SelectionMode.SingleSelection)
            self.hold_lay.addWidget(tree_view,0,0)
            self.clearHold()
            self.views.append(tree_view)
            i += 1

        self.setBrowserTree()
        self.setGalTree()
        self.setPlaylistTree()

        self.show()
    
    def slot(self, obj : int):
        for btn in [b for b in self.btns if b != self.btns[obj]]:
            btn.setChecked(False)
        self.clearHold()
        self.hold_lay.addWidget(self.views[obj],0,0)
        self.views[obj].show()
        btn_toggled = any([b.isChecked() for b in self.btns])
        self.view_hold.setVisible(btn_toggled)
        self.adjustSize()
    
    def clearHold(self):
        while self.hold_lay.count():
            item = self.hold_lay.takeAt(0)
            w = item.widget()
            if w:
                w.hide()
    
    def getFile(self, selected : QItemSelection, deselected: QItemSelection):
        sel = selected.indexes()
        index = sel[0]
        sender : QTreeView = self.sender()
        if isinstance(sender.model(), QFileSystemModel):
            model : QFileSystemModel = sender.model()
            path = model.filePath(index)
            #media_info = MediaInfo.parse(path, output='text', full=False)
            self.file_data.emit(path)

        
    def setBrowserTree(self):
        file_model= QFileSystemModel(self)
        file_model.setRootPath(QDir.rootPath())
        tree = self.views[0]
        tree.setModel(file_model)
        tree.selectionModel().selectionChanged.connect(self.getFile)
        tree.setRootIndex(file_model.index(QDir.homePath()))

    def setGalTree(self):
        file_model= QFileSystemModel(self)
        file_model.setRootPath(QDir.rootPath())
        tree = self.views[1]
        tree.setModel(file_model)
        tree.selectionModel().selectionChanged.connect(self.getFile)
        tree.setRootIndex(file_model.index('/home/anibal/Escritorio'))

    def setPlaylistTree(self):
        file_model= QFileSystemModel(self)
        file_model.setRootPath(QDir.rootPath())
        tree = self.views[2]
        tree.setModel(file_model)
        tree.selectionModel().selectionChanged.connect(self.getFile)
        tree.setRootIndex(file_model.index('/home/anibal/Documentos'))