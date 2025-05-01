#include <bits/stdc++.h>
using namespace std;
void split(char *str)
{
    int i = 0, n = 1;
    int max = 0, p = 0, maxp;
    while (str[i] != '\0')
    {
        if (str[i] == ' ')
        {
            if (i - p > max)
            {
                maxp = p;
                max = i - p;
            }
            p = i + 1;
            n++;
        }
        i++;
    }
    if (i - p > max)
    {
        maxp = p;
        max = i - p;
    }
    cout<<n<<" "<<max<<" ";
    while(str[maxp]!=' '&&str[maxp]!='\0')
    {
    cout<<str[maxp];
    maxp++;
    }
}
int main()
{
    char str[500];
    cin.getline(str, 500);
    split(str);
    return 0;
}