import numpy as np

a = -np.pi  # 因变量下界
b = np.pi  # 因变量上界
NP = 100  # 种群大小
NS = 2  # 种群数量
NG = 10  # 遗传代数
Pc = [0.9, 0.8]  # 交叉概率
Pm = [0.1, 0.3]  # 变异概率
eps = 0.1  # 精度


def initial(length):  # 初始化种群个体的基因，随机生成01串
    res = np.zeros(length)
    for ii in range(length):
        r = np.random.rand()  # 01分布概率随机数[0,1)
        res[ii] = np.round(r)  # 四舍五入取整函数，生成01序列
    return res


def fitness(x):  # 适应度函数
    return np.cos(x)


def dec(a, b, x, L):  # 将二进制还原成十进制的函数
    L2 = list(range(L - 1, -1, -1))
    Ji = []
    for m in range(len(L2)):
        Ji.append(x[m] * pow(2, L2[m]))
    y1 = sum(Ji)
    y = a + y1 * (b - a) / (pow(2, L) - 1)
    return y


# 初始化
L = int(np.ceil(np.log2((b - a) / eps + 1)))  # 确定待生成字串的长度
x = np.zeros((NS, NP, int(L)))  # x存储了种群个体（当前代种群）三维
fx = np.zeros((NS, NP))  # fx存储了每个个体的适应度

nx = np.zeros((NS, NP, int(L)))  # 下一回合种群
PPx = np.zeros( NP, )  # 本回合本种群累计概率

# 生成种群
for s0 in range(NS):
    for i0 in range(NP):
        x[s0, i0, :] = initial(L)  # 种群初始化
        fx[s0, i0] = fitness(dec(a, b, x[s0, i0, :], L))  # 个体适应值
nx = x

# 主循环
for k in range(NG):
    # 每个种群处理一遍
    for i0 in range(NS):
        sumfx = sum(fx[i0])
        Px = fx[i0] / sumfx  # 每个个体的选择概率
        PPx[0] = Px[0]
        for i2 in range(1, NP):
            PPx[i2] = PPx[i2 - 1] + Px[i2]  # 对应个体在本回合累计概率，准备进行轮盘赌

        for i in range(NP):   # 进行本轮遗传变异
            sita = np.random.rand()  # 轮盘赌选择父本
            for n in range(NP):
                if sita <= PPx[n]:
                    SelFather = n
                    break

            Selmother = int((np.random.rand() * (NP - 1)))  # 母本完全随机

            posCut = int((np.random.rand() * (L - 1)))  # 随机产生切点

            r1 = np.random.rand()  # 产生随机数来确定本次是否发生交叉

            if r1 <= Pc[i0]:
                # 产生交叉 前半段来自父本后半段来自母本
                nx[i0,i, 1:posCut] = x[i0,SelFather, 1:posCut]
                nx[i0,i, (posCut + 1):L] = x[i0,Selmother, (posCut + 1):L]
            else:
                nx[i0,i, :] = x[i0,SelFather, :]

            r2 = np.random.rand()
            if r2 <= Pm[i0]:
                posMut = round(np.random.rand() * (L - 1))  # 产生变异点
                # 翻转变异点
                if nx[i0,i, posMut] == 1.0:
                    nx[i0,i, posMut] = 0.0
                else:
                    nx[i0,i, posMut] = 1.0

    x = nx  # 新一代
    for s0 in range(NS):
        for i0 in range(NP):
            fx[s0, i0] = fitness(dec(a, b, x[s0, i0, :], L))  # 重新计算个体适应值

    # 种群个体交换
    if NS > 1:  # 兼容单种群
        num = int(NP * np.random.rand())  # 确定交换个数
        s1 = int((np.random.rand() * (NS - 1))) # 确定交换的两个种群
        s2 = int((np.random.rand() * (NS - 1)))
        if s1 == s2:
            s2 = (s2+1)%(NS - 1)

        max1 = max2 = 0
        for i0 in range(NP):  # 确保两个种群中的最大值至少进行一次交换
            if fx[s1, i0] > fx[s1, max1]:
                max1 = i0
            if fx[s2,i0]>fx[s2,max2]:
                max2 = i0
        row = x[s1,max1,:]
        x[s1,max1] = x[s2,max2,:]
        x[s2, max2] = row
        frow = fx[s1,max1]
        fx[s1,max1] = fx[s2,max2]
        fx[s2,max2] = frow
        for i0 in range(num): # 随机交换num个个体
            max1 = int((np.random.rand() * (NP - 1)))
            max2 = int((np.random.rand() * (NP - 1)))
            row = x[s1, max1, :]
            x[s1, max1] = x[s2, max2, :]
            x[s2, max2] = row
            frow = fx[s1, max1]
            fx[s1, max1] = fx[s2, max2]
            fx[s2, max2] = frow


# 在最终种群中选择答案（适应度最大值
fv = float('-inf')
for i0 in range(NS):
    for i1 in range(NP):
        fitx = fitness(dec(a, b, x[i0,i1, :], L))
        if fitx > fv:
            fv = fitx
            xv = dec(a, b, x[i0,i1, :], L)
# 输出最终答案,即函数在该区域的最大值
print("在",xv,"处取到最大值：",fv)
