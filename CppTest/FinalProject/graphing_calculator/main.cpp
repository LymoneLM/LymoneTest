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

// 日志记录函数
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

// 图形基类
class Shape {
public:
    virtual double area() const = 0;
    virtual double perimeter() const = 0;
    virtual void print(ostream& os) const = 0;
    virtual string getType() const = 0;
    virtual ~Shape() = default;
};

// 重载<<运算符用于输出图形信息
ostream& operator<<(ostream& os, const Shape& shape) {
    shape.print(os);
    return os;
}

// 重载+运算符用于面积相加
double operator+(const Shape& a, const Shape& b) {
    return a.area() + b.area();
}

// 圆形类
class Circle : public Shape {
    double radius;
public:
    Circle(double r) : radius(r) {
        if (r <= 0) throw invalid_argument("半径必须大于0");
    }

    double area() const override {
        return M_PI * radius * radius;
    }

    double perimeter() const override {
        return 2 * M_PI * radius;
    }

    void print(ostream& os) const override {
        os << "圆形 (半径=" << radius << ", 面积=" << area()
           << ", 周长=" << perimeter() << ")";
    }

    string getType() const override {
        return "圆形";
    }
};

// 椭圆类
class Ellipse : public Shape {
    double semiMajor;
    double semiMinor;
public:
    Ellipse(double a, double b) : semiMajor(a), semiMinor(b) {
        if (a <= 0 || b <= 0) throw invalid_argument("半轴长度必须大于0");
    }

    double area() const override {
        return M_PI * semiMajor * semiMinor;
    }

    double perimeter() const override {
        // 使用拉马努金近似公式
        double h = pow((semiMajor - semiMinor), 2) / pow((semiMajor + semiMinor), 2);
        return M_PI * (semiMajor + semiMinor) * (1 + (3*h)/(10 + sqrt(4 - 3*h)));
    }

    void print(ostream& os) const override {
        os << "椭圆 (长半轴=" << semiMajor << ", 短半轴=" << semiMinor
           << ", 面积=" << area() << ", 周长≈" << perimeter() << ")";
    }

    string getType() const override {
        return "椭圆";
    }
};

// 矩形类
class Rectangle : public Shape {
    double width;
    double height;
public:
    Rectangle(double w, double h) : width(w), height(h) {
        if (w <= 0 || h <= 0) throw invalid_argument("宽高必须大于0");
    }

    double area() const override {
        return width * height;
    }

    double perimeter() const override {
        return 2 * (width + height);
    }

    void print(ostream& os) const override {
        os << "矩形 (宽=" << width << ", 高=" << height
           << ", 面积=" << area() << ", 周长=" << perimeter() << ")";
    }

    string getType() const override {
        return "矩形";
    }
};

// 三角形类
class Triangle : public Shape {
    double a, b, c;
public:
    Triangle(double s1, double s2, double s3) : a(s1), b(s2), c(s3) {
        if (s1 <= 0 || s2 <= 0 || s3 <= 0)
            throw invalid_argument("边长必须大于0");
        if (s1+s2 <= s3 || s1+s3 <= s2 || s2+s3 <= s1)
            throw invalid_argument("边长无法构成三角形");
    }

    double area() const override {
        // 海伦公式
        double s = perimeter() / 2;
        return sqrt(s * (s - a) * (s - b) * (s - c));
    }

    double perimeter() const override {
        return a + b + c;
    }

    void print(ostream& os) const override {
        os << "三角形 (边=" << a << "," << b << "," << c
           << ", 面积=" << area() << ", 周长=" << perimeter() << ")";
    }

    string getType() const override {
        return "三角形";
    }
};

