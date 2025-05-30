#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

int mapc[27][27][2];
int maxc = -1;

void find(int key, int cost) {
    if (key == 'Z'-'A') {
        if (cost > maxc)
            maxc = cost;
        return;
    }
    for (int i = 1; i <= mapc[key][0][0]; i++)
        find(mapc[key][i][0], cost + mapc[key][i][1]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    cin >> N >> M;
    mm(mapc);
    char pre, next;
    int cost;
    for (int i = 0; i < M; i++) {
        cin >> pre >> next >> cost;
        mapc[pre-'A'][++mapc[pre-'A'][0][0]][0] = next-'A';
        mapc[pre-'A'][mapc[pre-'A'][0][0]][1] = cost;
    }

    find(0, 0);
    cout << maxc << endl;

    return 0;
}