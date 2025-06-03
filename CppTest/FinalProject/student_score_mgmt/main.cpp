#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <map>
#include <iomanip>
#include <memory>
#include <cctype> // 添加头文件用于大小写转换

using namespace std;

// 定义测试开关
#define TEST_MODE 1

// 基类：成绩成员
class ChengJiMember {
protected:
    string xingming;
    string xuehao;
public:
    ChengJiMember(const string& name, const string& id)
        : xingming(name), xuehao(id) {}
    virtual ~ChengJiMember() = default;

    virtual void xianshi(const vector<string>& kemu) const = 0;
    virtual double getKemuScore(const string& kemu) const = 0;
    virtual void xiugaiScore(const string& kemu, double score) = 0;

    // 添加科目和删除科目方法
    virtual void addSubject(const string& kemu) = 0;
    virtual void removeSubject(const string& kemu) = 0;

    string getName() const { return xingming; }
    string getID() const { return xuehao; }

    // 运算符重载：按学号排序
    bool operator<(const ChengJiMember& other) const {
        return xuehao < other.xuehao;
    }
};

// 普通学生类
class PuTongStudent : public ChengJiMember {
private:
    map<string, double> chengji; // 科目-成绩映射
public:
    PuTongStudent(const string& name, const string& id)
        : ChengJiMember(name, id) {}

    void xianshi(const vector<string>& kemu) const override {
        cout << left << setw(10) << xuehao << setw(10) << xingming;
        for (const auto& k : kemu) {
            auto it = chengji.find(k);
            if (it != chengji.end()) {
                cout << setw(10) << it->second;
            } else {
                cout << setw(10) << "0";
            }
        }
        cout << "[普通生]" << endl;
    }

    double getKemuScore(const string& kemu) const override {
        auto it = chengji.find(kemu);
        return (it != chengji.end()) ? it->second : 0.0;
    }

    void xiugaiScore(const string& kemu, double score) override {
        chengji[kemu] = score;
    }

    // 添加科目
    void addSubject(const string& kemu) override {
        if (chengji.find(kemu) == chengji.end()) {
            chengji[kemu] = 0.0;
        }
    }

    // 删除科目
    void removeSubject(const string& kemu) override {
        chengji.erase(kemu);
    }
};

// 旁听学生类
class PangTingStudent : public ChengJiMember {
private:
    map<string, double> chengji;
public:
    PangTingStudent(const string& name, const string& id)
        : ChengJiMember(name, id) {}

    void xianshi(const vector<string>& kemu) const override {
        cout << left << setw(10) << xuehao << setw(10) << xingming;
        for (const auto& k : kemu) {
            auto it = chengji.find(k);
            if (it != chengji.end()) {
                cout << setw(10) << it->second;
            } else {
                cout << setw(10) << "0";
            }
        }
        cout << "[旁听生]" << endl;
    }

    double getKemuScore(const string& kemu) const override {
        auto it = chengji.find(kemu);
        return (it != chengji.end()) ? it->second : 0.0;
    }

    void xiugaiScore(const string& kemu, double score) override {
        chengji[kemu] = score;
    }

    void addSubject(const string& kemu) override {
        if (chengji.find(kemu) == chengji.end()) {
            chengji[kemu] = 0.0;
        }
    }

    void removeSubject(const string& kemu) override {
        chengji.erase(kemu);
    }
};

// 成绩管理系统
class ChengJiGuanLi {
private:
    vector<unique_ptr<ChengJiMember>> xueshengList; // 学生列表
    vector<string> kemuList; // 科目列表

public:
    // 添加学生
    void addStudent(bool isPutong, const string& name, const string& id) {
        if (isPutong) {
            xueshengList.push_back(make_unique<PuTongStudent>(name, id));
        } else {
            xueshengList.push_back(make_unique<PangTingStudent>(name, id));
        }
        // 为新学生初始化所有科目
        for (const auto& kemu : kemuList) {
            xueshengList.back()->addSubject(kemu);
        }
    }

