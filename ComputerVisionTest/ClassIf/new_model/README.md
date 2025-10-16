# ResNet18猪瘟分类模型

本项目实现了一个基于ResNet18的猪瘟图像分类模型，作为MobileNetV2模型的替代方案。

## 模型结构

ResNet18是一个具有残差连接的深度卷积神经网络，具有以下特点：

- 18层深度网络结构
- 残差连接，有效缓解深度网络的梯度消失问题
- 强大的特征提取能力
- 比MobileNetV2更强的表现力，但计算量较大

## 文件结构

```
new_model/
├── model.py           # ResNet18模型定义
├── train.py           # 训练脚本
├── predict.py         # 推理脚本 
├── evaluate.py        # 评估和比较脚本
├── class_indices.json # 类别索引文件
└── README.md          # 说明文档
```

## 使用方法

### 1. 训练模型

```bash
python -m new_model.train
```

训练结果将保存在`logs/resnet18_<timestamp>/`目录下，包括：
- 模型权重文件 (best.pth)
- 训练过程可视化图表
- 训练指标记录

### 2. 推理预测

```bash
python -m new_model.predict
```

对验证集图像进行预测，并显示结果。

### 3. 模型评估

```bash
python -m new_model.evaluate
```

对ResNet18和MobileNetV2模型进行性能评估和比较，生成报告。

## 与MobileNetV2的主要区别

| 特性 | ResNet18 | MobileNetV2 |
|------|----------|-------------|
| 模型大小 | 较大 | 较小 |
| 参数数量 | ~11.7M | ~3.5M |
| 计算复杂度 | 较高 | 较低 |
| 推理速度 | 较慢 | 较快 |
| 准确率 | 可能更高 | 可能略低 |
| 训练策略 | Adam优化器<br>学习率调度器 | SGD优化器<br>固定学习率 |

## 改进策略

相比原始MobileNetV2模型，ResNet18模型做了以下改进：

1. **优化器变更**：从SGD改为Adam优化器，收敛更快
2. **学习率调度**：引入ReduceLROnPlateau调度器，动态调整学习率
3. **批量大小**：调整为32（原先为64），更适合ResNet模型
4. **预训练权重**：尝试加载ImageNet预训练权重
5. **可视化增强**：添加学习率变化曲线等更多可视化图表

## 性能对比

运行评估脚本后，可以在`new_model/evaluation_results/`目录中查看详细的性能对比报告，包括：

- 准确率对比图
- 推理时间对比图
- 每个模型的混淆矩阵
- 详细的分类报告
- 总结性能差异的文本报告 