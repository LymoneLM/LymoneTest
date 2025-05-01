#include<iostream>
using namespace std;
void func()
{
	int start,end,maxsum=0;
	cin>>start>>end;
	int i = start,temp = 0;
	for(; i <= end; i++)
	{
		int sum=1;
		for(int j = 2; j <= i / 2; j++)
		{
			if(0 == i%j)
			{
				sum+=j;
			}
		}
		if(sum > maxsum)
		{
			maxsum = sum;
			temp = i;
		}
	} 
	cout<<temp<<" "<<maxsum;
}
int main()
{
    func();
 	return 0;
}
