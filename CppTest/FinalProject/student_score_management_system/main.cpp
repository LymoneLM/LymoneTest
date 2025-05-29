#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <map>

using namespace std;

// 多态：虚拟基类
class DataItem {
public:
    virtual ~DataItem() = default;
    virtual void display() const = 0;
    virtual string toCSV() const = 0;
    virtual bool match(const string& keyword) const = 0;
};

// 学生成绩类
class Student : public DataItem {
private:
    string name;
    string id;
    map<string, double> scores;

public:
    Student(string n, string i) : name(n), id(i) {}

    // 运算符重载：比较学生ID（用于find）
    bool operator==(const Student& other) const {
        return id == other.id;
    }

    // 设置成绩
    void setScore(const string& subject, double score) {
        scores[subject] = score;
    }

    // 删除科目成绩
    void removeScore(const string& subject) {
        scores.erase(subject);
    }

    // 获取总分
    double getTotal() const {
        double total = 0.0;
        for (const auto& s : scores) {
            total += s.second;
        }
        return total;
    }

    // 获取指定科目成绩
    double getScore(const string& subject) const {
        auto it = scores.find(subject);
        return (it != scores.end()) ? it->second : -1.0;
    }

    // 显示学生信息
    void display() const override {
        cout << left << setw(15) << name << setw(15) << id;
        for (const auto& s : scores) {
            cout << setw(10) << s.first << ":" << setw(5) << s.second;
        }
        cout << "总分:" << setw(6) << getTotal() << endl;
    }

    // 转换为CSV格式
    string toCSV() const override {
        ostringstream oss;
        oss << name << "," << id;
        for (const auto& s : scores) {
            oss << "," << s.second;
        }
        return oss.str();
    }

    // 匹配查询
    bool match(const string& keyword) const override {
        return name.find(keyword) != string::npos || id.find(keyword) != string::npos;
    }

    const string& getName() const { return name; }
    const string& getId() const { return id; }
    const map<string, double>& getScores() const { return scores; }
};

// 表单管理类
class GradeForm {
private:
    string formName;
    vector<Student> students;
    vector<string> subjects;

public:
    GradeForm(string name) : formName(name) {
        subjects = {};
    }

    // 添加学生
    void addStudent(const Student& student) {
        // 检查学号是否重复
        auto it = find(students.begin(), students.end(), student);
        if (it != students.end()) {
            cout << "错误：学号 " << student.getId() << " 已存在！" << endl;
            return;
        }
        students.push_back(student);
        cout << "学生 " << student.getName() << " 添加成功" << endl;
    }

    // 删除学生
    void removeStudent(const string& id) {
        auto it = find_if(students.begin(), students.end(),
                         [&](const Student& s) { return s.getId() == id; });

        if (it != students.end()) {
            cout << "删除学生: " << it->getName() << endl;
            students.erase(it);
        } else {
            cout << "未找到学号为 " << id << " 的学生" << endl;
        }
    }

    // 查询学生
    void queryStudent(const string& keyword) {
        bool found = false;
        for (const auto& s : students) {
            if (s.match(keyword)) {
                s.display();
                found = true;
            }
        }
        if (!found) {
            cout << "未找到匹配的学生" << endl;
        }
    }

    // 修改成绩
    void modifyScore(const string& id, const string& subject, double score) {
        for (auto& s : students) {
            if (s.getId() == id) {
                if (find(subjects.begin(), subjects.end(), subject) != subjects.end()) {
                    s.setScore(subject, score);
                    cout << "成功修改 " << s.getName() << " 的" << subject << "成绩为: " << score << endl;
                } else {
                    cout << "科目不存在，请先添加科目" << endl;
                }
                return;
            }
        }
        cout << "未找到学号为 " << id << " 的学生" << endl;
    }

    // 添加科目
    void addSubject(const string& subject) {
        if (find(subjects.begin(), subjects.end(), subject) != subjects.end()) {
            cout << "科目已存在！" << endl;
            return;
        }
        subjects.push_back(subject);
        // 所有学生添加新科目（初始0分）
        for (auto& s : students) {
            s.setScore(subject, 0.0);
        }
        cout << "已添加科目: " << subject << endl;
    }

    // 删除科目
    void removeSubject(const string& subject) {
        auto it = find(subjects.begin(), subjects.end(), subject);
        if (it != subjects.end()) {
            subjects.erase(it);
            // 删除所有学生该科目成绩
            for (auto& s : students) {
                s.removeScore(subject);
            }
            cout << "已删除科目: " << subject << endl;
        } else {
            cout << "科目不存在！" << endl;
        }
    }

