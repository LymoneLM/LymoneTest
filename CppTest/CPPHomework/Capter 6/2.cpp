#include <bits/stdc++.h>
using namespace std;
int main()
{
    char data[101];
    cin.getline(data,100);
    int len=strlen(data);
    char max=0;int p=0;
    for(int i=0;i<len;i++)
    {
        if(data[i]>max)
        {
            p=i;
            max=data[i];
        }
    }
    for(int i=0;i<len;i++)
    {
        cout<<data[i];
        if(i==p)
            cout<<"ab";
    }
    return 0;
}