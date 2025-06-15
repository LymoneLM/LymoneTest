def future_value(present_value, interest_rate, num_periods):
    if present_value < 0 or interest_rate < 0 or num_periods < 0:
        print("Input values cannot be negative")
        return None
    return present_value * (1 + interest_rate) ** num_periods

result = future_value(1000, 0.005, 120)
print(result)