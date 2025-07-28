import pvporcupine
from pvrecorder import PvRecorder
import config.key as key

access_key = key.picovoice_access_key
keywords = ["哨兵"]

porcupine = pvporcupine.create(
  access_key=access_key,
  keyword_paths=['models/porcupine/哨兵_zh_raspberry-pi_v3_0_0.ppn'],
  model_path='models/porcupine/porcupine_params_zh.pv'
)
recoder = PvRecorder(device_index=11, frame_length=porcupine.frame_length)

try:
    recoder.start()
    print("检测开始")
    while True:
        keyword_index = porcupine.process(recoder.read())
        if keyword_index >= 0:
            print(f"Detected {keywords[keyword_index]}")


except KeyboardInterrupt:
    recoder.stop()
finally:
    porcupine.delete()
    recoder.delete()