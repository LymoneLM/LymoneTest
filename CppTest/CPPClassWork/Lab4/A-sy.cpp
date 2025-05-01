#include<iostream>
using namespace std;
int b = 0;
int main()
{
	double s[50] = {};
	double m[50]={};
	int k=0, i;
	double ava=0,sum=0;
	cin >> k;
	for (i = 0; i < k; ++i)
	{
		cin >> s[i];
		sum+=s[i];
	}
	ava = sum / k;
	for (i = 0; i < k; ++i)
	{
		if (ava < s[i])
			++b;
	}
	cout << ava << " " << b << endl;
	int c = 0;
	for (c=0; c <= k;c++)
		m[c] = s[c];
	for (i = 0; i < k; i++)
		cout << m[i] << " ";
	return 0;
}
