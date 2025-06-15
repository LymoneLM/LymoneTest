def future_value(pv, rate, periods):
    if pv < 0 or rate < 0 or periods < 0:
        raise ValueError("Inputs must be non-negative")
    return pv * (1 + rate) ** periods

fv = future_value(1000, 0.005, 120)
print(fv)
