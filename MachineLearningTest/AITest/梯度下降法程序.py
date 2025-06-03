import numpy as np
import matplotlib.pyplot as plt

num = 50
theta = 10
r = 0.1
Xresult=np.zeros(num)
Yresult=np.zeros(num)
def dJ(theta):
    return 2*theta+2

def J(theta):
    return 1*pow(theta,2)+2*theta

for i in range(0, num):
    theta = theta - r * dJ(theta)
    Xresult[i]= theta
    Yresult[i]=J(Xresult[i])
    if i % 10 == 0:
        print("迭代次数[%d] 对应x的值 %.2f" % (i, theta))

print(Xresult)

plt.plot(Yresult,'r:')
plt.axis([0, 50, -10, 100])
plt.tick_params(labelsize=10)

plt.show()

