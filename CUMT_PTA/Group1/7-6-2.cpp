#include <bits/stdc++.h>
using namespace std;

int main()
{
	long N,temp; //int����ָ������
	int start=0,len=0;
	cin >> N;
	for(int i=2; i<=sqrt(N); i++)
	{
		temp = 1;
		for(int j=i; temp*j<=N; j++)
		{
			temp *= j;
			if(N%temp==0 && j-i+1>len) // ��¼�����������
			{
				start = i; //������ʼ����
				len = j-i+1; //���³���
			}
		}
	}
	if(start==0) //����
		cout << "1" << '\n' << N;
	else  //������
	{
		cout << len << '\n' << start;
		for(int i=start+1; i<start+len; i++)
		{
			cout << "*" << i;
		}
	}
	return 0;
}

