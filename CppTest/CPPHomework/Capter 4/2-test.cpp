#include <bits/stdc++.h>
using namespace std;
int enSum(int n)
{
	int sum=0;
	int max=sqrt(n);
	for(int i=1;i<n;i++)
	{
		if(n%i==0)
		{
			sum+=i;
		}
	}
	return sum;
}
int main()
{
	cout<<enSum(220)<<endl;
	return 0;
}
