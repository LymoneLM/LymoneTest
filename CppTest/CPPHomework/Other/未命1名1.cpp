#include<iostream>
using namespace std;
int num;
int n;
int i = 0;
int sum = 0;
int main()
{
	cin >> num;
	//n = num % 10;
	//sum = sum + n;
	//cout << n ;
I:
	n = num % 10;
	cout << n ;
	sum +=n;
	i++;
	if ((num /= 10) > 0) goto I;
	cout << endl;
	cout << sum << endl;
	cout << i << endl;
	return 0;
}
