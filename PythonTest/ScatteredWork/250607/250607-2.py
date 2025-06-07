V = 180000
a = 200
b = 400
g = 2
d = 50.3
e = 1.43
z = 270
s = 500

t = 0.7 * e * a * b

while s >= 50:
    k = z * (g * d / s) * b
    d2 = t + k

    if d2 >= V:
        print(f":箍筋间距 s = {s} mm 满足要求")
        print(f"Vu = {d2 / 1000:.2f} kN >= V = {V / 1000} kN")
        break

    s -= 10

if s < 50:
    km = z * (g * d / 50) * b
    lm = t + km

    print("警告: 箍筋间距小于50mm仍不满足要求")
    print(f"最小间距50mm时: Vu = {lm / 1000:.2f} kN < V = {V / 1000} kN")