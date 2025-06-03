#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
#include <memory>
#include <stdexcept>
#include <typeinfo>
using namespace std;

// 列基类
class Column {
public:
    string name;
    Column(const string& n) : name(n) {}
    virtual ~Column() {}
    virtual void display() const = 0;
    virtual unique_ptr<Column> clone() const = 0;
    virtual double getNumericValue(const string& val) const { return 0.0; }
};

// 元对象列（如姓名、学号）
class MetaColumn : public Column {
public:
    MetaColumn(const string& n) : Column(n) {}
    void display() const override {
        cout << "【元数据】" << name;
    }
    unique_ptr<Column> clone() const override {
        return make_unique<MetaColumn>(*this);
    }
};

// 数据对象列（如科目成绩）
class DataColumn : public Column {
public:
    DataColumn(const string& n) : Column(n) {}
    void display() const override {
        cout << "【科目】" << name;
    }
    unique_ptr<Column> clone() const override {
        return make_unique<DataColumn>(*this);
    }
    double getNumericValue(const string& val) const override {
        try {
            return stod(val);
        } catch (...) {
            return 0.0;
        }
    }
};

// 行基类
class Row {
protected:
    vector<string> values;
public:
    virtual ~Row() {}
    virtual void display(const vector<unique_ptr<Column>>& columns) const = 0;
    virtual unique_ptr<Row> clone() const = 0;

    // 运算符重载：比较学号
    bool operator==(const string& id) const {
        if (values.size() > 1) {
            return values[1] == id;
        }
        return false;
    }

    void setValue(int index, const string& value) {
        if (index >= 0 && index < values.size()) {
            values[index] = value;
        }
    }

    string getValue(int index) const {
        if (index >= 0 && index < values.size()) {
            return values[index];
        }
        return "";
    }
};

// 普通学生行
class RegularStudent : public Row {
public:
    RegularStudent(const string& name, const string& id) {
        values.push_back(name);
        values.push_back(id);
    }

    void display(const vector<unique_ptr<Column>>& columns) const override {
        cout << "普通学生: ";
        for (size_t i = 0; i < values.size(); ++i) {
            cout << left << setw(12) << values[i];
        }
    }

    unique_ptr<Row> clone() const override {
        auto newRow = make_unique<RegularStudent>(values[0], values[1]);
        for (size_t i = 2; i < values.size(); ++i) {
            newRow->values.push_back(values[i]);
        }
        return newRow;
    }
};

// 旁听学生行
class AuditStudent : public Row {
public:
    AuditStudent(const string& name, const string& id) {
        values.push_back(name);
        values.push_back(id);
    }

    void display(const vector<unique_ptr<Column>>& columns) const override {
        cout << "旁听学生: ";
        for (size_t i = 0; i < values.size(); ++i) {
            if (i == 0) {
                cout << left << setw(12) << (values[i] + "(旁)");
            } else {
                cout << left << setw(12) << values[i];
            }
        }
    }

    unique_ptr<Row> clone() const override {
        auto newRow = make_unique<AuditStudent>(values[0], values[1]);
        for (size_t i = 2; i < values.size(); ++i) {
            newRow->values.push_back(values[i]);
        }
        return newRow;
    }
};

// 学生成绩表单
class GradeForm {
private:
    vector<unique_ptr<Column>> columns;
    vector<unique_ptr<Row>> rows;

public:
    GradeForm() {
        // 添加默认列
        columns.push_back(make_unique<MetaColumn>("姓名"));
        columns.push_back(make_unique<MetaColumn>("学号"));
    }

    // 添加列
    void addColumn(const string& name, bool isSubject = true) {
        if (isSubject) {
            columns.push_back(make_unique<DataColumn>(name));
        } else {
            columns.push_back(make_unique<MetaColumn>(name));
        }

        // 为现有行添加新列的值
        for (auto& row : rows) {
            row->setValue(columns.size() - 1, "0");
        }
    }

    // 删除列
    void deleteColumn(int index) {
        if (index < 2) {
            cout << "不能删除姓名或学号列!" << endl;
            return;
        }

        if (index >= 0 && index < static_cast<int>(columns.size())) {
            columns.erase(columns.begin() + index);

            // 从每行中移除该列的值
            for (auto& row : rows) {
                // 创建新行，跳过被删除的列
                auto newRow = row->clone();
                rows.push_back(move(newRow));
                rows.erase(remove_if(rows.begin(), rows.end(),
                    [&](const unique_ptr<Row>& r) { return r.get() == row.get(); }),
                    rows.end());
            }
        } else {
            cout << "无效的列索引!" << endl;
        }
    }

