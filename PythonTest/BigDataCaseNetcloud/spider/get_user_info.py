# 根据userId爬取用户信息

import json
import urllib.request
import urllib.parse
import time

data_path = "../data/origin"
output_path = "../output"

def doGet(url):
    while True:
        try:
            req = urllib.request.Request(url=url, method="GET")
            response = urllib.request.urlopen(req)
            res = response.read().decode('utf-8')
            return json.loads(res)
        except Exception as e:
            print("异常URL：{}".format(url))
            print(e)
            time.sleep(10)


def getUserCity(userId):
    url = "http://163api.qijieya.cn/user/detail?uid={}".format(userId)
    res = doGet(url)
    try:
        city = res['profile']['city']
        return city
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    file = open(output_path+"/userIds.txt")
    out_file = open(output_path+"/userCities.txt", mode="w")
    i = 1
    for line in file:
        try:
            s = line.replace('\n', '')
            userId = int(s)
            city = getUserCity(userId)
            out_file.write("{} {}\n".format(userId, city))
            print("{} {}\n".format(userId, city))
            out_file.flush()
            time.sleep(0.5)
        except Exception as e:
            print(e)
        if i % 100 == 0:
            print("No.{}".format(i))
    out_file.close()
