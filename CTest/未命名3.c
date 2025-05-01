#include<stdio.h>
int main()
{
	int i=0;char str[101];
	scanf("%s", str);
	while (str[i]!='\0')
		printf("%c ", str[i++]);
	return 0;
}
