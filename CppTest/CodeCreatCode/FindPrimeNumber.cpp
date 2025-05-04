#include <bits/stdc++.h>
const int ola_maxn = 1e6 + 10;
bool ola_ispri[ola_maxn];
int ola_pri[ola_maxn], ola_n = 0;
inline void ola() {
    memset(ola_ispri, true, sizeof(ola_ispri));
    ola_ispri[0] = ola_ispri[1] = false;
    for (int i = 2; i < ola_maxn; i++) {
        if (ola_ispri[i])
            ola_pri[ola_n++] = i;
        for (int j = 0; j < ola_n; j++) {
            if (i * ola_pri[j] >= ola_maxn)
                break;
            ola_ispri[i * ola_pri[j]] = false;
            if (i % ola_pri[j] == 0)
                break;
        }
    }
}
int main() {
    ola();
    std::ofstream code("PrimerPrime.cpp", std::ios::out | std::ios::trunc);
    long long N;
    std::cout << "Please type in the N, I will find the prime from 0 to N\n";
    std::cin >> N;
    if (N > 1e6)
        std::cout << "The " << N << " is so big that you need wait\n";
    code << "#include <iostream>\nusing namespace std;\nint main(){\n"
         << "    long long N;\n    cin >> N;\n";
    long long i = -1;
    while (++i != N)
        code << "    if ( N == " << i << " ){\n        cout << " << i << " << \" is " << ((ola_ispri[i]) ? "" : "not ") << "a prime\";\n        return 0;\n    }\n";
    code << "    return 0;\n}";
    std::cout << "The CPP code have been placed in your floder, it was named PrimerPrime.cpp\n"
              << "thanks for you use!\n";
    return 0;
}