    // 删除学生
    bool delStudent(const string& id) {
        auto it = find_if(xueshengList.begin(), xueshengList.end(),
            [&](const unique_ptr<ChengJiMember>& s) {
                return s->getID() == id;
            });

        if (it != xueshengList.end()) {
            xueshengList.erase(it);
            return true;
        }
        return false;
    }

    // 查询学生
    ChengJiMember* findStudent(const string& key) {
        for (auto& s : xueshengList) {
            if (s->getID() == key || s->getName() == key) {
                return s.get();
            }
        }
        return nullptr;
    }

    // 添加科目
    void addSubject(const string& kemu) {
        if (find(kemuList.begin(), kemuList.end(), kemu) == kemuList.end()) {
            kemuList.push_back(kemu);
            // 为所有学生添加新科目
            for (auto& s : xueshengList) {
                s->addSubject(kemu);
            }
        }
    }

    // 删除科目
    void delSubject(const string& kemu) {
        auto it = find(kemuList.begin(), kemuList.end(), kemu);
        if (it != kemuList.end()) {
            kemuList.erase(it);
            // 从所有学生中删除该科目
            for (auto& s : xueshengList) {
                s->removeSubject(kemu);
            }
        }
    }

    // 修改成绩
    void modScore(const string& stuKey, const string& kemu, double score) {
        auto stu = findStudent(stuKey);
        if (stu) {
            // 检查科目是否存在
            if (find(kemuList.begin(), kemuList.end(), kemu) != kemuList.end()) {
                stu->xiugaiScore(kemu, score);
                cout << "成绩修改成功!\n";
            } else {
                cout << "错误: 科目不存在!\n";
            }
        } else {
            cout << "错误: 学生不存在!\n";
        }
    }

    // 展示表单
    void display(bool byID = true, const string& sortKemu = "") {
    if (xueshengList.empty()) {
        cout << "\n表单为空!\n";
        return;
    }

    // 复制指针用于排序
    vector<ChengJiMember*> tempList;
    for (auto& s : xueshengList) {
        tempList.push_back(s.get());
    }

    // 排序逻辑
    if (!byID && !sortKemu.empty()) {
        sort(tempList.begin(), tempList.end(),
            [&](ChengJiMember* a, ChengJiMember* b) {
                return a->getKemuScore(sortKemu) > b->getKemuScore(sortKemu);
            });
    } else {
        sort(tempList.begin(), tempList.end(),
            [](ChengJiMember* a, ChengJiMember* b) {
                return *a < *b;
            });
    }

    // 计算最大宽度
    int idWidth = 10, nameWidth = 10;
    for (auto s : tempList) {
        if (s->getID().length() > idWidth) idWidth = s->getID().length() + 2;
        if (s->getName().length() > nameWidth) nameWidth = s->getName().length() + 2;
    }
    idWidth = max(idWidth, 6);
    nameWidth = max(nameWidth, 6);

    // 打印表头
    cout << "\n" << left
         << setw(idWidth) << "学号"
         << setw(nameWidth) << "姓名";

    for (const auto& k : kemuList) {
        cout << setw(12) << k;
    }
    cout << "类型" << endl;

    // 打印分隔线
    int totalWidth = idWidth + nameWidth + kemuList.size()*12 + 10;
    cout << string(totalWidth, '-') << endl;

    // 打印学生数据
    for (auto s : tempList) {
        cout << left
             << setw(idWidth) << s->getID()
             << setw(nameWidth) << s->getName();

        for (const auto& k : kemuList) {
            double score = s->getKemuScore(k);
            if (score == static_cast<int>(score)) {
                cout << setw(12) << static_cast<int>(score);
            } else {
                cout << setw(12) << fixed << setprecision(1) << score;
            }
        }

        // 动态显示学生类型
        if (dynamic_cast<PuTongStudent*>(s)) {
            cout << "[普通生]";
        } else if (dynamic_cast<PangTingStudent*>(s)) {
            cout << "[旁听生]";
        }
        cout << endl;
    }

    // 计算平均分
    if (!kemuList.empty()) {
        cout << "\n" << setw(idWidth) << "平均分:"
             << setw(nameWidth) << " ";

        for (const auto& k : kemuList) {
            double sum = 0;
            for (auto s : tempList) {
                sum += s->getKemuScore(k);
            }
            double avg = sum / tempList.size();

            if (avg == static_cast<int>(avg)) {
                cout << setw(12) << static_cast<int>(avg);
            } else {
                cout << setw(12) << fixed << setprecision(2) << avg;
            }
        }
        cout << endl;
    }
    cout << endl;
}

