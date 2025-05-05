# 高维数据可视化 折线图 + 直方图
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

write.csv(data_long, "./output/2/data_long.csv", row.names = FALSE)

p3 <- ggplot(data, aes(x = NrSiblings)) +
  geom_histogram(binwidth = 1, fill = "grey50", color = "black") +
  labs(title = "Distribution of Sibling Counts", x = "Number of Siblings", y = "Count") +
  theme_bw()


p4 <- data %>%
  group_by(NrSiblings) %>%
  summarise(AvgMath = mean(MathScore, na.rm = TRUE)) %>%
  ggplot(aes(x = NrSiblings, y = AvgMath)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(title = "Sibling Count vs. Math Scores", x = "Number of Siblings", y = "Average Math Score") +
  theme_bw()

png("./output/2/plot2.png", width = 1600, height = 900)
print(
p3 + p4
)
dev.off()