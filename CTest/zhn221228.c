#include <bits/stdc++.h>
using namespace std;
int main(){
    int blank=0,digit=0,other=0;
    char str[101];
    cin.getline(str,101);
    int len=strlen(str);
    while(len--){
        blank+=(str[len]==' '?1:0);
        if(str[len]>='0'&&str[len]<='9')
            ++digit;
        else    
            ++other;
    }
    printf("blank = %d,digit = %d,other = %d",
        blank,digit,other-blank);
}