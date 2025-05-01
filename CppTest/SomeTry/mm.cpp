#include <bits/stdc++.h>
using namespace std;
bool prev[100001], curr[100001];
int main() {
    int n, m, temp;
    cin >> n >> m;
    while (m--) {
        cin >> temp;
        prev[temp] = true;
    }
    for (int i = 1; i <= n; i++)
        prev[i] = !prev[i];
    for (int len = 2; len <= n; len++) {
        for (int i = 1; i + len - 1 <= n; i++) {
            int j = i + len - 1;
            curr[i] = !prev[i + 1] || !prev[i];
        }
        for (int i = 1; i <= n; i++)
            prev[i] = curr[i];
    }
    cout << (prev[1] ? "Xiaozhu Hahaha" : "Goldye") << endl;
    return 0;
}

