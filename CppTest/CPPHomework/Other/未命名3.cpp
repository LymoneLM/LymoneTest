#include <bits/stdc++.h>
using namespace std;
int main()
{
	double sum = 0;
	long long i = 0;
	while (i<1e9)
		sum += 1.0 / (2*i+1) * (i++%2==0?:-1);
	printf("%d:%.16lf\n",i,4*sum);
	return 0;
}

