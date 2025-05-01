#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    char temp[110];
    cin>>temp;
    int cnt=-1,len=strlen(temp);

    stack<char> ch;
    while(++cnt<len)
        switch(temp[cnt]){
            case '{':
                ch.push('}');
                break;
            case '[':
                ch.push(']');
                break;
            case '(':
                ch.push(')');
                break;
            case ')':
            case ']':
            case '}':
                if(ch.size()==0||ch.top()!=temp[cnt]){
                    if(ch.size()==0)
                        ch.push(temp[cnt]);
                    goto end;
                }else
                    ch.pop();   
        }
end:if(ch.size()==0)
        cout<<"YES";
    else switch (ch.top()){
    case ')':
        cout<<"NO1";
        break;
    case ']':
        cout<<"NO2";
        break;
    case '}':
        cout<<"NO3";
        break;
    }
    return 0;
}