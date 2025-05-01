flag = False
for a in range(1,10):
    for b in range (0,10):
        for c in range(0, 10):
            if pow(a, 3)+pow(b, 3)+pow(c,3)==a*100+b*10+c:
                if flag:
                    print(",", end='')
                else:
                    flag = True
                print(a * 100 + b * 10 + c, end='')
