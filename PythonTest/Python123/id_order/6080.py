x = input()
c = x[0]
n = eval(x[3:])
if c == 'R':
    print("USD{:.2f}".format(n/6.78))
else:
    print("RMB{:.2f}".format(n * 6.78))