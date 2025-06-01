w = float(input())
y = w * 0.25 if w <= 50 else 50 * 0.25 + (w - 50) * 0.35
print(f"行李托运的运费是:{y}元")