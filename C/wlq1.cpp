#include <stdio.h>
void input(int &x, int &y);
void output(int x, int y);
int main()
{
	int n, x, y;
	scanf("%d", &n);
	while(n--)
	{
		input(x, y);
		output(x, y);
	}
}
// ��� solution �ᱻ��������
void input(int &x,int &y)
{
	scanf("%d%d",&x,&y);
}
void output(int x,int y)
{
	printf("%d",x+y);
}
