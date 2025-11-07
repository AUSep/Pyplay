import pyaudio
import wave
import time
from PyQt6.QtCore import QThread, QObject, pyqtSignal

class OutStream(QObject):
    finished = pyqtSignal()

    def __init__(self, path : str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.path = path
        self.playing = False
        self.paused = False

    def run(self)->None:
        self.playing = True
        with wave.open(self.path, 'rb') as wf:
            self.stream = self.pa.open(format=self.pa.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
            while len(data := wf.readframes(1064)) and self.playing:
                if self.paused:
                    self.stream.stop_stream()
                else:
                    if self.stream.is_stopped():
                        self.stream.start_stream()
                    self.stream.write(data)
            self.stream.close()
            self.pa.terminate()
            self.finished.emit()
            self.playing = False
