#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <map>

using namespace std;

// 数据项抽象基类
class DataItem {
public:
    virtual ~DataItem() {}
    virtual void show() const = 0;
    virtual string csvFormat() const = 0;
    virtual bool contains(const string& term) const = 0;
};

// 学生成绩类
class Student : public DataItem {
private:
    string fullName;
    string studentID;
    map<string, double> grades;

public:
    Student(string name, string id) : fullName(name), studentID(id) {}

    // 比较运算符重载用于find
    bool operator==(const Student& other) const {
        return studentID == other.studentID;
    }

    void updateGrade(const string& subject, double score) {
        grades[subject] = score;
    }

    void removeSubjectGrade(const string& subject) {
        grades.erase(subject);
    }

    double calculateTotal() const {
        double sum = 0.0;
        for (const auto& g : grades) {
            sum += g.second;
        }
        return sum;
    }

    double getSubjectScore(const string& subject) const {
        auto it = grades.find(subject);
        return (it != grades.end()) ? it->second : -1.0;
    }

    void show() const override {
        cout << left << setw(15) << fullName << setw(15) << studentID;
        for (const auto& g : grades) {
            cout << setw(10) << g.first << ":" << setw(5) << g.second;
        }
        cout << "总分:" << setw(6) << calculateTotal() << endl;
    }

    string csvFormat() const override {
        ostringstream oss;
        oss << fullName << "," << studentID;
        for (const auto& g : grades) {
            oss << "," << g.second;
        }
        return oss.str();
    }

    bool contains(const string& term) const override {
        return fullName.find(term) != string::npos || studentID.find(term) != string::npos;
    }

    const string& getName() const { return fullName; }
    const string& getID() const { return studentID; }
    const map<string, double>& getGrades() const { return grades; }
};

// 成绩表单类
class GradeSheet {
private:
    string sheetTitle;
    vector<Student> students;
    vector<string> subjectsList;

public:
    GradeSheet(string title) : sheetTitle(title) {}

    void addStudentRecord(const Student& student) {
        auto it = find(students.begin(), students.end(), student);
        if (it != students.end()) {
            cout << "错误：学号 " << student.getID() << " 已存在！" << endl;
            return;
        }
        students.push_back(student);
        cout << "已添加学生: " << student.getName() << endl;
    }

    void removeStudent(const string& id) {
        auto it = find_if(students.begin(), students.end(),
                         [&](const Student& s) { return s.getID() == id; });

        if (it != students.end()) {
            cout << "删除学生: " << it->getName() << " (" << it->getID() << ")" << endl;
            students.erase(it);
        } else {
            cout << "未找到学号: " << id << endl;
        }
    }

    void searchStudents(const string& term) {
        bool found = false;
        for (const auto& s : students) {
            if (s.contains(term)) {
                s.show();
                found = true;
            }
        }
        if (!found) {
            cout << "未找到匹配的学生记录" << endl;
        }
    }

    void updateGrade(const string& id, const string& subject, double score) {
        bool studentFound = false;

        for (auto& s : students) {
            if (s.getID() == id) {
                studentFound = true;
                auto subIt = find(subjectsList.begin(), subjectsList.end(), subject);
                if (subIt != subjectsList.end()) {
                    s.updateGrade(subject, score);
                    cout << "已更新 " << s.getName() << " 的" << subject << "成绩: " << score << endl;
                } else {
                    cout << "错误：科目 '" << subject << "' 不存在" << endl;
                }
                break;
            }
        }

        if (!studentFound) {
            cout << "未找到学号: " << id << endl;
        }
    }

    void addSubject(const string& subject) {
        if (find(subjectsList.begin(), subjectsList.end(), subject) != subjectsList.end()) {
            cout << "科目已存在！" << endl;
            return;
        }
        subjectsList.push_back(subject);

        // 初始化
        for (auto& s : students) {
            s.updateGrade(subject, 0.0);
        }
        cout << "已添加科目: " << subject << endl;
    }

    void removeSubject(const string& subject) {
        auto it = find(subjectsList.begin(), subjectsList.end(), subject);
        if (it != subjectsList.end()) {
            subjectsList.erase(it);
            for (auto& s : students) {
                s.removeSubjectGrade(subject);
            }
            cout << "已移除科目: " << subject << endl;
        } else {
            cout << "错误：科目不存在" << endl;
        }
    }

