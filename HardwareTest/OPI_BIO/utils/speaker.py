import pyaudio
import wave
import numpy as np
import threading

# 播放WAV音频文件
def play_wav_file(wav_file, volume=1.0, device_index=0):
    # 打开WAV文件
    with wave.open(wav_file, 'rb') as wf:
        # 初始化PyAudio
        p = pyaudio.PyAudio()
        # 打开音频流
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=device_index)
        # 读取数据并播放
        data = wf.readframes(1024)
        while data:
            # 音量调整
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_data = (audio_data * volume).astype(np.int16)
            stream.write(audio_data.tobytes())
            data = wf.readframes(1024)
        # 停止并关闭音频流
        stream.stop_stream()
        stream.close()
        # 终止PyAudio
        p.terminate()

def play_wav_file_async(wav_file, volume=1.0, device_index=0):
    t = threading.Thread(target=play_wav_file, args=(wav_file, volume, device_index), daemon=True)
    t.start()

