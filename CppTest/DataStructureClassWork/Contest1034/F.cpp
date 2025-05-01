#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;
struct calc {
    bool is_op;
    union F {
        char op;
        double num;
    } mem;
};
int main() {

    vector<calc> vt;
    double a;
    calc m;
    char x[200];
    while (cin >> x) {
        if (x[0] > '9' || x[0] < '0') {
            m.is_op = true;
            m.mem.op = x[0];
        } else {
            m.is_op = false;
            sscanf(x, "%lf", &a);
            m.mem.num = a;
        }
        vt.push_back(m);
    }
    for (int i = vt.size() - 1; i >= 0; i--) {
        if (vt[i].is_op) {
            double &x = vt[i + 2].mem.num, &y = vt[i + 1].mem.num;
            switch (vt[i].mem.op) {
            case '+':
                y += x;
                break;
            case '-':
                y -= x;
                break;
            case '*':
                y *= x;
                break;
            case '/':
                y /= x;
                break;
            }
            vt.erase(vt.begin() + i + 2);
            vt.erase(vt.begin() + i);
        }
    }
    printf("%.6lf", vt[0].mem.num);
    return 0;
}