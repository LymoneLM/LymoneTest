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
bool g(int a)
{
	bool flag=false;
	for (int b = 2; b <= a; b++)
	{
		int fb=f(b);
		if (b == f(fb) && fb < a && b < fb)
		{
			cout << b << " " << fb << "\n";
			flag=true;
		}
	}
	return flag;
}
int main()
{
	int a;
	cin >> a;
	if (!g(a))
		cout << "N0";
	return 0;
}

