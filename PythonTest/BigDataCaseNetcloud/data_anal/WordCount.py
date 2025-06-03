from pyspark import SparkConf, SparkContext
from visualize import visualize
import jieba

SRCPATH = '/home/hadoop/Experiment/Ex2_WordCount/src/'

conf = SparkConf().setAppName("ex2").setMaster("local")
sc = SparkContext(conf=conf)

def getStopWords(stopWords_filePath):
    stopwords = [line.strip() for line in open(stopWords_filePath, 'r', encoding='utf-8').readlines()]
    return stopwords

def jiebaCut(answers_filePath):

    # 读取answers.txt
    answersRdd = sc.textFile(answers_filePath) # answersRdd每一个元素对应answers.txt每一行
    # 利用SpardRDD reduce()函数,合并所有回答
    # 【现在你应该完成下面函数编码】

    str = answersRdd.reduce(lambda a, b: a + b)

    # jieba分词
    words_list = jieba.lcut(str)
    return words_list

def wordcount(isvisualize=False):
    # 读取停用词表
    stopwords = getStopWords(SRCPATH + 'stop_words.txt')
    # 结巴分词
    words_list = jiebaCut("file://" + SRCPATH + "commentwrite.txt")
    # 词频统计
    wordsRdd = sc.parallelize(words_list)
    resRdd = wordsRdd.filter(lambda word: word not in stopwords).filter(lambda word: len(word) >1).map(lambda word: (word,1)).reduceByKey(lambda a, b: a + b ).sortBy(ascending=False, numPartitions=None, keyfunc=lambda x: x[1])
    #resRdd.foreach(print)
    # 可视化展示
    if isvisualize:
        v = visualize()
        # 词云可视化
        wwDic = v.rdd2dic(resRdd,100)
        v.drawWorcCloud(wwDic)
        # 饼状图可视化
        pieDic = v.rdd2dic(resRdd,10)
        #v.drawPie(pieDic)
    return  resRdd
    
if __name__ == '__main__':

    # 进行词频统计并可视化
    resRdd = wordcount(isvisualize=True)
    print(resRdd.take(100))  # 查看前10个
    #wordcount(isvisualize=True)

