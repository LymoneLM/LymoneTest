import os
from utils.baidu import text2audio

os.makedirs('assets', exist_ok=True)
voice_map = {
    # 'iamhere': '我在',
    # 'rotated': '已旋转',
    # 'face_tracking': '人脸追踪',
    # 'danger_detection': '安全监测',
    # 'voice_awake': '指令唤醒',
    # 'off': '已关闭',
    # 'on': '已开启',
    # 'normal_mode': '普通模式',
    # 'mute_mode': '静音模式',
    # 'sentry_mode': '哨兵模式',
    # 'privacy_mode': '隐私模式',
    # 'open': '开启',
    # 'close': '关闭',
    # 'success': '操作成功',
    # 'fail': '操作失败',
    # 'welcome': '欢迎使用',
    # 'goodbye': '再见',
    # 'alarm': '警报',
    # 'fire_alarm': '火灾警报',
    # 'danger': '危险',
    # 'please_wait': '请稍候',
    # 'completed': '已完成',
    # 'start': '开始',
    # 'stop': '停止',
    'noidea': '哨兵没有听懂您的指令',
}
for name, text in voice_map.items():
    wav_path = os.path.join('assets', f'{name}.wav')
    print(f'生成: {wav_path} ({text})')
    text2audio(text, output_file=wav_path)
print('全部语音已生成。') 