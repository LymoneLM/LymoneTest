#include <bits/stdc++.h>
using namespace std;
void swapstr(char a[], char b[])
{
    char t[50];
    strcpy(t, a);
    strcpy(a, b);
    strcpy(b, t);
}
char pickchar(char str[])
{
    return str[2] == 0 ? ' ' : str[2];
}
int main()
{
    char str[5][50] = {};
    for (int i = 0; i < 5; i++)
        cin >> str[i];
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 4; j++)
            if (strlen(str[j]) > strlen(str[j + 1]))
                swapstr(str[j + 1], str[j]);
    for (int i = 0; i < 5; i++)
        cout << str[i] << " ";
    cout << endl
         << "concatenate string:";
    for (int i = 0; i < 5; i++)
        cout << pickchar(str[i]);
    return 0;
}