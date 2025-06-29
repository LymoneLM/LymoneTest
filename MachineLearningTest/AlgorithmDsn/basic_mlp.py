# Basic feature extraction and MLP
from sklearn.neural_network import MLPClassifier  # 导入MLP分类器
import matplotlib.pyplot as plt
import time
from basic_feature_extraction import load_and_preprocess_data
from model_evaluation import evaluate_model

# 类别名称
CLASS_NAMES = ['无泄漏', '弱泄漏', '严重泄漏']
# 加载预处理数据
X_train, X_test, y_train, y_test, scaler, X_train_scaled, X_test_scaled = load_and_preprocess_data()

# 训练MLP模型
# ========================================================================
print("开始训练MLP模型...")
start_time = time.time()

# 初始化MLP分类器
mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64),  # 两层隐藏层：128个神经元和64个神经元
    activation='relu',             # ReLU激活函数
    solver='adam',                 # Adam优化器
    alpha=0.0001,                  # L2正则化项参数
    batch_size=256,                # 小批量大小
    learning_rate='adaptive',      # 自适应学习率
    learning_rate_init=0.001,      # 初始学习率
    max_iter=500,                  # 最大迭代次数
    validation_fraction=0.1,       # 10%的训练数据用于验证
    n_iter_no_change=10,           # 10次迭代无改进则停止
    verbose=True,                  # 显示训练过程
    random_state=42,               # 随机种子
    tol=1e-4,                      # 容忍度
)

# 训练模型
mlp.fit(X_train_scaled, y_train)

# 训练结束时间
end_time = time.time()
training_time = end_time - start_time
print(f"MLP训练完成! 耗时: {training_time:.2f}秒")

# 绘制训练损失曲线
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False # 解决坐标轴负号显示问题
plt.figure(figsize=(10, 6))
plt.plot(mlp.loss_curve_)
plt.title('MLP训练损失曲线')
plt.xlabel('迭代次数')
plt.ylabel('损失值')
plt.grid(True)
plt.savefig('./output/mlp_loss_curve.png')
plt.show()

# 评估模型
# ========================================================================
evaluate_model(mlp, X_test, y_test, class_names=CLASS_NAMES)
