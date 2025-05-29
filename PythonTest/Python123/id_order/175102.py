x=eval(input())
k=2
print(x,"=",end="")
while x>1:
    if  x%k == 0:
        print(k,end="")
        x/=k
        if x>1:
            print("*",end="")
    else:
        k=k+1