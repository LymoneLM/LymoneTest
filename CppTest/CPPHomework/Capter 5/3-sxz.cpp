#include<iostream>
using namespace std;
int main()
{
	int a[3][4],max[3]={0}, min[4]={0};
	int i, j,mx,mn;
	for (i = 0; i < 3; i++)
	{
		for (j = 0; j < 4; j++)
			cin >> a[i][j];
	}
	for (i = 0; i < 3; i++)
	{
		mx = a[i][0];
		for (j = 0; j < 4; j++)
		{
			if (a[i][j] > a[i][0])
				mx = a[i][j];
		}
		
		max[i] = mx;
	}
	for (j = 0; j < 4; j++)
	{
		mn = a[0][j];
		for (i = 0; i < 3; i++)
			if (a[i][j] < a[0][j])
				mn = a[i][j];

		min[j] = mn;
	}
	int x = 0;
	for (i = 0; i < 3; i++)
	{
		for(j=0;j<4;j++)
			if (max[i] == min[j])
			{
				cout << "[" << i<< "]" << "[" << j << "]" << "=" << max[j] << " is Saddle Point";
				x++;
			}

	}
	if (x == 0)cout << "No Saddle Point";
	return 0;
}

