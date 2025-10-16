import os
import json
import time
import numpy as np
import torch
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, precision_score, recall_score, f1_score
from tqdm import tqdm
import pandas as pd
import matplotlib as mpl

# 设置matplotlib使用中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi', 'FangSong']  # 优先使用的中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['font.family'] = 'sans-serif'  # 使用无衬线字体

# 导入模型
from new_model.model import ResNet18
from moudle.mobilenet import MobileNetV2

def find_latest_model(model_name_prefix):
    """查找最新的模型目录"""
    logs_dir = "./logs"
    model_dirs = [d for d in os.listdir(logs_dir) if d.startswith(model_name_prefix)]
    if not model_dirs:
        return None
    return os.path.join(logs_dir, sorted(model_dirs)[-1], "best.pth")

def load_model(model_type, model_path, num_classes=2):
    """加载模型"""
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    if model_type == "resnet18":
        model = ResNet18(num_classes=num_classes)
    elif model_type == "mobilenet":
        model = MobileNetV2(num_classes=num_classes)
    else:
        raise ValueError(f"不支持的模型类型: {model_type}")
        
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    
    return model, device

def count_parameters(model):
    """计算模型参数量"""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def get_model_size(model):
    """获取模型大小（MB）"""
    # 创建临时文件保存模型
    tmp_path = "temp_model.pth"
    torch.save(model.state_dict(), tmp_path)
    # 获取文件大小
    size_bytes = os.path.getsize(tmp_path)
    # 删除临时文件
    os.remove(tmp_path)
    # 转换为MB
    size_mb = size_bytes / (1024 * 1024)
    return size_mb

def calculate_fps(inference_time_ms):
    """根据推理时间计算FPS"""
    return 1000 / inference_time_ms

def evaluate_model(model, data_loader, device, class_names):
    """评估模型性能"""
    # 初始化变量
    correct = 0
    total = 0
    all_preds = []
    all_targets = []
    all_scores = []  # 存储预测概率
    inference_times = []
    
    # 评估模型
    with torch.no_grad():
        for images, labels in tqdm(data_loader, desc="评估"):
            images = images.to(device)
            labels = labels.to(device)
            
            # 测量推理时间
            start_time = time.time()
            outputs = model(images)
            end_time = time.time()
            
            # 记录单张图像的平均推理时间
            inference_times.append((end_time - start_time) / images.size(0))
            
            # 获取预测结果
            scores = torch.softmax(outputs, dim=1)
            _, predicted = torch.max(outputs.data, 1)
            
            # 统计准确率
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            # 收集所有预测和实际标签，用于混淆矩阵
            all_preds.extend(predicted.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())
            all_scores.extend(scores.cpu().numpy())
    
    # 计算指标
    accuracy = correct / total
    avg_inference_time = np.mean(inference_times) * 1000  # 转换为毫秒
    fps = calculate_fps(avg_inference_time)
    
    # 计算精确率和召回率
    precision = precision_score(all_targets, all_preds, average='weighted')
    recall = recall_score(all_targets, all_preds, average='weighted')
    f1 = f1_score(all_targets, all_preds, average='weighted')
    
    # 计算mAP (这里简化处理，使用精确率作为近似)
    mAP = precision * 100  # 转换为百分比
    
    # 计算混淆矩阵
    cm = confusion_matrix(all_targets, all_preds)
    
    # 生成分类报告
    report = classification_report(all_targets, all_preds, target_names=class_names, digits=4)
    
    # 获取模型参数量和大小
    param_count = count_parameters(model)
    model_size = get_model_size(model)
    
    return {
        'accuracy': accuracy,
        'confusion_matrix': cm,
        'report': report,
        'inference_time': avg_inference_time,
        'all_preds': all_preds,
        'all_targets': all_targets,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'fps': fps,
        'mAP': mAP,
        'param_count': param_count,
        'model_size': model_size
    }

