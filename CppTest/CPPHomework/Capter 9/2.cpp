#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <iomanip>
using namespace std;
class Score
{
private:
    int Chinese, Math, English;
    static int TotalScore;
    static int TotalStudent;

public:
    Score() {}
    void setScore(int c, int m, int e)
    {
        Chinese = c, Math = m, English = e;
        TotalScore += (c + m + e);
        ++TotalStudent;
    }
    int Sum()
    {
        return Chinese + Math + English;
    }
    void Show()
    {
        printf("%d %d %d\n", Chinese, Math, English);
    }
    double static getAve()
    {
        return 1.0 * TotalScore / TotalStudent;
    }
};
int Score::TotalScore;
int Score::TotalStudent;
int main()
{
    int n, op, i, c, m, e;
    cin >> n;
    int id = 1;
    Score sco[11];
    while (n--)
    {
        cin >> op;
        if (op == 1)
        {
            cin >> c >> m >> e;
            sco[id].setScore(c, m, e);
            id++;
        }
        else if (op == 2)
        {
            cin >> i;
            cout << sco[i].Sum() << endl;
        }
        else if (op == 3)
        {
            cin >> i;
            sco[i].Show();
        }
        else
        {
            printf("%.2lf\n", Score::getAve());
        }
    }
    return 0;
}