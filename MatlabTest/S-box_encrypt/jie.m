clc
clear
I=imread('jiami.bmp');%输入加密图像
[m,n]=size(I);
S=S_box_generate(3.81415,0.100001,256);%生成相同的S盒

for i=1:m
    for j=1:n     
 [m1,n1]=find(S==I(i,j));%利用find函数寻找加密像素的位置保存在坐标(m1,n1)中
 m1=dec2bin(m1-1,4);%行坐标代表前四位二进制数，十进制转化为二进制
 n1=dec2bin(n1-1,4);%列坐标代表后四位二进制数
 u=strcat(m1,n1);%将得到的前四位和后四位二进制组合，得到原像素值的二进制数
 I(i,j)=bin2dec(u);%二进制转化为十进制
    end
end
I=uint8(I);
imshow(I);
imwrite(I,'jiami.bmp');
   
