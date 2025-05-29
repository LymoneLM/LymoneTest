import math
r,h = eval(input()),eval(input())
S = r*r*math.pi
V = S*h
S = math.pi*r*2*h+S*2
print("{:.2f}\n{:.2f}".format(S,V))