    // 添加学生
    void addStudent(unique_ptr<Row> student) {
        // 检查学号是否重复
        string id = student->getValue(1);
        auto it = find_if(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& r) { return *r == id; });

        if (it != rows.end()) {
            cout << "学号 " << id << " 已存在，不能重复添加!" << endl;
            return;
        }

        // 确保学生数据有所有列的值
        while (student->getValue(columns.size() - 1) == "") {
            student->setValue(columns.size() - 1, "0");
        }

        rows.push_back(move(student));
    }

    // 删除学生
    void deleteStudent(const string& id) {
        auto it = find_if(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& r) { return *r == id; });

        if (it != rows.end()) {
            rows.erase(it);
            cout << "学号 " << id << " 的学生已删除" << endl;
        } else {
            cout << "找不到学号 " << id << " 的学生" << endl;
        }
    }

    // 查询学生
    void findStudent(const string& id) const {
        auto it = find_if(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& r) { return *r == id; });

        if (it != rows.end()) {
            displayHeader();
            (*it)->display(columns);
            cout << endl;
        } else {
            cout << "找不到学号 " << id << " 的学生" << endl;
        }
    }

    // 修改成绩
    void updateGrade(const string& id, int colIndex, const string& newValue) {
        if (colIndex < 2 || colIndex >= static_cast<int>(columns.size())) {
            cout << "无效的列索引!" << endl;
            return;
        }

        auto it = find_if(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& r) { return *r == id; });

        if (it != rows.end()) {
            // 验证输入
            try {
                if (dynamic_cast<DataColumn*>(columns[colIndex].get())) {
                    double value = stod(newValue);
                    if (value < 0 || value > 100) {
                        cout << "成绩必须在0-100之间!" << endl;
                        return;
                    }
                }
            } catch (...) {
                cout << "无效的成绩格式!" << endl;
                return;
            }

            (*it)->setValue(colIndex, newValue);
            cout << "成绩更新成功!" << endl;
        } else {
            cout << "找不到学号 " << id << " 的学生" << endl;
        }
    }

    // 显示表头
    void displayHeader() const {
        for (const auto& col : columns) {
            cout << left << setw(12) << col->name.substr(0, 10);
        }
        cout << endl;

        for (size_t i = 0; i < columns.size(); ++i) {
            cout << left << setw(12) << "---------";
        }
        cout << endl;
    }

    // 展示表单
    void display() const {
        if (rows.empty()) {
            cout << "表单为空!" << endl;
            return;
        }

        displayHeader();
        for (const auto& row : rows) {
            row->display(columns);
            cout << endl;
        }
    }

    // 按列排序
    void sortByColumn(int colIndex) {
        if (colIndex < 0 || colIndex >= static_cast<int>(columns.size())) {
            cout << "无效的列索引!" << endl;
            return;
        }

        sort(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& a, const unique_ptr<Row>& b) {
                string valA = a->getValue(colIndex);
                string valB = b->getValue(colIndex);

                // 如果是成绩列，按数值比较
                if (dynamic_cast<DataColumn*>(columns[colIndex].get())) {
                    try {
                        double numA = stod(valA);
                        double numB = stod(valB);
                        return numA > numB;
                    } catch (...) {
                        return valA > valB;
                    }
                }
                // 否则按字符串比较
                return valA > valB;
            });

        cout << "已按 " << columns[colIndex]->name << " 降序排序" << endl;
    }

    // 计算平均分
    void calculateAverage(int colIndex) const {
        if (colIndex < 2 || colIndex >= static_cast<int>(columns.size())) {
            cout << "无效的列索引!" << endl;
            return;
        }

        if (!dynamic_cast<DataColumn*>(columns[colIndex].get())) {
            cout << "该列不是科目成绩列!" << endl;
            return;
        }

        double total = 0.0;
        int count = 0;

        for (const auto& row : rows) {
            string value = row->getValue(colIndex);
            try {
                double grade = stod(value);
                total += grade;
                count++;
            } catch (...) {
                // 忽略无效成绩
            }
        }

        if (count > 0) {
            cout << columns[colIndex]->name << " 平均分: "
                 << fixed << setprecision(2) << (total / count) << endl;
        } else {
            cout << "没有有效的成绩数据!" << endl;
        }
    }

    // 获取列数
    int getColumnCount() const {
        return columns.size();
    }

    // 获取列名
    string getColumnName(int index) const {
        if (index >= 0 && index < static_cast<int>(columns.size())) {
            return columns[index]->name;
        }
        return "";
    }

    // 显示所有列
    void displayColumns() const {
        cout << "当前列 (" << columns.size() << "):" << endl;
        for (size_t i = 0; i < columns.size(); ++i) {
            cout << i << ": " << columns[i]->name;
            if (dynamic_cast<MetaColumn*>(columns[i].get())) {
                cout << " (元数据)";
            } else {
                cout << " (科目)";
            }
            cout << endl;
        }
    }
};

