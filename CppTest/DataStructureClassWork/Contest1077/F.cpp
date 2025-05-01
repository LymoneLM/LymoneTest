#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int x[10], y[10], j = 0, k = 0, temp;
    for (int i = 0; i < 10; i++) {
        cin >> temp;
        if (temp % 2 == 0)
            y[k++] = temp;
        else
            x[j++] = temp;
    }
    sort(x,x+5,greater<int>());
    sort(y,y+5);
    for (int i = 0; i < 5; i++)
        cout<<x[i]<<" ";
    for (int i = 0; i < 5; i++)
        cout<<y[i]<<" \n"[i==4?1:0];

    return 0;
}