 function S=S_box_generate(u,x0,nn)
n=nn+100;
L=logistic(u,x0,n);
L=L(101:356);
[LL,L_index]=sort(L);
L_index=L_index-1;
S=reshape(L_index,16,16);
% S=L_index;