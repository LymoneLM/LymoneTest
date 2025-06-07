Q = 180000
W = 200
H = 400
L = 2
A = 50.3
Fc = 1.43
Fs = 270
d = 500

Cv = 0.7 * Fc
Cv = Cv * W * H

def func(d):
    TA = L * A
    Sv = Fs * TA
    Sv = Sv * H / d
    Tv = Cv + Sv
    return Tv

while d >= 50:
    Tv = func(d)

    if Tv >= Q:
        print(f"箍筋间距={d}mm")
        print(f"Vu:{Tv / 1000:.2f}kN > V:{Q / 1000:.2f}kN")
        break

    d = d - 10

if d < 50:
    Tv = func(50)
    print("!! 无法满足")
    print(f"50mm时 Vu:{Tv / 1000:.2f}kN < V:{Q / 1000:.2f}kN")