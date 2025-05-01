# 3. 关键指标的描述性统计分析（以“年龄”、“性别”指标为例）data-indicator-DSC.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('TaiwanRawDataSample.csv')
age = df.iloc[:, 4]
plt.figure(figsize=(8, 4), dpi=80)
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
n, bins, patches = plt.hist(age, 10, facecolor='blue', alpha=0.8, edgecolor='white', lw=1)
mu = np.mean(age)  # 平均值
sigma = np.std(age)   # 标准差
plt.title('年龄频数直方图' + '，人数：' + str(len(age)))
plt.legend([r'正态分布: $\mu=%.2f$, $\sigma=%.2f$' % (mu, sigma)])
plt.show()


label = ["男", "女"]
# df = pd.read_csv('TaiwanRawDataSample.csv')
data = [7, 5]  # 需要查看自己数据集的男、女人数各自为多少
exp = [0, 0]   # 各项离饼图圆心为n个半径
plt.pie(x=data, labels=label, explode=exp, shadow=True, autopct='%1.0f%%')
plt.legend()
plt.show()
