import pyaudio
import wave

# 播放WAV音频文件的函数
def play_wav_file(wav_file):
    # 打开WAV文件
    with wave.open(wav_file, 'rb') as wf:
        # 初始化PyAudio
        p = pyaudio.PyAudio()

        # 打开音频流
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # 读取数据并播放
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        # 停止并关闭音频流
        stream.stop_stream()
        stream.close()

        # 终止PyAudio
        p.terminate()

# 使用函数播放WAV文件
play_wav_file('tts.wav')
