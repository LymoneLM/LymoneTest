function L=logistic(u,x0,n) %L=logistic(3.81415,0.100001,100)
%��������:Logistic��������ϵͳ������������L
%����˵��:%uΪLogistic�����Ĳ���,L(1)ΪLogistic�����ĳ�ֵ
L=zeros(1,n);
L(1)=x0;
for i=1:n-1 %����ʱ����100���漴��֮�������x_(n+1)=ax_n(1-x_n)��
    L(i+1)=u*(1-L(i))*L(i);
end