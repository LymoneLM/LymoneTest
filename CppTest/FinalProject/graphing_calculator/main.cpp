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

// 日志函数
void writelog(const string& what, double num) {
    ofstream logfile("rilog.txt", ios::app);
    if (logfile) {
        time_t now = time(0);
        tm* timenow = localtime(&now);
        logfile << "[" << put_time(timenow, "%Y-%m-%d %H:%M:%S") << "] "
                << what << ": " << fixed << setprecision(2) << num << endl;
    }
}

// 图形基类
class ShapeBase {
public:
    virtual double mianji() const = 0;
    virtual double zhouchang() const = 0;
    virtual void showinfo(ostream& out) const = 0;
    virtual string leixing() const = 0;
    virtual ~ShapeBase() = default;
};

// 输出运算符重载
ostream& operator<<(ostream& out, const ShapeBase& s) {
    s.showinfo(out);
    return out;
}

// 加法运算符重载
double operator+(const ShapeBase& a, const ShapeBase& b) {
    return a.mianji() + b.mianji();
}

// 圆形类
class RoundShape : public ShapeBase {
    double banjing;  // 使用拼音变量名
public:
    RoundShape(double r) : banjing(r) {
        if (r <= 0) throw runtime_error("半径需>0");
    }

    double mianji() const override {
        return 3.1415926 * banjing * banjing;
    }

    double zhouchang() const override {
        return 2 * 3.1415926 * banjing;
    }

    void showinfo(ostream& out) const override {
        out << "圆形 (半径=" << banjing << ", 面积=" << mianji()
           << ", 周长=" << zhouchang() << ")";
    }

    string leixing() const override {
        return "圆形";
    }
};

// 椭圆类
class OvalShape : public ShapeBase {
    double changzhou;  // 长轴
    double duanzhou;   // 短轴
public:
    OvalShape(double a, double b) : changzhou(a), duanzhou(b) {
        if (a <= 0 || b <= 0) throw runtime_error("半轴需>0");
    }

    double mianji() const override {
        return 3.1415926 * changzhou * duanzhou;
    }

    double zhouchang() const override {
        double temp = pow((changzhou - duanzhou), 2) / pow((changzhou + duanzhou), 2);
        return 3.1415926 * (changzhou + duanzhou) * (1 + (3*temp)/(10 + sqrt(4 - 3*temp)));
    }

    void showinfo(ostream& out) const override {
        out << "椭圆 (长轴=" << changzhou << ", 短轴=" << duanzhou
           << ", 面积=" << mianji() << ", 周长≈" << zhouchang() << ")";
    }

    string leixing() const override {
        return "椭圆";
    }
};

// 矩形类
class RectShape : public ShapeBase {
    double kuan;   // 宽
    double gao;    // 高
public:
    RectShape(double w, double h) : kuan(w), gao(h) {
        if (w <= 0 || h <= 0) throw runtime_error("宽高需>0");
    }

    double mianji() const override {
        return kuan * gao;
    }

    double zhouchang() const override {
        return 2 * (kuan + gao);
    }

    void showinfo(ostream& out) const override {
        out << "矩形 (宽=" << kuan << ", 高=" << gao
           << ", 面积=" << mianji() << ", 周长=" << zhouchang() << ")";
    }

    string leixing() const override {
        return "矩形";
    }
};

// 三角形类
class TriShape : public ShapeBase {
    double bianA;  // 边A
    double bianB;  // 边B
    double bianC;  // 边C
public:
    TriShape(double a, double b, double c) : bianA(a), bianB(b), bianC(c) {
        if (a <= 0 || b <= 0 || c <= 0)
            throw runtime_error("边长需>0");
        if (a+b <= c || a+c <= b || b+c <= a)
            throw runtime_error("非三角形边长");
    }

    double mianji() const override {
        double s = (bianA + bianB + bianC) / 2;
        return sqrt(s * (s - bianA) * (s - bianB) * (s - bianC));
    }

    double zhouchang() const override {
        return bianA + bianB + bianC;
    }

    void showinfo(ostream& out) const override {
        out << "三角形 (边=" << bianA << "," << bianB << "," << bianC
           << ", 面积=" << mianji() << ", 周长=" << zhouchang() << ")";
    }

    string leixing() const override {
        return "三角形";
    }
};

// 显示主菜单
void showmenu(){
    cout << "\n=====图形计算器=====" << endl;
    cout << "1. 创建图形" << endl;
    cout << "2. 计算面积" << endl;
    cout << "3. 计算周长" << endl;
    cout << "4. 显示所有图形" << endl;
    cout << "5. 面积相加" << endl;
    cout << "0. 退出程序" << endl;
    cout << "==================" << endl;
    cout << "输入选择: ";
}

