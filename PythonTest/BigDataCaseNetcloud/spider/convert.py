# 筛选出用于打标签的评论数据集

import json
import random
import pandas

data_path = "../data/origin"
output_path = "../output"

def main1():
    in_file = open(data_path+"/comments_1.txt", mode="r", encoding="utf-8")
    out_file = open(output_path+"/1_comm.txt", mode="w", encoding="utf-8")

    remove = "，。、？》《：；“”‘’.\r\n"

    i = 0
    for line in in_file:
        try:
            obj = json.loads(line)
        except:
            print("error")
            continue
        s = obj['content']

        # print(line)
        # print(obj['likedCount'])
        if obj['likedCount'] < 5000:
            continue

        for c in remove:
            s = s.replace(c, " ")

        if len(s) < 40:
            continue
        out_file.write(s + "\n")
        # print(s)
        i += 1
        if i % 100 == 0:
            print(i)
    print("完成: {}条评论".format(i))
    out_file.close()
    in_file.close()


# 以概率1/n返回True
def my_rand(n: int):
    i = random.randint(1, n)
    return i == 1


def main2():
    keywords = ['爱', '伤', '情', '抱歉', '对不起', '世']
    in_file = open(output_path+"/1_comm.txt", encoding="utf-8")
    res = []
    for line in in_file:
        f = 0
        for k in keywords:
            if line.find(k) != -1:
                f = 1
        if f == 0:
            if my_rand(6):
                res.append(line.replace('\n', ''))
        else:
            if my_rand(3):
                res.append(line.replace('\n', ''))
    in_file.close()

    t = []
    i = 0
    for item in res:
        t.append(item)
        if len(t) >= 500:
            i += 1
            data = pandas.DataFrame(t)
            data.to_csv(output_path+"/comments_excel{}.csv".format(i), index=False, encoding='utf-8')
            t.clear()
    i += 1
    data = pandas.DataFrame(t)
    data.to_csv(output_path+"/comments_excel{}.csv".format(i), index=False, encoding='utf-8')
    t.clear()


if __name__ == '__main__':
    main2()
