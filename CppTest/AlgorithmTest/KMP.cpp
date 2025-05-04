#include <bits/stdc++.h>
using namespace std;
class KMP {
private:
    string pat;
    int **dp;

public:
    KMP(string _pat) {
        pat = _pat;
        dp = new int *[pat.length()];
        dp[0] = new int[256];
        dp[0][pat[0]] = 1;
        int x = 0;
        for (int j = 1; j < pat.length(); j++) {
            dp[j] = new int[256];
            for (int i = 0; i < 256; i++)
                dp[j][i] = (i == pat[j] ? j + 1 : dp[x][i]);
            x = dp[x][pat[j]];
        }
    }
    int find(string text) {
        int j = 0;
        for (int i = 0; i < text.length(); i++) {
            j = dp[j][text[i]];
            if (j == pat.length())
                return i - pat.length() + 1;
        }
        return -1;
    }
    ~KMP() {
        int x = pat.length();
        while (x--)
            delete[] dp[x];
        delete[] dp;
    }
};
int main() {
    KMP kmp("abc");
    cout << kmp.find("abdababababababababc");
}