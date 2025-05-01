#include <bits/stdc++.h>
using namespace std;
int main()
{
    char s[50];
    cin.getline(s, 50);
    int a=0,b=0;int n=0;
    while(s[a-1]!='.')
    {
        b++;
        if(s[b]==' '||s[b]=='.')
        {
            n++;
            for(int i=a;i<b;i++)
                cout<<s[i];
            cout<<endl;
            a=b+1;
        }
    }
    cout<<n;
    return 0;
}