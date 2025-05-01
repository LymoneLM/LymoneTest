num1=1;
den1=[1 0];
num2=4;
den2=[1 1];
num3=[0.63 1];
den3=[0.26 1];
sys3=tf(num3,den3);
sys1=tf(num1,den1);
sys2=tf(num2,den2);
sys4=series(sys1,sys2);
sys5=series(sys4,sys3);
sysc=feedback(sys5,1);
sisotool(sysc)