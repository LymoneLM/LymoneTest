
import matplotlib.pyplot as plt
import numpy as np
import math
import random

#用来正常显示中文标签
plt.rcParams['font.sans-serif']=['STSong']
plt.rcParams['font.size'] = 20
#用来正常显示负号
plt.rcParams['axes.unicode_minus']=False
std=0
Lnn=100
# X = np.linspace(-1, 1,Lnn)
# T0 = np.sin(X)
X = np.linspace(-1, 3,Lnn)
T0 = pow(X,3)+0.3*pow(X,2)-0.5*X

Ln= len(T0)
Noisem=np.random.randn(Ln)
T=T0+std*Noisem



eta=0.001
def polynomial(x,params):
    poly=0
    for i in range(len(params)):
        poly=poly+params[i]*x**i
    return poly

def grad_params(X,T,params):
    grad_ps=np.zeros(len(params))
    for i in range(len(params)):
        for j in range(len(X)):
            grad_ps[i]+=(polynomial(X[j],params)-T[j])*pow(X[j],i)
    return grad_ps

def fit (X,T,degree,epoch):
    params=np.random.randn(degree+1)
    for i in range(len(params)):
        params[i]*=2**i

    for i in range(epoch):
        params-=eta*grad_params(X,T,params)
    return params



degree=2
params=fit(X,T,degree,1000)
Y=polynomial(X,params)
plt.scatter(X,T)
plt.plot(X,Y,'r')
plt.show()

print(params)

# degrees=[1,3,6]
# for degreee in degrees:
#     params=fit(X,T,degreee,1000)
#     Y=polynomial(X,params)
#
#     plt.scatter(X,T)
#     plt.plot(X,Y)
#     plt.show()






