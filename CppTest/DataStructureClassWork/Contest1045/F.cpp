#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;
int tree[28][28];
int func(int x){
    cout<<char(x+'A')<<" ";
    if(tree[x][0]==0)   
        return 0;
    for(int i=1;i<=tree[x][0];i++)
        func(tree[x][i]);
    return 0;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    mm(tree);
    char A,B;
    while(cin>>A){
        cin>>B;
        tree[A-'A'][++tree[A-'A'][0]]=B-'A';
    }
    func(0);
    return 0;
}