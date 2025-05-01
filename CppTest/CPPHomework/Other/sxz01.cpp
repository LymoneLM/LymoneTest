#include <iostream>
#include <iomanip>
using namespace std;

int main()
{
    int a[3][3];
    int (*p)[3];
    p = a;
    int i, j, t;
    for (i = 0; i < 3; i++)
        for (j = 0; j < 3; j++)
            cin >> *(*(a + i) + j);
    for (i = 0; i < 3; i++)
        for (j = 0; j < 3; j++)
        {
            //t = *(*(p + i) + j);
            //*(*(p + i) + j) = *(*(p + j) + i);
            //*(*(p + j) + i) = t;
            t=p[i][j];
            p[i][j]=p[j][i];
            p[j][i]=t;
        }
    for (i = 0; i < 3; i++)
    {
        for (j = 0; j < 3; j++)
            cout << setw(5) << p[i][j] << " ";
        cout << endl;
    }
    return 0;
}
