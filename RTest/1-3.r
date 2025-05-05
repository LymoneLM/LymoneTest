# 地理数据可视化
library(tidyverse)
library(ggplot2)
library(maps)
library(countrycode)

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
  ) %>%
  filter(Death_Cause %in% c(
    "Deaths...HIV.AIDS...Sex..Both...Age..All.Ages..Number."
  ))
colnames(df_long)[colnames(df_long) == "Code"] <- "iso3c" 

world_map_clean <- map_data("world") %>%
  mutate(iso3c = countrycode(region, "country.name", "iso3c")) %>%
  filter(!is.na(iso3c))

world_map_merged <- world_map_clean %>%
  left_join(df_long, by = "iso3c") %>%
  filter(!is.na(Year))

png("./output/1/plot3.png", width = 1600, height = 900)
print(
  ggplot(world_map_merged, aes(x = long, y = lat, group = group)) +
    geom_polygon(aes(fill = Count), colour = "black", linewidth = 0.1) +
    scale_fill_gradient(low = "white", high = "black") +
    # 黑白填充色
    labs(title = "Global HIV/AIDS Deaths by Country and Year") +
    theme_void() +
    theme(
      legend.position = "bottom",
      strip.text = element_text(size = 8)
    ) +
    facet_wrap(~Year, ncol = 6)
)
dev.off()
