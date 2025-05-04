#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

char ma[103][103];
int c[103][103];
int ans = 1000000;
bool flag;
int m, n, si, sj, fi, fj;
void dfs(int x, int y, int step) {
    if (step > ans)
        return;
    if (ma[y][x] == '#')
        return;
    if (c[y][x] == 1)
        return;
    else
        c[y][x] = 1;
    if (ma[y][x] == 'E') {
        ans = min(step, ans);
        flag = true;
        c[y][x] = 0;
        return;
    }
    dfs(x + 1, y, step + 1);
    dfs(x - 1, y, step + 1);
    dfs(x, y + 1, step + 1);
    dfs(x, y - 1, step + 1);
    c[y][x] = 0;
}

int main() {
    int T;
    cin >> T;
    while (T--) {
        cin >> n >> m;
        flag = false;
        ans = 1000000;
        memset(c, 0, sizeof(c));
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                cin >> ma[i][j];
                if (ma[i][j] == 'S') {
                    si = i;
                    sj = j;
                } else if (ma[i][j] == 'F') {
                    fi = i;
                    fj = j;
                }
            }
        }
        for (int i = 0; i <= n + 1; i++) {
            ma[i][0] = '#';
            ma[i][n + 1] = '#';
        }
        for (int j = 0; j <= m + 1; j++) {
            ma[0][j] = '#';
            ma[n + 1][j] = '#';
        }
        dfs(sj, si, 0);
        if (!flag)
            ans = -1;
        cout << ans << endl;
    }
}
