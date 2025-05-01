#include <bits/stdc++.h>
using namespace std;
int main()
{
	double sum=0;int i=1;
	//for(;i<=100;i++)
	while(i<=100)
		//sum += 1.0/i*(i++%2==1?1:-1);
		sum += 1.0/i*(i++%2==0?-1:1);
	cout<<"sum:"<<sum;
	return 0;
}
