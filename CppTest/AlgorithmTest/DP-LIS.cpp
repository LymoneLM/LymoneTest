#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int f[105]={0},a[105]={0},i,x,p,n,ans=0;
    scanf("%d",&n);
    for(i=1;i<+n;i++)
        scanf("%d",&a[i]),f[i]=1;

    for(x=1;x<=n;x++){
        for(p=1;p<x;p++)
            if(a[p]<a[x])
                f[x]=max(f[x],f[p]+1);
        printf("f[%d]=%d\n",x,f[x]);
    }

    for(x=1;x<=n;x++)
        ans=max(ans,f[x]);

    printf("%d\n",ans);

    return 0;
}