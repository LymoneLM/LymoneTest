import subprocess

# 录制音频的持续时间（秒）
duration = 3
# 输出音频文件的路径
output_file = "output.wav"
# 指定音频设备（对应arecord -D参数）
audio_device = "plughw:3,0"

# 构建arecord命令
command = [
    "arecord",
    "-D", audio_device,  # 指定USB音频设备
    "-d", str(duration),  # 录制时长
    "-f", "S16_LE",      # 采样格式（16位小端）
    "-r", "48000",       # 采样率（44.1kHz）
    "-c", "2",           # 声道数（立体声）
    output_file          # 输出文件
]

# 执行命令
try:
    print(f"开始使用设备 {audio_device} 录制音频，持续 {duration} 秒...")
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"音频已成功录制到 {output_file}")
except subprocess.CalledProcessError as e:
    print(f"录制音频时发生错误: {e.stderr.decode('utf-8')}")
except FileNotFoundError:
    print("错误：未找到arecord命令，请确保已安装alsa-utils")