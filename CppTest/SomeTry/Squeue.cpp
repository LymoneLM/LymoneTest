#include <iostream>
using namespace std;

class sNode {
public:
    short x, y;
    sNode *snext;
};

class Linkqueue {
    // ������-��
    // ɾβ��ͷ
public:
    void initQ();
    void enQ(short xx, short yy);
    bool deQ();
    void destoryQ();
    void printQ(); // devOnly
private:
    sNode *front;
    sNode *rear;
};
void Linkqueue::initQ() {
    sNode *p = new sNode;
    front = p;
    rear = p;
    p->snext = NULL;
    return;
}
void Linkqueue::enQ(short xx, short yy) {
    sNode *p = new sNode;
    p->x = xx;
    p->y = yy;
    rear->snext = p;
    rear = p;
    p->x = xx;
    p->y = yy;
    return;
}
bool Linkqueue::deQ() {
    if (rear == front)
        return false;
    sNode *p;
    p = front->snext;
    front->snext = p->snext;
    delete p;
    return true;
}
void Linkqueue::destoryQ() {
    while (rear != front)
        Linkqueue::deQ();
    delete front;
    return;
}
void Linkqueue::printQ() {
    if (rear == front)
        return;
    sNode *p = front;
    do {
        p = p->snext;
        cout << "X=" << p->x << "Y=" << p->y << endl;
    } while (p != rear);
    return;
}

int main() {
    Linkqueue Q;
    Q.initQ();
    Q.enQ(1, 1);
    Q.enQ(2, 2);
    Q.enQ(3, 3);
    Q.deQ();
    Q.enQ(4, 4);
    Q.printQ();
    Q.destoryQ();
    return 0;
}
