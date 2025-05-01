#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;
class KMP {
private:
    string pat;
    int *next;
public:
    KMP(string _pat) {
        pat = _pat;
        next = new int[pat.length()];
        next[0] = 0;
        for (int i = 1, j = 0; i < pat.length(); i++) {
            while (j > 0 && pat[i] != pat[j])
                j = next[j - 1];
            if (pat[i] == pat[j])
                j++;
            next[i] = j;
        }
    }    
    int find(string text) {
        for (int i = 0, j = 0; i < text.length(); i++) {
            while (j > 0 && text[i] != pat[j])
                j = next[j - 1];
            if (text[i] == pat[j])
                j++;
            if (j == pat.length())
                return i - j + 1;
        }
        return -1;
    }
    ~KMP() { delete[] next; }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    string pattern,text;
    cin>>text>>pattern;
    KMP kmp(pattern);
    cout<<kmp.find(text)+1;

    return 0;
}