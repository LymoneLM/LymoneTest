#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

struct Node {
    char data;
    Node *l, *r;
};

void postOrderTraversal(Node *p) {
    if (p->l != NULL)
        postOrderTraversal(p->l);
    if (p->r != NULL)
        postOrderTraversal(p->r);
    cout << p->data;
    delete p;
}

Node *creatBTreePI(char *pres, char *ins, int n) {
    if (n == 0)
        return NULL;
    Node *p = new Node;
    p->data = pres[0];
    int i = 0;
    while (ins[i] != pres[0])
        i++;
    p->l = creatBTreePI(pres + 1, ins, i);
    p->r = creatBTreePI(pres + i + 1, ins + i + 1, n - i - 1);
    return p;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    char pres[30], ins[30];
    while (cin >> pres >> ins) {
        Node *p = creatBTreePI(pres, ins, strlen(pres));
        postOrderTraversal(p);
        cout<<endl;
    }

    return 0;
}