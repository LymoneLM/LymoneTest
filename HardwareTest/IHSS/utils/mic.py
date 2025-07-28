import sounddevice as sd
import numpy as np
import librosa

def get_audio(duration=5, samplerate=16000, device=3):
    """
    采集指定时长的音频，返回numpy数组。
    :param duration: 采集时长（秒）
    :param samplerate: 采样率
    :param device: 音频设备索引，None表示使用默认设备
    :return: 采集到的音频数据（numpy数组，float32）
    """
    # print(f"正在采集音频，时长{duration}秒...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, 
                   channels=1, dtype='float32', device=device)
    sd.wait()
    # print("音频采集完成。")
    return np.squeeze(audio)

def get_audio_frame(frame_length, samplerate=16000, device=3):
    """
    采集一帧音频数据，用于实时处理。
    :param frame_length: 帧长度（采样点数）
    :param samplerate: 采样率
    :param device: 音频设备索引，None表示使用默认设备
    :return: 采集到的音频数据（numpy数组，int16）
    """
    audio = sd.rec(frame_length, samplerate=samplerate, 
                   channels=1, dtype='int16', device=device)
    sd.wait()
    return np.squeeze(audio)

def get_audio_16k(duration=5, device=3):
    """
    采集指定时长的音频并重采样到16kHz，返回numpy数组。
    :param duration: 采集时长（秒）
    :param device: 音频设备索引
    :return: 采集到的音频数据（numpy数组，float32，16kHz采样率）
    """
    # 以44.1kHz采集音频（设备3的要求）
    original_sr = 44100
    audio = sd.rec(int(duration * original_sr), samplerate=original_sr, 
                   channels=1, dtype='float32', device=device)
    sd.wait()
    audio = np.squeeze(audio)
    
    # 重采样到16kHz
    if len(audio) > 0:
        audio_16k = librosa.resample(audio, orig_sr=original_sr, target_sr=16000)
        return audio_16k
    else:
        return np.array([])

def get_audio_frame_16k(frame_duration=0.5, device=3):
    """
    采集一帧音频数据并重采样到16kHz，用于实时处理。
    :param frame_duration: 帧时长（秒）
    :param device: 音频设备索引
    :return: 采集到的音频数据（numpy数组，float32，16kHz采样率）
    """
    # 以44.1kHz采集音频（设备3的要求）
    original_sr = 44100
    frame_length = int(frame_duration * original_sr)
    audio = sd.rec(frame_length, samplerate=original_sr, 
                   channels=1, dtype='float32', device=device)
    sd.wait()
    audio = np.squeeze(audio)
    
    # 重采样到16kHz
    if len(audio) > 0:
        audio_16k = librosa.resample(audio, orig_sr=original_sr, target_sr=16000)
        return audio_16k
    else:
        return np.array([])

