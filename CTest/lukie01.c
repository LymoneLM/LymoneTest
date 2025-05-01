#include <bits/stdc++.h>
int main()
{
    int A, B, i = 0, m = 0, j = 0;
    char C[100];
    scanf("%d", &A);
    scanf("%d", &B);
    scanf("%s", C);
    while (C[i] != '\0')
        i++;
    i--;
    if (A == 2 || A == 8 || A == 10)
    {
        for (; i >= 0; i--, j++)
        {
            m = m + (C[i] - 48) * pow(A, j);
        }
        int a[100];
        j = 0;
        do
        {
            a[j] = m % B;
            m = m / B;
            j++;
        } while (m != 0);
        for (j--; j >= 0; j--)
            printf("%d", a[j]);
    }
}