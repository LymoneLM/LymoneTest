#include <iostream>
#include <vector>
#include <algorithm>
#include <cctype>
#include <iomanip>
#include <memory>
#include <set>

using namespace std;

// 成员基类
class ChengYuan {
protected:
    string xuehao;      // 学号
    string mingzi;      // 名字
    string zhiwei;      // 职位
    int weidaoCount = 0; // 未到次数

public:
    ChengYuan(const string& xh, const string& mz, const string& zw)
        : xuehao(xh), mingzi(mz), zhiwei(zw) {}

    virtual ~ChengYuan() {}

    // 虚函数展示信息
    virtual void xianshi() const {
        cout << left << setw(12) << xuehao
             << setw(10) << mingzi
             << setw(10) << zhiwei
             << "缺席:" << weidaoCount << "次";
    }

    void addWeidao() {
        weidaoCount++;
    }

    string getXuehao() const { return xuehao; }

    string getMingzi() const { return mingzi; }

    void setXinxi(const string& mz, const string& zw) {
        mingzi = mz;
        zhiwei = zw;
    }

    virtual int getType() const = 0;
};

// 普通成员类
class PuTong : public ChengYuan {
public:
    PuTong(const string& xh, const string& mz)
        : ChengYuan(xh, mz, "普通成员") {}

    void xianshi() const override {
        cout << "[普通] ";
        ChengYuan::xianshi();
    }

    int getType() const override { return 1; }
};

// 干部成员类
class GanBu : public ChengYuan {
public:
    GanBu(const string& xh, const string& mz, const string& zw)
        : ChengYuan(xh, mz, zw) {}

    void xianshi() const override {
        cout << "[干部] ";
        ChengYuan::xianshi();
    }

    int getType() const override { return 2; }
};

// 社团管理类
class SheTuan {
private:
    vector<unique_ptr<ChengYuan>> chengyuanList;

public:
    // 重载 += 添加成员
    SheTuan& operator+=(unique_ptr<ChengYuan> cy) {
        chengyuanList.push_back(move(cy));
        return *this;
    }

    // 重载 -= 删除成员
    bool operator-=(const string& xh) {
        auto it = find_if(chengyuanList.begin(), chengyuanList.end(),
            [&](const unique_ptr<ChengYuan>& c) {
                return c->getXuehao() == xh;
            });

        if (it != chengyuanList.end()) {
            chengyuanList.erase(it);
            return true;
        }
        return false;
    }

    // 重载 << 输出所有成员
    friend ostream& operator<<(ostream& os, const SheTuan& st) {
        if (st.chengyuanList.empty()) {
            os << "暂无成员信息\n";
            return os;
        }

        // 排序：先按类型再按学号
        vector<ChengYuan*> temp;
        for (const auto& c : st.chengyuanList) {
            temp.push_back(c.get());
        }

        sort(temp.begin(), temp.end(), [](ChengYuan* a, ChengYuan* b) {
            if (a->getType() != b->getType())
                return a->getType() > b->getType();
            return a->getXuehao() < b->getXuehao();
        });

        os << "======== 社团成员列表 ========\n";
        for (const auto& c : temp) {
            c->xianshi();
            os << endl;
        }
        return os;
    }

    // 查找成员
    ChengYuan* find(const string& key) {
        for (auto& c : chengyuanList) {
            if (c->getXuehao() == key ||
                c->getMingzi().find(key) != string::npos) {
                return c.get();
            }
        }
        return nullptr;
    }

    // 检查学号是否存在
    bool xuehaoExists(const string& xh) {
        return any_of(chengyuanList.begin(), chengyuanList.end(),
            [&](const unique_ptr<ChengYuan>& c) {
                return c->getXuehao() == xh;
            });
    }

    // 获取所有成员
    vector<ChengYuan*> getAll() const {
        vector<ChengYuan*> result;
        for (const auto& c : chengyuanList) {
            result.push_back(c.get());
        }
        return result;
    }
};

