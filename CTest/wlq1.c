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
// 你的 solution 会被放置在这
void input(int &x,int &y)
{
	scanf("%d%d",&x,&y);
}
void output(int x,int y)
{
	printf("%d",x+y);
}
