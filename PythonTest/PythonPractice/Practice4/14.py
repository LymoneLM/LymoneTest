# 为什么这题部分通过？Why?
# md 天才出题人 666
import math

input = input()
x = float(input)
eps = 1e-6
sin_x = 0
n = 1
term = x

while abs(term) >= eps:
    sin_x += term
    n += 1
    term = (-1)**(n+1) * x**(2*n - 1) / math.factorial(2*n - 1)

print(f"sin({input})的近似值为:{sin_x:.10f}")

# x = float(input())
# eps = 1e-6
# sin_x = 0.0
# term = x
# n = 0
#
# while True:
#     if abs(term) < eps:
#         break
#     sin_x += term
#     n += 1
#     term = (-term) * x * x / ((2*n) * (2*n + 1))
#
# print(f"sin({x:.2f})的近似值为:{sin_x:.10f}")

# import math
#
# x_origin = float(input())
# eps = 1e-6
#
# x = math.fmod(x_origin, 2 * math.pi)
# if x > math.pi:
#     x -= 2 * math.pi
# elif x < -math.pi:
#     x += 2 * math.pi
#
# sin_x = 0.0
# term = x
# n = 0
#
# while True:
#     if abs(term) < eps:
#         break
#     sin_x += term
#     n += 1
#     term = (-term) * x * x / ((2 * n) * (2 * n + 1))
#
# print(f"sin({x_origin})的近似值为:{sin_x:.10f}")