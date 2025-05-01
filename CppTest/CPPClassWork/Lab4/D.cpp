#include <bits/stdc++.h>
using namespace std;
int main()
{
    int a[10],b[10],c[20];
    for(int i=0;i<10;i++)
        cin>>a[i];
    for(int i=0;i<10;i++)
        cin>>b[i];
    int a_max=a[0],a_min=a[0];
    int b_max=b[0],b_min=b[0];
    for(int i=1;i<10;i++)
    {
        if(a[i]>a_max)
            a_max=a[i];
        if(a[i]<a_min)
            a_min=a[i];
        if(b[i]>b_max)
            b_max=b[i];
        if(b[i]<b_min)
            b_min=b[i];
    }
    printf("%d %d\n%d %d\n",a_max,a_min,b_max,b_min);
    sort(a,a+10);
    sort(b,b+10);
    for(int i=0;i<10;i++)
        cout<<a[i]<<" ";
    cout<<endl;
    for(int i=9;i>=0;i--)
        cout<<b[i]<<" ";
    cout<<endl;
    int t=0;
    int ax=0,bx=0;
    while(t!=20)
    {
        if(a[ax]<=b[bx]&&ax<10)
        {
            c[t]=a[ax];
            ax++;
        }
        else
        {
            c[t]=b[bx];
            bx++;
        }
        t++;
    }
    for(int i=0;i<20;i++)
        cout<<c[i]<<" ";
    return 0;
}