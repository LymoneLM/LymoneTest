#include <bits/stdc++.h>
using namespace std;

template<typename T>
void mysort(T arry[],int len)
{
	for(int xi=0; xi<len; xi++)
	{
		for(int yi=0; yi<len; yi++)
		{
			if(arry[xi]>arry[yi])
			{
				T c;
				c=arry[xi],arry[xi]=arry[yi],arry[yi]=c;
			}
		}
	}
	for(int xi=0; xi<len; xi++)
		cout<<arry[xi]<<" ";
	return;
}

void test()
{
	int arryint[]= {5,3,7,8,2,9,0};
	char arrychar[]="ILOVEYOU";
	int len1=sizeof(arryint)/sizeof(int)
	         ,len2=sizeof(arrychar)/sizeof(char);
	mysort(arryint,len1);
	mysort(arrychar,len2);
	return;
}

int main()
{
	test();
	return 0;
}
