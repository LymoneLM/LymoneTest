function L=logistic(u,x0,n) %L=logistic(3.81415,0.100001,100)
%函数功能:Logistic函数混沌系统产生加密序列L
%参数说明:%u为Logistic函数的参数,L(1)为Logistic函数的初值
L=zeros(1,n);
L(1)=x0;
for i=1:n-1 %加密时利用100个随即数之后的数　x_(n+1)=ax_n(1-x_n)，
    L(i+1)=u*(1-L(i))*L(i);
end