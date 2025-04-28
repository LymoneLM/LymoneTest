# 2. 描述性统计分析data-DSC.py
import pandas as pd
df = pd.read_csv('TaiwanRawDataSample.csv')
DSC = df.describe()
# 输出到本地文件中，文件名根据自己情况进行重新设定
writer = pd.ExcelWriter('TaiwanRawDataSample-DSC.xlsx')
DSC.to_excel(writer)

# writer.save()
writer.close()
