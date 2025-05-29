s = input().split(',')
bmi = float(s[1])/float(s[0])**2
print("BMI数值为:{:.2f}".format(bmi))
if bmi < 18.5:
    s1 = s2 = "偏瘦"
elif bmi < 24:
    s1 = s2 = "正常"
elif bmi < 25:
    s1, s2 = "正常", "偏胖"
elif bmi < 28:
    s1 = s2 = "偏胖"
elif bmi < 30:
    s1, s2 = "偏胖", "肥胖"
else:
    s1 = s2 = "肥胖"
print("BMI指标为:国际'{:s}',国内'{:s}'".format(s1, s2))
