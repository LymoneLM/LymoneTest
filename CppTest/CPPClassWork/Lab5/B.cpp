#include <bits/stdc++.h>
using namespace std;
int main()
{
    int data[101][101];
    int m, n;
    cin >> m >> n;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            cin >> data[i][j];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
        {
            cout << data[j][i];
            cout <<((j+1==m)?'\n':' ');
        }         
    return 0;
}