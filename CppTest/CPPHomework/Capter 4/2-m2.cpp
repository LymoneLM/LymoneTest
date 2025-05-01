#include<iostream>
#include<cmath>
using namespace std;
int f(int n)
{
	int i = 1,c=0;
	for (; i < n; i++)
	{
		if (n % i == 0)
		{
			c += i;
		}
		if (i >=n)break;
	}
	return c;
}
int g(int a)
{
	int e = -1;
	for (int b = 2; b <= a; b++)
	{
		if (b == f(f(b)) && f(b) < a && b < f(b))
		{
			cout << b << " " << f(b) << "\n";
			e=1;
		}
	}
	return e;
}
int main()
{
	int a;
	cin >> a;
	if (g(a)==-1)
	{
		cout << "No";
	}
	return 0;
}

