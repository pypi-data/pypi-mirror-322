import pyaudio
import wave      
class AudioCapture:
    def __init__(self, filename, rate=44100, chunk=1024, channels=1, format=pyaudio.paInt16):
        self.filename = filename
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.format = format

    def record(self, duration):
        """
        录制指定时长的音频。
        :param duration: 录制时长，单位为秒。
        """
        audio = pyaudio.PyAudio()

        # 打开音频流
        stream = audio.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk)

        print("正在录音...")

        frames = []

        # 录制音频数据
        for _ in range(0, int(self.rate / self.chunk * duration + 1)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("录音结束")

        # 关闭音频流
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 保存音频数据到文件
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        return self.filename