# four.py
import warnings

warnings.filterwarnings("ignore", message="The number of unique classes is greater than 50% of the number of samples")
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import joblib
import matplotlib.pyplot as plt

# 显示中文
plt.rcParams['font.sans-serif']=['Microsoft YaHei']
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# 1. 加载Otto数据集
dpath = "./data/"
otto_df = pd.read_csv(dpath + "otto_train.csv")

# 2. 数据预处理
# 分离特征和标签
X = otto_df.drop('target', axis=1)
y = otto_df['target']


# 编码标签
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=33
)

# 3. SVM分类训练
C_values = np.logspace(-2, 3, 10)  # 10个不同的C值
results = []

for C_val in C_values:
    svm = LinearSVC(C=C_val, max_iter=10000, random_state=33)
    svm.fit(X_train, y_train)

    # 预测
    y_train_pred = svm.predict(X_train)
    y_test_pred = svm.predict(X_test)

    # 计算准确率
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)

    results.append({
        'C': C_val,
        'train_accuracy': train_acc,
        'test_accuracy': test_acc
    })

    print(f"C={C_val:.4f}: 训练集准确率={train_acc:.4f}, 测试集准确率={test_acc:.4f}")

# 4. 保存最佳模型
best_result = max(results, key=lambda x: x['test_accuracy'])
best_svm = LinearSVC(C=best_result['C'], max_iter=10000, random_state=33)
best_svm.fit(X_train, y_train)
joblib.dump(best_svm, 'Otto_LinearSVC.pkl')
print(f"\n保存最佳模型: C={best_result['C']:.4f}, 测试集准确率={best_result['test_accuracy']:.4f}")

# 5. 可视化结果
plt.figure(figsize=(10, 6))
plt.semilogx(C_values, [res['train_accuracy'] for res in results], 'bo-', label='训练集')
plt.semilogx(C_values, [res['test_accuracy'] for res in results], 'ro-', label='测试集')
plt.xlabel('C值 (正则化强度)')
plt.ylabel('准确率')
plt.title('SVM不同C值下的准确率')
plt.legend()
plt.grid(True)
plt.savefig('svm_accuracy_results.png')
plt.show()

# 保存结果为Excel
results_df = pd.DataFrame(results)
results_df.to_excel('svm_accuracy_results.xlsx', index=False)