    // 生成测试数据
    void generateTestData() {
        addSubject("语文");
        addSubject("数学");
        addSubject("英语");

        addStudent(true, "张三", "2023001");
        modScore("2023001", "语文", 85.5);
        modScore("2023001", "数学", 92.0);
        modScore("2023001", "英语", 78.5);

        addStudent(true, "李四", "2023002");
        modScore("2023002", "语文", 76.0);
        modScore("2023002", "数学", 88.5);
        modScore("2023002", "英语", 92.5);

        addStudent(false, "王五", "2023003");
        modScore("2023003", "语文", 92.5);
        modScore("2023003", "数学", 65.0);
        modScore("2023003", "英语", 85.0);
    }
};

// 用户交互菜单
void userMenu() {
    ChengJiGuanLi manager;

#if TEST_MODE
    manager.generateTestData();
    cout << "已加载测试数据\n";
#endif

    while (true) {
        cout << "\n===== 学生成绩管理系统 =====";
        cout << "\n1. 插入学生";
        cout << "\n2. 删除学生";
        cout << "\n3. 查询学生";
        cout << "\n4. 修改成绩";
        cout << "\n5. 展示表单";
        cout << "\n6. 添加科目";
        cout << "\n7. 删除科目";
        cout << "\n0. 退出系统";
        cout << "\n=========================";
        cout << "\n请选择操作: ";

        int choice;
        cin >> choice;

        // 清除输入缓冲区
        cin.ignore();

        string name, id, kemu;
        double score;
        ChengJiMember* stu;

        switch (choice) {
            case 1: {
                cout << "学生类型 (1.普通 2.旁听): ";
                int type;
                cin >> type;
                cin.ignore(); // 清除换行符

                cout << "姓名: ";
                getline(cin, name);
                cout << "学号: ";
                getline(cin, id);

                manager.addStudent(type == 1, name, id);
                cout << "添加成功!\n";
                break;
            }
            case 2: {
                cout << "输入学号: ";
                getline(cin, id);
                if (manager.delStudent(id)) {
                    cout << "删除成功!\n";
                } else {
                    cout << "学号不存在!\n";
                }
                break;
            }
            case 3: {
                cout << "输入学号或姓名: ";
                getline(cin, id);
                stu = manager.findStudent(id);
                if (stu) {
                    cout << "找到学生: " << stu->getName()
                         << "(" << stu->getID() << ")\n";
                } else {
                    cout << "未找到学生!\n";
                }
                break;
            }
            case 4: {
                cout << "输入学号或姓名: ";
                getline(cin, id);
                cout << "输入科目: ";
                getline(cin, kemu);
                cout << "输入新成绩: ";
                cin >> score;
                cin.ignore(); // 清除换行符

                manager.modScore(id, kemu, score);
                break;
            }
            case 5: {
                cout << "排序方式 (1.学号 2.科目成绩): ";
                int sortType;
                cin >> sortType;
                cin.ignore(); // 清除换行符

                if (sortType == 2) {
                    cout << "输入排序科目: ";
                    getline(cin, kemu);
                    manager.display(false, kemu);
                } else {
                    manager.display();
                }
                break;
            }
            case 6: {
                cout << "输入新科目名称: ";
                getline(cin, kemu);
                manager.addSubject(kemu);
                cout << "添加成功!\n";
                break;
            }
            case 7: {
                cout << "输入删除科目名称: ";
                getline(cin, kemu);
                manager.delSubject(kemu);
                cout << "删除成功!\n";
                break;
            }
            case 0:
                cout << "系统已退出!\n";
                return;
            default:
                cout << "无效选择，请重新输入!\n";
        }
    }
}

int main() {
    userMenu();
    return 0;
}