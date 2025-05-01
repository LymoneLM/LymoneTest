#include <bits/stdc++.h>
using namespace std;
int main()
{
	int N;
	cin>>N;
	for(int xi=0;xi<=100;xi++) 
	{
		for(int yi=0;yi<=100;yi++)
		{
			for(int zi=0;zi<=34;zi++)
			{
				if(5*xi+3*yi+zi==N&&xi+yi+3*zi==100)
					printf("x=%d,y=%d,z=%d\n",xi,yi,3*zi);
			}
		}
	}
	return 0;
}
