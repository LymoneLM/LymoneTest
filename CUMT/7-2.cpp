#include <iostream>
using namespace std;
int main()
{
	int N=0,floor=1,sum=1,add=6;
	char sign;
	cin>>N>>sign;
	if(N==1)
	{
		cout<<sign<<endl;
		cout<<'1';
		return 0;
	}
	while(sum<=N)
	{
		sum+=add;
		add+=4;
		++floor;
	}
	add-=4;
	sum-=add;
	--floor;
	//�����ӡ 
	for(int yi=floor;yi>=1;yi--)
	{
		//��ӡ�ո� 
		for(int xi=1;xi<=floor-yi;xi++)
			cout<<" ";
		//��ӡ�ַ� 
		for(int xi=1;xi<=yi*2-1;xi++)
			cout<<sign;
		cout<<endl;
	}
	//�����ӡ 
	for(int yi=2;yi<=floor;yi++)
	{
		//��ӡ�ո� 
		for(int xi=1;xi<=floor-yi;xi++)
			cout<<" ";
		//��ӡ�ַ� 
		for(int xi=1;xi<=yi*2-1;xi++)
			cout<<sign;	
		cout<<endl;
	}
	cout<<N-sum;
	return 0;
}
