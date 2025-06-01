M = int(input())
N = int(input())

if N % 2 != 0:
    print("输入的脚数为奇数，不合理！")
else:
    found = False
    for chicken in range(M + 1):
        rabbit = M - chicken
        if 2 * chicken + 4 * rabbit == N:
            print(f"鸡有{chicken}只，兔有{rabbit}只")
            found = True
            break

    if not found:
        print("求出的只数为负，输入的数据不合理！")