#include <bits/stdc++.h>
using namespace std;

template<typename T>
void swap(T &a,T &b)
{
	
}

template<typename T>
void mysort(T *arry[],int len)
{
	for(int xi=0; xi<len; xi++)
	{
		for(int yi=0; yi<len; yi++)
		{
			if(arry[xi]>arry[yi])
				swap(arry[xi],arry[yi]); 
		}
	}
	for(int xi=0; xi<len; xi++)
	return;
}
void test()
{
	int arryint[]={78,42,432,6554,3463,612,22,888,9,332,114,34,2};
	char arrychar[]="9123ILOVEYOU";
	mysort(&arryint,int(sizeof(arryint)/sizeof(int)));
	for(int i=0;i<sizeof(arryint)/sizeof(int);i++)
		printf("%d ",arrtint[i]);
	cout<<endl;
	mysort(&arrychar,int(sizeof(arrychar)/sizeof(char)));
	for(int i=0;i<sizeof(arrychar)/sizeof(char);i++)
		printf("%c ",arrtchar[i]);
	return ;
}



int main()
{
	test();
	return 0;
}
