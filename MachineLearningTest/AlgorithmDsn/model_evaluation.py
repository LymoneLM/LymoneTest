# model_evaluation.py
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def evaluate_model(model, X_test, y_test, class_names=None, model_name="模型"):
    """
    评估模型性能并生成报告

    参数:
        model: 训练好的模型
        X_test: 测试集特征
        y_test: 测试集标签
        class_names: 类别名称列表
    """
    # 预测测试集
    y_pred = model.predict(X_test)

    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n{model_name}测试集准确率: {accuracy:.4f}")

    # 生成分类报告
    print("\n分类报告:")
    if class_names:
        print(classification_report(y_test, y_pred, target_names=class_names))
    else:
        print(classification_report(y_test, y_pred))

    # 计算混淆矩阵
    conf_matrix = confusion_matrix(y_test, y_pred)
    print("混淆矩阵:")
    print(conf_matrix)

    return accuracy, conf_matrix