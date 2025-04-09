# 1. 数据抽取
import pandas as pd
df = pd.read_csv('TaiwanRawData-nonDefault.csv')
df.head()
# 随机抽取n条数据
n = 6636
sampled_data = df.sample(n=n)

# 输出到本地文件中，文件名根据自己情况进行重新设定
writer = pd.ExcelWriter('TaiwanRawData-nonDefault-sample.xlsx')
sampled_data.to_excel(writer)

writer.save()
writer.close()