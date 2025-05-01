#include <iostream>
using namespace std;
void abc(const char *strin, char *strout)
{
    int i = 0;
    int f = 0;
    while (strin[i] != '\0')
    {
        if (strin[i] >= 'A' && strin[i] <= 'Z')
            strout[f++] = strin[i];
        if (strin[i] < '0' || strin[i] > '9')
            strout[f++] = strin[i];
        i++;
    }
}
int main()
{
    char strin[64] = {}, strout[64] = {};
    cin >> strin;
    abc(strin, strout);
    cout << strout;
}