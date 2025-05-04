#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    static int strStr(string haystack, string needle) {
        int* next = new int[needle.length()];
        int j=0;
        next[0]=0;
        for(int i=1;i<needle.length();i++){
            while(j>0&&needle[i]!=needle[j])
                j=next[j-1];
            if(needle[i]==needle[j])
                j++;
            next[i]=j;
        }
        for(int i=0;i<haystack.length();i++){
            while(j>0&&haystack[i]!=needle[j])
                j=next[j-1];
            if(haystack[i]==needle[j])
                j++;
            if(j==needle.length()){
                cout<<i-j+1;
                return 0;
            }
        }
        cout<<-1;
        return 0;
    }
};
int main(){
    Solution::strStr(string("aaa"),string("aa"));
}