// 显示图形菜单
void showshapemenu(){
    cout << "\n====图形类型====" << endl;
    cout << "1. 圆形" << endl;
    cout << "2. 椭圆" << endl;
    cout << "3. 矩形" << endl;
    cout << "4. 三角形" << endl;
    cout << "===============" << endl;
    cout << "输入类型: ";
}

int main() {
    vector<unique_ptr<ShapeBase>> allshapes;

    while (true) {
        int choose;
        showmenu();
        cin >> choose;

        if (choose == 0) {
            cout << "程序结束" << endl;
            break;
        }

        try {
            switch (choose) {
                case 1: {  // 创建图形
                    int shapetype;
                    showshapemenu();
                    cin >> shapetype;

                    if (shapetype == 1) {  // 圆形
                        double r;
                        cout << "输入半径: ";
                        cin >> r;
                        allshapes.push_back(make_unique<RoundShape>(r));
                    }
                    else if (shapetype == 2) {  // 椭圆
                        double a, b;
                        cout << "输入长半轴: ";
                        cin >> a;
                        cout << "输入短半轴: ";
                        cin >> b;
                        allshapes.push_back(make_unique<OvalShape>(a, b));
                    }
                    else if (shapetype == 3) {  // 矩形
                        double w, h;
                        cout << "输入宽度: ";
                        cin >> w;
                        cout << "输入高度: ";
                        cin >> h;
                        allshapes.push_back(make_unique<RectShape>(w, h));
                    }
                    else if (shapetype == 4) {  // 三角形
                        double s1, s2, s3;
                        cout << "输入第一条边: ";
                        cin >> s1;
                        cout << "输入第二条边: ";
                        cin >> s2;
                        cout << "输入第三条边: ";
                        cin >> s3;
                        allshapes.push_back(make_unique<TriShape>(s1, s2, s3));
                    }
                    else {
                        cout << "无效类型!" << endl;
                        break;
                    }
                    cout << "图形已创建!" << endl;
                    break;
                }

                case 2: {  // 计算面积
                    if (allshapes.empty()) {
                        cout << "无图形数据!" << endl;
                        break;
                    }

                    cout << "选择图形(0-" << allshapes.size()-1 << "): ";
                    int idx;
                    cin >> idx;

                    if (idx < 0 || idx >= allshapes.size()) {
                        cout << "无效编号!" << endl;
                        break;
                    }

                    double mj = allshapes[idx]->mianji();
                    cout << "面积: " << mj << endl;
                    writelog(allshapes[idx]->leixing() + "面积计算", mj);
                    break;
                }

                case 3: {  // 计算周长
                    if (allshapes.empty()) {
                        cout << "无图形数据!" << endl;
                        break;
                    }

                    cout << "选择图形(0-" << allshapes.size()-1 << "): ";
                    int idx;
                    cin >> idx;

                    if (idx < 0 || idx >= allshapes.size()) {
                        cout << "无效编号!" << endl;
                        break;
                    }

                    double zc = allshapes[idx]->zhouchang();
                    cout << "周长: " << zc << endl;
                    writelog(allshapes[idx]->leixing() + "周长计算", zc);
                    break;
                }

                case 4: {  // 显示所有图形
                    if (allshapes.empty()) {
                        cout << "无图形数据!" << endl;
                        break;
                    }

                    cout << "\n图形列表:" << endl;
                    for (size_t i = 0; i < allshapes.size(); i++) {
                        cout << i << ": " << *allshapes[i] << endl;
                    }
                    break;
                }

                case 5: {  // 面积相加
                    if (allshapes.size() < 2) {
                        cout << "需至少两个图形!" << endl;
                        break;
                    }

                    cout << "选择第一个图形(0-" << allshapes.size()-1 << "): ";
                    int idx1;
                    cin >> idx1;

                    cout << "选择第二个图形(0-" << allshapes.size()-1 << "): ";
                    int idx2;
                    cin >> idx2;

                    if (idx1 < 0 || idx1 >= allshapes.size() ||
                        idx2 < 0 || idx2 >= allshapes.size()) {
                        cout << "无效编号!" << endl;
                        break;
                    }

                    double sum = *allshapes[idx1] + *allshapes[idx2];
                    cout << "面积总和: " << sum << endl;
                    writelog("面积相加操作", sum);
                    break;
                }

                default:
                    cout << "无效选择!" << endl;
            }
        }
        catch (const exception& e) {
            cout << "错误: " << e.what() << endl;
        }
    }

    return 0;
}