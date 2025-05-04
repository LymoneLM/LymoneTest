salary = int(input())
if salary <= 400:
    f = salary * 0.005
elif salary <= 600:
    f = salary * 0.01
elif salary <= 800:
    f = salary * 0.015
elif salary <= 1500:
    f = salary * 0.02
else:
    f = salary * 0.03
print(f"工资{salary}，应缴党费{f:.2f}元")