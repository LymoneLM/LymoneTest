# 加载必要的包
library(xts)
library(vars)
library(FinTS)
library(rugarch)
library(rmgarch)
library(fBasics)
library(fUnitRoots)
library(ggplot2)

data <- read.csv("bank_returns.csv",
                 header = TRUE,
                 stringsAsFactors = FALSE,
                 fileEncoding = "UTF-8")

returns <- xts(x = data[, -1],
               order.by = as.Date(data$Date))

# 描述性统计（使用xts对象）
cat("\n描述性统计:\n")
print(basicStats(returns))

# 平稳性检验 (ADF)
cat("\nADF检验:\n")
print(adfTest(coredata(returns), lags = 1, type = 'c'))

# 正态性检验 (Jarque-Bera)
cat("\n正态性检验:\n")
print(normalTest(returns[, 1], method = 'jb'))

# 自相关性检验 (Ljung-Box)
cat("\nLjung-Box检验:\n")
print(Box.test(returns[, 1], lag = 15, type = 'Ljung'))

# ARCH效应检验 (LM检验)
cat("\nARCH效应检验:\n")
print(FinTS::ArchTest(returns[, 1], 15))

# ========ARMA-GARCH-VaR方法==========
# GARCH建模与诊断
# 模型设定（使用正态分布）
garch_spec <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
  distribution.model = "norm"
)
pdf("All_Banks_VaR_Plots.pdf", width = 12, height = 6)
bank_names <- c("ICBC", "ABC", "BOC", "CCB", "CMB")
for(bank_name in bank_names) {
  # 模型拟合
  garch_fit <- ugarchfit(data = returns[, bank_name], spec = garch_spec)
  print(garch_fit)

  # 标准化残差分析
  std_resid <- residuals(garch_fit, standardize = TRUE)
  ArchTest(std_resid, 15)


  # VaR计算
  # 提取模型参数
  sigma <- sigma(garch_fit)
  mu <- fitted(garch_fit)

  # 计算分位数（使用正态分布）
  alpha <- c(0.01, 0.05)
  q_lower <- qnorm(alpha)
  q_upper <- qnorm(1 - alpha)

  # 计算VaR（假设多头头寸关注左尾，空头头寸关注右尾）
  # 提取日期序列
  dates <- index(returns)

  VaR <- data.frame(
    Date = as.character(dates),     # 日期列
    Returns = returns[, bank_name], # 银行收益率
    VaR_1D_Lower = mu + sigma * q_lower[1],  # 1% 左尾
    VaR_5D_Lower = mu + sigma * q_lower[2],  # 5% 左尾
    VaR_5U_Upper = mu + sigma * q_upper[2],  # 5% 右尾
    VaR_1U_Upper = mu + sigma * q_upper[1]   # 1% 右尾
  )

  # 结果保存
  write.csv(VaR, paste0("VaR_results_", bank_name, ".csv"), row.names = FALSE)

  # 模型估计结果可视化
  # 读取数据并转换日期格式
  var_data <- read.csv(paste0("VaR_results_", bank_name, ".csv"))
  var_data$Date <- as.Date(var_data$Date)

  # 绘制带完整图例的线条图
  print(
    ggplot(var_data) +
      geom_line(aes(x = Date, y = returns[, bank_name], color = "实际收益率"),
                linewidth = 0.7) +
      geom_line(aes(x = Date, y = VaR_1D_Lower, color = "1% VaR下界"),
                linetype = "dashed") +
      geom_line(aes(x = Date, y = VaR_5D_Lower, color = "5% VaR下界"),
                linetype = "dashed") +
      geom_line(aes(x = Date, y = VaR_1U_Upper, color = "1% VaR上界"),
                linetype = "dashed") +
      geom_line(aes(x = Date, y = VaR_5U_Upper, color = "5% VaR上界"),
                linetype = "dashed") +
      scale_color_manual(
        name = "图例",
        values = c(
          "实际收益率" = "#1f77b4",
          "1% VaR下界" = "#ff7f0e",
          "5% VaR下界" = "#d62728",
          "1% VaR上界" = "#2ca02c",
          "5% VaR上界" = "#9467bd"
        ),
        guide = guide_legend(
          title.position = "top",
          title.hjust = 0.5,
          ncol = 5
        )
      ) +
      labs(
        title = paste(bank_name, "收益率与风险价值(VaR)动态监测"),
        x = "日期",
        y = "收益率"
      ) +
      theme_minimal() +
      theme(
        legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold"),
        panel.grid.minor = element_blank()
      )
  )
  # 保存图形
  ggsave(paste0("VaR_Plot_", bank_name, ".png"),
         width = 12, height = 6, dpi = 300)
}
dev.off()