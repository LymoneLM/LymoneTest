V = 180000  # 总剪力 (N)
b = 200  # 梁宽 (mm)
h0 = 400  # 梁有效高度 (mm)
n = 2  # 箍筋肢数
A_sv = 50.3  # 单肢箍筋截面积 (mm²)
ft = 1.43  # 混凝土轴心抗拉强度 (N/mm²)
fyv = 270  # 箍筋抗拉强度 (N/mm²)
s = 500  # 初始箍筋间距 (mm)

Vc = 0.7 * ft * b * h0

while s >= 50:
    total_Asv = n * A_sv
    Vs = fyv * (total_Asv / s) * h0

    Vu = Vc + Vs

    if Vu >= V:
        print(f":箍筋间距 s = {s} mm 满足要求")
        print(f"Vu = {Vu / 1000} kN >= V = {V / 1000} kN")
        break

    s -= 10

if s < 50:
    print("警告: 箍筋间距小于50mm仍不满足要求")
    print(f"50mm时: Vu = {Vu / 1000} kN < V = {V / 1000} kN")