//��������OJ����(Linux x64 g++ 7.5.0)��AC
//��win11,DEVCPP5.9.2����(TDM-GCC4.8.1 64-bit)������ó���ȷ��
//��Ҫ�������¸Ķ���
// 29�� 0��Ϊ 1
//41��49��yi��Ϊyi-1
#include <iostream>
using namespace std;
int main()
{
	char tel[11]= {},
	              num[10]= {},
	                       num2[10]= {};
	cin>>tel;
	for(int i=0; i<11; i++)
	{
		num[tel[i]-'0']++;
	}
	int n=0;
	for(int i=10; i>=0; i--)
	{
		if(num[i]!=0)
		{
			num2[n]=i+'0';
			n++;
		}
	}
	n--;
	cout<<"int[] arr = new int[]{";
	for(int i=0; i<n; i++)
	{
		cout<<num2[i]<<",";
	}
	cout<<num2[n]<<"};"<<endl;
	cout<<"int[] index = new int[]{";
	for(int i=0; i<10; i++)
	{
		for(int yi=0; yi<=n; yi++)
		{
			if(tel[i]==num2[yi])
			{
				cout<<yi<<",";
			}
		}
	}
	for(int yi=0; yi<=n; yi++)
	{
		if(tel[10]==num2[yi])
		{
			cout<<yi<<"};"<<endl;
			break;
		}
	}
	return 0;
}
