/*
9 80 205 40
90 60 96 1
210 3 101 89 
*/
#include <bits/stdc++.h>
using namespace std;
int main()
{
	int data[3][4];
	for(int xi=0;xi<3;xi++)
	{
		for(int yi=0;yi<4;yi++)
		{
			cin>>data[xi][yi];
		}
	}
	int max[3]={},min[4]={};
	for(int xi=0;xi<3;xi++)
	{
		int temp=data[xi][0];
		for(int yi=0;yi<4;yi++)
		{
			if(data[xi][yi]>temp)
			{
				temp=data[xi][yi];
				max[xi]=yi;
			}
		}
	}
	for(int yi=0;yi<4;yi++)
	{
		int temp=data[0][yi];
		for(int xi=0;xi<3;xi++)
		{
			if(data[xi][yi]<temp)
			{
				temp=data[xi][yi];
				min[yi]=xi;
			}
		}
	}
	bool flag=true;
	for(int xi=0;xi<3;xi++)
	{
		for(int yi=0;yi<4;yi++)
		{
			if(max[xi]==yi&&min[yi]==xi)
			{
				printf("[%d][%d]=%d is Saddle Point",xi,yi,data[xi][yi]);
				flag=false;
			}
		}
	}
	if(flag)
		cout<<"No Saddle Point";
	return 0;
}
