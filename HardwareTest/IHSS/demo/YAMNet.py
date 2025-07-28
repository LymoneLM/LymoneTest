#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAMNet音频分类Demo
基于本地YAMNet模型进行音频事件检测
"""

import os
import numpy as np
import tensorflow as tf
import librosa
import pandas as pd
from typing import Tuple, List, Dict
import json

# 抑制TensorFlow的内存警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

class YAMNetDemo:
    def __init__(self, model_path: str = "models/yamnet"):
        """
        初始化YAMNet模型
        
        Args:
            model_path: 本地模型路径，默认为models/yamnet
        """
        self.model = None
        self.class_names = None
        self.sample_rate = 16000  # YAMNet要求的采样率
        
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
    
    def load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """
        加载音频文件
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            audio_data: 音频数据
            sample_rate: 采样率
        """
        try:
            print(f"正在加载音频文件: {audio_path}")
            audio_data, sample_rate = librosa.load(audio_path, sr=None)
            
            # 如果是立体声，转换为单声道
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            print(f"音频加载成功 - 采样率: {sample_rate}Hz, 时长: {len(audio_data)/sample_rate:.2f}秒")
            return audio_data, sample_rate
            
        except Exception as e:
            print(f"加载音频文件失败: {e}")
            return None, None
    
    def resample_audio(self, audio_data: np.ndarray, original_sr: int) -> np.ndarray:
        """
        重采样音频到YAMNet要求的16kHz
        
        Args:
            audio_data: 原始音频数据
            original_sr: 原始采样率
            
        Returns:
            重采样后的音频数据
        """
        if original_sr != self.sample_rate:
            print(f"重采样音频从 {original_sr}Hz 到 {self.sample_rate}Hz")
            audio_data = librosa.resample(audio_data, orig_sr=original_sr, target_sr=self.sample_rate)
        
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
            print("模型未加载，无法进行预测")
            return None
        
        try:
            # print("正在进行音频分类预测...")
            
            # 确保音频数据是float32类型
            audio_data = audio_data.astype(np.float32)
            
            # 运行模型推理
            scores, embeddings, spectrogram = self.model(audio_data)
            
            # 使用本地加载的类别名称
            class_names = self.class_names
            
            # 计算平均分数
            mean_scores = np.mean(scores, axis=0)
            
            # 获取前10个最高分数的类别
            top_indices = np.argsort(mean_scores)[-10:][::-1]
            
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
            # print(f"预测过程中出现错误: {e}")
            return None
    
    def print_results(self, results: Dict):
        """
        在控制台打印预测结果
        
        Args:
            results: 预测结果
        """
        if results is None:
            print("没有结果可以显示")
            return
        
        try:
            print("\n" + "="*50)
            print("YAMNet音频分类结果")
            print("="*50)
            
            # 显示前10个预测结果
            print("\n前10个预测类别:")
            print("-" * 40)
            for pred in results['top_predictions'][:10]:
                print(f"{pred['rank']:2d}. {pred['class_name']:25s}: {pred['score']:.4f}")
            
            # 显示音频信息
            duration_frames = len(results['scores'])
            duration_seconds = duration_frames * 0.96  # YAMNet的帧率
            
            print(f"\n音频信息:")
            print("-" * 40)
            print(f"采样率: {self.sample_rate} Hz")
            print(f"时长: {duration_seconds:.2f} 秒")
            print(f"时间帧数: {duration_frames}")
            print(f"类别总数: {len(results['class_names'])}")
            
            # 显示最高置信度的预测
            top_pred = results['top_predictions'][0]
            print(f"\n最高置信度预测: {top_pred['class_name']} ({top_pred['score']:.4f})")
            
        except Exception as e:
            print(f"显示结果时出现错误: {e}")
    
    def save_results(self, results: Dict, output_path: str):
        """
        保存预测结果到JSON文件
        
        Args:
            results: 预测结果
            output_path: 输出文件路径
        """
        if results is None:
            print("没有结果可以保存")
            return
        
        try:
            # 准备保存的数据
            save_data = {
                'top_predictions': results['top_predictions'],
                'mean_scores': results['mean_scores'].tolist(),
                'class_names': results['class_names'].tolist(),
                'audio_info': {
                    'sample_rate': self.sample_rate,
                    'duration_frames': len(results['scores']),
                    'duration_seconds': len(results['scores']) * 0.96  # YAMNet的帧率
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print(f"预测结果已保存到: {output_path}")
            
        except Exception as e:
            print(f"保存结果时出现错误: {e}")


def main():
    """主函数 - 演示YAMNet的使用"""
    print("=== YAMNet音频分类Demo ===\n")
    
    # 初始化YAMNet（使用本地模型）
    try:
        yamnet = YAMNetDemo("models/yamnet")
    except RuntimeError as e:
        print(f"初始化失败: {e}")
        return
    
    # 检查是否有input.wav文件
    audio_path = "input.wav"
    if not os.path.exists(audio_path):
        print(f"警告: 未找到音频文件 {audio_path}")
        print("请将音频文件命名为 'input.wav' 并放在当前目录下")
        print("或者修改代码中的 audio_path 变量指向您的音频文件")
        return
    
    # 加载音频
    audio_data, sample_rate = yamnet.load_audio(audio_path)
    if audio_data is None:
        return
    
    # 重采样到16kHz
    audio_data = yamnet.resample_audio(audio_data, sample_rate)
    
    # 进行预测
    results = yamnet.predict(audio_data)
    if results is None:
        return
    
    # 显示结果
    yamnet.print_results(results)
    
    # 保存结果
    yamnet.save_results(results, "yamnet_results.json")
    
    print("\n=== Demo完成 ===")


if __name__ == "__main__":
    main()
