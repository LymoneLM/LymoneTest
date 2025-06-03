#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
#include <memory>
#include <stdexcept>
#include <typeinfo>
using namespace std;

// �л���
class Column {
public:
    string name;
    Column(const string& n) : name(n) {}
    virtual ~Column() {}
    virtual void display() const = 0;
    virtual unique_ptr<Column> clone() const = 0;
    virtual double getNumericValue(const string& val) const { return 0.0; }
};

// Ԫ�����У���������ѧ�ţ�
class MetaColumn : public Column {
public:
    MetaColumn(const string& n) : Column(n) {}
    void display() const override {
        cout << "��Ԫ���ݡ�" << name;
    }
    unique_ptr<Column> clone() const override {
        return make_unique<MetaColumn>(*this);
    }
};

// ���ݶ����У����Ŀ�ɼ���
class DataColumn : public Column {
public:
    DataColumn(const string& n) : Column(n) {}
    void display() const override {
        cout << "����Ŀ��" << name;
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

// �л���
class Row {
protected:
    vector<string> values;
public:
    virtual ~Row() {}
    virtual void display(const vector<unique_ptr<Column>>& columns) const = 0;
    virtual unique_ptr<Row> clone() const = 0;

    // ��������أ��Ƚ�ѧ��
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

// ��ͨѧ����
class RegularStudent : public Row {
public:
    RegularStudent(const string& name, const string& id) {
        values.push_back(name);
        values.push_back(id);
    }

    void display(const vector<unique_ptr<Column>>& columns) const override {
        cout << "��ͨѧ��: ";
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

// ����ѧ����
class AuditStudent : public Row {
public:
    AuditStudent(const string& name, const string& id) {
        values.push_back(name);
        values.push_back(id);
    }

    void display(const vector<unique_ptr<Column>>& columns) const override {
        cout << "����ѧ��: ";
        for (size_t i = 0; i < values.size(); ++i) {
            if (i == 0) {
                cout << left << setw(12) << (values[i] + "(��)");
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

// ѧ���ɼ���
class GradeForm {
private:
    vector<unique_ptr<Column>> columns;
    vector<unique_ptr<Row>> rows;

public:
    GradeForm() {
        // ���Ĭ����
        columns.push_back(make_unique<MetaColumn>("����"));
        columns.push_back(make_unique<MetaColumn>("ѧ��"));
    }

    // �����
    void addColumn(const string& name, bool isSubject = true) {
        if (isSubject) {
            columns.push_back(make_unique<DataColumn>(name));
        } else {
            columns.push_back(make_unique<MetaColumn>(name));
        }

        // Ϊ������������е�ֵ
        for (auto& row : rows) {
            row->setValue(columns.size() - 1, "0");
        }
    }

    // ɾ����
    void deleteColumn(int index) {
        if (index < 2) {
            cout << "����ɾ��������ѧ����!" << endl;
            return;
        }

        if (index >= 0 && index < static_cast<int>(columns.size())) {
            columns.erase(columns.begin() + index);

            // ��ÿ�����Ƴ����е�ֵ
            for (auto& row : rows) {
                // �������У�������ɾ������
                auto newRow = row->clone();
                rows.push_back(move(newRow));
                rows.erase(remove_if(rows.begin(), rows.end(),
                    [&](const unique_ptr<Row>& r) { return r.get() == row.get(); }),
                    rows.end());
            }
        } else {
            cout << "��Ч��������!" << endl;
        }
    }

    // ���ѧ��
    void addStudent(unique_ptr<Row> student) {
        // ���ѧ���Ƿ��ظ�
        string id = student->getValue(1);
        auto it = find_if(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& r) { return *r == id; });

        if (it != rows.end()) {
            cout << "ѧ�� " << id << " �Ѵ��ڣ������ظ����!" << endl;
            return;
        }

        // ȷ��ѧ�������������е�ֵ
        while (student->getValue(columns.size() - 1) == "") {
            student->setValue(columns.size() - 1, "0");
        }

        rows.push_back(move(student));
    }

    // ɾ��ѧ��
    void deleteStudent(const string& id) {
        auto it = find_if(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& r) { return *r == id; });

        if (it != rows.end()) {
            rows.erase(it);
            cout << "ѧ�� " << id << " ��ѧ����ɾ��" << endl;
        } else {
            cout << "�Ҳ���ѧ�� " << id << " ��ѧ��" << endl;
        }
    }

    // ��ѯѧ��
    void findStudent(const string& id) const {
        auto it = find_if(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& r) { return *r == id; });

        if (it != rows.end()) {
            displayHeader();
            (*it)->display(columns);
            cout << endl;
        } else {
            cout << "�Ҳ���ѧ�� " << id << " ��ѧ��" << endl;
        }
    }

    // �޸ĳɼ�
    void updateGrade(const string& id, int colIndex, const string& newValue) {
        if (colIndex < 2 || colIndex >= static_cast<int>(columns.size())) {
            cout << "��Ч��������!" << endl;
            return;
        }

        auto it = find_if(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& r) { return *r == id; });

        if (it != rows.end()) {
            // ��֤����
            try {
                if (dynamic_cast<DataColumn*>(columns[colIndex].get())) {
                    double value = stod(newValue);
                    if (value < 0 || value > 100) {
                        cout << "�ɼ�������0-100֮��!" << endl;
                        return;
                    }
                }
            } catch (...) {
                cout << "��Ч�ĳɼ���ʽ!" << endl;
                return;
            }

            (*it)->setValue(colIndex, newValue);
            cout << "�ɼ����³ɹ�!" << endl;
        } else {
            cout << "�Ҳ���ѧ�� " << id << " ��ѧ��" << endl;
        }
    }

    // ��ʾ��ͷ
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

    // չʾ��
    void display() const {
        if (rows.empty()) {
            cout << "��Ϊ��!" << endl;
            return;
        }

        displayHeader();
        for (const auto& row : rows) {
            row->display(columns);
            cout << endl;
        }
    }

    // ��������
    void sortByColumn(int colIndex) {
        if (colIndex < 0 || colIndex >= static_cast<int>(columns.size())) {
            cout << "��Ч��������!" << endl;
            return;
        }

        sort(rows.begin(), rows.end(),
            [&](const unique_ptr<Row>& a, const unique_ptr<Row>& b) {
                string valA = a->getValue(colIndex);
                string valB = b->getValue(colIndex);

                // ����ǳɼ��У�����ֵ�Ƚ�
                if (dynamic_cast<DataColumn*>(columns[colIndex].get())) {
                    try {
                        double numA = stod(valA);
                        double numB = stod(valB);
                        return numA > numB;
                    } catch (...) {
                        return valA > valB;
                    }
                }
                // �����ַ����Ƚ�
                return valA > valB;
            });

        cout << "�Ѱ� " << columns[colIndex]->name << " ��������" << endl;
    }

    // ����ƽ����
    void calculateAverage(int colIndex) const {
        if (colIndex < 2 || colIndex >= static_cast<int>(columns.size())) {
            cout << "��Ч��������!" << endl;
            return;
        }

        if (!dynamic_cast<DataColumn*>(columns[colIndex].get())) {
            cout << "���в��ǿ�Ŀ�ɼ���!" << endl;
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
                // ������Ч�ɼ�
            }
        }

        if (count > 0) {
            cout << columns[colIndex]->name << " ƽ����: "
                 << fixed << setprecision(2) << (total / count) << endl;
        } else {
            cout << "û����Ч�ĳɼ�����!" << endl;
        }
    }

    // ��ȡ����
    int getColumnCount() const {
        return columns.size();
    }

    // ��ȡ����
    string getColumnName(int index) const {
        if (index >= 0 && index < static_cast<int>(columns.size())) {
            return columns[index]->name;
        }
        return "";
    }

    // ��ʾ������
    void displayColumns() const {
        cout << "��ǰ�� (" << columns.size() << "):" << endl;
        for (size_t i = 0; i < columns.size(); ++i) {
            cout << i << ": " << columns[i]->name;
            if (dynamic_cast<MetaColumn*>(columns[i].get())) {
                cout << " (Ԫ����)";
            } else {
                cout << " (��Ŀ)";
            }
            cout << endl;
        }
    }
};

// ��ʾ�˵�
void displayMenu() {
    cout << "\n======= ѧ���ɼ�����ϵͳ =======" << endl;
    cout << "1. ���ѧ��" << endl;
    cout << "2. ɾ��ѧ��" << endl;
    cout << "3. ��ѯѧ��" << endl;
    cout << "4. �޸ĳɼ�" << endl;
    cout << "5. ��ӿ�Ŀ" << endl;
    cout << "6. ɾ����Ŀ" << endl;
    cout << "7. չʾ��" << endl;
    cout << "8. ����Ŀ����" << endl;
    cout << "9. ����ƽ����" << endl;
    cout << "0. �˳�ϵͳ" << endl;
    cout << "=============================" << endl;
    cout << "��ѡ�����: ";
}

int main() {
    GradeForm form;
    int choice;

    // ���һЩ��ʼ����
    form.addColumn("��ѧ", true);
    form.addColumn("Ӣ��", true);
    form.addStudent(make_unique<RegularStudent>("����", "2023001"));
    form.addStudent(make_unique<RegularStudent>("����", "2023002"));
    form.addStudent(make_unique<AuditStudent>("����", "2023003"));

    do {
        displayMenu();
        cin >> choice;

        // ������뻺����
        cin.ignore();

        switch (choice) {
            case 1: { // ���ѧ��
                string name, id;
                int type;

                cout << "����ѧ������: ";
                getline(cin, name);
                cout << "����ѧ��: ";
                getline(cin, id);
                cout << "ѡ������ (1.��ͨѧ�� 2.����ѧ��): ";
                cin >> type;
                cin.ignore();

                if (type == 1) {
                    form.addStudent(make_unique<RegularStudent>(name, id));
                } else if (type == 2) {
                    form.addStudent(make_unique<AuditStudent>(name, id));
                } else {
                    cout << "��Ч��ѡ��!" << endl;
                }
                break;
            }
            case 2: { // ɾ��ѧ��
                string id;
                cout << "����Ҫɾ��ѧ����ѧ��: ";
                getline(cin, id);
                form.deleteStudent(id);
                break;
            }
            case 3: { // ��ѯѧ��
                string id;
                cout << "����Ҫ��ѯѧ����ѧ��: ";
                getline(cin, id);
                form.findStudent(id);
                break;
            }
            case 4: { // �޸ĳɼ�
                string id, newValue;
                int colIndex;

                cout << "����ѧ��ѧ��: ";
                getline(cin, id);

                form.displayColumns();
                cout << "����Ҫ�޸ĵ�������: ";
                cin >> colIndex;
                cin.ignore();

                cout << "������ֵ: ";
                getline(cin, newValue);

                form.updateGrade(id, colIndex, newValue);
                break;
            }
            case 5: { // ��ӿ�Ŀ
                string subject;
                cout << "�����¿�Ŀ����: ";
                getline(cin, subject);
                form.addColumn(subject, true);
                cout << "����ӿ�Ŀ: " << subject << endl;
                break;
            }
            case 6: { // ɾ����Ŀ
                form.displayColumns();
                int colIndex;
                cout << "����Ҫɾ���Ŀ�Ŀ����: ";
                cin >> colIndex;
                cin.ignore();
                form.deleteColumn(colIndex);
                break;
            }
            case 7: // չʾ��
                form.display();
                break;
            case 8: { // ����Ŀ����
                form.displayColumns();
                int colIndex;
                cout << "����Ҫ�����������: ";
                cin >> colIndex;
                cin.ignore();
                form.sortByColumn(colIndex);
                break;
            }
            case 9: { // ����ƽ����
                form.displayColumns();
                int colIndex;
                cout << "����Ҫ����ƽ���ֵĿ�Ŀ����: ";
                cin >> colIndex;
                cin.ignore();
                form.calculateAverage(colIndex);
                break;
            }
            case 0: // �˳�ϵͳ
                cout << "��лʹ��ѧ���ɼ�����ϵͳ���ټ�!" << endl;
                break;
            default:
                cout << "��Ч��ѡ������������!" << endl;
        }

        if (choice != 0) {
            cout << "\n���س�������...";
            cin.ignore();
        }
    } while (choice != 0);

    return 0;
}