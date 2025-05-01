#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;
class num {
public:
    long long dat, abs;
    friend bool operator<(num A, num B) { return (A.abs == B.abs) ? (A.dat < B.dat) : (A.abs < B.abs); }
    void input() {
        cin >> dat;
        ll a = dat, x = 0;
        while (a > 0)
            x += a % 10, a /= 10;
        abs = x;
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    num dat[1010];
    for (int i = 0; i < n; i++)
        dat[i].input();
    sort(dat, dat + n);
    while (n--)
        cout << dat[n].dat << " \n"[n == 0 ? 1 : 0];

    return 0;
}