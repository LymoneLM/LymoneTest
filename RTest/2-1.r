# 二维数据（高维数据）可视化
library(tidyverse)
library(ggplot2)
library(patchwork) 

data <- read.csv("./data/Expanded_data_with_more_features.csv") %>%
  mutate(WklyStudyHours = ifelse(WklyStudyHours == "2025/5/10", "5-10", WklyStudyHours)) %>%
  mutate(across(c(
    Gender, EthnicGroup, ParentEduc, LunchType, TestPrep,
    ParentMaritalStatus, PracticeSport, IsFirstChild, TransportMeans,
    WklyStudyHours
  ), as.factor))

data_long <- data %>%
  pivot_longer(
    cols = c(MathScore, ReadingScore, WritingScore),
    names_to = "Subject",
    values_to = "Score"
  )
p1 <- ggplot(data_long, aes(x = Gender, y = Score, fill = Gender)) +
  geom_boxplot(alpha = 0.7) +
  scale_fill_grey(start = 0.3, end = 0.7) +
  labs(title = "Gender vs. Subject Scores", x = "Gender", y = "Score") +
  facet_wrap(~Subject) +
  theme_bw()
p2 <- ggplot(data_long, aes(x = Gender, y = Score, fill = Gender)) +
  geom_violin(trim = FALSE, alpha = 0.7) +
  scale_fill_grey(start = 0.3, end = 0.7) +
  labs(title = "Score Density by Gender", x = "Gender", y = "Score") +
  facet_wrap(~Subject) +
  theme_bw()
png("./output/2/plot1.png", width = 1600, height = 900)
print(
  (p1 / p2) + plot_layout(guides = "collect")
)
dev.off()
