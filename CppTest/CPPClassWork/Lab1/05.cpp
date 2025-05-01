#include <bits/stdc++.h>
using namespace std;
int main()
{
	int sec1,sec2;
	int h,min,sec;
	cin>>h>>min>>sec;
	sec1=(h*60+min)*60+sec;
	cin>>h>>min>>sec;
	sec2=(h*60+min)*60+sec;
	cout<<abs(sec2-sec1);
	return 0;
}
