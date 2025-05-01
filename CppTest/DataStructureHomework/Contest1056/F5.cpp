#include <deque>
#include <iostream>
#include <string>
using namespace std;
void judge(string s) {
    deque<char> v;
    for (int a = 0; a < s.length(); a++) {
        v.push_back(s[a]);
    }
    int a = 0;
    char c, d;
    while (a < s.length() / 2) {
        c = v.front();
        v.pop_front();
        d = v.back();
        v.pop_back();
        if (c != '(' && c != '[' && c != '{') {
            if (d == ')') {
                cout << "NO1" << endl;
                return;
            } else if (d == ']') {
                cout << "NO2" << endl;
                return;
            } else if (d == '}') {
                cout << "NO3" << endl;
                return;
            } else {
                a++;
            }
        } else {
            if (c == '(' && d != ')') {
                cout << "NO1" << endl;
                return;
            } else if (c == '[' && d != ']') {
                cout << "NO2" << endl;
                return;
            } else if (c == '{' && d != '}') {
                cout << "NO3" << endl;
                return;
            }
        }
    }
    cout << "YES" << endl;
    return;
}
int main() {
    string s;
    getline(cin, s);
    judge(s);
    return 0;
}
