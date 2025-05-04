M = int(input())
N = int(input())

if N % 2 != 0:
    print("输入的脚数为奇数，不合理！")
else:
    x = 2 * M - N // 2
    y = M - x

    if x < 0 or y < 0:
        print("求出的只数为负，输入的数据不合理！")
    else:
        print(f"鸡有{x}只，兔有{y}只")