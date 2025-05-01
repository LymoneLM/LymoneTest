#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N,search,dat[110][2];cin>>N;
    string name[110];
    for(int i=0;i<N;i++)
        cin>>dat[i][0]>>name[i]>>dat[i][1];
    cin>>search;
    for(int i=0;i<N;i++)
        if(dat[i][0]==search)
            cout<<name[i]<<" "<<dat[i][1]<<endl;

    return 0;
}