library(quantmod)
library(tidyverse)
library(xts)
library(purrr)

bank_symbols <- c(
  "601398.ss", # 工商银行
  "601288.ss", # 农业银行
  "601988.ss", # 中国银行
  "601939.ss", # 建设银行
  "600036.ss"  # 招商银行
)
bank_names <- c("ICBC", "ABC", "BOC", "CCB", "CMB")

create_xts_from_list <- function(data, symbol) {
  close_vec <- sapply(data, function(x) x$close)
  date_vec <- as.Date(sapply(data, function(x) x$date))
  xts_obj <- xts(close_vec, order.by = date_vec)
  colnames(xts_obj) <- symbol
  return(xts_obj)
}

bank_data <- list()
for (i in seq_along(bank_symbols)) {
  symbol <- bank_symbols[i]
  temp_data <- md_stock(symbol,
                        from = "2010-01-01",
                        to = "2025-03-31",
                        source = "163")
  temp_xts <- create_xts_from_list(temp_data, bank_names[i])
  bank_data[[i]] <- temp_xts
}

# 合并数据并计算收益率
merged_bank <- do.call(merge, bank_data)
bank_returns <- na.omit(100 * diff(log(merged_bank)))
returns_df <- data.frame(Date = index(bank_returns), coredata(bank_returns))
write.csv(returns_df, "bank_returns.csv", row.names = FALSE)