# -*- encoding=utf-8 -*-

# 导入包
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import jieba
import sklearn
from sklearn.metrics import classification_report
import jieba.analyse
import csv
# 设置不以科学计数法输出
import numpy as np
np.set_printoptions(suppress=True)

# 载入自定义词典
# jieba.load_userdict(r'F:\文本标签\文本反垃圾\恶意推广文本分类\第一类赛事主体标签.txt')
# jieba.load_userdict(r'F:\文本标签\文本反垃圾\恶意推广文本分类\第二类网络主体标签.txt')

# 载入自定义停止词
# jieba.analyse.set_stop_words(r'F:\文本标签\文本反垃圾\恶意推广文本分类\stopwords.txt')


def preprocess_sentence(w):
    w = jieba.lcut(w)
    return w


def create_dataset():
    # 读取csv至字典
    csvFile = open("../output/comments_excel1.csv", "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    # labels = [item[0] for item in reader if item]
    # sentences = [preprocess_sentence(item[1]) for item in reader if item]
    items = [[int(float(item[0])), preprocess_sentence(item[1])] for item in reader if item]
    csvFile.close()
    # print(len(labels))
    # print(len(sentences))
    return zip(*items)


# 模型训练
def model_train(x_train, x_test, y_train, y_test):

    # 进行tfidf特征抽取
    tf = TfidfVectorizer()
    x_train = tf.fit_transform(x_train)
    joblib.dump(tf, "saved_model/Tfidf_model_test.m")
    x_test = tf.transform(x_test)

    # 通过朴素贝叶斯进行预测(拉普拉斯平滑系数为设置为1)
    mlb = MultinomialNB(alpha=1)
    mlb.fit(x_train, y_train)
    joblib.dump(mlb, "saved_model/mlb_model_test.m")

    # 训练集上的评测结果
    accuracy, auc = evaluate(mlb, x_train, y_train)
    print("训练集正确率：%.4f%%\n" % (accuracy * 100))
    print("训练集AUC值：%.6f\n" % (auc))

    # 测试集上的评测结果
    accuracy, auc = evaluate(mlb, x_test, y_test)
    print("测试集正确率：%.4f%%\n" % (accuracy * 100))
    print("测试AUC值：%.6f\n" % (auc))

    y_predict = mlb.predict(x_test)
    print(classification_report(y_test, y_predict, target_names=['0', '1']))

    return mlb, tf


# 模型评估
def evaluate(model, X, y):
    """评估数据集，并返回评估结果，包括：正确率、AUC值
    """
    accuracy = model.score(X, y)
    fpr, tpr, thresholds = sklearn.metrics.roc_curve(
        y, model.predict_proba(X)[:, 1], pos_label=1)
    return accuracy, sklearn.metrics.auc(fpr, tpr)


# 模型预测
def model_predict(text, model, tf):
    """
    :param text: 单个文本
    :param model: 朴素贝叶斯模型
    :param tf: 向量器
    :return: 返回预测概率和预测类别
    """
    text1 = [" ".join(jieba.cut(text))]

    # 进行tfidf特征抽取
    text2 = tf.transform(text1)

    predict_type = model.predict(text2)[0]

    predict_prob = model.predict_proba(text2)

    prob_0 = predict_prob[0][0]
    prob_1 = predict_prob[0][1]

    if predict_type == 1:
        result_prob = round(prob_1, 3)
    else:
        result_prob = round(prob_0, 3)

    return predict_type, result_prob


if __name__ == '__main__':

    # 读取数据
    # df = pd.read_table('F:/1.6期反垃圾改版/1.7期反垃圾升级/恶意推广/恶意推广训练文本.txt', sep='\t')
    label, data = create_dataset()
    data = (' '.join(item) for item in data)
    tem_data = []
    for item in data:
        str = (''.join(item))
        tem_data.append(str)

    data = tuple(tem_data)
    # print(label)
    # print(data)

    # Creating training and validation sets using an 80-20 split
    input_train, input_val, target_train, target_val = train_test_split(data, label, test_size=0.2)
    mlb, tf = model_train(input_train, input_val, target_train, target_val)

    # 预测单文本
    text = "既然选择相信，那就等他涅槃重生吧"
    predict_type, predict_prob = model_predict(text, mlb, tf)
    print(predict_type)
    print(predict_prob)
