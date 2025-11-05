import pyaudio
import wave
import time

class OutStream():
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.wave = None

    def callback(self, in_data, frame_count, time_info, status):
        data = self.wave.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def openStream(self, path : str)->None:
        self.wave = wave.open(path, 'rb')
        self.stream = self.pa.open(format=self.pa.get_format_from_width(self.wave.getsampwidth()),
                channels=self.wave.getnchannels(),
                rate=self.wave.getframerate(),
                output=True,
                stream_callback=self.callback)
        while self.stream.is_active():
            time.sleep(0.1)
        self.terminateAudio()

    def terminateAudio(self)->None:
        self.stream.close()
        self.wave.close()
        self.pa.terminate()


if __name__ == "__main__":
    player = OutStream()
    player.openStream('/home/anibal/Documentos/Fisura2/16x44 amuse/Ataque de Pánico.wav')
    # Mantén el programa en ejecución para que el audio se reproduzca
    import time
    time.sleep(10)  # Ajusta el tiempo según la duración del archivo de audio
    player.terminateAudio()