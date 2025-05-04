a, b, c = eval(input())

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

gcd_ab = gcd(a, b)
gcd_abc = gcd(gcd_ab, c)

lcm_ab = a * b // gcd_ab
lcm_abc = lcm_ab * c // gcd(lcm_ab, c)

print(f"最大公约数是{gcd_abc}，最小公倍数是{lcm_abc}。")