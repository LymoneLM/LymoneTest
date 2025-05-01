#include<iostream>
using namespace std;
int f(int x)
{
	if(x%4==0&&x%100!=0) return 1; 
	if(x%400==0) return 1;
}
int main()
{
	int a[12]={31,28,31,30,31,30,31,31,30,31,30,31};
	int y1;
	int m1;
	int d1;
	cin>>y1>>m1>>d1;
	int y2,m2,d2;
	cin>>y2>>m2>>d2;
	int sumy=0;
	for(int i=y1;i<y2;i++)
	if(f(i)) sumy+=366;
	else sumy+=365;
	int summ1=0;
	if(f(y1))
	{
		a[1]=29;
		for(int i=0;i<m1-1;i++)
		{
			summ1+=a[i];
		}
	}
	else
	{
		for(int i=0;i<m1-1;i++)
		{
			summ1+=a[i];
		}
	}
    int sum1;
    sum1=summ1+d1;
    int summ2=0;
    if(f(y2))
    {
    	a[1]=29;
    	for(int i=0;i<m2-1;i++)
    	{
    		summ2+=a[i];
		}
	}
	else
	{
		for(int i=0;i<m2-1;i++)
		{
			summ2+=a[i];
		}
	}
	int sum2;
	sum2=summ2+d2;
	int m;
	m=sumy+sum2-sum1;
	cout<<m;
	return 0;
}

