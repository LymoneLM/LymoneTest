#include <stdio.h>
#include <string.h>
char s[5007];
int main() {
    while (scanf("%s", s) != EOF) {
        int len = strlen(s) - 1, ans = 0, l, r;
        for (int i = 0; i <= len; ++i, ++ans) {
            for (l = i - 1, r = i + 1; l >= 0 && r <= len && s[l] == s[r]; --l, ++r, ++ans);
            for (l = i, r = i + 1; l >= 0 && r <= len && s[l] == s[r]; --l, ++r, ++ans);
        }
        printf("%d\n", ans);
    }
    return 0;
}
