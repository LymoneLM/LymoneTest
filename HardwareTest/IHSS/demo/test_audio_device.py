#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sounddevice as sd
import numpy as np
import wave
import os
from utils.mic import list_audio_devices, get_audio_frame
from scipy import signal

def resample_audio(audio_data, original_sr, target_sr, target_length):
    """
    重采样音频数据到指定长度
    """
    if original_sr == target_sr:
        return audio_data[:target_length]
    
    # 使用 scipy 进行重采样
    resampled = signal.resample(audio_data, target_length)
    return resampled.astype(np.int16)

def test_audio_device(device_index=None, duration=3, filename="test_audio.wav"):
    """
    测试指定音频设备并录制音频
    
    :param device_index: 音频设备索引，None表示使用默认设备
    :param duration: 录制时长（秒）
    :param filename: 保存的音频文件名
    """
    print("=== 音频设备测试 ===")
    
    # 列出所有设备
    list_audio_devices()
    
    # 获取设备信息
    devices = sd.query_devices()
    if device_index is not None:
        if device_index >= len(devices):
            print(f"错误: 设备索引 {device_index} 超出范围")
            return False
        device = devices[device_index]
        device_name = device['name']
        print(f"\n选择的设备: {device_name} (索引: {device_index})")
    else:
        device = devices[sd.default.device[0]]
        device_name = device['name']
        print(f"\n使用默认音频设备: {device_name}")
    
    # 使用设备支持的采样率
    device_samplerate = 44100  # 设备支持的采样率
    target_samplerate = 16000  # 目标采样率
    print(f"设备采样率: {device_samplerate} Hz")
    print(f"目标采样率: {target_samplerate} Hz")
    
    # 测试音频采集
    print(f"\n开始录制 {duration} 秒音频...")
    try:
        # 使用设备支持的采样率录制音频
        audio_data = sd.rec(int(duration * device_samplerate), 
                           samplerate=device_samplerate, 
                           channels=1, dtype='int16', device=device_index)
        sd.wait()
        
        print(f"录制完成，数据形状: {audio_data.shape}")
        print(f"数据类型: {audio_data.dtype}")
        print(f"音量范围: {audio_data.min()} 到 {audio_data.max()}")
        
        # 检查音频质量
        max_volume = abs(audio_data).max()
        if max_volume < 100:
            print("⚠️  警告: 音量较低，请检查麦克风设置")
        elif max_volume < 1000:
            print("✅ 音量正常")
        else:
            print("✅ 音量良好")
        
        # 保存原始音频文件（44.1kHz）
        original_filename = filename.replace('.wav', '_original_44k.wav')
        print(f"\n保存原始音频到: {original_filename}")
        with wave.open(original_filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(device_samplerate)
            wav_file.writeframes(audio_data.tobytes())
        
        # 重采样到16kHz
        print(f"重采样到 {target_samplerate} Hz...")
        target_length = int(len(audio_data) * target_samplerate / device_samplerate)
        audio_data_resampled = resample_audio(audio_data, device_samplerate, target_samplerate, target_length)
        
        print(f"重采样完成，数据形状: {audio_data_resampled.shape}")
        print(f"重采样后音量范围: {audio_data_resampled.min()} 到 {audio_data_resampled.max()}")
        
        # 保存重采样后的音频文件（16kHz）
        resampled_filename = filename.replace('.wav', '_resampled_16k.wav')
        print(f"保存重采样音频到: {resampled_filename}")
        with wave.open(resampled_filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(target_samplerate)
            wav_file.writeframes(audio_data_resampled.tobytes())
        
        # 显示文件信息
        original_size = os.path.getsize(original_filename)
        resampled_size = os.path.getsize(resampled_filename)
        print(f"原始文件大小: {original_size} 字节")
        print(f"重采样文件大小: {resampled_size} 字节")
        print(f"压缩比: {original_size/resampled_size:.2f}:1")
        
        return True
        
    except Exception as e:
        print(f"❌ 音频录制失败: {e}")
        return False

def test_device_samplerates(device_index):
    """
    测试设备支持的不同采样率
    """
    print(f"\n=== 测试设备 {device_index} 支持的采样率 ===")
    
    test_rates = [8000, 16000, 22050, 44100, 48000]
    supported_rates = []
    
    for rate in test_rates:
        try:
            # 尝试录制一小段音频
            test_audio = sd.rec(1024, samplerate=rate, channels=1, 
                               dtype='int16', device=device_index)
            sd.wait()
            supported_rates.append(rate)
            print(f"✅ {rate} Hz - 支持")
        except Exception as e:
            print(f"❌ {rate} Hz - 不支持 ({e})")
    
    return supported_rates

if __name__ == "__main__":
    import sys
    
    # 解析命令行参数
    device_index = None
    duration = 3
    filename = "test_audio.wav"
    
    if len(sys.argv) > 1:
        try:
            device_index = int(sys.argv[1])
        except ValueError:
            print("错误: 设备索引必须是数字")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        try:
            duration = float(sys.argv[2])
        except ValueError:
            print("错误: 录制时长必须是数字")
            sys.exit(1)
    
    if len(sys.argv) > 3:
        filename = sys.argv[3]
    
    print(f"测试参数:")
    print(f"  设备索引: {device_index}")
    print(f"  录制时长: {duration} 秒")
    print(f"  文件名: {filename}")
    
    # 执行测试
    success = test_audio_device(device_index, duration, filename)
    
    if success and device_index is not None:
        # 测试支持的采样率
        supported_rates = test_device_samplerates(device_index)
        print(f"\n支持的采样率: {supported_rates}")
    
    if success:
        print("\n✅ 音频设备测试完成")
    else:
        print("\n❌ 音频设备测试失败")
        sys.exit(1) 