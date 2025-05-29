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

// ��־��¼����
void logToFile(const string& operation, double result) {
    ofstream logFile("shape_calculator.log", ios::app);
    if (logFile.is_open()) {
        time_t now = time(nullptr);
        tm* ltm = localtime(&now);
        logFile << "[" << put_time(ltm, "%Y-%m-%d %H:%M:%S") << "] "
               << operation << ": " << fixed << setprecision(2) << result << endl;
        logFile.close();
    }
}

// ͼ�λ���
class Shape {
public:
    virtual double area() const = 0;
    virtual double perimeter() const = 0;
    virtual void print(ostream& os) const = 0;
    virtual string getType() const = 0;
    virtual ~Shape() = default;
};

// ����<<������������ͼ����Ϣ
ostream& operator<<(ostream& os, const Shape& shape) {
    shape.print(os);
    return os;
}

// ����+���������������
double operator+(const Shape& a, const Shape& b) {
    return a.area() + b.area();
}

// Բ����
class Circle : public Shape {
    double radius;
public:
    Circle(double r) : radius(r) {
        if (r <= 0) throw invalid_argument("�뾶�������0");
    }

    double area() const override {
        return M_PI * radius * radius;
    }

    double perimeter() const override {
        return 2 * M_PI * radius;
    }

    void print(ostream& os) const override {
        os << "Բ�� (�뾶=" << radius << ", ���=" << area()
           << ", �ܳ�=" << perimeter() << ")";
    }

    string getType() const override {
        return "Բ��";
    }
};

// ��Բ��
class Ellipse : public Shape {
    double semiMajor;
    double semiMinor;
public:
    Ellipse(double a, double b) : semiMajor(a), semiMinor(b) {
        if (a <= 0 || b <= 0) throw invalid_argument("���᳤�ȱ������0");
    }

    double area() const override {
        return M_PI * semiMajor * semiMinor;
    }

    double perimeter() const override {
        // ʹ������Ŭ����ƹ�ʽ
        double h = pow((semiMajor - semiMinor), 2) / pow((semiMajor + semiMinor), 2);
        return M_PI * (semiMajor + semiMinor) * (1 + (3*h)/(10 + sqrt(4 - 3*h)));
    }

    void print(ostream& os) const override {
        os << "��Բ (������=" << semiMajor << ", �̰���=" << semiMinor
           << ", ���=" << area() << ", �ܳ���" << perimeter() << ")";
    }

    string getType() const override {
        return "��Բ";
    }
};

// ������
class Rectangle : public Shape {
    double width;
    double height;
public:
    Rectangle(double w, double h) : width(w), height(h) {
        if (w <= 0 || h <= 0) throw invalid_argument("��߱������0");
    }

    double area() const override {
        return width * height;
    }

    double perimeter() const override {
        return 2 * (width + height);
    }

    void print(ostream& os) const override {
        os << "���� (��=" << width << ", ��=" << height
           << ", ���=" << area() << ", �ܳ�=" << perimeter() << ")";
    }

    string getType() const override {
        return "����";
    }
};

// ��������
class Triangle : public Shape {
    double a, b, c;
public:
    Triangle(double s1, double s2, double s3) : a(s1), b(s2), c(s3) {
        if (s1 <= 0 || s2 <= 0 || s3 <= 0)
            throw invalid_argument("�߳��������0");
        if (s1+s2 <= s3 || s1+s3 <= s2 || s2+s3 <= s1)
            throw invalid_argument("�߳��޷�����������");
    }

    double area() const override {
        // ���׹�ʽ
        double s = perimeter() / 2;
        return sqrt(s * (s - a) * (s - b) * (s - c));
    }

    double perimeter() const override {
        return a + b + c;
    }

    void print(ostream& os) const override {
        os << "������ (��=" << a << "," << b << "," << c
           << ", ���=" << area() << ", �ܳ�=" << perimeter() << ")";
    }

    string getType() const override {
        return "������";
    }
};

