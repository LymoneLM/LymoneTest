import pyaudio
import wave
import numpy as np
import threading
import queue

# 全局音频播放队列
_audio_queue = queue.Queue()

# 后台音频播放线程
_def_player_started = False

def _audio_player_worker():
    while True:
        wav_file, volume, device_index = _audio_queue.get()
        try:
            _play_wav_file_sync(wav_file, volume, device_index)
        except Exception as e:
            print(f"[音频播放失败] {e}")
        _audio_queue.task_done()

def _ensure_player():
    global _def_player_started
    if not _def_player_started:
        threading.Thread(target=_audio_player_worker, daemon=True).start()
        _def_player_started = True

# 原始同步播放函数
def _play_wav_file_sync(wav_file, volume=1.0, device_index=0):
    with wave.open(wav_file, 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=device_index)
        data = wf.readframes(1024)
        while data:
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_data = (audio_data * volume).astype(np.int16)
            stream.write(audio_data.tobytes())
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()
        p.terminate()

# 队列播放接口

def play_wav_file_queued(wav_file, volume=1.0, device_index=0):
    _ensure_player()
    _audio_queue.put((wav_file, volume, device_index))

# 兼容原有异步接口

def play_wav_file_async(wav_file, volume=1.0, device_index=0):
    play_wav_file_queued(wav_file, volume, device_index)

