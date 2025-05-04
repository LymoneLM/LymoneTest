import numpy as np

a = -np.pi  # 因变量下界
b = np.pi  # 因变量上界
NP = 100  # 种群大小
NG = 2000  # 遗传代数
Pc = 0.9  # 交叉概率
Pc2 = 0.9  # 隐性子交叉概率
Pm = 0.1  # 变异概率
Pm2 = 0.3  # 隐性子变异概率
eps = 0.1  # 精度


def initial(length):
    """
    生成一定长度的01序列
    :param length: 待生成字串的长度
    :return: 生成的字串
    """
    res = np.zeros(length)
    for ii in range(length):
        r = np.random.rand()  # 01分布概率随机数[0,1)
        res[ii] = np.round(r)  # 四舍五入取整函数，生成01序列
    return res


def fitness(x):
    """
    适应度函数，此处可以说明该程序为寻找sin
    :param x: 待计算数值
    :return:
    """
    return np.cos(x)


def dec(a, b, x, L):
    """
    将二进制还原成十进制的函数
    :param a: 因变量下界
    :param b: 因变量上界
    :param x: 待还原的二进制字符串
    :param L: 二进制字符串的长度
    :return: 换算后的十进制数
    """
    L2 = list(range(L - 1, -1, -1))
    Ji = []
    for m in range(len(L2)):
        Ji.append(x[m] * pow(2, L2[m]))
    y1 = sum(Ji)
    y = a + y1 * (b - a) / (pow(2, L) - 1)
    return y


# 主函数部分


# 初始化
L = int(np.ceil(np.log2((b - a) / eps + 1)))
# 确定待生成字串的长度，因变量是sin的一个周期[-pi,pi],精度eps=0.1,结果加一并向下取整保证可行
x = np.zeros((NP, int(L)))
fx = np.zeros(NP)
# x存储了种群个体（即x为当前种群）二维
# fx存储了每个个体的适应度
nx = np.zeros((NP, int(L)))
# 下一回合种群
PPx = np.zeros(NP, )
# 本回合累计概率
rr2 = np.zeros(NP, )

# 生成种群
for i0 in range(NP):
    x[i0, :] = initial(L)  # 种群初始化
nx = x

# 主循环
for k in range(NG):
    for j in range(NP):
        fx[i0] = fitness(dec(a, b, x[i0, :], L))  # 个体适应值
    sumfx = sum(fx)
    Px = fx / sumfx  # 每个个体的选择概率
    PPx[0] = Px[0]
    for i2 in range(1, NP):
        PPx[i2] = PPx[i2 - 1] + Px[i2]  # 对应个体在本回合累计概率，准备进行轮盘赌

    for i in range(NP):
        sita = np.random.rand()  # 轮盘赌选择父本
        for n in range(NP):
            if sita <= PPx[n]:
                SelFather = n
                break

        Selmother = int((np.random.rand() * (NP - 1)))  # 母本完全随机

        posCut = int((np.random.rand() * (L - 1)))  # 随机产生切点

        r1 = np.random.rand()  # 产生随机数来确定本次是否发生交叉
        rr2[i] = r1

        if r1 <= Pc:
            # 产生交叉 前半段来自父本后半段来自母本
            nx[i, 1:posCut] = x[SelFather, 1:posCut]
            nx[i, (posCut + 1):L] = x[Selmother, (posCut + 1):L]
        else:
            nx[i, :] = x[SelFather, :]

        r2 = np.random.rand()
        if r2 <= Pm:
            posMut = round(np.random.rand() * (L - 1))  # 产生变异点
            # 翻转变异点
            if nx[i, posMut] == 1.0:
                nx[i, posMut] = 0.0
            else:
                nx[i, posMut] = 1.0

    x = nx  # 新一代

# 在最终种群中选择答案（适应度最大值
fv = float('-inf')
for i3 in range(NP):
    fitx = fitness(dec(a, b, x[i3, :], L))
    if fitx > fv:
        fv = fitx
        xv = dec(a, b, x[i3, :], L)
# 输出
print(xv)
print(fv)
