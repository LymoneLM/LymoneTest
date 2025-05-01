#include<iostream>
using namespace std;
int main()
{
    int n,d=0,N=0,max=0,j=1,s=0;
    int m[1000];
    int f[1000];
    cin>>n;
    for(int i=1;i<=n;i++)
    {
        cin>>m[i];
    }
    for(int i=1;i<=n;i++)
    {
        f[i]=0;
    }
    for(int i=1;i<=n-1;i++)
    { 
          if(m[i]<=m[i+1])
        {    
            f[j]=f[j]+m[i+1]-m[i];
            N++;
        }
        else
        {   
        if(f[j])
        {
            j++;
        }  
        }
    }
    if(N>0)
    {
        for(int i=1;i<=j;i++)
    {
        if(f[i]>=max)
        {
            max=f[i];
            s++;
        }
    }
 
        cout<<max;
    }
    return 0;
}
