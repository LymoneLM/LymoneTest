#include <bits/stdc++.h>
using namespace std;
int main()
{
    double all,w,p;
    char temp;
    cin>>temp;
    while (temp!='q')
    {
        cin>>w>>p;
        switch (temp)
        {
            case 'a':
            all+=w*p;
            break;
            case 'b':
            all+=w*p/2;
            break;
            case 'o':
            all+=(w>10?w*p/2:(w>5?w*p*0.8:w*p));
            break;
        }
        cin>>temp;
    }
    printf("%.2lf",all);
    return 0;
}