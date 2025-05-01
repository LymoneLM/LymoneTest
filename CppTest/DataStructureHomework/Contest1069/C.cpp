#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;
int find(int *dat, int n, const int x) {
    if(n==0) return -1010;
    return 1 + (dat[n / 2] == x ? 0 : (dat[n / 2] > x ? find(dat, n / 2, x) : find(dat + n / 2 + 1, n - n / 2 - 1, x)));
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, dat[1010];
    cin>>N;
    for (int i = 0; i <= N; i++)
        cin >> dat[i];
    int x=find(dat, N, dat[N]);
    if(x>0)
        cout<<x<<endl;
    else
        cout<<"NO"<<endl;

    return 0;
}