# Basic feature extraction and Kernel SVM
from sklearn.svm import SVC  # 改为导入SVM分类器
from basic_feature_extraction import load_and_preprocess_data
from model_evaluation import evaluate_model

# 类别名称
CLASS_NAMES = ['无泄漏', '弱泄漏', '严重泄漏']
# 加载预处理数据
X_train, X_test, y_train, y_test, scaler, X_train_scaled, X_test_scaled = load_and_preprocess_data()

# 训练Kernel SVM模型
# ========================================================================
# 初始化Kernel SVM分类器
svm = SVC(
    kernel='rbf',           # 使用径向基函数(RBF)核
    C=1.0,                  # 正则化参数
    gamma='scale',          # 核函数系数 (自动根据特征方差计算)
    class_weight='balanced',# 处理类别不平衡
    random_state=42,        # 确保结果可复现
    probability=True,       # 启用概率估计
    verbose=True            # 显示训练过程
)

print("开始训练Kernel SVM模型...")
svm.fit(X_train_scaled, y_train)
print("Kernel SVM训练完成!")

# 评估模型
# ========================================================================
evaluate_model(svm, X_test, y_test, class_names=CLASS_NAMES)