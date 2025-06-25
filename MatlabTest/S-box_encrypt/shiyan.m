clc
clear
I=imread('Lena.png'); %输入Lena图像
[m,n]=size(I);
S=S_box_generate(3.81415,0.100001,256);%利用logistic混沌生成16x16的S盒
I=double(I);

for i=1:m
    for j=1:n     
      b=dec2bin(I(i,j),8);%将输入的像素值转化成二进制数放在b中
            y=bin2dec(b(1,1:4))+1;%取b的前四位作为行号y
            x=bin2dec(b(1,5:8))+1;%取b的后四位作为列号x
           I(i,j)=S(y,x);%S盒替换
    end
end

I=uint8(I);
imshow(I);
imwrite(I,'jiami.bmp');
   