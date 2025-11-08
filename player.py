import pyaudio
import wave
import time
from PyQt6.QtCore import QThread, QObject, pyqtSignal

class OutStream(QObject):
    finished = pyqtSignal()

    def __init__(self, path : str, pos : int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.path = path
        self.playing = False
        self.pos = pos


    def run(self)->None:
        self.playing = True
        with wave.open(self.path, 'rb') as wf:
            self.stream = self.pa.open(format=self.pa.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
            print(self.pos)
            wf.setpos(self.pos//wf.getsampwidth())
            while len(data := wf.readframes(1024)) and self.playing:
                self.pos += len(data)
                self.stream.write(data)
            
            self.stream.close()
            self.pa.terminate()
            self.finished.emit()
            self.playing = False
    
    def stop(self)->None:
        self.playing = False

    def getPos(self)->int:
        return self.pos