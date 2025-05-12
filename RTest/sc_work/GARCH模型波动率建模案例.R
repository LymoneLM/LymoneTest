# 金融数据分析：上证指数波动率建模
# 日期：2025-03-31

#---------------------- 初始化环境 ----------------------#
### 清理工作空间并设定工作目录
rm(list = ls())
#setwd('F:/桌面/2025_Financial data analysis')
setwd("D:/GitCode/LymoneTest/RTest/sc_work")

#---------------------- 数据准备 ------------------------#
### 读取原始数据
# 数据说明：包含1990-12-19至2025-03-25的上证指数数据
# 第4列为日期列，第7列为收盘价列（根据实际情况调整）
szzs <- read.csv("my_data.csv")

### 日期格式转换
# 注意：日期格式需与实际数据匹配，此处假设为"%Y-%m-%d"
szzs$Date <- as.Date(szzs[, 4], format = "%Y-%m-%d")  

### 创建时间序列对象
# 使用xts包处理时间序列数据，保留日期信息
library(xts)
sz_xts <- xts(szzs[, 7], order.by = szzs$Date)
colnames(sz_xts) <- "ClosePrice"  # 明确列名

#---------------------- 收益率计算 ----------------------#
### 计算对数收益率
# 公式：r_t = 100 * (ln(P_t) - ln(P_{t-1}))
rt <- 100 * diff(log(sz_xts))  
rt <- na.omit(rt)  # 删除首个NA值
colnames(rt) <- "Returns"  # 明确列名

#---------------------- 探索性分析 ----------------------#
### 绘制价格与收益率序列图
# 价格序列图
plot(sz_xts, 
     type = "l", 
     main = "上证指数价格序列 (1990-2025)",
     xlab = "日期", 
     ylab = "收盘价",
     col = "darkblue",
     major.ticks = "years",
     grid.ticks.on = "years")

# 收益率序列图
plot(rt, 
     type = "l", 
     main = "上证指数日收益率序列",
     xlab = "日期", 
     ylab = "收益率 (%)",
     col = "steelblue",
     major.ticks = "years",
     grid.ticks.on = "years")

#---------------------- 自相关性检验 --------------------#
### ACF/PACF分析
#windows(width = 10, height = 5)（Windows系统电脑）
dev.new(width = 10, height = 5)
par(mfrow = c(1, 2))
acf(rt, lag.max = 20, main = "收益率ACF")
pacf(rt, lag.max = 20, main = "收益率PACF")

### Ljung-Box白噪声检验
# 检验原假设：序列不存在自相关
cat("Ljung-Box检验结果:\n")
print(Box.test(rt, lag = 1, type = "Ljung-Box"))  # 短期相关性
print(Box.test(rt, lag = 10, type = "Ljung-Box")) # 长期相关性

#---------------------- 均值方程建模 --------------------#
### 自动ARIMA建模
library(forecast)
best_model <- auto.arima(rt)
cat("最优ARIMA模型:", capture.output(best_model), "\n")

### 手动指定ARIMA(2,0,3)模型
fit_arima <- arima(rt, order = c(2, 0, 3))
cat("\nARIMA(2,0,3)模型摘要:\n")
print(summary(fit_arima))

### 残差分析
et <- residuals(fit_arima)
tsdiag(fit_arima)  # 残差诊断图

# 残差白噪声检验
cat("\n残差Ljung-Box检验:\n")
print(Box.test(et, lag = 1, type = "Ljung-Box"))  # 滞后1期
print(Box.test(et, lag = 5, type = "Ljung-Box"))  # 滞后5期

#---------------------- 波动率建模 ----------------------#
### ARCH效应检验
# Ljung-Box检验平方残差
cat("\nARCH效应检验(Ljung-Box):\n")
print(Box.test(et^2, lag = 1, type = "Ljung-Box"))
print(Box.test(et^2, lag = 5, type = "Ljung-Box"))
print(Box.test(et^2, lag = 10, type = "Ljung-Box"))

# Engle's LM检验
library(FinTS)
cat("\nARCH效应检验(Engle's LM):\n")
print(ArchTest(et, lags = 10))

#---------------------- GARCH模型构建 -------------------#
### 基础GARCH(1,1)模型
library(rugarch)

# 模型设定
garch_spec <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = FALSE), # 简化均值方程
  distribution.model = "norm"
)

# 模型拟合
garch_fit <- ugarchfit(garch_spec, data = rt)
cat("\nGARCH(1,1)模型结果:\n")
print(garch_fit)

### 模型诊断
# 标准化残差检验
std_resid <- residuals(garch_fit, standardize = TRUE)
cat("\n标准化残差检验:\n")
for (lag in c(1, 5, 10)) {
  cat("---- 滞后", lag, "期检验 ----\n")
  print(Box.test(std_resid, lag = lag, type = "Ljung-Box"))   # 均值方程
  print(Box.test(std_resid^2, lag = lag, type = "Ljung-Box")) # 波动率方程
}

#---------------------- 波动率提取与可视化 --------------#
### 提取条件波动率
volatility <- sigma(garch_fit)
vol_xts <- xts(volatility, order.by = index(rt))  # 绑定日期信息

### 波动率可视化
# 单一波动率图
plot(vol_xts, 
     type = "l", 
     main = "上证指数条件波动率 (GARCH(1,1))",
     xlab = "日期", 
     ylab = "波动率",
     col = "darkred",
     major.ticks = "years",
     grid.ticks.on = "years")

# 收益率与波动率对比图
plot(rt, 
     main = "收益率 vs 波动率",
     col = "gray50",
     major.ticks = "years")
lines(vol_xts, col = "darkred", lwd = 1.2)
legend("topright", 
       legend = c("收益率", "波动率"), 
       col = c("gray50", "darkred"), 
       lty = 1,
       cex = 0.8)

#---------------------- 扩展模型比较 --------------------#
### EGARCH模型
egarch_spec <- ugarchspec(
  variance.model = list(model = "eGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(2, 3), include.mean = TRUE),
  distribution.model = "norm"
)
egarch_fit <- ugarchfit(egarch_spec, rt)
cat("\nEGARCH(1,1)模型结果:\n")
print(egarch_fit)

### GJR-GARCH模型
gjrgarch_spec <- ugarchspec(
  variance.model = list(model = "gjrGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(2, 3), include.mean = TRUE),
  distribution.model = "norm"
)
gjrgarch_fit <- ugarchfit(gjrgarch_spec, rt)
cat("\nGJR-GARCH(1,1)模型结果:\n")
print(gjrgarch_fit)
