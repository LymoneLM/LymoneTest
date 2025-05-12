# 金融数据分析：基于pedquant下载数据的DY2012波动率溢出指数建模（通用版）
# 金融市场：债券、原油、黄金、股票
# 日期：2025-04-13

#---------------------- 初始化环境 ----------------------#
### 清理工作空间并设定工作目录
rm(list = ls())
setwd("D:/GitCode/LymoneTest/RTest/sc_work")
#setwd('/Users/macbookair2023/Desktop/2025_Financial data analysis')

library(pedquant)
library(xts)
library(rugarch)
library(vars)                 
library(frequencyConnectedness)  

#下载债券市场数据
df_Bond = md_future(symbol = 'T0')
pq_plot(df_Bond,chart_type="line")

#下载原油期货价格数据
df_Oil = md_future(symbol = 'OIL')
pq_plot(df_Oil,chart_type="line")

#下载伦敦黄金数据
df_hist_Gold = md_future(symbol = 'XAU')
pq_plot(df_hist_Gold,chart_type="line")

#下载股票价格数据
df_stock<-md_stock("000001.ss",date_range="max",source="163")
pq_plot(df_stock, chart_type = 'line') 

# 数据持久化保存
write.csv(df_Bond, file = "Bond.csv")
write.csv(df_Oil, file = "Oil.csv")
write.csv(df_hist_Gold, file = "Gold.csv")
write.csv(df_stock, file = "Stock.csv")

# 数据读取与格式转换 ---------------------------------------------------------
# 从本地文件读取数据
Bond <- read.csv("Bond.csv")
Oil <- read.csv("Oil.csv")
Gold <- read.csv("Gold.csv")
Stock <- read.csv("Stock.csv")

# 日期格式转换（假设第4列为日期列）
Bond$Date <- as.Date(Bond[, 4], format = "%Y-%m-%d")
Oil$Date <- as.Date(Oil[, 4], format = "%Y-%m-%d")
Gold$Date <- as.Date(Gold[, 4], format = "%Y-%m-%d")
Stock$Date <- as.Date(Stock[, 4], format = "%Y-%m-%d")

# 创建时间序列对象 -----------------------------------------------------------
# 使用收盘价构建时间序列（假设第8列为收盘价）
Bond_xts <- xts(Bond[, 8], order.by = Bond$Date)
Oil_xts <- xts(Oil[, 8], order.by = Oil$Date)
Gold_xts <- xts(Gold[, 8], order.by = Gold$Date)
Stock_xts <- xts(Stock[, 8], order.by = Stock$Date)

# 设置明确的列名
colnames(Bond_xts) <- "BondPrice"
colnames(Oil_xts) <- "OilPrice"
colnames(Gold_xts) <- "GoldPrice"
colnames(Stock_xts) <- "StockPrice"

# 收益率计算 ----------------------------------------------------------------
# 计算对数收益率：r_t = 100*(ln(P_t) - ln(P_{t-1}))
Bond_rt <- 100 * diff(log(Bond_xts))  
Oil_rt <- 100 * diff(log(Oil_xts))
Gold_rt <- 100 * diff(log(Gold_xts))
Stock_rt <- 100 * diff(log(Stock_xts))

# 数据清洗
Bond_rt <- na.omit(Bond_rt)
Oil_rt <- na.omit(Oil_rt)
Gold_rt <- na.omit(Gold_rt)
Stock_rt <- na.omit(Stock_rt)

# 设置收益率列名
colnames(Bond_rt) <- "BondReturns"
colnames(Oil_rt) <- "OilReturns"
colnames(Gold_rt) <- "GoldReturns"
colnames(Stock_rt) <- "StockReturns"

# GARCH模型波动率估计 ---------------------------------------------------------
# 模型设定
garch_spec <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = FALSE), # 简化均值方程
  distribution.model = "norm"
)

# 模型拟合
garch_fit_Bond <- ugarchfit(garch_spec, data = Bond_rt)
garch_fit_Oil <- ugarchfit(garch_spec, data = Oil_rt)
garch_fit_Gold <- ugarchfit(garch_spec, data = Gold_rt)
garch_fit_Stock <- ugarchfit(garch_spec, data = Stock_rt)
print(garch_fit_Bond)
print(garch_fit_Oil)
print(garch_fit_Gold)
print(garch_fit_Stock)

