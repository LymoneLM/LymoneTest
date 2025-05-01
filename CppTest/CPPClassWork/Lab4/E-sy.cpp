#include <iostream>
using namespace std;
int main()
{
    char s[50];
    cin.getline(s, 50);
    int i;
    int n = 0;
    for (i = 0;; i++)
    {
        if (s[i] == ' ')
        {
            cout << endl;
            ++n;
        }
        if (s[i] == '.')
        {
            cout << endl;
            break;
        }
        if (s[i] != ' ')
            cout << s[i];
       // else
           // cout << '\0';
    }
    cout << n + 1;
    return 0;
}
