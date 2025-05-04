#include <bits/stdc++.h>
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
        //单行整活版
        /*
        for(int i=1,j=next[0]=0;i<pat.length();next[i++]=j==0?0:++j)while(j>0&&pat[i]!=pat[j])j=next[j-1];
        */
    }
    void print(){
        int len = pat.length();
        cout<<"0 -1\n";
        for(int i=1;i<len;i++)
            cout<<i<<" "<<next[i-1]<<"\n";    
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
int main(int argc, char *argv[]) {
    KMP kmp("abcabcabcabcabcabc");
    kmp.print();
    cout << kmp.find("hello");
}