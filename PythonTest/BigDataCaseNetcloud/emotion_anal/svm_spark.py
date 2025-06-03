#!/usr/bin/python3
# -*-coding: UTF-8 -*-
import csv
import jieba
from gensim.models.doc2vec import Doc2Vec
from sklearn.model_selection import train_test_split
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import SVMWithSGD

# 命令行下以下不用设置，已存在相应实例
conf = SparkConf().setAppName("ex4").setMaster("local")
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")   # 设置日志级别
spark = SparkSession(sc)
root_dir = 'file:///home/hadoop/project/'


def preprocess_sentence(w):
    w = jieba.lcut(w)
    return w


def create_dataset():
    # 读取csv至字典
    data_path = root_dir + 'labeled_data.csv'
    csvFile = open(data_path, "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    # labels = [item[0] for item in reader if item]
    # sentences = [preprocess_sentence(item[1]) for item in reader if item]
    items = [[int(float(item[0])),
              preprocess_sentence(item[1])] for item in reader if item]
    csvFile.close()
    # print(len(labels))
    # print(len(sentences))
    return zip(*items)


def create_rdd_data(data, label):
    list = [LabeledPoint(i, item) for item, i in zip(data, label)]
    rdd_data = sc.parallelize(list)
    return rdd_data


def Getpoint(model, point):
    """
    预测并返回结果(元组)
    :param model: 训练集构建的SVMWithSGD模型
    :param point: 测试集数据，标准LabeledPoint类型数据
    :return:(测试集预测得分，原始标签)
    """
    score = model.predict(point.features)
    return (score, point.label)


if __name__ == '__main__':

    # 加载句子向量模型
    model_file = root_dir + "doc2vec_files/save.model"
    doc_vector_model = Doc2Vec.load(model_file)

    label, data = create_dataset()
    data = [doc_vector_model.infer_vector(item) for item in data]
    data = tuple(data)
    input_train, input_val, target_train, target_val = train_test_split(data, label, test_size=0.2)

    # 创建rdd数据
    train_data = create_rdd_data(input_train, target_train)
    test_data = create_rdd_data(input_val, target_val)

    # 模型训练
    svm = SVMWithSGD.train(train_data, iterations=10)
    # result = svm.predict(test_data.features()).collect()

    # 评估模型
    svm.setThreshold(-90000)  # 默认阈值 -90000
    scoreAndLabels = test_data.map(lambda point: Getpoint(svm, point))
    # 计算精度
    accuracy = scoreAndLabels.filter(lambda l: l[0] == l[1]).count() / test_data.count()
    print(accuracy)
