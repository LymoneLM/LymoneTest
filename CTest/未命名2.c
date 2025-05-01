#include<stdio.h>
#include<math.h>
int main()
{
	int a, b, c, n, r;
	scanf("%d", &r);
	n = log10(r);
	b = pow(10, n);
	a = r % b;
	while (b != 0)
	{
		a = r / b;
		printf("%d ", a%10);
		r = r - b;
		b = b / 10;
	}
	return 0;
}
