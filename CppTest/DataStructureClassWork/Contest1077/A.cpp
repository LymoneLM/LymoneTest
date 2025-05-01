#include <bits/stdc++.h>
using namespace std;
const int N = 10000;
map<string, string> parent;
map<string, int> data;
int main() {
    int n;
    cin >> n;
    for (int i = 0; i < pow(2, n + 1) - 2; i++) {
        string m, n;
        int len;
        cin >> m >> n >> len;
        parent[n] = m;
        data[n] = len;
    }
    string p;
    cin >> p;
    int ans = 0;
    while (parent.count(p)) {
        ans += data[p];
        p = parent[p];
    }
    cout << ans;
    return 0;
}
