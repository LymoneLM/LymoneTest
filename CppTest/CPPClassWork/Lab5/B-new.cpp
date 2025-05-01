#include <bits/stdc++.h>
using namespace std;
int main()
{
    int m, n;
    cin >> m >> n;
    int** data = new int* [m];
    for (int i = 0; i < m; i++)
    {
        data[i] = new int [n];
        for (int j = 0; j < n; j++)
            cin >> data[i][j];
    }
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
        {
            cout << data[j][i];
            cout <<((j+1==m)?'\n':' ');
        }   
    for (int i = 0; i < m; i++)
        delete[] data[i];      
    delete[] data;
    return 0;
}