# 时间序列数据可视化
library(tidyverse)

df <- read.csv("./data/20220327 annual-number-of-deaths-by-cause.csv") %>%
  mutate(across(
    -c(Entity, Code, Year),
    as.numeric
  ))

df_long <- df %>%
  pivot_longer(
    cols = -c(Entity, Code, Year),
    names_to = "Death_Cause",
    values_to = "Count"
  )

write.csv(df_long,"./output/1/df_long.csv",row.names = F)

selected_countries <- c("Afghanistan")
final_data <- df_long %>%
  filter(Entity %in% selected_countries) 

# 分面绘图
png("./output/1/plot1.png", width = 800, height = 450)
print(
  ggplot(final_data, aes(x = Year, y = Count, color = Death_Cause)) +
    geom_line(linewidth = 1) +
    geom_point(size = 2) +
    facet_wrap(~Entity, scales = "free_y") + 
    labs(title = "Deaths in Afghanistan") +
    theme_minimal() +
    theme(legend.position = "none") 
)
dev.off()
