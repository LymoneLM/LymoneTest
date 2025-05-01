#include<iostream>
#include<cmath>
using namespace std;
int digit(long n,int k)
{
	int b=n/pow(10,k-1);
	if (b!=0)
	{
		int a=b%10;
		return a;
	}
	else
	return -1;
}
int main()
{
	long n;
	int k;
	cin>>n>>k;
	digit(n, k);
	return 0;
}
