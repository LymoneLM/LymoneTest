#include <bits/stdc++.h>
using namespace std;
int main()
{
	double sum=0;
	int i=1;
	while(i<=100)
		sum += 1./i*(i++%2==0?:-1);
	cout<<"sum="<<sum;
	return 0;
}
