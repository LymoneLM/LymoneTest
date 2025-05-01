#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define INF 0x3f3f3f3f
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;
    int matrix[60][60];
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            cin >> matrix[i][j];
    bool A[60];
    mm(A);
    A[0] = true;
    int allCost = 0, minCost, minB, thisMinCost;
    for (int x = 1; x < N; x++) {
        minCost=INF;
        for (int i = 0; i < N; i++) {
            if (A[i]) {
                thisMinCost = INF;
                for (int j = 0; j < N; j++)
                    if (!A[j] && matrix[i][j] != 0)
                        thisMinCost = min(thisMinCost, matrix[i][j])
            }
            if(thisMinCost<minCost){
                minB=
            }
        }
    }

    return 0;
}