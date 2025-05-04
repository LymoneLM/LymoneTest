a, b, c = map(float, input().split(','))
if a + b > c and a + c > b and b + c > a:
    if a == b == c:
        print("三角形是等边三角形")
    elif a == b or a == c or b == c:
        if abs(a**2 + b**2 - c**2) < 1e-6 or abs(a**2 + c**2 - b**2) < 1e-6 or abs(b**2 + c**2 - a**2) < 1e-6:
            print("三角形是等腰直角三角形")
        else:
            print("三角形是等腰非直角三角形")
    elif abs(a**2 + b**2 - c**2) < 1e-6 or abs(a**2 + c**2 - b**2) < 1e-6 or abs(b**2 + c**2 - a**2) < 1e-6:
        print("三角形是非等腰直角三角形")
    else:
        print("三角形是普通三角形")
else:
    print("输入的三个数，不能作为三角形的边组成三角形。")