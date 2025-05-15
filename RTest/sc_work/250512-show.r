# 250512-show.R
library(xts)
library(ggplot2)
library(tidyr)
library(scales)
library(dplyr)

data <- read.csv("bank_returns.csv",
                 header = TRUE,
                 stringsAsFactors = FALSE,
                 fileEncoding = "UTF-8")

returns_long <- data %>%
  pivot_longer(
    cols = -Date,
    names_to = "Bank",
    values_to = "Return"
  ) %>%
  mutate(Date = as.Date(Date))
bank_names <- c("ICBC", "ABC", "BOC", "CCB", "CMB")
for(bank_name in bank_names) {
  temp <- returns_long %>%
    filter(Bank == bank_name) %>%
    select(Date, Return)
  ggplot(temp, aes(x = Date, y = Return)) +
    geom_line(linewidth = 0.6, alpha = 0.8) +
    labs(
      title = paste(bank_name, "股票收益率时间序列"),
      x = "日期",
      y = "对数收益率",
      color = "银行"
    ) +
    theme_bw(base_size = 12) +
    theme(
      legend.position = "top",
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      axis.text.x = element_text(angle = 45, hjust = 1),
      panel.grid.minor = element_blank()
    ) +
    scale_x_date(
      date_labels = "%Y/%m",
      date_breaks = "6 months",
      minor_breaks = "1 month"
    ) +
    scale_y_continuous(
      labels = scales::percent_format(accuracy = 0.1),
      breaks = seq(-0.2, 0.2, by = 0.05)
    ) +
    geom_hline(yintercept = 0, linetype = "dashed", color = "grey50")

  ggsave(paste("Bank_Returns", bank_name, ".png"),
         width = 16,
         height = 8,
         dpi = 300)
}