#include <iostream>
using namespace std;
int main()
{
	int N;
	cin>>N;
	for(int xi=1; xi<=N; xi++)
	{
		if(xi==1)
		{
			cout<<1<<endl;
			continue;
		}
		int temp=1;
		for(int yi=1;yi<xi;yi++)
		{
			cout<<temp;
			temp+=2;
		}
		cout<<temp;
		for(int yi=xi;yi>1;yi--)
		{
			temp-=2;
			cout<<temp;			
		}
		cout<<endl;
	}
	return 0;

}