// 显示菜单
void displayMenu() {
    cout << "\n======= 学生成绩管理系统 =======" << endl;
    cout << "1. 添加学生" << endl;
    cout << "2. 删除学生" << endl;
    cout << "3. 查询学生" << endl;
    cout << "4. 修改成绩" << endl;
    cout << "5. 添加科目" << endl;
    cout << "6. 删除科目" << endl;
    cout << "7. 展示表单" << endl;
    cout << "8. 按科目排序" << endl;
    cout << "9. 计算平均分" << endl;
    cout << "0. 退出系统" << endl;
    cout << "=============================" << endl;
    cout << "请选择操作: ";
}

int main() {
    GradeForm form;
    int choice;

    // 添加一些初始数据
    form.addColumn("数学", true);
    form.addColumn("英语", true);
    form.addStudent(make_unique<RegularStudent>("张三", "2023001"));
    form.addStudent(make_unique<RegularStudent>("李四", "2023002"));
    form.addStudent(make_unique<AuditStudent>("王五", "2023003"));

    do {
        displayMenu();
        cin >> choice;

        // 清除输入缓冲区
        cin.ignore();

        switch (choice) {
            case 1: { // 添加学生
                string name, id;
                int type;

                cout << "输入学生姓名: ";
                getline(cin, name);
                cout << "输入学号: ";
                getline(cin, id);
                cout << "选择类型 (1.普通学生 2.旁听学生): ";
                cin >> type;
                cin.ignore();

                if (type == 1) {
                    form.addStudent(make_unique<RegularStudent>(name, id));
                } else if (type == 2) {
                    form.addStudent(make_unique<AuditStudent>(name, id));
                } else {
                    cout << "无效的选择!" << endl;
                }
                break;
            }
            case 2: { // 删除学生
                string id;
                cout << "输入要删除学生的学号: ";
                getline(cin, id);
                form.deleteStudent(id);
                break;
            }
            case 3: { // 查询学生
                string id;
                cout << "输入要查询学生的学号: ";
                getline(cin, id);
                form.findStudent(id);
                break;
            }
            case 4: { // 修改成绩
                string id, newValue;
                int colIndex;

                cout << "输入学生学号: ";
                getline(cin, id);

                form.displayColumns();
                cout << "输入要修改的列索引: ";
                cin >> colIndex;
                cin.ignore();

                cout << "输入新值: ";
                getline(cin, newValue);

                form.updateGrade(id, colIndex, newValue);
                break;
            }
            case 5: { // 添加科目
                string subject;
                cout << "输入新科目名称: ";
                getline(cin, subject);
                form.addColumn(subject, true);
                cout << "已添加科目: " << subject << endl;
                break;
            }
            case 6: { // 删除科目
                form.displayColumns();
                int colIndex;
                cout << "输入要删除的科目索引: ";
                cin >> colIndex;
                cin.ignore();
                form.deleteColumn(colIndex);
                break;
            }
            case 7: // 展示表单
                form.display();
                break;
            case 8: { // 按科目排序
                form.displayColumns();
                int colIndex;
                cout << "输入要排序的列索引: ";
                cin >> colIndex;
                cin.ignore();
                form.sortByColumn(colIndex);
                break;
            }
            case 9: { // 计算平均分
                form.displayColumns();
                int colIndex;
                cout << "输入要计算平均分的科目索引: ";
                cin >> colIndex;
                cin.ignore();
                form.calculateAverage(colIndex);
                break;
            }
            case 0: // 退出系统
                cout << "感谢使用学生成绩管理系统，再见!" << endl;
                break;
            default:
                cout << "无效的选择，请重新输入!" << endl;
        }

        if (choice != 0) {
            cout << "\n按回车键继续...";
            cin.ignore();
        }
    } while (choice != 0);

    return 0;
}