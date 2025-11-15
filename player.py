import pyaudio as pa
import soundfile as sf
from PyQt6.QtCore import QObject, pyqtSignal

class OutStream(QObject):
    finished = pyqtSignal()

    def __init__(self, path : str, pos : int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p = pa.PyAudio()
        self.stream = None
        self.path = path
        self.playing = False
        self.pos = pos

    def run(self)->None:
        self.playing = True
        with sf.SoundFile(self.path, 'r') as sf_file:
            self.stream = self.p.open(format=pa.paFloat32,
                    channels=sf_file.channels,
                    rate=sf_file.samplerate,
                    output=True)
            while self.playing:
                data = sf_file.read(1024, 'float32')
                if len(data) == 0:
                    break
                self.pos += len(data)
                self.stream.write(data.tobytes())
            
            self.stream.close()
            self.p.terminate()
            self.finished.emit()
            self.playing = False
    
    def stop(self)->None:
        self.playing = False

    def getPos(self)->int:
        return self.pos