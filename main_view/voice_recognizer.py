# -*- coding:utf-8 -*-
import requests
import pyaudio
import sys
import time
import wave
import numpy
import threading
from event import EventManager
import config

class AudioStream:

    def __init__(self):
        self.chunk = 1024
        self.rate = 16000

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = self.rate,
            frames_per_buffer = self.chunk,
            input = True
            )

    def get_step(self, seconds):
        return (int)(self.rate / self.chunk * seconds)
    
    def is_active(self):
        return self.stream.is_active()

    def read(self):
        return self.stream.read(self.chunk, exception_on_overflow=False)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        

#音声認識クラス
class VoiceAnalyzer:
    
    def __init__(self):
        #ファイルとしてアップする必要ある。一時保存用。
        self.voice_file_path = 'voice.wav'

    def record(self, audio):

        voice_sequence = []
        for i in range(audio.get_step(config.VR_RECORD_SECONDS)):
            data = audio.read()
            voice_sequence.append(data)
        
        data = b''.join(voice_sequence)

        with wave.open(self.voice_file_path, "w") as out:
            out.setnchannels(1) #mono
            out.setsampwidth(2) #16bit
            out.setframerate(audio.rate)
            out.writeframes(data)
            

    def analyze(self):
        files = {"a": open(self.voice_file_path, 'rb'), "v":"off"}
        r = requests.post(config.VR_URL, files=files)
        return r.json()['text']

#音声監視クラス

        
class VoiceRecognizer(threading.Thread):

    #event : イベント管理クラス
    def __init__(self, event_manager):
        super(VoiceRecognizer, self).__init__()
        self.event_manager = event_manager
        self.running = True

    #大きい音かな？
    def is_big_volume(self, input_stream):
        #入力を正規化（-1～1）して、絶対値とって、最大値を返す
        #signalはCHUNKの個数分の配列です。
        signal = numpy.absolute(numpy.frombuffer(input_stream, dtype="int16") / float(2 ** 15))      

        return numpy.max(signal) > config.VR_THRESHOLD


    #threadの実行部分
    def run(self):

        
        audio = AudioStream()
        import event
        while audio.is_active() and self.running:
            input_stream = audio.read()
            if self.is_big_volume(input_stream):
                self.event_manager.enqueue_event(event.Command.TRANSITION, event.Value.VOICE_RECOGNITION)
                va = VoiceAnalyzer()
                va.record(audio)
                result = va.analyze()
                print(result)
                command, value = event.parse_from_string(result)
                self.event_manager.enqueue_event(command, value)
                time.sleep(2)
            
        audio.close()

    #外から無理やり止める
    def stop(self):
        self.running = False
        


if __name__ == "__main__":
    VoiceRecognizer(None).start()



    """
    #しきい値判定するやつ
    def record_threshold(self):

        self.setStream()
        judge = []
        for i in range(100):
            input = self.stream.read(self.CHUNK)
            result = self.audio_trans(input)
            judge.append(result)
        judge = numpy.array(judge)
        mean = judge.mean()
        sd = judge.std()
        self.judgeValue = mean + sd * 3
        self.closeStream()
    """
