def f(n):
    if n == 0:
        return 1
    elif n == 1:
        return 7
    else:
        return 8 * f(n - 1)


def main():
    l = []
    for i in range(1, 9):
        a = 4 * f(i - 1)
        l.append(a)
        print(f"{i}位奇数有{a}个")
    print(f"有{sum(l)}个奇数")


if __name__ == '__main__':
    main()
