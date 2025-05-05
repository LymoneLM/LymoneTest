library(ggplot2)

stock_data <- read.csv("./data/HistoricalData_1617855933643.csv")

stock_data$Date <- as.Date(stock_data$Date, format = "%m/%d/%Y")
stock_data$Close.Last <- as.numeric(gsub("\\$", "", stock_data$Close.Last))

max_close <- max(stock_data$Close.Last)
max_volume <- max(stock_data$Volume)
stock_data$Volume_scaled <- stock_data$Volume * (max_close / max_volume)

p <- ggplot(stock_data, aes(x = Date)) +
  geom_line(aes(y = Close.Last), color = "black", size = 1) +  
  geom_bar(aes(y = Volume_scaled), stat = "identity", fill = "gray", alpha = 0.5) +  
  scale_y_continuous(
    name = "收盘价 (美元)",
    sec.axis = sec_axis(~ . * (max_volume / max_close), name = "交易量")
  ) +
  labs(title = "股票收盘价与交易量时间序列", x = "日期") +
  theme_minimal() +
  theme(
    axis.title.y = element_text(color = "black"),
    axis.title.y.right = element_text(color = "gray")
  )

print(p)

ggsave("./output/3/price_volume_plot.png", p, width = 10, height = 6, dpi = 300, bg = "white")