    // 展示表单
    void display(bool showAverage = false) {
        // 显示表头
        cout << "\n表单: " << formName << endl;
        cout << left << setw(15) << "姓名" << setw(15) << "学号";
        for (const auto& sub : subjects) {
            cout << setw(15) << sub;
        }
        cout << setw(15) << "总分" << endl;
        cout << string(15*(subjects.size()+2), '-') << endl;

        // 显示学生数据
        for (const auto& s : students) {
            cout << left << setw(15) << s.getName() << setw(15) << s.getId();
            for (const auto& sub : subjects) {
                double score = s.getScore(sub);
                if (score >= 0) {
                    cout << setw(15) << score;
                } else {
                    cout << setw(15) << "N/A";
                }
            }
            cout << setw(15) << s.getTotal() << endl;
        }

        // 显示平均分
        if (showAverage && !students.empty()) {
            cout << string(15*(subjects.size()+2), '-') << endl;
            cout << left << setw(30) << "平均分"; // 独占姓名槽+学号槽长度
            for (const auto& sub : subjects) {
                double total = 0.0;
                int count = 0;
                for (const auto& s : students) {
                    double score = s.getScore(sub);
                    if (score >= 0) {
                        total += score;
                        count++;
                    }
                }
                double avg = (count > 0) ? total / count : 0.0;
                cout << setw(15) << fixed << setprecision(1) << avg;
            }
            cout << endl;
        }
    }

    // 排序展示
    void sortAndDisplay(const string& criteria, bool ascending = true) {
        if (criteria == "学号") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getId() < b.getId() : a.getId() > b.getId();
                });
        } else if (criteria == "姓名") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getName() < b.getName() : a.getName() > b.getName();
                });
        } else if (criteria == "总分") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getTotal() < b.getTotal() : a.getTotal() > b.getTotal();
                });
        } else {
            // 按科目排序
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    double scoreA = a.getScore(criteria);
                    double scoreB = b.getScore(criteria);
                    return ascending ? scoreA < scoreB : scoreA > scoreB;
                });
        }
        display(true);
    }

    // 保存到CSV
    void saveToCSV(const string& filename) {
        ofstream file(filename);
        if (!file.is_open()) {
            cerr << "无法打开文件: " << filename << endl;
            return;
        }

        // 表头
        file << "姓名,学号";
        for (const auto& sub : subjects) {
            file << "," << sub;
        }
        file << endl;

        // 数据
        for (const auto& s : students) {
            file << s.toCSV() << endl;
        }

        cout << "成功保存到 " << filename << endl;
        file.close();
    }

    // 从CSV加载
    void loadFromCSV(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            cerr << "无法打开文件: " << filename << endl;
            return;
        }

        students.clear();
        subjects.clear();

        string line;
        // 表头
        if (getline(file, line)) {
            stringstream ss(line);
            string cell;
            vector<string> headers;

            while (getline(ss, cell, ',')) {
                headers.push_back(cell);
            }

            // 前两列是姓名和学号，其余是科目
            if (headers.size() >= 2) {
                subjects = vector<string>(headers.begin() + 2, headers.end());
            }
        }

        // 数据
        while (getline(file, line)) {
            stringstream ss(line);
            string cell;
            vector<string> rowData;

            while (getline(ss, cell, ',')) {
                rowData.push_back(cell);
            }

            if (rowData.size() >= 2) {
                Student s(rowData[0], rowData[1]);
                for (int i = 0; i < subjects.size() && i + 2 < rowData.size(); i++) {
                    try {
                        double score = stod(rowData[i + 2]);
                        s.setScore(subjects[i], score);
                    } catch (...) {
                        // 转换失败时跳过
                    }
                }
                students.push_back(s);
            }
        }

        cout << "成功从 " << filename << " 加载 " << students.size() << " 条记录" << endl;
        file.close();
    }

    const string& getName() const { return formName; }
    const vector<string>& getSubjects() const { return subjects; }
};

// 成绩管理系统
class GradeSystem {
private:
    vector<GradeForm> forms;

    // 查找表单索引
    int findFormIndex(const string& name) {
        for (int i = 0; i < forms.size(); i++) {
            if (forms[i].getName() == name) {
                return i;
            }
        }
        return -1;
    }

public:
    // 创建新表单
    void createForm(const string& name) {
        if (findFormIndex(name) != -1) {
            cout << "表单已存在！" << endl;
            return;
        }
        forms.emplace_back(name);
        cout << "已创建表单: " << name << endl;
    }

    // 删除表单
    void removeForm(const string& name) {
        int index = findFormIndex(name);
        if (index != -1) {
            forms.erase(forms.begin() + index);
            cout << "已删除表单: " << name << endl;
        } else {
            cout << "表单不存在！" << endl;
        }
    }

    // 获取表单
    GradeForm* getForm(const string& name) {
        int index = findFormIndex(name);
        if (index != -1) {
            // 这里传回指针比较好，不宜用find传回迭代器
            return &forms[index];
        }
        return nullptr;
    }