    void display(bool showAvg = true) {
        cout << "\n=== " << sheetTitle << " ===" << endl;
        cout << left << setw(15) << "姓名" << setw(15) << "学号";
        for (const auto& sub : subjectsList) {
            cout << setw(15) << sub;
        }
        cout << setw(15) << "总分" << endl;
        cout << string(15*(subjectsList.size()+2), '-') << endl;

        for (const auto& s : students) {
            cout << left << setw(15) << s.getName() << setw(15) << s.getID();
            for (const auto& sub : subjectsList) {
                double score = s.getSubjectScore(sub);
                if (score >= 0) {
                    cout << setw(15) << score;
                } else {
                    cout << setw(15) << "N/A";
                }
            }
            cout << setw(15) << s.calculateTotal() << endl;
        }

        if (showAvg && !students.empty()) {
            cout << string(15*(subjectsList.size()+2), '-') << endl;
            cout << left << setw(30) << "平均分";
            for (const auto& sub : subjectsList) {
                double total = 0.0;
                int count = 0;
                for (const auto& s : students) {
                    double score = s.getSubjectScore(sub);
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

    void sortAndShow(const string& field, bool ascending = true) {
        // 排序
        if (field == "学号") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getID() < b.getID() : a.getID() > b.getID();
                });
        } else if (field == "姓名") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getName() < b.getName() : a.getName() > b.getName();
                });
        } else if (field == "总分") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.calculateTotal() < b.calculateTotal()
                                     : a.calculateTotal() > b.calculateTotal();
                });
        } else {
            // 科目
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    double scoreA = a.getSubjectScore(field);
                    double scoreB = b.getSubjectScore(field);
                    return ascending ? scoreA < scoreB : scoreA > scoreB;
                });
        }
        display(true);
    }

    void exportToCSV(const string& filename) {
        ofstream outFile(filename);
        if (!outFile) {
            cerr << "文件打开失败: " << filename << endl;
            return;
        }

        outFile << "姓名,学号";
        for (const auto& sub : subjectsList) {
            outFile << "," << sub;
        }
        outFile << endl;

        for (const auto& s : students) {
            outFile << s.csvFormat() << endl;
        }

        cout << "数据已导出到: " << filename << endl;
        outFile.close();
    }

    void importFromCSV(const string& filename) {
        ifstream inFile(filename);
        if (!inFile) {
            cerr << "无法打开文件: " << filename << endl;
            return;
        }

        students.clear();
        subjectsList.clear();

        string line;

        if (getline(inFile, line)) {
            stringstream headerStream(line);
            string cell;
            vector<string> headers;

            while (getline(headerStream, cell, ',')) {
                headers.push_back(cell);
            }

            if (headers.size() < 2) {
                cerr << "无效文件格式" << endl;
                return;
            }

            // 姓名\学号+N*科目
            subjectsList = vector<string>(headers.begin() + 2, headers.end());
        }

        while (getline(inFile, line)) {
            if (line.empty()) continue;

            stringstream dataStream(line);
            string cell;
            vector<string> rowData;

            while (getline(dataStream, cell, ',')) {
                rowData.push_back(cell);
            }

            if (rowData.size() < 2) continue;

            Student s(rowData[0], rowData[1]);
            for (int i = 0; i < subjectsList.size() && i + 2 < rowData.size(); i++) {
                try {
                    double score = stod(rowData[i + 2]);
                    s.updateGrade(subjectsList[i], score);
                } catch (...) {
                    cerr << "成绩转换错误: " << rowData[i+2] << endl;
                }
            }
            students.push_back(s);
        }

        cout << "已导入 " << students.size() << " 条记录" << endl;
        inFile.close();
    }

    const string& getTitle() const { return sheetTitle; }
    const vector<string>& getSubjects() const { return subjectsList; }
};

// 成绩管理系统
class GradeManager {
private:
    vector<GradeSheet> sheets;

    int findSheetIndex(const string& title) const{
        for (int i = 0; i < sheets.size(); i++) {
            if (sheets[i].getTitle() == title) {
                return i;
            }
        }
        return -1;
    }

public:
    void createSheet(const string& title) {
        if (findSheetIndex(title) != -1) {
            cout << "表单已存在！" << endl;
            return;
        }
        sheets.emplace_back(title);
        cout << "已创建表单: " << title << endl;
    }

    void removeSheet(const string& title) {
        int index = findSheetIndex(title);
        if (index != -1) {
            sheets.erase(sheets.begin() + index);
            cout << "已删除表单: " << title << endl;
        } else {
            cout << "表单不存在！" << endl;
        }
    }

    GradeSheet* getSheet(const string& title) {
        int index = findSheetIndex(title);
        if (index != -1) {
            return &sheets[index];
        }
        return nullptr;
    }

