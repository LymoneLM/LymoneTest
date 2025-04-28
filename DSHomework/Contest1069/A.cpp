#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

bool matrix[110][110];
bool flag[110];
int m,n,cnt;

void find(int x){
    cout<<x<<" ";
    flag[x]=true;
    for(int i=0;i<m;i++)
        if(matrix[x][i]&&!flag[i])
            find(i);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    mm(matrix);
    mm(flag);
    cin>>m>>n;
    cnt=0;
    int tempx,tempy;
    for(int i=0;i<n;i++){
        cin>>tempx>>tempy;
        matrix[tempx][tempy]=true;
        matrix[tempy][tempx]=true;
    }
    find(0);

    return 0;
}