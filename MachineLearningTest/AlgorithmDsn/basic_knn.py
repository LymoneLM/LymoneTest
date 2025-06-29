# Basic feature extraction and KNN
from sklearn.neighbors import KNeighborsClassifier  # 导入KNN分类器
from sklearn.model_selection import  GridSearchCV
import time
from basic_feature_extraction import load_and_preprocess_data
from model_evaluation import evaluate_model

# 类别名称
CLASS_NAMES = ['无泄漏', '弱泄漏', '严重泄漏']
# 加载预处理数据
X_train, X_test, y_train, y_test, scaler, X_train_scaled, X_test_scaled = load_and_preprocess_data()

# 训练KNN模型
# ========================================================================
print("开始训练KNN模型...")
start_time = time.time()

# 初始化KNN分类器
# 使用网格搜索寻找最佳参数
param_grid = {
    'n_neighbors': [3, 5, 7, 9, 11],
    'weights': ['uniform', 'distance'],
    'p': [1, 2]  # 1:曼哈顿距离, 2:欧氏距离
}

# 创建基础KNN模型
base_knn = KNeighborsClassifier(
    n_jobs=-1  # 使用所有CPU核心加速计算
)

# 使用网格搜索进行超参数调优
grid_search = GridSearchCV(
    estimator=base_knn,
    param_grid=param_grid,
    cv=5,  # 5折交叉验证
    scoring='accuracy',
    verbose=1,
    n_jobs=-1
)

# 执行网格搜索
grid_search.fit(X_train_scaled, y_train)

# 获取最佳模型
knn = grid_search.best_estimator_

# 训练结束时间
end_time = time.time()
training_time = end_time - start_time
print(f"KNN训练完成! 耗时: {training_time:.2f}秒")
print(f"最佳参数: {grid_search.best_params_}")
print(f"最佳交叉验证准确率: {grid_search.best_score_:.4f}")

# 评估模型
# ========================================================================
evaluate_model(knn, X_test, y_test, class_names=CLASS_NAMES)
