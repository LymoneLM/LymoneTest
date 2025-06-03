# -*- encoding=utf-8 -*-

# 导入包
from sklearn.model_selection import train_test_split
import os
import json
import joblib
import jieba
import sklearn
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
    csvFile = open("labeled_data.csv", "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    # labels = [item[0] for item in reader if item]
    # sentences = [preprocess_sentence(item[1]) for item in reader if item]
    items = [[int(float(item[0])),
              preprocess_sentence(item[1])] for item in reader if item]
    csvFile.close()
    # print(len(labels))
    # print(len(sentences))
    return zip(*items)


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


def load_predict_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [preprocess_sentence(line.strip()) for line in f if len(line) > 10]
    data = [" ".join(str_list) for str_list in data]
    return data


def model_predict_file(data, model, tf):
    if data:
        data = tf.transform(data)
        predict_type = model.predict(data)
        comment_len = len(predict_type)
        sensitive_score = np.sum(predict_type)/comment_len
        return comment_len, sensitive_score
    else:
        return 0, 0


def model_predict_forder(folder, model, tf):
    info_dict = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            # single file predict
            try:
                data = load_predict_data(file_path)
                comment_len, sensitive_score = model_predict_file(data, mlb, tf)
                item_dict = {}
                item_dict['len'] = comment_len
                item_dict['score'] = sensitive_score
                item_name, extension = os.path.splitext(file)
                info_dict[item_name] = item_dict
            except Exception as e:
                print(e)

    return info_dict


if __name__ == '__main__':
    # 测试集上进行测试
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
    input_train, input_val, target_train, target_val = train_test_split(
        data, label, test_size=0.2)
    mlb = joblib.load("saved_model/mlb_model.m")
    tf = joblib.load("saved_model/Tfidf_model.m")

    x_test = tf.transform(input_val)
    # for i in x_test:
    #     print(i)
    y_test = target_val
    # 测试集上的评测结果
    accuracy, auc = evaluate(mlb, x_test, y_test)
    print("测试集正确率：%.4f%%\n" % (accuracy * 100))
    print("测试AUC值：%.6f\n" % (auc))

    # 预测歌曲数据，歌手数据，时间数据
    base_dir = "classes_data"
    singers_dir = os.path.join(base_dir, "singers_data")
    songs_dir = os.path.join(base_dir, "songs_data")
    time_dir = os.path.join(base_dir, "time_data")

    # info_dict = model_predict_forder(time_dir, mlb, tf)
    # with open("classes_data/time_info.json", 'w') as f:
    #     json.dump(info_dict, f)
