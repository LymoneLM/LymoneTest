Points = [
    [0.0, 0.0, 0.0], [1.0, 0.0, 0.5], [2.0, 0.0, 0.0],
    [0.0, 1.0, 0.3], [1.0, 1.0, 1.0], [2.0, 1.0, 0.7],
    [0.0, 2.0, 0.0], [1.0, 2.0, 0.2], [2.0, 2.0, 0.0]
]
Mesh = [
    [0,1,4], [0,4,3], [1,2,4], [2,5,4],
    [3,4,6], [4,7,6], [4,5,8], [4,8,7]
]

def surface_math(a,b,c):
    v1 = [b[i]-a[i] for i in range(3)]
    v2 = [c[i]-a[i] for i in range(3)]
    cross = [
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0]
    ]
    return 0.5 * sum(x**2 for x in cross)**0.5

def calc(p1,p2,p3,w,proj=False):
    if proj:
        p1,p2,p3 = [(x[0],x[1],0) for x in (p1,p2,p3)]
    return surface_math(p1,p2,p3)*w

for n in range(len(Mesh)):
    i,j,k = Mesh[n]
    a,b,c = Points[i],Points[j],Points[k]
    print(f"面板{n}号: "+
        f"恒载荷={calc(a,b,c,1.0)}kN "+
        f"活载荷={calc(a,b,c,0.5,True)}kN")