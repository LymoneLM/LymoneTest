#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <ctime>
#include <iomanip>
#include <string>
#include <memory>
#include <stdexcept>

using namespace std;

// ��־����
void writelog(const string& what, double num) {
    ofstream logfile("rilog.txt", ios::app);
    if (logfile) {
        time_t now = time(0);
        tm* timenow = localtime(&now);
        logfile << "[" << put_time(timenow, "%Y-%m-%d %H:%M:%S") << "] "
                << what << ": " << fixed << setprecision(2) << num << endl;
    }
}

// ͼ�λ���
class ShapeBase {
public:
    virtual double mianji() const = 0;
    virtual double zhouchang() const = 0;
    virtual void showinfo(ostream& out) const = 0;
    virtual string leixing() const = 0;
    virtual ~ShapeBase() = default;
};

// ������������
ostream& operator<<(ostream& out, const ShapeBase& s) {
    s.showinfo(out);
    return out;
}

// �ӷ����������
double operator+(const ShapeBase& a, const ShapeBase& b) {
    return a.mianji() + b.mianji();
}

// Բ����
class RoundShape : public ShapeBase {
    double banjing;  // ʹ��ƴ��������
public:
    RoundShape(double r) : banjing(r) {
        if (r <= 0) throw runtime_error("�뾶��>0");
    }

    double mianji() const override {
        return 3.1415926 * banjing * banjing;
    }

    double zhouchang() const override {
        return 2 * 3.1415926 * banjing;
    }

    void showinfo(ostream& out) const override {
        out << "Բ�� (�뾶=" << banjing << ", ���=" << mianji()
           << ", �ܳ�=" << zhouchang() << ")";
    }

    string leixing() const override {
        return "Բ��";
    }
};

// ��Բ��
class OvalShape : public ShapeBase {
    double changzhou;  // ����
    double duanzhou;   // ����
public:
    OvalShape(double a, double b) : changzhou(a), duanzhou(b) {
        if (a <= 0 || b <= 0) throw runtime_error("������>0");
    }

    double mianji() const override {
        return 3.1415926 * changzhou * duanzhou;
    }

    double zhouchang() const override {
        double temp = pow((changzhou - duanzhou), 2) / pow((changzhou + duanzhou), 2);
        return 3.1415926 * (changzhou + duanzhou) * (1 + (3*temp)/(10 + sqrt(4 - 3*temp)));
    }

    void showinfo(ostream& out) const override {
        out << "��Բ (����=" << changzhou << ", ����=" << duanzhou
           << ", ���=" << mianji() << ", �ܳ���" << zhouchang() << ")";
    }

    string leixing() const override {
        return "��Բ";
    }
};

// ������
class RectShape : public ShapeBase {
    double kuan;   // ��
    double gao;    // ��
public:
    RectShape(double w, double h) : kuan(w), gao(h) {
        if (w <= 0 || h <= 0) throw runtime_error("�����>0");
    }

    double mianji() const override {
        return kuan * gao;
    }

    double zhouchang() const override {
        return 2 * (kuan + gao);
    }

    void showinfo(ostream& out) const override {
        out << "���� (��=" << kuan << ", ��=" << gao
           << ", ���=" << mianji() << ", �ܳ�=" << zhouchang() << ")";
    }

    string leixing() const override {
        return "����";
    }
};

// ��������
class TriShape : public ShapeBase {
    double bianA;  // ��A
    double bianB;  // ��B
    double bianC;  // ��C
public:
    TriShape(double a, double b, double c) : bianA(a), bianB(b), bianC(c) {
        if (a <= 0 || b <= 0 || c <= 0)
            throw runtime_error("�߳���>0");
        if (a+b <= c || a+c <= b || b+c <= a)
            throw runtime_error("�������α߳�");
    }

    double mianji() const override {
        double s = (bianA + bianB + bianC) / 2;
        return sqrt(s * (s - bianA) * (s - bianB) * (s - bianC));
    }

    double zhouchang() const override {
        return bianA + bianB + bianC;
    }

    void showinfo(ostream& out) const override {
        out << "������ (��=" << bianA << "," << bianB << "," << bianC
           << ", ���=" << mianji() << ", �ܳ�=" << zhouchang() << ")";
    }

    string leixing() const override {
        return "������";
    }
};

// ��ʾ���˵�
void showmenu(){
    cout << "\n=====ͼ�μ�����=====" << endl;
    cout << "1. ����ͼ��" << endl;
    cout << "2. �������" << endl;
    cout << "3. �����ܳ�" << endl;
    cout << "4. ��ʾ����ͼ��" << endl;
    cout << "5. ������" << endl;
    cout << "0. �˳�����" << endl;
    cout << "==================" << endl;
    cout << "����ѡ��: ";
}

