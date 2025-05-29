while True:
    x = input()
    if x == '000':
        break
    x = int(x)
    if x % 5 == 0 and x % 7 == 0:
        print("yes")
    else:
        print("no")