    // 显示所有表单
    void listForms() {
        if (forms.empty()) {
            cout << "当前没有表单" << endl;
            return;
        }

        cout << "\n可用表单:" << endl;
        for (const auto& form : forms) {
            cout << "- " << form.getName() << " (科目数: " << form.getSubjects().size() << ")" << endl;
        }
    }
};

// 显示主菜单
void displayMainMenu() {
    cout << "\n===== 学生成绩管理系统 =====";
    cout << "\n1. 创建表单";
    cout << "\n2. 删除表单";
    cout << "\n3. 管理表单";
    cout << "\n4. 列出所有表单";
    cout << "\n5. 从CSV导入";
    cout << "\n6. 导出到CSV";
    cout << "\n0. 退出";
    cout << "\n=========================";
    cout << "\n请选择操作: ";
}

// 显示表单管理菜单
void displayFormMenu() {
    cout << "\n===== 表单管理 =====";
    cout << "\n1. 添加学生";
    cout << "\n2. 删除学生";
    cout << "\n3. 查询学生";
    cout << "\n4. 修改成绩";
    cout << "\n5. 添加科目";
    cout << "\n6. 删除科目";
    cout << "\n7. 展示表单";
    cout << "\n8. 排序展示";
    cout << "\n0. 返回主菜单";
    cout << "\n==================";
    cout << "\n请选择操作: ";
}

int main() {
    GradeSystem system;

    while (true) {
        displayMainMenu();
        int choice;
        cin >> choice;
        if (choice == 0) break;
        switch (choice) {
            case 1: { // 创建表单
                string name;
                cout << "输入新表单名称: ";
                cin >> name;
                system.createForm(name);
                break;
            }
            case 2: { // 删除表单
                string name;
                cout << "输入要删除的表单名称: ";
                cin >> name;
                system.removeForm(name);
                break;
            }
            case 3: { // 管理表单
                string sheet_name;
                cout << "输入要管理的表单名称: ";
                cin >> sheet_name;
                GradeForm* form = system.getForm(sheet_name);
                if (!form) {
                    cout << "表单不存在！" << endl;
                    break;
                }
                while (true) {
                    displayFormMenu();
                    int formChoice;
                    cin >> formChoice;
                    if (formChoice == 0) break;
                    switch (formChoice) {
                        case 1: { // 添加学生
                            string stu_name, id;
                            cout << "输入学生姓名: ";
                            cin >> stu_name;
                            cout << "输入学生学号: ";
                            cin >> id;
                            form->addStudent(Student(stu_name, id));
                            break;
                        }
                        case 2: { // 删除学生
                            string id;
                            cout << "输入要删除的学生学号: ";
                            cin >> id;
                            form->removeStudent(id);
                            break;
                        }
                        case 3: { // 查询学生
                            string keyword;
                            cout << "输入姓名或学号: ";
                            cin >> keyword;
                            form->queryStudent(keyword);
                            break;
                        }
                        case 4: { // 修改成绩
                            string id, subject;
                            double score;
                            cout << "输入学生学号: ";
                            cin >> id;
                            cout << "输入科目名称: ";
                            cin >> subject;
                            cout << "输入新成绩: ";
                            cin >> score;
                            form->modifyScore(id, subject, score);
                            break;
                        }
                        case 5: { // 添加科目
                            string subject;
                            cout << "输入新科目名称: ";
                            cin >> subject;
                            form->addSubject(subject);
                            break;
                        }
                        case 6: { // 删除科目
                            string subject;
                            cout << "输入要删除的科目名称: ";
                            cin >> subject;
                            form->removeSubject(subject);
                            break;
                        }
                        case 7: // 展示表单
                            form->display(true);
                            break;
                        case 8: { // 排序展示
                            string criteria;
                            cout << "输入排序依据(姓名/学号/总分/科目名): ";
                            cin >> criteria;
                            form->sortAndDisplay(criteria);
                            break;
                        }
                        default:
                            cout << "无效选择！" << endl;
                    }
                }
                break;
            }
            case 4: // 列出所有表单
                system.listForms();
                break;
            case 5: { // 从CSV导入
                string formName, filename;
                cout << "输入表单名称: ";
                cin >> formName;
                cout << "输入CSV文件名: ";
                cin >> filename;
                system.createForm(formName);
                GradeForm* form = system.getForm(formName);
                if (form) {
                    form->loadFromCSV(filename);
                }
                break;
            }
            case 6: { // 导出到CSV
                string formName, filename;
                cout << "输入表单名称: ";
                cin >> formName;
                GradeForm* form = system.getForm(formName);
                if (!form) {
                    cout << "表单不存在！" << endl;
                    break;
                }
                cout << "输入保存文件名: ";
                cin >> filename;
                form->saveToCSV(filename);
                break;
            }
            default:
                cout << "无效选择！" << endl;
        }
    }

    cout << "系统已退出" << endl;
    return 0;
}