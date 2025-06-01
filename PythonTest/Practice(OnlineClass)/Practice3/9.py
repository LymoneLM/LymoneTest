a, b, c = map(float, input().split(','))

if a == 0 and b == 0:
    print("方程无意义")
elif a == 0:
    x = -c / b
    print(f"方程有一个根:{x:.2f}")
else:
    delta = b**2 - 4*a*c
    if delta > 0:
        x1 = (-b + delta**0.5) / (2*a)
        x2 = (-b - delta**0.5) / (2*a)
        print(f"方程有两个不等实根:x1={x1:.2f},x2={x2:.2f}")
    elif delta == 0:
        x = -b / (2*a)
        print(f"方程有两个相等实根:x1={x:.2f},x2={x:.2f}")
    else:
        real = -b / (2*a)
        imag = (-delta)**0.5 / (2*a)
        x1 = complex(real, imag)
        x2 = complex(real, -imag)
        print(f"方程有两个不等虚根:x1=({x1:.2f}),x2=({x2:.2f})")