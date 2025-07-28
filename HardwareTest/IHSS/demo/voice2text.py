import sys
import numpy as np
import os
from utils.mic import get_audio
from mediapipe.tasks.python.audio import SpeechRecognizer, SpeechRecognizerOptions, RunningMode
from mediapipe.tasks import BaseOptions

# MediaPipe 语音识别相关导入
import tempfile
import soundfile as sf

# 采集音频
DURATION = 5  # 采集5秒
SAMPLERATE = 16000

audio = get_audio(duration=DURATION, samplerate=SAMPLERATE)

# 保存为临时wav文件（MediaPipe需要文件输入）
tmp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
sf.write(tmp_wav.name, audio, SAMPLERATE)

options = SpeechRecognizerOptions(
    base_options=BaseOptions(model_asset_path='speech_recognition.tflite'),
    running_mode=RunningMode.AUDIO_CLIPS
)

with SpeechRecognizer.create_from_options(options) as recognizer:
    with open(tmp_wav.name, 'rb') as f:
        audio_data = f.read()
    result = recognizer.recognize(audio_data)
    print('识别结果:', result.text)