// 活动签到管理
void huodongCheck(SheTuan& st) {
    set<string> qiandaoSet;
    string input;

    cout << "\n==== 活动签到 ====\n"
         << "输入学号签到 (exit结束)\n";

    while (true) {
        cout << "> ";
        cin >> input;
        if (input == "exit") break;

        ChengYuan* c = st.find(input);
        if (c) {
            qiandaoSet.insert(c->getXuehao());
            cout << c->getMingzi() << " 签到成功\n";
        } else {
            cout << "未找到成员，请重新输入\n";
        }
    }

    // 统计未到人员
    vector<ChengYuan*> weidaoList;
    for (auto c : st.getAll()) {
        if (qiandaoSet.find(c->getXuehao()) == qiandaoSet.end()) {
            weidaoList.push_back(c);
            c->addWeidao();
        }
    }

    // 排序：先类型后学号
    sort(weidaoList.begin(), weidaoList.end(),
        [](ChengYuan* a, ChengYuan* b) {
            if (a->getType() != b->getType())
                return a->getType() > b->getType();
            return a->getXuehao() < b->getXuehao();
        });

    // 显示未到人员
    if (weidaoList.empty()) {
        cout << "所有成员均已到场!\n";
    } else {
        cout << "\n==== 未到人员 ====\n";
        for (auto c : weidaoList) {
            c->xianshi();
            cout << endl;
        }
    }
}

// 显示主菜单
void showMenu() {
    cout << "\n==== 社团管理系统 ====\n"
         << "1. 新增成员\n"
         << "2. 删除成员\n"
         << "3. 查询成员\n"
         << "4. 修改成员\n"
         << "5. 展示所有成员\n"
         << "6. 活动签到\n"
         << "0. 退出\n"
         << "请选择: ";
}

// 新增成员
void addMember(SheTuan& st) {
    string xh, mz, zw;
    int type;

    cout << "输入学号: ";
    cin >> xh;
    if (st.xuehaoExists(xh)) {
        cout << "学号已存在!\n";
        return;
    }

    cout << "输入姓名: ";
    cin >> mz;

    cout << "选择类型 (1-普通成员 2-干部): ";
    cin >> type;

    if (type == 1) {
        st += make_unique<PuTong>(xh, mz);
    } else if (type == 2) {
        cout << "输入干部职位: ";
        cin >> zw;
        st += make_unique<GanBu>(xh, mz, zw);
    } else {
        cout << "无效类型!\n";
        return;
    }
    cout << "添加成功!\n";
}

// 查询成员
void searchMember(const SheTuan& st) {
    string key;
    cout << "输入学号或姓名: ";
    cin >> key;

    vector<ChengYuan*> result;
    for (auto c : st.getAll()) {
        if (c->getXuehao().find(key) != string::npos ||
            c->getMingzi().find(key) != string::npos) {
            result.push_back(c);
        }
    }

    if (result.empty()) {
        cout << "未找到匹配成员\n";
        return;
    }

    cout << "==== 查询结果 ====\n";
    for (auto c : result) {
        c->xianshi();
        cout << endl;
    }
}

// 修改成员
void modifyMember(SheTuan& st) {
    string xh;
    cout << "输入要修改的学号: ";
    cin >> xh;

    ChengYuan* c = st.find(xh);
    if (!c) {
        cout << "成员不存在\n";
        return;
    }

    string mz, zw;
    cout << "输入新姓名 (留空不修改): ";
    cin.ignore();
    getline(cin, mz);
    if (mz.empty()) mz = c->getMingzi();

    if (c->getType() == 2) {
        cout << "输入新职位 (留空不修改): ";
        getline(cin, zw);
        if (zw.empty()) zw = dynamic_cast<GanBu*>(c)->getMingzi();
    } else {
        zw = "普通成员";
    }

    c->setXinxi(mz, zw);
    cout << "修改成功!\n";
}

int main() {
    SheTuan shetuan;
    int choice;

    do {
        showMenu();
        cin >> choice;

        switch (choice) {
            case 1:
                addMember(shetuan);
                break;
            case 2: {
                string xh;
                cout << "输入要删除的学号: ";
                cin >> xh;
                if (shetuan -= xh) {
                    cout << "删除成功\n";
                } else {
                    cout << "成员不存在\n";
                }
                break;
            }
            case 3:
                searchMember(shetuan);
                break;
            case 4:
                modifyMember(shetuan);
                break;
            case 5:
                cout << shetuan;
                break;
            case 6:
                huodongCheck(shetuan);
                break;
            case 0:
                cout << "系统已退出\n";
                break;
            default:
                cout << "无效选择，请重新输入\n";
        }
    } while (choice != 0);

    return 0;
}