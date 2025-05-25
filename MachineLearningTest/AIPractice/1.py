import os
from scipy.io import loadmat

data_path = "./data"
data = loadmat(data_path+"/spectra_data.mat")
octane = data["octane"]
NIR = data["NIR"]

# -*- coding: UTF-8 -*-

# 1-导入包库
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score
import matplotlib.pyplot as plt

# 2-数据准备（假设已加载数据）
# 请替换以下示例数据为实际数据
# X = np.array(NIR)  # 形状 (60, 401)
# y = np.array(octane)  # 形状 (60,)
np.random.seed(116)
X = np.random.randn(60, 401)  # 示例输入数据
y = np.random.rand(60) * 10 + 85  # 示例输出数据（85-95之间）

# 3-数据乱序
np.random.seed(116)
shuffle_indices = np.random.permutation(len(X))
X = X[shuffle_indices]
y = y[shuffle_indices]

# 4-切分数据
test_size = 12  # 20% 测试数据
X_train, X_test = X[:-test_size], X[-test_size:]
y_train, y_test = y[:-test_size], y[-test_size:]

# 5-数据标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 转换为PyTorch张量
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test_np = y_test  # 保留numpy格式用于评估


# 6-建立模型
class BPRegressor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(401, 5),  # 输入层 -> 隐藏层 (5 neurons)
            nn.ReLU(),  # 激活函数
            nn.Linear(5, 1)  # 隐藏层 -> 输出层
        )

    def forward(self, x):
        return self.net(x)


model = BPRegressor()

# 7-编译模型（PyTorch方式）
lr = 0.1
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=lr)

# 8-训练模型
epochs = 300
batch_size = 32
loss_history = []

# 转换为数据集
train_dataset = torch.utils.data.TensorDataset(X_train, y_train)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

for epoch in range(epochs):
    epoch_loss = 0.0
    for batch_X, batch_y in train_loader:
        # 前向传播
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    # 记录平均损失
    avg_loss = epoch_loss / len(train_loader)
    loss_history.append(avg_loss)

    # 打印训练进度
    if (epoch + 1) % 50 == 0:
        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.4f}')

# 9-可视化损失曲线
plt.title('Loss Function Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.plot(loss_history, label="Training Loss")
plt.legend()
plt.show()

# 10-评估模型
model.eval()
with torch.no_grad():
    y_pred = model(X_test).numpy().flatten()

# 计算评价指标
mape = mean_absolute_percentage_error(y_test_np, y_pred)
r2 = r2_score(y_test_np, y_pred)

print("\n模型评估结果:")
print(f"测试集相对误差（MAPE）: {mape:.4f}")
print(f"决定系数 R²: {r2:.4f}")

# 11-预测结果展示（替代混淆矩阵）
print("\n预测结果对比:")
print("真实值\t预测值\t误差")
for true, pred in zip(y_test_np, y_pred):
    print(f"{true:.2f}\t{pred:.2f}\t{(pred - true):.2f}")