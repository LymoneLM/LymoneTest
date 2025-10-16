import random
import time

str_list = [
    "wgf",
    "Python 3.9.7",
    "2023-04-15 数据记录",
    "温度: 23.5°C, 湿度: 45%",
    "错误代码: 404",
    "用户: admin, 登录时间: 10:30",
    "处理完成，耗时: 1.25秒",
    "警告: 内存使用超过阈值",
    "数据分析结果: 正相关",
    "最后更新: 2023-04-15"
]

i = 0
while i < 100:
    time.sleep(random.randint(0,5))
    file_str = str(random.randint(0,1000))
    file_path = "/home/hadoop/data/out"+"wgf140"+file_str+".txt"
    with open(file_path,'w') as out:
        for _ in range(4):
            out.write(str_list[random.randint(0,13)])
    i += 1