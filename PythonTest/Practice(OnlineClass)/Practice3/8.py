year = int(input())
month = int(input())

if not (1000 <= year <= 2100 and 1 <= month <= 12):
    print("输入的年份或月份不合法！")
else:
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    print(f"{year}年{'是闰年' if is_leap else '不是闰年'}")

    if month in [1, 2, 3]:
        quarter = "第一"
    elif month in [4, 5, 6]:
        quarter = "第二"
    elif month in [7, 8, 9]:
        quarter = "第三"
    else:
        quarter = "第四"
    print(f"{month}月是{quarter}季度")

    if month == 2:
        days = 29 if is_leap else 28
    elif month in [4, 6, 9, 11]:
        days = 30
    else:
        days = 31
    print(f"{month}月有{days}天")
