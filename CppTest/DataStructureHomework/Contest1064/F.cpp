#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

char nmap[110][110];
bool flag[110][110];
int minStep[110][110];
const int cstep[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

void find(int step, int x, int y) {
    if (minStep[x][y] != 0 && step >= minStep[x][y])
        return;
    minStep[x][y] = step;
    if (nmap[x][y] == 'E')
        return;
    flag[x][y] = true;
    for (int i = 0; i < 4; i++) {
        if (!flag[x + cstep[i][0]][y + cstep[i][1]] && (nmap[x + cstep[i][0]][y + cstep[i][1]] == '-'||nmap[x + cstep[i][0]][y + cstep[i][1]] == 'E'))
            find(step + 1, x + cstep[i][0], y + cstep[i][1]);
    }
    flag[x][y] = false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T, N, M;
    int Sx, Sy, Ex, Ey;
    cin >> T;
    while (T--) {
        cin >> N >> M;
        for (int x = 1; x <= N; x++) {
            for (int y = 1; y <= M; y++) {
                cin >> nmap[x][y];
                if (nmap[x][y] == 'S')
                    Sx = x, Sy = y;
                if (nmap[x][y] == 'E')
                    Ex = x, Ey = y;
            }
        }
        mm(flag);
        mm(minStep);
        flag[Sx][Sy] = true;
        find(0, Sx, Sy);
        cout << (minStep[Ex][Ey] ? minStep[Ex][Ey] : -1) << endl;
    }

    return 0;
}