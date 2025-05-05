library(ggplot2)
library(reshape2)

stock_data <- read.csv("./data/HistoricalData_1617855933643.csv")

stock_data$Close.Last <- as.numeric(gsub("\\$", "", stock_data$Close.Last))
stock_data$Open <- as.numeric(gsub("\\$", "", stock_data$Open))
stock_data$High <- as.numeric(gsub("\\$", "", stock_data$High))
stock_data$Low <- as.numeric(gsub("\\$", "", stock_data$Low))

numeric_data <- stock_data[, c("Close.Last", "Open", "High", "Low", "Volume")]
cor_matrix <- cor(numeric_data)

melted_cor <- melt(cor_matrix)

p <- ggplot(melted_cor, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile() +
  scale_fill_gradient2(low = "black", high = "white", mid = "gray", midpoint = 0, 
                       limits = c(-1, 1), name = "相关性") +
  geom_text(aes(label = round(value, 2)), color = "black", size = 4) +  
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

print(p)

ggsave("./output/3/correlation_heatmap.png", p, width = 8, height = 6, dpi = 300, bg = "white")
write.csv(stock_data, "./output/3/processed_stock_data.csv", row.names = FALSE)
