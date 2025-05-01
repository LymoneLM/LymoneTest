#include <stdio.h>
int main()
{
	double h=100,sum=0;
	int n;
	scanf("%d",&n);
	for(int i=0;i<n;i++)
	{
		sum+=h;
		h/=2;
		sum+=h;
	}
	printf("%.4lf %.4lf\n",sum-h,h);
	return 0;
 } 
