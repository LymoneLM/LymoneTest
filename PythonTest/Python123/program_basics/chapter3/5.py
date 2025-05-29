x = int(input())
if x == 1:
    print("1=1")
else:
    res = []
    n = x
    i = 2
    while i <= n:
        if n % i == 0:
            res.append(str(i))
            n = n // i
        else:
            i += 1
    print(f"{x} ={'*'.join(res)}")