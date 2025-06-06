#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <ctime>

// 日期类
class RiQi {
private:
    int nian, yue, ri;
    static int ceshi;  // 静态变量用于存储测试日期
public:
    RiQi(int n = 0, int y = 0, int r = 0) : nian(n), yue(y), ri(r) {}

    // 重载+运算符（计算归还日期）
    RiQi operator+(int days) const {
        RiQi result = *this;
        result.ri += days;
        while (result.ri > 30) {
            result.ri -= 30;
            result.yue++;
            if (result.yue > 12) {
                result.yue = 1;
                result.nian++;
            }
        }
        return result;
    }

    // 重载>运算符（比较日期）
    bool operator>(const RiQi& other) const {
        if (nian != other.nian) return nian > other.nian;
        if (yue != other.yue) return yue > other.yue;
        return ri > other.ri;
    }

    // 计算日期差（用于罚款）
    int operator-(const RiQi& other) const {
        int a = (nian * 360) + (yue * 30) + ri;
        int b = (other.nian * 360) + (other.yue * 30) + other.ri;
        return a - b;
    }

    void xianshi() const {
        std::cout << nian << "-" << yue << "-" << ri;
    }

    static RiQi dangqianRiQi() {
        std::time_t t = std::time(0);
        std::tm* now = std::localtime(&t);
        return RiQi(now->tm_year + 1900, now->tm_mon + 1, now->tm_mday) + ceshi;
    }

    // 测试功能
    static void tianjiaDays(int days) {
        ceshi = ceshi + days;
    }

    // 重置测试日期
    static void chongzhiCeshi() {
        ceshi = 0;
    }
};
int RiQi::ceshi = 0;

// 图书馆物品基类
class TushuguanItem {
protected:
    std::string biaoti;
    std::string zuozhe;
    std::string ISBN;
    bool jieyueZhuangtai;
    RiQi jiechuRiqi;
    RiQi yingguihuanRiqi;
public:
    TushuguanItem(const std::string& bt, const std::string& zz, const std::string& isbn)
        : biaoti(bt), zuozhe(zz), ISBN(isbn), jieyueZhuangtai(false) {}

    virtual ~TushuguanItem() {}

    // 多态方法：获取借阅期限
    virtual int getJieyueQixian() const = 0;

    // 多态方法：计算罚款
    virtual double jisuanFakuan(int chaoguoDays) const {
        return chaoguoDays * 0.5; // 默认每天0.5元
    }

    void jieyue(const RiQi& jiechu) {
        jieyueZhuangtai = true;
        jiechuRiqi = jiechu;
        yingguihuanRiqi = jiechu + getJieyueQixian();
    }

    double guihuan(const RiQi& guihuanRiqi) {
        if (!jieyueZhuangtai) return 0.0;

        jieyueZhuangtai = false;
        if (guihuanRiqi > yingguihuanRiqi) {
            int chaoguoDays = guihuanRiqi - yingguihuanRiqi;
            return jisuanFakuan(chaoguoDays);
        }
        return 0.0;
    }

    void xujie() {
        if (jieyueZhuangtai) {
            yingguihuanRiqi = yingguihuanRiqi + getJieyueQixian();
        }
    }

    const std::string& getBiaoti() const { return biaoti; }
    const std::string& getZuozhe() const { return zuozhe; }
    const std::string& getISBN() const { return ISBN; }
    bool getJieyueZhuangtai() const { return jieyueZhuangtai; }
    void xianshiXinxi() const {
        std::cout << "标题: " << biaoti << " | 作者: " << zuozhe
                  << " | ISBN: " << ISBN << " | 状态: ";
        if (jieyueZhuangtai) {
            std::cout << "已借出 (应还日期: ";
            yingguihuanRiqi.xianshi();
            std::cout << ")";
        } else {
            std::cout << "可借阅";
        }
    }
};

// 图书类
class Shu : public TushuguanItem {
public:
    Shu(const std::string& bt, const std::string& zz, const std::string& isbn)
        : TushuguanItem(bt, zz, isbn) {}

    int getJieyueQixian() const override { return 30; } // 30天借期
};

// 期刊类
class Qikan : public TushuguanItem {
public:
    Qikan(const std::string& bt, const std::string& zz, const std::string& isbn)
        : TushuguanItem(bt, zz, isbn) {}

    int getJieyueQixian() const override { return 14; } // 14天借期
    double jisuanFakuan(int a) const override {
        return a * 1.0; // 期刊逾期每天1元
    }
};

// 论文类
class Lunwen : public TushuguanItem {
public:
    Lunwen(const std::string& bt, const std::string& zz, const std::string& isbn)
        : TushuguanItem(bt, zz, isbn) {}

    int getJieyueQixian() const override { return 7; } // 7天借期
    double jisuanFakuan(int b) const override {
        return b * 2.0; // 论文逾期每天2元
    }
};

// 图书馆管理系统
class Tushuguan {
private:
    std::vector<TushuguanItem*> wupin;

public:
    ~Tushuguan() {
        for (auto c : wupin) delete c;
    }

    void tianjia(TushuguanItem* a) {
        wupin.push_back(a);
    }

    bool shanchu(const std::string& d) {
        auto it = std::remove_if(wupin.begin(), wupin.end(),
            [&](TushuguanItem* e) {
                if (e->getISBN() == d) {
                    delete e;
                    return true;
                }
                return false;
            });

        if (it != wupin.end()) {
            wupin.erase(it, wupin.end());
            return true;
        }
        return false;
    }

