#include <queue>
#include <stdio.h>
#include <string.h>
using namespace std;

struct node {
    int x, y, step;
};

char map[105][105];
int vis[105][105];
int to[4][2] = {1, 0, -1, 0, 0, 1, 0, -1};
int n, m, sx, sy, ex, ey, ans;

int check(int x, int y) {
    if (x < 0 || x >= n || y < 0 || y >= m)
        return 1;
    if (vis[x][y] || map[x][y] == '#')
        return 1;
    return 0;
}

void bfs() {
    int i;
    queue<node> Q;
    node a, next;
    a.x = sx;
    a.y = sy;
    a.step = 0;
    vis[a.x][a.y] = 1;
    Q.push(a);
    while (!Q.empty()) {
        a = Q.front();
        Q.pop();
        if (map[a.x][a.y] == 'E') {
            ans = a.step;
            return;
        }
        for (i = 0; i < 4; i++) {
            next = a;
            next.x += to[i][0];
            next.y += to[i][1];
            if (check(next.x, next.y))
                continue;
            next.step = a.step + 1;
            vis[next.x][next.y] = 1;
            Q.push(next);
        }
    }
    ans = -1;
}

int main() {
    int t;
    scanf("%d", &t);
    while (t--) {
        scanf("%d%d", &n, &m);
        int i, j;
        for (i = 0; i < n; i++)
            scanf("%s", map[i]);
        for (i = 0; i < n; i++) {
            for (j = 0; j < m; j++) {
                if (map[i][j] == 'S') {
                    sx = i;
                    sy = j;
                }
            }
        }
        memset(vis, 0, sizeof(vis));
        bfs();
        printf("%d\n", ans);
    }

    return 0;
}
