# 层次数据
library(tidyverse)
library(ggplot2)

data <- read.csv("./data/Expanded_data_with_more_features.csv") %>%
  mutate(WklyStudyHours = ifelse(WklyStudyHours == "2025/5/10", "5-10", WklyStudyHours)) %>%
  mutate(across(c(
    Gender, EthnicGroup, ParentEduc, LunchType, TestPrep,
    ParentMaritalStatus, PracticeSport, IsFirstChild, TransportMeans,
    WklyStudyHours
  ), as.factor))

data_hierarchy <- data %>%
  group_by(Gender, EthnicGroup) %>%
  summarise(
    AvgMath = mean(MathScore, na.rm = TRUE),
    AvgReading = mean(ReadingScore, na.rm = TRUE),
    AvgWriting = mean(WritingScore, na.rm = TRUE)
  ) %>%
  pivot_longer(
    cols = starts_with("Avg"),
    names_to = "Subject",
    values_to = "Score"
  )

x <- ggplot(data_hierarchy, aes(x = Gender, y = Score, fill = EthnicGroup)) +
  geom_col(position = "stack", width = 0.7) +
  scale_fill_manual(
    values = c(
      "na.value" = "black",
      "group A" = "#1230da",
      "group B" = "#3055b1",
      "group C" = "#21918C",
      "group D" = "#5DC863",
      "group E" = "#FDE725"
    )
  ) +
  labs(title = "不同性别和族群成绩", x = "Gender", y = "Average Score") +
  facet_wrap(~Subject) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

png("./output/2/plot3.png", width = 1600, height = 900)
print(x)
dev.off()
