# 加载必要的包
library(xts)
library(vars)
library(rugarch)
library(rmgarch)
library(fBasics)
library(frequencyConnectedness) 
library(dplyr)

data <- read.csv("bank_returns.csv",
                 header = TRUE,
                 stringsAsFactors = FALSE,
                 fileEncoding = "UTF-8")

returns <- xts(x = data[, -1],
               order.by = as.Date(data$Date))

# ========DY2012方法==========

# GARCH模型波动率估计 --------------------------------------------------------
# 模型设定（使用与示例相同的参数）
garch_spec <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = FALSE),
  distribution.model = "norm"
)

# 对每家银行分别拟合GARCH模型
garch_fit_ICBC <- ugarchfit(garch_spec, data = returns$ICBC)
garch_fit_ABC <- ugarchfit(garch_spec, data = returns$ABC)
garch_fit_BOC <- ugarchfit(garch_spec, data = returns$BOC)
garch_fit_CCB <- ugarchfit(garch_spec, data = returns$CCB)
garch_fit_CMB <- ugarchfit(garch_spec, data = returns$CMB)

# 提取条件波动率 ------------------------------------------------------------
vol_ICBC <- xts(log(sigma(garch_fit_ICBC)), order.by = index(returns))
vol_ABC <- xts(log(sigma(garch_fit_ABC)), order.by = index(returns))
vol_BOC <- xts(log(sigma(garch_fit_BOC)), order.by = index(returns))
vol_CCB <- xts(log(sigma(garch_fit_CCB)), order.by = index(returns))
vol_CMB <- xts(log(sigma(garch_fit_CMB)), order.by = index(returns))

# 合并波动率数据
GARCH_vol <- cbind(vol_ICBC, vol_ABC, vol_BOC, vol_CCB, vol_CMB)
colnames(GARCH_vol) <- c("ICBC_vol", "ABC_vol", "BOC_vol", "CCB_vol", "CMB_vol")
GARCH_vol <- na.omit(GARCH_vol)

# 描述性统计
print(basicStats(GARCH_vol))

# 静态溢出指数分析 ----------------------------------------------------------
# 使用BIC准则选择最优滞后阶数
lag_select <- VARselect(GARCH_vol, lag.max = 5, type = "const")
best_p <- lag_select$selection["SC(n)"]

# 估计VAR模型
var_model <- vars::VAR(GARCH_vol, p = best_p, type = "const")

# 计算溢出指数
sp_dy <- spilloverDY12(var_model, n.ahead = 10, no.corr = F)

# 结果输出
list(
  Total = overall(sp_dy),
  To = to(sp_dy),
  From = from(sp_dy),
  Net = net(sp_dy),
  Pairwise = pairwise(sp_dy)
) %>%
write.csv("Static_Spillover_Results.csv", row.names = FALSE)

# 动态滚动窗口分析 ----------------------------------------------------------
# 设置滚动窗口参数（窗口大小根据数据量调整）
params_est <- list(p = best_p, type = "const")
sp_roll <- spilloverRollingDY12(
  GARCH_vol,
  n.ahead = 10,
  no.corr = FALSE,
  "VAR",
  params_est = params_est,
  window = 200
)

# 可视化分析
pdf("Dynamic_Spillover_Plots.pdf", width = 10)
plotOverall(sp_roll) # 动态总溢出指数
plotTo(sp_roll) # 动态To溢出指数
plotFrom(sp_roll) # 动态From溢出指数
plotNet(sp_roll) # 动态净溢出指数
plotPairwise(sp_roll) # 动态净配对溢出指数
dev.off()

# 结果保存
list(
  Total = overall(sp_roll),
  To = to(sp_roll),
  From = from(sp_roll),
  Net = net(sp_roll),
  Pairwise = pairwise(sp_roll)
) %>%
  write.csv("Dynamic_Spillover_Results.csv", row.names = FALSE)