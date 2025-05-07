class BMI:
    def __init__(self, height, weight):
        self.bmi = weight / (height ** 2)
    def printBMI(self):
        print("您的BMI指数是：{:.1f}".format(self.bmi))

class ChinaBMI(BMI):
    def printBMI(self):
        bmi_level = ["偏瘦","正常","偏胖","肥胖","重度肥胖"]
        rate_level = ["低","平均水平","增加","中毒增加","严重增加"]
        level = 0
        if self.bmi < 18.5:
            level = 0
        elif self.bmi <= 23.9:
            level = 1
        elif self.bmi <= 26.9:
            level = 2
        elif self.bmi <= 29.9:
            level = 3
        else:
            level = 4
        print(f"您的BMI指数是：{self.bmi:.1f}\n"
              f"{bmi_level[level]}，相关疾病发病的危险性：{rate_level[level]}")
height = float(input())
weight = float(input())
person = ChinaBMI(height, weight)
person.printBMI()
