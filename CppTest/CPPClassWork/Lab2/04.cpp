#include <bits/stdc++.h>
using namespace std;
int main()
{
	int num;cin>>num;
	double sum=0;
	double temp;int i=num;
	double ma=-1,mi=11;
	while(i--)
	{
		cin>>temp;
		ma=max(temp,ma);//if(temp>ma)ma=temp;
		mi=min(temp,mi);//if(temp<mi)mi=temp;
		sum+=temp;
	}
	cout<<(sum-ma-mi)/(num-2);
	return 0;
}
