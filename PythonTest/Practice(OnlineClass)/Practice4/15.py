a = float(input())
eps = 1e-6
x_prev = a
x_next = 0.5 * (x_prev + a / x_prev)

while abs(x_next - x_prev) >= eps:
    x_prev = x_next
    x_next = 0.5 * (x_prev + a / x_prev)

print(f"x的近似值为:{x_next:.6f}")