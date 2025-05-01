#include <stdio.h>
char timur[]= {'T','i','m','r','u'};

int main()
{
	int t;
	scanf("%d",&t);
	int n;
	char name[11];
	for(int i=0; i<t; i++)
	{
		scanf("%d%s",&n,&name);
		if(n!=5)
		{
			bool isit=true;
			for(int xi=0; xi<5; xi++)
			{
				for(int yi=0; yi<5; yi++)
				{
					if(name[xi]>name[yi])
					{
						char c;
						c=name[xi];
						name[xi]=name[yi];
						name[yi]=c;
					}
				}
			}
			for(int xi=0; xi<5; xi++)
			{
				printf("%c",name[xi]);
				if(timur[xi]!=name[xi])
					isit=false;
			}
			if(isit)
				printf("YES");
			else
				printf("NO");
		}
		else
		{
			printf("NO");
		}
	}
	return 0;
}
