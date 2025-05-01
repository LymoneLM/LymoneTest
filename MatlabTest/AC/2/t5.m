A=[-2 -1 1; 1 0 1; -1 0 1];
B=[1;1;1];
C=[1 0 1];
D=[];
Qc=ctrb(A,B);
n1=rank(Qc);
Qo=obsv(A,C);
n2=rank(Qo);
step(A,B,C,D);