// ��ʾͼ�β˵�
void showshapemenu(){
    cout << "\n====ͼ������====" << endl;
    cout << "1. Բ��" << endl;
    cout << "2. ��Բ" << endl;
    cout << "3. ����" << endl;
    cout << "4. ������" << endl;
    cout << "===============" << endl;
    cout << "��������: ";
}

int main() {
    vector<unique_ptr<ShapeBase>> allshapes;

    while (true) {
        int choose;
        showmenu();
        cin >> choose;

        if (choose == 0) {
            cout << "�������" << endl;
            break;
        }

        try {
            switch (choose) {
                case 1: {  // ����ͼ��
                    int shapetype;
                    showshapemenu();
                    cin >> shapetype;

                    if (shapetype == 1) {  // Բ��
                        double r;
                        cout << "����뾶: ";
                        cin >> r;
                        allshapes.push_back(make_unique<RoundShape>(r));
                    }
                    else if (shapetype == 2) {  // ��Բ
                        double a, b;
                        cout << "���볤����: ";
                        cin >> a;
                        cout << "����̰���: ";
                        cin >> b;
                        allshapes.push_back(make_unique<OvalShape>(a, b));
                    }
                    else if (shapetype == 3) {  // ����
                        double w, h;
                        cout << "������: ";
                        cin >> w;
                        cout << "����߶�: ";
                        cin >> h;
                        allshapes.push_back(make_unique<RectShape>(w, h));
                    }
                    else if (shapetype == 4) {  // ������
                        double s1, s2, s3;
                        cout << "�����һ����: ";
                        cin >> s1;
                        cout << "����ڶ�����: ";
                        cin >> s2;
                        cout << "�����������: ";
                        cin >> s3;
                        allshapes.push_back(make_unique<TriShape>(s1, s2, s3));
                    }
                    else {
                        cout << "��Ч����!" << endl;
                        break;
                    }
                    cout << "ͼ���Ѵ���!" << endl;
                    break;
                }

                case 2: {  // �������
                    if (allshapes.empty()) {
                        cout << "��ͼ������!" << endl;
                        break;
                    }

                    cout << "ѡ��ͼ��(0-" << allshapes.size()-1 << "): ";
                    int idx;
                    cin >> idx;

                    if (idx < 0 || idx >= allshapes.size()) {
                        cout << "��Ч���!" << endl;
                        break;
                    }

                    double mj = allshapes[idx]->mianji();
                    cout << "���: " << mj << endl;
                    writelog(allshapes[idx]->leixing() + "�������", mj);
                    break;
                }

                case 3: {  // �����ܳ�
                    if (allshapes.empty()) {
                        cout << "��ͼ������!" << endl;
                        break;
                    }

                    cout << "ѡ��ͼ��(0-" << allshapes.size()-1 << "): ";
                    int idx;
                    cin >> idx;

                    if (idx < 0 || idx >= allshapes.size()) {
                        cout << "��Ч���!" << endl;
                        break;
                    }

                    double zc = allshapes[idx]->zhouchang();
                    cout << "�ܳ�: " << zc << endl;
                    writelog(allshapes[idx]->leixing() + "�ܳ�����", zc);
                    break;
                }

                case 4: {  // ��ʾ����ͼ��
                    if (allshapes.empty()) {
                        cout << "��ͼ������!" << endl;
                        break;
                    }

                    cout << "\nͼ���б�:" << endl;
                    for (size_t i = 0; i < allshapes.size(); i++) {
                        cout << i << ": " << *allshapes[i] << endl;
                    }
                    break;
                }

                case 5: {  // ������
                    if (allshapes.size() < 2) {
                        cout << "����������ͼ��!" << endl;
                        break;
                    }

                    cout << "ѡ���һ��ͼ��(0-" << allshapes.size()-1 << "): ";
                    int idx1;
                    cin >> idx1;

                    cout << "ѡ��ڶ���ͼ��(0-" << allshapes.size()-1 << "): ";
                    int idx2;
                    cin >> idx2;

                    if (idx1 < 0 || idx1 >= allshapes.size() ||
                        idx2 < 0 || idx2 >= allshapes.size()) {
                        cout << "��Ч���!" << endl;
                        break;
                    }

                    double sum = *allshapes[idx1] + *allshapes[idx2];
                    cout << "����ܺ�: " << sum << endl;
                    writelog("�����Ӳ���", sum);
                    break;
                }

                default:
                    cout << "��Чѡ��!" << endl;
            }
        }
        catch (const exception& e) {
            cout << "����: " << e.what() << endl;
        }
    }

    return 0;
}