    void jieyueItem(const std::string& f, const RiQi& g) {
        for (auto h : wupin) {
            if (h->getISBN() == f && !h->getJieyueZhuangtai()) {
                h->jieyue(g);
                return;
            }
        }
    }

    double guihuanItem(const std::string& i, const RiQi& j) {
        for (auto k : wupin) {
            if (k->getISBN() == i && k->getJieyueZhuangtai()) {
                return k->guihuan(j);
            }
        }
        return -1; // 未找到
    }

    void xujieItem(const std::string& l) {
        for (auto m : wupin) {
            if (m->getISBN() == l && m->getJieyueZhuangtai()) {
                m->xujie();
                return;
            }
        }
    }

    void chaxun(const std::string& n) const {
        for (auto o : wupin) {
            if (o->getBiaoti().find(n) != std::string::npos ||
                o->getZuozhe().find(n) != std::string::npos ||
                o->getISBN() == n) {
                o->xianshiXinxi();
                std::cout << std::endl;
            }
        }
    }

    void xianshiAll() const {
        for (auto p : wupin) {
            p->xianshiXinxi();
            std::cout << std::endl;
        }
    }
};

// 用户界面
void showMenu() {
    std::cout << "\n===== 图书馆管理系统 =====";
    std::cout << "\n1. 添加图书";
    std::cout << "\n2. 删除图书";
    std::cout << "\n3. 借阅图书";
    std::cout << "\n4. 归还图书";
    std::cout << "\n5. 续借图书";
    std::cout << "\n6. 查询图书";
    std::cout << "\n7. 展示所有图书";
    std::cout << "\n8. 增加天数（测试）";
    std::cout << "\n9. 重置日期（测试）";
    std::cout << "\n0. 退出系统";
    std::cout << "\n========================";
    std::cout << "\n请选择操作: ";
}

int main() {
    Tushuguan library;
    int choice;

    // 添加示例数据
    library.tianjia(new Shu("C++ Primer", "Stanley Lippman", "978711548"));
    library.tianjia(new Qikan("Science Journal", "Nature", "SCI2023"));
    library.tianjia(new Lunwen("Deep Learning", "Yann LeCun", "AI2024"));

    do {
        showMenu();
        std::cin >> choice;
        std::cin.ignore();

        std::string a, b, c;
        RiQi d;

        switch (choice) {
            case 1: {
                int type;
                std::cout << "选择类型 (1.图书 2.期刊 3.论文): ";
                std::cin >> type;
                std::cin.ignore();

                std::cout << "输入标题: ";
                std::getline(std::cin, a);
                std::cout << "输入作者: ";
                std::getline(std::cin, b);
                std::cout << "输入ISBN: ";
                std::getline(std::cin, c);

                if (type == 1) library.tianjia(new Shu(a, b, c));
                else if (type == 2) library.tianjia(new Qikan(a, b, c));
                else if (type == 3) library.tianjia(new Lunwen(a, b, c));
                std::cout << "添加成功!\n";
                break;
            }
            case 2:
                std::cout << "输入要删除的ISBN: ";
                std::getline(std::cin, a);
                if (library.shanchu(a)) {
                    std::cout << "删除成功!\n";
                } else {
                    std::cout << "未找到该图书!\n";
                }
                break;
            case 3:
                std::cout << "输入要借阅的ISBN: ";
                std::getline(std::cin, a);
                d = RiQi::dangqianRiQi();
                library.jieyueItem(a, d);
                std::cout << "借阅成功! 借出日期: ";
                d.xianshi();
                std::cout << std::endl;
                break;
            case 4:
                std::cout << "输入要归还的ISBN: ";
                std::getline(std::cin, a);
                d = RiQi::dangqianRiQi();
                double fakuan;
                fakuan = library.guihuanItem(a, d);
                if (fakuan >= 0) {
                    if (fakuan > 0) {
                        std::cout << "归还成功! 逾期罚款: " << fakuan << "元\n";
                    } else {
                        std::cout << "归还成功! 无逾期\n";
                    }
                } else {
                    std::cout << "未找到该图书或未借出!\n";
                }
                break;
            case 5:
                std::cout << "输入要续借的ISBN: ";
                std::getline(std::cin, a);
                library.xujieItem(a);
                std::cout << "续借成功!\n";
                break;
            case 6:
                std::cout << "输入查询内容(书名/作者/ISBN): ";
                std::getline(std::cin, a);
                library.chaxun(a);
                break;
            case 7:
                library.xianshiAll();
                break;
            case 8:
                int days;
                std::cout << "输入要增加的天数: ";
                std::cin >> days;
                RiQi::tianjiaDays(days);
                std::cout << "当前日期已设置为: ";
                RiQi::dangqianRiQi().xianshi();
                std::cout << std::endl;
                break;
            case 9:
                RiQi::chongzhiCeshi();
                std::cout << "已重置为真实日期: ";
                RiQi::dangqianRiQi().xianshi();
                std::cout << std::endl;
                break;
            case 0:
                std::cout << "感谢使用，再见!\n";
                break;
            default:
                std::cout << "无效选择，请重新输入!\n";
        }
    } while (choice != 0);

    return 0;
}