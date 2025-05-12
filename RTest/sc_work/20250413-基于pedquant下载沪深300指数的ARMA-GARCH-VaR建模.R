# 金融数据分析：基于pedquant下载沪深300指数的ARMA-GARCH-VaR建模
# 日期：2025-04-13

#---------------------- 初始化环境 ----------------------#
### 清理工作空间并设定工作目录
rm(list = ls())
setwd("D:/GitCode/LymoneTest/RTest/sc_work")
#setwd('/Users/macbookair2023/Desktop/2025_Financial data analysis')

library(pedquant)
library(xts)
library(rugarch)
library(readxl)
library(fBasics)

# 数据获取与预处理 -----------------------------------------------------------
# 通过网易财经接口获取股票数据
hs300 <- md_stock("000300.ss", 
                 from = '2005-01-04',
                 to = '2025-04-11',
                 source = "163")  # 上证指数

# 数据持久化保存
write.csv(hs300, file = "hs300.csv")

# 数据读取与格式转换 ---------------------------------------------------------

# 数据说明：包含2005-04-11至2022-07-08的上证指数数据
# 第4列为日期列，第8列为收盘价列（根据实际情况调整）
hs300 <- read.csv("hs300.csv")

### 日期格式转换
# 注意：日期格式需与实际数据匹配，此处假设为"%Y-%m-%d"
hs300$Date <- as.Date(hs300[, 4], format = "%Y-%m-%d")  

### 创建时间序列对象
# 使用xts包处理时间序列数据，保留日期信息
hs300_xts <- xts(hs300[, 8], order.by = hs300$Date)
colnames(hs300_xts) <- "ClosePrice"  # 明确列名

#---------------------- 收益率计算 ----------------------#
### 计算对数收益率
# 公式：r_t = 100 * (ln(P_t) - ln(P_{t-1}))
returns_xts <- 100 * diff(log(hs300_xts))  
returns_xts <- na.omit(returns_xts)  # 删除首个NA值
colnames(returns_xts) <- "Returns"  # 明确列名

# 探索性数据分析
plot(returns_xts, main = "HS300收益率序列", col = "blue")

# 描述性统计（使用xts对象）
cat("\n描述性统计:\n")
print(basicStats(returns_xts))

# 平稳性检验 (ADF)
cat("\nADF检验:\n")
print(adf.test(coredata(returns_xts), lags = 1, type = 'c'))

# 正态性检验 (Jarque-Bera)
cat("\n正态性检验:\n")
print(normalTest(returns_xts[, 1], method = 'jb'))

# 自相关性检验 (Ljung-Box)
cat("\nLjung-Box检验:\n")
print(Box.test(returns_xts[, 1], lag = 15, type = 'Ljung'))

# ARCH效应检验 (LM检验)
cat("\nARCH效应检验:\n")
print(ArchTest(returns_xts[, 1], 15))


# GARCH建模与诊断 ----------------------------------------------------------
# 模型设定（使用正态分布）
garch_spec <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "norm"
)

# 模型拟合
garch_fit <- ugarchfit(data = returns_xts[, 1], spec = garch_spec)
print(garch_fit)  # 显示模型摘要

# 标准化残差分析
std_resid <- residuals(garch_fit, standardize = TRUE)
ArchTest(std_resid, 15)  # 再次检验ARCH效应


# VaR计算 ----------------------------------------------------------------
# 提取模型参数
sigma <- sigma(garch_fit)
mu <- fitted(garch_fit)

# 计算分位数（使用正态分布）
alpha <- c(0.01, 0.05)
q_lower <- qnorm(alpha)        # 左尾分位数
q_upper <- qnorm(1 - alpha)    # 右尾分位数

# 计算VaR（假设多头头寸关注左尾，空头头寸关注右尾）
# 提取日期序列
dates <- index(returns_xts)

VaR <- data.frame(
  Date = as.character(dates),     # 日期列
  Returns = returns_xts[, 1],     # 收益率
  VaR_1D_Lower = mu + sigma * q_lower[1],  # 1% 左尾
  VaR_5D_Lower = mu + sigma * q_lower[2],  # 5% 左尾
  VaR_5U_Upper = mu + sigma * q_upper[2],  # 5% 右尾
  VaR_1U_Upper = mu + sigma * q_upper[1]   # 1% 右尾
)

# 结果保存
write.csv(VaR, "VaR_results.csv", row.names = FALSE)

# 模型估计结果可视化（可选） ----------------------------------------------------------

# 读取数据并转换日期格式
var_data <- read.csv("VaR_results.csv")
var_data$Date <- as.Date(var_data$Date)

# 绘制带完整图例的线条图
library(ggplot2)
ggplot(var_data) +
  geom_line(aes(x = Date, y = Returns, color = "实际收益率"), linewidth = 0.7) +
  geom_line(aes(x = Date, y = VaR_1D_Lower, color = "1% VaR下界"), linetype = "dashed") +
  geom_line(aes(x = Date, y = VaR_5D_Lower, color = "5% VaR下界"), linetype = "dashed") +
  geom_line(aes(x = Date, y = VaR_1U_Upper, color = "1% VaR上界"), linetype = "dashed") +
  geom_line(aes(x = Date, y = VaR_5U_Upper, color = "5% VaR上界"), linetype = "dashed") +
  scale_color_manual(
    name = "图例",
    values = c(
      "实际收益率" = "#1f77b4",      # 蓝色
      "1% VaR下界" = "#ff7f0e",    # 橙色
      "5% VaR下界" = "#d62728",    # 红色
      "1% VaR上界" = "#2ca02c",    # 绿色
      "5% VaR上界" = "#9467bd"     # 紫色
    ),
    guide = guide_legend(
      title.position = "top",
      title.hjust = 0.5,
      ncol = 5  # 分两列显示图例
    )
  ) +
  labs(
    title = "收益率与风险价值（VaR）动态监测",
    x = "日期",
    y = "收益率"
  ) +
  theme_minimal() +
  theme(
    legend.position = "bottom",
    plot.title = element_text(hjust = 0.5, face = "bold"),
    panel.grid.minor = element_blank()
  )