#---------------------- 波动率提取与可视化 --------------#
### 提取条件波动率
volatility_Bond <- sigma(garch_fit_Bond)
volatility_Oil <- sigma(garch_fit_Oil)
volatility_Gold <- sigma(garch_fit_Gold)
volatility_Stock <- sigma(garch_fit_Stock)

vol_Bond_xts <- xts(volatility_Bond, order.by = index(Bond_rt))  # 绑定日期信息
vol_Oil_xts <- xts(volatility_Oil, order.by = index(Oil_rt)) 
vol_Gold_xts <- xts(volatility_Gold, order.by = index(Gold_rt)) 
vol_Stock_xts <- xts(volatility_Stock, order.by = index(Stock_rt))

# 设置波动率列名
colnames(vol_Bond_xts) <- "BondVolatility"
colnames(vol_Oil_xts) <- "OilVolatility"
colnames(vol_Gold_xts) <- "GoldVolatility"
colnames(vol_Stock_xts) <- "StockVolatility"

# 波动率序列取自然对数以使得序列平稳
vol_Bond_xts <- log(vol_Bond_xts)
vol_Oil_xts <- log(vol_Oil_xts)
vol_Gold_xts <- log(vol_Gold_xts)
vol_Stock_xts <- log(vol_Stock_xts)

# 合并波动率数据 ------------------------------------------------------------
GARCH_volatility <- cbind(vol_Bond_xts, vol_Oil_xts,vol_Gold_xts,vol_Stock_xts)
GARCH_volatility <- na.omit(GARCH_volatility)

head(GARCH_volatility)  # 展示前6行数据

# 波动溢出指数建模 ------------------------------------------------------------
# 数据描述性统计
print("数据基本统计量：")
print(basicStats(GARCH_volatility))

# 静态溢出指数分析 ----------------------------------------------------------

est <- VAR(GARCH_volatility, p = 4, type = "const") #更改VAR模型的滞后阶数p
spilloverDY12(est, n.ahead = 10, no.corr = F) #更改VAR模型的预测步长n.ahead
sp_dy <- spilloverDY12(est, n.ahead = 10, no.corr = F) #得到静态溢出指数表


# 结果展示
overall(sp_dy) #总溢出指数
to(sp_dy) #To溢出指数
from(sp_dy) #From溢出指数
net(sp_dy) #净溢出指数
pairwise(sp_dy) #净配对溢出指数

# 结果输出
write.csv(overall(sp_dy),'overall(sp_dy).csv') #总溢出指数结果输出为CSV数据表
write.csv(to(sp_dy),'to(sp_dy).csv') #To溢出指数结果输出为CSV数据表
write.csv(from(sp_dy),'from(sp_dy).csv') #From溢出指数结果输出为CSV数据表
write.csv(net(sp_dy),'net(sp_dy).csv') #净溢出指数结果输出为CSV数据表
write.csv(pairwise(sp_dy),'pairwise(sp_dy).csv') #净配对溢出指数结果输出为CSV数据表

# 动态滚动窗口分析 ----------------------------------------------------------
params_est = list(p = 4, type = "const") #更改VAR模型的滞后阶数p
sp_dyrw <- spilloverRollingDY12(GARCH_volatility, n.ahead = 10, no.corr = F, "VAR", params_est = params_est, window = 200) #更改VAR模型的预测步长n.ahead；更改滚动窗口期数window

# 可视化分析结果
plotOverall(sp_dyrw)  #动态总溢出指数
plotTo(sp_dyrw)  #动态To溢出指数
plotFrom(sp_dyrw) #动态From溢出指数
plotNet(sp_dyrw) #动态净溢出指数
plotPairwise(sp_dyrw) #动态净配对溢出指数

# 动态结果输出
write.csv(overall(sp_dyrw),'overall(sp_dyrw).csv') #动态总溢出指数结果输出为CSV数据表
write.csv(to(sp_dyrw),'to(sp_dyrw).csv') #动态To溢出指数结果输出为CSV数据表
write.csv(from(sp_dyrw),'from(sp_dyrw).csv') #动态From溢出指数结果输出为CSV数据表
write.csv(net(sp_dyrw),'net(sp_dyrw).csv') #动态净溢出指数结果输出为CSV数据表
write.csv(pairwise(sp_dyrw),'pairwise(sp_dyrw).csv') #动态净配对溢出指数结果输出为CSV数据表