// 打印主菜单
void printMenu(){
    cout << "\n=====图形计算器菜单=====" << endl;
    cout << "1. 创建图形" << endl;
    cout << "2. 计算面积" << endl;
    cout << "3. 计算周长" << endl;
    cout << "4. 显示所有图形" << endl;
    cout << "5. 图形面积相加" << endl;
    cout << "0. 退出" << endl;
    cout << "=====================" << endl;
    cout << "请选择操作: ";
}
// 打印图形选择菜单
void printGrapMenu()
{
    cout << "\n====选择图形类型====" << endl;
    cout << "1. 圆形" << endl;
    cout << "2. 椭圆" << endl;
    cout << "3. 矩形" << endl;
    cout << "4. 三角形" << endl;
    cout << "=================" << endl;
    cout << "请选择: ";
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
                case 1: { // 创建图形
                    int type;
                    printGrapMenu();
                    cin >> type;

                    if (type < 1 || type > 4) {
                        cout << "无效选择!" << endl;
                        break;
                    }

                    cout << "输入参数: ";
                    if (type == 1) { // 圆形
                        double r;
                        cin >> r;
                        shapes.push_back(make_unique<Circle>(r));
                    } else if (type == 2) { // 椭圆
                        double a, b;
                        cin >> a >> b;
                        shapes.push_back(make_unique<Ellipse>(a, b));
                    } else if (type == 3) { // 矩形
                        double w, h;
                        cin >> w >> h;
                        shapes.push_back(make_unique<Rectangle>(w, h));
                    } else if (type == 4) { // 三角形
                        double s1, s2, s3;
                        cin >> s1 >> s2 >> s3;
                        shapes.push_back(make_unique<Triangle>(s1, s2, s3));
                    }
                    cout << "图形创建成功!" << endl;
                    break;
                }

                case 2: { // 计算面积
                    if (shapes.empty()) {
                        cout << "没有可用的图形!" << endl;
                        break;
                    }

                    cout << "选择图形(0-" << shapes.size()-1 << "): ";
                    int index;
                    cin >> index;

                    if (index < 0 || index >= static_cast<int>(shapes.size())) {
                        cout << "无效索引!" << endl;
                        break;
                    }

                    double a = shapes[index]->area();
                    cout << "面积: " << a << endl;
                    logToFile(shapes[index]->getType() + "面积计算", a);
                    break;
                }

                case 3: { // 计算周长
                    if (shapes.empty()) {
                        cout << "没有可用的图形!" << endl;
                        break;
                    }

                    cout << "选择图形(0-" << shapes.size()-1 << "): ";
                    int index;
                    cin >> index;

                    if (index < 0 || index >= static_cast<int>(shapes.size())) {
                        cout << "无效索引!" << endl;
                        break;
                    }

                    double p = shapes[index]->perimeter();
                    cout << "周长: " << p << endl;
                    logToFile(shapes[index]->getType() + "周长计算", p);
                    break;
                }

                case 4: { // 显示所有图形
                    if (shapes.empty()) {
                        cout << "没有可用的图形!" << endl;
                        break;
                    }

                    cout << "\n所有图形:" << endl;
                    for (size_t i = 0; i < shapes.size(); ++i) {
                        cout << i << ": " << *shapes[i] << endl;
                    }
                    break;
                }

                case 5: { // 面积相加
                    if (shapes.size() < 2) {
                        cout << "至少需要两个图形!" << endl;
                        break;
                    }

                    cout << "选择第一个图形(0-" << shapes.size()-1 << "): ";
                    int idx1;
                    cin >> idx1;

                    cout << "选择第二个图形(0-" << shapes.size()-1 << "): ";
                    int idx2;
                    cin >> idx2;

                    if (idx1 < 0 || idx1 >= static_cast<int>(shapes.size()) ||
                        idx2 < 0 || idx2 >= static_cast<int>(shapes.size())) {
                        cout << "无效索引!" << endl;
                        break;
                    }

                    double sum = *shapes[idx1] + *shapes[idx2];
                    cout << "面积总和: " << sum << endl;
                    logToFile("面积相加操作", sum);
                    break;
                }

                default:
                    cout << "无效选择!" << endl;
            }
        } catch (const exception& e) {
            cout << "错误: " << e.what() << endl;
        }
    }

    cout << "程序已退出" << endl;
    return 0;
}