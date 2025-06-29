# Basic feature extraction and random forest
from sklearn.ensemble import RandomForestClassifier
from basic_feature_extraction import load_and_preprocess_data
from model_evaluation import evaluate_model

# 类别名称
CLASS_NAMES = ['无泄漏', '弱泄漏', '严重泄漏']
# 加载预处理数据
X_train, X_test, y_train, y_test, scaler, X_train_scaled, X_test_scaled = load_and_preprocess_data()

# 训练随机森林模型
# ========================================================================
# 初始化随机森林分类器
rf = RandomForestClassifier(
    n_estimators=100,  # 树的数量
    class_weight='balanced',  # 处理类别不平衡
    random_state=42,  # 确保结果可复现
    n_jobs=-1,  # 使用所有CPU核心
    verbose=1  # 添加训练进度条 (1=显示进度)
)

# 训练模型
rf.fit(X_train_scaled, y_train)

# 评估模型
# ========================================================================
evaluate_model(rf, X_test, y_test, class_names=CLASS_NAMES)