def plot_confusion_matrix(cm, class_names, title, save_path):
    """绘制混淆矩阵"""
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title, fontsize=14)
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45, fontsize=12)
    plt.yticks(tick_marks, class_names, fontsize=12)

    # 标注具体数字
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontsize=12)

    plt.tight_layout()
    plt.ylabel('真实标签', fontsize=13)
    plt.xlabel('预测标签', fontsize=13)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_model_comparison(metrics_list, model_names, save_dir):
    """绘制模型比较图表"""
    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)
    
    # 比较准确率
    plt.figure(figsize=(10, 6))
    accuracies = [m['accuracy'] * 100 for m in metrics_list]
    plt.bar(model_names, accuracies)
    plt.title('模型准确率比较', fontsize=14)
    plt.ylabel('准确率 (%)', fontsize=13)
    plt.ylim(0, 100)
    # 在柱状图上标注具体数值
    for i, v in enumerate(accuracies):
        plt.text(i, v + 1, f"{v:.2f}%", ha='center', fontsize=12)
    plt.savefig(os.path.join(save_dir, 'accuracy_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 比较推理时间
    plt.figure(figsize=(10, 6))
    times = [m['inference_time'] for m in metrics_list]
    plt.bar(model_names, times)
    plt.title('模型推理时间比较 (毫秒/图像)', fontsize=14)
    plt.ylabel('推理时间 (ms)', fontsize=13)
    # 在柱状图上标注具体数值
    for i, v in enumerate(times):
        plt.text(i, v + 0.05, f"{v:.2f}ms", ha='center', fontsize=12)
    plt.savefig(os.path.join(save_dir, 'inference_time_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 比较FPS
    plt.figure(figsize=(10, 6))
    fps_values = [m['fps'] for m in metrics_list]
    plt.bar(model_names, fps_values)
    plt.title('模型FPS比较', fontsize=14)
    plt.ylabel('FPS', fontsize=13)
    # 在柱状图上标注具体数值
    for i, v in enumerate(fps_values):
        plt.text(i, v + 0.5, f"{v:.2f}", ha='center', fontsize=12)
    plt.savefig(os.path.join(save_dir, 'fps_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()

def create_comparison_table(metrics_list, model_names, save_dir):
    """创建模型对比表格"""
    # 准备数据
    data = []
    
    # 基准模型指标
    base_model_map = metrics_list[1]['mAP'] if len(metrics_list) > 1 else 0
    
    for i, metrics in enumerate(metrics_list):
        # 计算相对于基准模型的提升
        if i == 1:  # 基准模型
            improvement = "-"
        else:
            improvement = f"{(metrics['mAP'] - base_model_map) / base_model_map * 100:.2f}%"
        
        data.append({
            "模型": model_names[i],
            "参数量(Params)": f"{metrics['param_count']:,}",
            "mAP/%": f"{metrics['mAP']:.2f}",
            "提升": improvement,
            "FPS": f"{metrics['fps']:.2f}",
            "P": f"{metrics['precision']:.4f}",
            "R": f"{metrics['recall']:.4f}",
            "模型大小/MB": f"{metrics['model_size']:.2f}"
        })
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 保存为CSV
    csv_path = os.path.join(save_dir, 'model_comparison.csv')
    df.to_csv(csv_path, index=False)
    
    # 保存为漂亮的markdown表格
    markdown_path = os.path.join(save_dir, 'model_comparison.md')
    with open(markdown_path, 'w') as f:
        f.write(df.to_markdown(index=False))
    
    return df

def main():
    # 设置评估参数
    batch_size = 32
    results_dir = "./new_model/evaluation_results"
    os.makedirs(results_dir, exist_ok=True)
    
    # 加载类别信息
    if os.path.exists("new_model/class_indices.json"):
        class_indices_path = "new_model/class_indices.json"
    else:
        class_indices_path = "class_indices.json"
        
    with open(class_indices_path, 'r') as f:
        class_dict = json.load(f)
    class_names = list(class_dict.values())
    
    # 加载验证数据集
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_dataset = torchvision.datasets.ImageFolder(
        root="./datasets/val",
        transform=val_transform
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0
    )
    
    print(f"验证集数量: {len(val_dataset)}")
    
    # 直接使用指定的模型路径
    models_to_evaluate = [
        {"name": "resnet18", "path": "./logs/resnet18_20250513-011514/best.pth"},
        {"name": "mobilenet", "path": "./logs/mobilenet_20250508-000646/best.pth"}
    ]
    
    # 评估结果
    all_metrics = []
    model_names = []
    
    for model_info in models_to_evaluate:
        model_type = model_info["name"]
        model_path = model_info["path"]
        
        if os.path.exists(model_path):
            print(f"\n评估模型: {model_type} (路径: {model_path})")
            
            # 加载模型
            model, device = load_model(model_type, model_path, num_classes=len(class_names))
            
            # 评估模型
            metrics = evaluate_model(model, val_loader, device, class_names)
            
            # 保存评估结果
            model_result_dir = os.path.join(results_dir, model_type)
            os.makedirs(model_result_dir, exist_ok=True)
            
            # 保存混淆矩阵
            plot_confusion_matrix(
                metrics['confusion_matrix'], 
                class_names, 
                f'{model_type} 混淆矩阵',
                os.path.join(model_result_dir, 'confusion_matrix.png')
            )
            
            # 保存分类报告
            with open(os.path.join(model_result_dir, 'classification_report.txt'), 'w') as f:
                f.write(f"模型: {model_type}\n")
                f.write(f"准确率: {metrics['accuracy']:.4f}\n")
                f.write(f"平均推理时间: {metrics['inference_time']:.4f}ms/图像\n")
                f.write(f"FPS: {metrics['fps']:.2f}\n")
                f.write(f"mAP: {metrics['mAP']:.2f}%\n")
                f.write(f"精确率(P): {metrics['precision']:.4f}\n")
                f.write(f"召回率(R): {metrics['recall']:.4f}\n")
                f.write(f"F1分数: {metrics['f1_score']:.4f}\n")
                f.write(f"参数量: {metrics['param_count']:,}\n")
                f.write(f"模型大小: {metrics['model_size']:.2f}MB\n\n")
                f.write(metrics['report'])
            
            print(f"准确率: {metrics['accuracy']:.4f}")
            print(f"平均推理时间: {metrics['inference_time']:.4f}ms/图像")
            print(f"FPS: {metrics['fps']:.2f}")
            print(f"mAP: {metrics['mAP']:.2f}%")
            print(f"精确率(P): {metrics['precision']:.4f}")
            print(f"召回率(R): {metrics['recall']:.4f}")
            print(f"参数量: {metrics['param_count']:,}")
            print(f"模型大小: {metrics['model_size']:.2f}MB")
            print("分类报告:")
            print(metrics['report'])
            
            # 收集比较结果
            all_metrics.append(metrics)
            model_names.append(model_type)
        else:
            print(f"找不到模型文件: {model_path}")
    
    # 如果找到多个模型，绘制比较图表
    if len(all_metrics) > 1:
        plot_model_comparison(all_metrics, model_names, results_dir)
        
        # 创建比较表格
        comparison_table = create_comparison_table(all_metrics, model_names, results_dir)
        print("\n模型对比表格:")
        print(comparison_table)
        
        # 保存总结报告
        with open(os.path.join(results_dir, 'summary.txt'), 'w') as f:
            f.write("模型性能比较\n")
            f.write("=================\n\n")
            
            for i, model in enumerate(model_names):
                f.write(f"模型: {model}\n")
                f.write(f"准确率: {all_metrics[i]['accuracy']:.4f}\n")
                f.write(f"平均推理时间: {all_metrics[i]['inference_time']:.4f}ms/图像\n")
                f.write(f"FPS: {all_metrics[i]['fps']:.2f}\n")
                f.write(f"mAP: {all_metrics[i]['mAP']:.2f}%\n")
                f.write(f"精确率(P): {all_metrics[i]['precision']:.4f}\n")
                f.write(f"召回率(R): {all_metrics[i]['recall']:.4f}\n")
                f.write(f"参数量: {all_metrics[i]['param_count']:,}\n")
                f.write(f"模型大小: {all_metrics[i]['model_size']:.2f}MB\n\n")
            
            # 性能差异百分比
            if len(all_metrics) >= 2:
                acc_diff = (all_metrics[0]['accuracy'] - all_metrics[1]['accuracy']) / all_metrics[1]['accuracy'] * 100
                time_diff = (all_metrics[1]['inference_time'] - all_metrics[0]['inference_time']) / all_metrics[1]['inference_time'] * 100
                map_diff = (all_metrics[0]['mAP'] - all_metrics[1]['mAP']) / all_metrics[1]['mAP'] * 100
                
                f.write("性能比较:\n")
                f.write(f"{model_names[0]} vs {model_names[1]}:\n")
                if acc_diff > 0:
                    f.write(f"- 准确率提高: {acc_diff:.2f}%\n")
                else:
                    f.write(f"- 准确率降低: {abs(acc_diff):.2f}%\n")
                    
                if time_diff > 0:
                    f.write(f"- 推理速度提高: {time_diff:.2f}%\n")
                else:
                    f.write(f"- 推理速度降低: {abs(time_diff):.2f}%\n")
                    
                if map_diff > 0:
                    f.write(f"- mAP提高: {map_diff:.2f}%\n")
                else:
                    f.write(f"- mAP降低: {abs(map_diff):.2f}%\n")
        
        print(f"\n比较结果已保存到 {results_dir}")

if __name__ == "__main__":
    main() 