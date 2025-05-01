#include <bits/stdc++.h>
using namespace std;

int a = 5;
int main() {
    int s = 0;
    {   int a = 3;
        s += a++;
    }
    s += a;
    cout << s;
}



