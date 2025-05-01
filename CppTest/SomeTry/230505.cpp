#include <bits/stdc++.h>
using namespace std;

template<int a>
int func(int b){
    cout<<a+b;
}
int main(){
    const int a=20;
    func<a>(2);
    return 0;
}