#include <algorithm>
#include <iostream>
using namespace std;
int main() {
    float a[15];
    while (1) {
        int dc = 1, db = 1, fb = 1;
        for (int i = 0; i < 5; i++)
            cin >> a[i];
        if (a[0] == 0 && a[4] == a[0] && a[3] == 0 && a[2] == 0 && a[1] == 0)
            break;
        float d;
        float q;
        for (int i = 1; i < 5; i++) {
            if (dc == 1)
                if (i == 1)
                    d = a[i] - a[i - 1];
                else if (d != a[i] - a[i - 1])
                    dc = 0;
            if (db == 1)
                if (i == 1)
                    q = a[i] / a[i - 1];
                else if ((q != a[i] / a[i - 1]))
                    db = 0;
            if (fb == 1)
                if (i >= 2 && i < 5)
                    if (a[i] != (a[i - 1] + a[i - 2]))
                        fb = 0;
        }
        int num;
        if (dc == 1) {
            num = a[4];
            for (int i = 0; i < 5; i++) {
                num = num + d;
                cout << num;
                if (i != 4)
                    cout << " ";
            }
            cout << endl;
        } else if (db == 1) {
            num = a[4];
            for (int i = 0; i < 5; i++) {
                num = num * q;
                cout << num;
                if (i != 4)
                    cout << " ";
            }
            cout << endl;
        } else if (fb == 1) {
            for (int i = 5; i < 10; i++) {
                a[i] = a[i - 1] + a[i - 2];
                cout << a[i];
                if (i != 9)
                    cout << " ";
            }
            cout << endl;
        }
    }
    return 0;
}