// ��ӡ���˵�
void printMenu(){
    cout << "\n=====ͼ�μ������˵�=====" << endl;
    cout << "1. ����ͼ��" << endl;
    cout << "2. �������" << endl;
    cout << "3. �����ܳ�" << endl;
    cout << "4. ��ʾ����ͼ��" << endl;
    cout << "5. ͼ��������" << endl;
    cout << "0. �˳�" << endl;
    cout << "=====================" << endl;
    cout << "��ѡ�����: ";
}
// ��ӡͼ��ѡ��˵�
void printGrapMenu()
{
    cout << "\n====ѡ��ͼ������====" << endl;
    cout << "1. Բ��" << endl;
    cout << "2. ��Բ" << endl;
    cout << "3. ����" << endl;
    cout << "4. ������" << endl;
    cout << "=================" << endl;
    cout << "��ѡ��: ";
}

int main() {
    vector<unique_ptr<Shape>> shapes;
    while (true) {
        int choice;
        printMenu();
        cin >> choice;
        if (choice == 0)
            break;
        try {
            switch (choice) {
                case 1: { // ����ͼ��
                    int type;
                    printGrapMenu();
                    cin >> type;

                    if (type < 1 || type > 4) {
                        cout << "��Чѡ��!" << endl;
                        break;
                    }

                    cout << "�������: ";
                    if (type == 1) { // Բ��
                        double r;
                        cin >> r;
                        shapes.push_back(make_unique<Circle>(r));
                    } else if (type == 2) { // ��Բ
                        double a, b;
                        cin >> a >> b;
                        shapes.push_back(make_unique<Ellipse>(a, b));
                    } else if (type == 3) { // ����
                        double w, h;
                        cin >> w >> h;
                        shapes.push_back(make_unique<Rectangle>(w, h));
                    } else if (type == 4) { // ������
                        double s1, s2, s3;
                        cin >> s1 >> s2 >> s3;
                        shapes.push_back(make_unique<Triangle>(s1, s2, s3));
                    }
                    cout << "ͼ�δ����ɹ�!" << endl;
                    break;
                }

                case 2: { // �������
                    if (shapes.empty()) {
                        cout << "û�п��õ�ͼ��!" << endl;
                        break;
                    }

                    cout << "ѡ��ͼ��(0-" << shapes.size()-1 << "): ";
                    int index;
                    cin >> index;

                    if (index < 0 || index >= static_cast<int>(shapes.size())) {
                        cout << "��Ч����!" << endl;
                        break;
                    }

                    double a = shapes[index]->area();
                    cout << "���: " << a << endl;
                    logToFile(shapes[index]->getType() + "�������", a);
                    break;
                }

                case 3: { // �����ܳ�
                    if (shapes.empty()) {
                        cout << "û�п��õ�ͼ��!" << endl;
                        break;
                    }

                    cout << "ѡ��ͼ��(0-" << shapes.size()-1 << "): ";
                    int index;
                    cin >> index;

                    if (index < 0 || index >= static_cast<int>(shapes.size())) {
                        cout << "��Ч����!" << endl;
                        break;
                    }

                    double p = shapes[index]->perimeter();
                    cout << "�ܳ�: " << p << endl;
                    logToFile(shapes[index]->getType() + "�ܳ�����", p);
                    break;
                }

                case 4: { // ��ʾ����ͼ��
                    if (shapes.empty()) {
                        cout << "û�п��õ�ͼ��!" << endl;
                        break;
                    }

                    cout << "\n����ͼ��:" << endl;
                    for (size_t i = 0; i < shapes.size(); ++i) {
                        cout << i << ": " << *shapes[i] << endl;
                    }
                    break;
                }

                case 5: { // ������
                    if (shapes.size() < 2) {
                        cout << "������Ҫ����ͼ��!" << endl;
                        break;
                    }

                    cout << "ѡ���һ��ͼ��(0-" << shapes.size()-1 << "): ";
                    int idx1;
                    cin >> idx1;

                    cout << "ѡ��ڶ���ͼ��(0-" << shapes.size()-1 << "): ";
                    int idx2;
                    cin >> idx2;

                    if (idx1 < 0 || idx1 >= static_cast<int>(shapes.size()) ||
                        idx2 < 0 || idx2 >= static_cast<int>(shapes.size())) {
                        cout << "��Ч����!" << endl;
                        break;
                    }

                    double sum = *shapes[idx1] + *shapes[idx2];
                    cout << "����ܺ�: " << sum << endl;
                    logToFile("�����Ӳ���", sum);
                    break;
                }

                default:
                    cout << "��Чѡ��!" << endl;
            }
        } catch (const exception& e) {
            cout << "����: " << e.what() << endl;
        }
    }

    cout << "�������˳�" << endl;
    return 0;
}