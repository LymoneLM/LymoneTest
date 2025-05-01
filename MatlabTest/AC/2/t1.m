num1=1;
den1=[1 0];
num2=4;
den2=[1 1];
sys1=tf(num1,den1);
sys2=tf(num2,den2);
sys3=series(sys1,sys2);
sysc=feedback(sys3,1);
sisotool(sysc)