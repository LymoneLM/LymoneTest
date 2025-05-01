#include <bits/stdc++.h>
using namespace std;
int main()
{
	double a,b,c;
	cin>>a>>b>>c;
	double delta=b*b-4*a*c;
	double td=sqrt(delta);
	cout<<(-b+td)/(2*a)<<" "
	<<(-b-td)/(2*a);
	return 0;
}
