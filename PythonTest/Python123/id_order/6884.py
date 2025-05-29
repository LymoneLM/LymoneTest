import random
random.seed(123)
a = eval(input())
hits = 0.0
for i in range(a):
    x, y = random.random(), random.random()
    dist = pow(x ** 2 + y ** 2, 0.5)
    if dist <= 1.0:
        hits = hits + 1
pi = 4 * (hits/a)
print("{:.6f}".format(pi))