#include <bits/stdc++.h>
using namespace std;
int main()
{
    int x[50],y[50];
    int k,n=0;
    cin>>k; 
    double ave=0;
    for(int i=0;i<k;i++)
    {
        cin>>x[i];
        ave+=x[i];
    }
    ave/=k;
    int t=0;
    for(int i=0;i<k;i++)
    {
        if(x[i]>ave)
            n++;
        bool flag=false;
        for(int m=0;m<t;m++)
        {
            if(x[i]==y[m])
                flag=true;
        }
        if(flag)
            continue;
        y[t++]=x[i];
    }
    
    cout<<ave<<" "<<n<<" \n";

    for(int i=0;i<t;i++)
    {
        cout<<y[i]<<" ";

    }
    return 0;
}