    void listSheets() {
        if (sheets.empty()) {
            cout << "当前没有表单" << endl;
            return;
        }

        cout << "\n表单列表:" << endl;
        for (const auto& sheet : sheets) {
            cout << "- " << sheet.getTitle() << " (" << sheet.getSubjects().size() << "个科目)" << endl;
        }
    }
};

// 菜单系统
void showMainMenu() {
    cout << "\n===== 学生成绩管理系统 =====";
    cout << "\n1. 新建表单";
    cout << "\n2. 删除表单";
    cout << "\n3. 管理表单";
    cout << "\n4. 表单列表";
    cout << "\n5. 导入CSV";
    cout << "\n6. 导出CSV";
    cout << "\n0. 退出系统";
    cout << "\n=========================";
    cout << "\n请选择: ";
}

void showSheetMenu() {
    cout << "\n===== 表单操作 =====";
    cout << "\n1. 添加学生";
    cout << "\n2. 删除学生";
    cout << "\n3. 查找学生";
    cout << "\n4. 修改成绩";
    cout << "\n5. 添加科目";
    cout << "\n6. 删除科目";
    cout << "\n7. 显示表单";
    cout << "\n8. 排序显示";
    cout << "\n0. 返回主菜单";
    cout << "\n==================";
    cout << "\n请选择操作: ";
}

int main() {
    GradeManager manager;

    while (true) {
        showMainMenu();
        int choice;
        cin >> choice;

        if (choice == 0) {
            cout << "系统已退出" << endl;
            break;
        }

        switch (choice) {
            case 1: { // 新建表单
                string title;
                cout << "输入表单名称: ";
                cin >> title;
                manager.createSheet(title);
                break;
            }
            case 2: { // 删除表单
                string title;
                cout << "输入要删除的表单名称: ";
                cin >> title;
                manager.removeSheet(title);
                break;
            }
            case 3: { // 管理表单
                string title;
                cout << "输入表单名称: ";
                cin >> title;
                GradeSheet* sheet = manager.getSheet(title);

                if (!sheet) {
                    cout << "表单不存在！" << endl;
                    break;
                }

                while (true) {
                    showSheetMenu();
                    int sheetChoice;
                    cin >> sheetChoice;

                    if (sheetChoice == 0) break;

                    switch (sheetChoice) {
                        case 1: { // 添加学生
                            string name, id;
                            cout << "学生姓名: ";
                            cin >> name;
                            cout << "学生学号: ";
                            cin >> id;
                            sheet->addStudentRecord(Student(name, id));
                            break;
                        }
                        case 2: { // 删除学生
                            string id;
                            cout << "输入学号: ";
                            cin >> id;
                            sheet->removeStudent(id);
                            break;
                        }
                        case 3: { // 查找学生
                            string term;
                            cout << "输入姓名或学号: ";
                            cin >> term;
                            sheet->searchStudents(term);
                            break;
                        }
                        case 4: { // 修改成绩
                            string id, subject;
                            double score;
                            cout << "学生学号: ";
                            cin >> id;
                            cout << "科目名称: ";
                            cin >> subject;
                            cout << "新成绩: ";
                            cin >> score;
                            sheet->updateGrade(id, subject, score);
                            break;
                        }
                        case 5: { // 添加科目
                            string subject;
                            cout << "新科目名称: ";
                            cin >> subject;
                            sheet->addSubject(subject);
                            break;
                        }
                        case 6: { // 删除科目
                            string subject;
                            cout << "要删除的科目: ";
                            cin >> subject;
                            sheet->removeSubject(subject);
                            break;
                        }
                        case 7:
                            sheet->display(true);
                            break;
                        case 8: {
                            string field;
                            cout << "排序依据(姓名/学号/总分/科目): ";
                            cin >> field;
                            sheet->sortAndShow(field);
                            break;
                        }
                        default:
                            cout << "无效操作！" << endl;
                    }
                }
                break;
            }
            case 4:
                manager.listSheets();
                break;
            case 5: { // 导入CSV
                string title, filename;
                cout << "表单名称: ";
                cin >> title;
                cout << "CSV文件名: ";
                cin >> filename;
                manager.createSheet(title);
                GradeSheet* sheet = manager.getSheet(title);
                if (sheet) {
                    sheet->importFromCSV(filename);
                }
                break;
            }
            case 6: { // 导出CSV
                string title, filename;
                cout << "表单名称: ";
                cin >> title;
                GradeSheet* sheet = manager.getSheet(title);
                if (!sheet) {
                    cout << "表单不存在！" << endl;
                    break;
                }
                cout << "导出文件名: ";
                cin >> filename;
                sheet->exportToCSV(filename);
                break;
            }
            default:
                cout << "无效选择！" << endl;
        }
    }

    return 0;
}