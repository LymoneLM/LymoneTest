
#---------------------- 初始化环境 ----------------------#
### 清理工作空间并设定工作目录
rm(list = ls())
setwd("D:/GitCode/LymoneTest/RTest/sc_work")
#setwd('/Users/macbookair2023/Desktop/2025_Financial data analysis')

library(pedquant)
library(ggplot2)
library(xts)
library(rugarch)
library(rmgarch)

# 下载美元指数数据
dt_USD = ed_fred(symbol = 'DTWEXBGS', date_range = 'max')
# 查看数据结构
str(dt_USD)

# 提取 data.table 数据框
dt_USD_df <- dt_USD[[1]]

# 绘制折线图
ggplot(dt_USD_df, aes(x = date, y = value)) +
  geom_line() +
  labs(title = "Nominal Broad U.S. Dollar Index",
       x = "Date",
       y = "Index Value")

#下载原油期货价格数据
df_Oil = md_future(symbol = 'OIL')
pq_plot(df_Oil,chart_type="line")

# 数据持久化保存
write.csv(dt_USD, file = "USD.csv")
write.csv(df_Oil, file = "Oil.csv")

# 数据读取与格式转换 ---------------------------------------------------------
# 从本地文件读取数据
USD <- read.csv("USD.csv")
Oil <- read.csv("Oil.csv")

# 日期格式转换（假设第4列为日期列）
USD$Date <- as.Date(USD[, 4], format = "%Y-%m-%d")
Oil$Date <- as.Date(Oil[, 4], format = "%Y-%m-%d")

# 创建时间序列对象 -----------------------------------------------------------
# 使用收盘价构建时间序列（假设第8列为收盘价）
USD_xts <- xts(USD[, 5], order.by = USD$Date)
Oil_xts <- xts(Oil[, 8], order.by = Oil$Date)

# 设置明确的列名
colnames(USD_xts) <- "USDPrice"
colnames(Oil_xts) <- "OilPrice"

# 收益率计算 ----------------------------------------------------------------
# 计算对数收益率：r_t = 100*(ln(P_t) - ln(P_{t-1}))
USD_rt <- 100 * diff(log(USD_xts))  
Oil_rt <- 100 * diff(log(Oil_xts))

# 数据清洗
USD_rt <- na.omit(USD_rt)
Oil_rt <- na.omit(Oil_rt)

# 设置收益率列名
colnames(USD_rt) <- "USDReturns"
colnames(Oil_rt) <- "OilReturns"

# 合并收益率数据 ------------------------------------------------------------
USD_Oil_ret <- cbind(USD_rt, Oil_rt)
USD_Oil_ret <- na.omit(USD_Oil_ret)
head(USD_Oil_ret)  # 展示前6行数据

# DCC-GARCH模型设定 ---------------------------------------------------------
# 单变量GARCH模型设定（对每个收益率序列）
### 第1个股票的设定
uspec1 = ugarchspec(variance.model=list(model="sGARCH",
                                        garchOrder = c(1, 1)),mean.model = list(armaOrder = c(0, 0),
                                                                                include.mean = TRUE))
### 第2个股票的设定
uspec2 = ugarchspec(variance.model=list(model="sGARCH",
                                        garchOrder = c(1, 1)),mean.model = list(armaOrder = c(0, 0), 
                                                                                include.mean = TRUE))

# 创建多变量模型设定
mspec = multispec(c(uspec1,uspec2)) 

# DCC模型参数设定
dcc_spec = dccspec(mspec,dccOrder = c(1,1),model="DCC",
                   distribution = c("mvnorm")) 
# 模型估计 ----------------------------------------------------------------
dcc_fit <- dccfit(dcc_spec, data = USD_Oil_ret)

# 模型结果展示 ------------------------------------------------------------
show(dcc_fit)      # 显示估计结果
plot(dcc_fit)      # 绘制模型诊断图形

# 结果提取与输出 -----------------------------------------------------------
# 提取时变协方差矩阵（维度：资产数×资产数×时间点）
dynamic_cov <- rcov(dcc_fit)
dim(dynamic_cov)  # 查看数据维度

# 提取美元指数与原油间的协方差序列
USD_Oil_cov <- dynamic_cov[1, 2, ]

# 提取时变相关系数矩阵
dynamic_cor <- rcor(dcc_fit)

# 提取特定资产间的相关系数序列
USD_Oil_cor <- dynamic_cor[1, 2, ]

# 保存动态相关系数到CSV文件
write.csv(USD_Oil_cor, file = "USD_Oil_DCC_Correlation.csv")

# 提取模型残差 ------------------------------------------------------------
model_residuals <- residuals(dcc_fit)

