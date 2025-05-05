library(ggplot2)
library(dplyr)


bike_data <- read.csv("./data/LondonBikeJourneyAug2023.csv")


bike_data$minutes <- as.numeric(sub("m.*", "", bike_data$Total.duration))  
bike_data$seconds <- as.numeric(sub(".*m ", "", sub("s", "", bike_data$Total.duration)))  
bike_data$Total.duration.min <- bike_data$minutes + bike_data$seconds / 60 


bike_data_filtered <- bike_data %>%
  filter(!is.na(Bike.model)) 

p <- ggplot(bike_data_filtered, aes(x = Bike.model, y = Total.duration.min)) +
  geom_violin(fill = "#558ffc", color = "black", alpha = 0.5) +  
  geom_boxplot(width = 0.2, fill = "white", color = "black") + 
  labs(title = "不同自行车型号的租赁时长分布", 
       x = "自行车型号", 
       y = "租赁时长（分钟）") +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5), 
    axis.text.x = element_text(angle = 45, hjust = 1)  
  )


print(p)


ggsave("./output/4/bike_duration_model_plot.png", p, bg = "white", width = 8, height = 6, dpi = 300)
write.csv(bike_data_filtered, "./output/4/processed_bike_data.csv", row.names = FALSE)
