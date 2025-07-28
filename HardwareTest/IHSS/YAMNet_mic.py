#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAMNet麦克风音频分类Demo
基于本地YAMNet模型进行实时音频事件检测
从麦克风读取音频，实时进行检测
"""

import os
import numpy as np
import tensorflow as tf
import librosa
import pandas as pd
from typing import Tuple, List, Dict
import json
import time
import threading
from collections import deque
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.mic import get_audio_16k, get_audio_frame_16k

# 抑制TensorFlow的内存警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

class YAMNetMicDemo:
    def __init__(self, model_path: str = "models/yamnet", device=3):
        """
        初始化YAMNet麦克风检测模型
        
        Args:
            model_path: 本地模型路径，默认为models/yamnet
            device: 音频设备索引
        """
        self.model = None
        self.class_names = None
        self.sample_rate = 16000  # YAMNet要求的采样率
        self.device = device
        self.is_running = False
        self.audio_buffer = deque(maxlen=int(self.sample_rate * 10))  # 10秒音频缓冲区
        self.detection_interval = 2.0  # 检测间隔（秒）
        self.frame_duration = 0.5  # 每帧时长（秒）
        
        # 加载本地模型
        if not self.load_local_model(model_path):
            raise RuntimeError(f"无法加载模型: {model_path}")
    
    def load_local_model(self, model_path: str) -> bool:
        """加载本地YAMNet模型"""
        try:
            print(f"正在从本地路径加载模型: {model_path}")
            
            # 检查模型路径是否存在
            if not os.path.exists(model_path):
                print(f"错误: 模型路径不存在: {model_path}")
                return False
            
            # 加载SavedModel
            self.model = tf.saved_model.load(model_path)
            print("模型加载成功！")
            
            # 加载类别映射文件
            class_map_path = os.path.join(model_path, "assets", "yamnet_class_map.csv")
            if os.path.exists(class_map_path):
                class_map_df = pd.read_csv(class_map_path)
                self.class_names = class_map_df['display_name'].values
                print(f"已加载 {len(self.class_names)} 个类别")
            else:
                print("警告: 未找到类别映射文件，将使用默认类别名称")
                # 创建默认类别名称
                self.class_names = [f"class_{i}" for i in range(521)]  # YAMNet有521个类别
            
            return True
            
        except Exception as e:
            print(f"加载本地模型失败: {e}")
            return False
    
    def audio_collection_thread(self):
        """音频收集线程"""
        print("开始音频收集...")
        while self.is_running:
            try:
                # 使用utils/mic获取16kHz音频帧
                audio_frame = get_audio_frame_16k(self.frame_duration, self.device)
                
                # 添加到缓冲区
                if len(audio_frame) > 0:
                    self.audio_buffer.extend(audio_frame)
                
            except Exception as e:
                print(f"音频收集错误: {e}")
                time.sleep(0.1)
    
    def get_audio_segment(self, duration: float) -> np.ndarray:
        """
        从缓冲区获取指定时长的音频片段
        
        Args:
            duration: 音频时长（秒）
            
        Returns:
            音频数据
        """
        samples_needed = int(duration * self.sample_rate)
        
        # 如果缓冲区数据不足，返回空数组
        if len(self.audio_buffer) < samples_needed:
            return np.array([])
        
        # 从缓冲区末尾获取最新的音频数据
        audio_data = np.array(list(self.audio_buffer)[-samples_needed:])
        return audio_data
    
    def predict(self, audio_data: np.ndarray) -> Dict:
        """
        使用YAMNet进行音频分类预测
        
        Args:
            audio_data: 音频数据（16kHz采样率）
            
        Returns:
            预测结果字典
        """
        if self.model is None:
            return None
        
        if len(audio_data) == 0:
            return None
        
        try:
            # 确保音频数据是float32类型
            audio_data = audio_data.astype(np.float32)
            
            # 运行模型推理
            scores, embeddings, spectrogram = self.model(audio_data)
            
            # 使用本地加载的类别名称
            class_names = self.class_names
            
            # 计算平均分数
            mean_scores = np.mean(scores, axis=0)
            
            # 获取前5个最高分数的类别
            top_indices = np.argsort(mean_scores)[-5:][::-1]
            
            results = {
                'scores': scores.numpy(),
                'embeddings': embeddings.numpy(),
                'spectrogram': spectrogram.numpy(),
                'class_names': class_names,
                'mean_scores': mean_scores,
                'top_predictions': []
            }
            
            for i, idx in enumerate(top_indices):
                score = mean_scores[idx]
                class_name = class_names[idx]
                results['top_predictions'].append({
                    'class_name': class_name,
                    'score': float(score),
                    'rank': i + 1
                })
            
            return results
            
        except Exception as e:
            print(f"预测过程中出现错误: {e}")
            return None
    
    def print_results(self, results: Dict, timestamp: str):
        """
        在控制台打印预测结果
        
        Args:
            results: 预测结果
            timestamp: 时间戳
        """
        if results is None:
            return
        
        try:
            # 获取最高置信度的预测
            top_pred = results['top_predictions'][0]
            
            # 只显示置信度较高的预测
            if top_pred['score'] > 0.3:  # 阈值可调整
                print(f"[{timestamp}] 检测到: {top_pred['class_name']} (置信度: {top_pred['score']:.3f})")
                
                # 显示前3个预测结果
                for i, pred in enumerate(results['top_predictions'][:3]):
                    if pred['score'] > 0.1:  # 只显示置信度大于0.1的
                        print(f"  {pred['rank']}. {pred['class_name']}: {pred['score']:.3f}")
                print()
            
        except Exception as e:
            print(f"显示结果时出现错误: {e}")
    
    def save_results(self, results: Dict, timestamp: str, output_dir: str = "results"):
        """
        保存预测结果到JSON文件（仅保存高置信度结果）
        
        Args:
            results: 预测结果
            timestamp: 时间戳
            output_dir: 输出目录
        """
        if results is None:
            return
        
        # 只保存置信度较高的结果
        top_pred = results['top_predictions'][0]
        if top_pred['score'] < 0.5:  # 阈值可调整
            return
        
        try:
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成文件名
            filename = f"yamnet_realtime_{timestamp.replace(':', '-').replace(' ', '_')}.json"
            output_path = os.path.join(output_dir, filename)
            
            # 准备保存的数据
            save_data = {
                'timestamp': timestamp,
                'top_predictions': results['top_predictions'],
                'mean_scores': results['mean_scores'].tolist(),
                'audio_info': {
                    'sample_rate': self.sample_rate,
                    'duration_frames': len(results['scores']),
                    'duration_seconds': len(results['scores']) * 0.96  # YAMNet的帧率
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print(f"高置信度结果已保存: {output_path}")
            
        except Exception as e:
            print(f"保存结果时出现错误: {e}")
    
    def run_realtime_detection(self):
        """运行实时检测"""
        print("=== YAMNet实时音频分类Demo ===")
        print(f"检测间隔: {self.detection_interval} 秒")
        print(f"音频设备: {self.device}")
        print("按 Ctrl+C 停止检测\n")
        
        try:
            self.is_running = True
            
            # 启动音频收集线程
            audio_thread = threading.Thread(target=self.audio_collection_thread)
            audio_thread.daemon = True
            audio_thread.start()
            
            # 等待缓冲区填充
            print("等待音频缓冲区填充...")
            time.sleep(3)
            
            detection_count = 0
            last_detection_time = time.time()
            
            while self.is_running:
                current_time = time.time()
                
                # 检查是否到了检测时间
                if current_time - last_detection_time >= self.detection_interval:
                    detection_count += 1
                    timestamp = time.strftime("%H:%M:%S")
                    
                    # 获取音频片段（使用最近5秒的音频）
                    audio_data = self.get_audio_segment(5.0)
                    
                    if len(audio_data) > 0:
                        # 进行预测
                        results = self.predict(audio_data)
                        
                        if results:
                            # 显示结果
                            self.print_results(results, timestamp)
                            
                            # 保存高置信度结果
                            self.save_results(results, timestamp)
                    
                    last_detection_time = current_time
                
                # 短暂休眠以避免CPU占用过高
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n检测已停止")
        finally:
            self.is_running = False
            if audio_thread.is_alive():
                audio_thread.join(timeout=1)
    
    def cleanup(self):
        """清理资源"""
        self.is_running = False


def main():
    """主函数 - 演示YAMNet实时检测的使用"""
    yamnet_mic = None
    
    try:
        # 初始化YAMNet麦克风检测
        yamnet_mic = YAMNetMicDemo("models/yamnet", device=3)
        
        # 运行实时检测
        yamnet_mic.run_realtime_detection()
        
    except RuntimeError as e:
        print(f"初始化失败: {e}")
    except Exception as e:
        print(f"运行过程中出现错误: {e}")
    finally:
        if yamnet_mic:
            yamnet_mic.cleanup()


if __name__ == "__main__":
    main() 