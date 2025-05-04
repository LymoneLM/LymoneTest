import numpy as np

a=-np.pi
b=np.pi
NP=100
NG=1000
Pc=0.9
Pm=0.1
eps=0.1


def initial(length):
    res=np.zeros(length)
    for ii in range(length):
        r = np.random.rand()
        res[ii]=np.round(r)
    return res


def fitness(x):
    return np.sin(x)


def dec(a,b,x,L):
    L2 = list(range(L-1,-1,-1))
    Ji = []
    for m in range(len(L2)):
         Ji.append(x[m]*pow(2,L2[m]))
    y1 = sum(Ji)
    y = a + y1 * (b-a)/(pow(2,L)-1)
    return y


L=int( np.ceil(np.log2((b - a)/eps+1)))  # 根据离散精度，确定二进制编码需要的码长
x = np.zeros((NP,int(L)))
fx= np.zeros(NP)
nx = np.zeros((NP,int(L)))
PPx=np.zeros(NP,)
rr2 = np.zeros(NP, )

for i0 in range(NP):
    x[i0,:]= initial(L)                  #种群初始化
    fx[i0] = fitness(dec(a,b,x[i0,:],L))  #个体适应值
nx =x
for k in range(NG):
    sumfx = sum(fx)
    Px= fx/sumfx
    PPx[0]=Px[0]
    for i2 in range(1,NP):
        PPx[i2] = PPx[i2-1]+Px[i2]

    for i in range(NP):
        sita = np.random.rand()
        for n in range(NP):
            if sita <= PPx[n]:
                SelFather=n
                break

        Selmother = int((np.random.rand() * (NP - 1)))
        posCut = int((np.random.rand() * (L - 1)))
        r1 = np.random.rand()
        rr2[i]=r1
        if r1<=Pc:
            nx[i,1:posCut] = x[SelFather,1:posCut]
            nx[i,(posCut+1):L] = x[Selmother,(posCut+1):L]
        else:
            nx[i, :] = x[SelFather, :]

            r2 = np.random.rand()
            if r2 <= Pm:
                posMut = round(np.random.rand()*(L-1))
                if nx[i,posMut]==1.0:
                    nx[i,posMut]=0.0
                else:
                    nx[i, posMut] = 1.0

    x = nx
    for j in range(NP):
        fx[j] = fitness(dec(a,b,x[j,:],L))


fv =float('-inf')
for i3 in range(NP):
    fitx = fitness(dec(a, b, x[i3,:], L))
    if fitx > fv:
        fv = fitx
        xv = dec(a, b, x[i3,:], L)

print(xv)
print(fv)






