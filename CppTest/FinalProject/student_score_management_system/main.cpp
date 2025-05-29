#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <map>

using namespace std;

// ��̬���������
class DataItem {
public:
    virtual ~DataItem() = default;
    virtual void display() const = 0;
    virtual string toCSV() const = 0;
    virtual bool match(const string& keyword) const = 0;
};

// ѧ���ɼ���
class Student : public DataItem {
private:
    string name;
    string id;
    map<string, double> scores;

public:
    Student(string n, string i) : name(n), id(i) {}

    // ��������أ��Ƚ�ѧ��ID������find��
    bool operator==(const Student& other) const {
        return id == other.id;
    }

    // ���óɼ�
    void setScore(const string& subject, double score) {
        scores[subject] = score;
    }

    // ɾ����Ŀ�ɼ�
    void removeScore(const string& subject) {
        scores.erase(subject);
    }

    // ��ȡ�ܷ�
    double getTotal() const {
        double total = 0.0;
        for (const auto& s : scores) {
            total += s.second;
        }
        return total;
    }

    // ��ȡָ����Ŀ�ɼ�
    double getScore(const string& subject) const {
        auto it = scores.find(subject);
        return (it != scores.end()) ? it->second : -1.0;
    }

    // ��ʾѧ����Ϣ
    void display() const override {
        cout << left << setw(15) << name << setw(15) << id;
        for (const auto& s : scores) {
            cout << setw(10) << s.first << ":" << setw(5) << s.second;
        }
        cout << "�ܷ�:" << setw(6) << getTotal() << endl;
    }

    // ת��ΪCSV��ʽ
    string toCSV() const override {
        ostringstream oss;
        oss << name << "," << id;
        for (const auto& s : scores) {
            oss << "," << s.second;
        }
        return oss.str();
    }

    // ƥ���ѯ
    bool match(const string& keyword) const override {
        return name.find(keyword) != string::npos || id.find(keyword) != string::npos;
    }

    const string& getName() const { return name; }
    const string& getId() const { return id; }
    const map<string, double>& getScores() const { return scores; }
};

// ��������
class GradeForm {
private:
    string formName;
    vector<Student> students;
    vector<string> subjects;

public:
    GradeForm(string name) : formName(name) {
        subjects = {};
    }

    // ���ѧ��
    void addStudent(const Student& student) {
        // ���ѧ���Ƿ��ظ�
        auto it = find(students.begin(), students.end(), student);
        if (it != students.end()) {
            cout << "����ѧ�� " << student.getId() << " �Ѵ��ڣ�" << endl;
            return;
        }
        students.push_back(student);
        cout << "ѧ�� " << student.getName() << " ��ӳɹ�" << endl;
    }

    // ɾ��ѧ��
    void removeStudent(const string& id) {
        auto it = find_if(students.begin(), students.end(),
                         [&](const Student& s) { return s.getId() == id; });

        if (it != students.end()) {
            cout << "ɾ��ѧ��: " << it->getName() << endl;
            students.erase(it);
        } else {
            cout << "δ�ҵ�ѧ��Ϊ " << id << " ��ѧ��" << endl;
        }
    }

    // ��ѯѧ��
    void queryStudent(const string& keyword) {
        bool found = false;
        for (const auto& s : students) {
            if (s.match(keyword)) {
                s.display();
                found = true;
            }
        }
        if (!found) {
            cout << "δ�ҵ�ƥ���ѧ��" << endl;
        }
    }

    // �޸ĳɼ�
    void modifyScore(const string& id, const string& subject, double score) {
        for (auto& s : students) {
            if (s.getId() == id) {
                if (find(subjects.begin(), subjects.end(), subject) != subjects.end()) {
                    s.setScore(subject, score);
                    cout << "�ɹ��޸� " << s.getName() << " ��" << subject << "�ɼ�Ϊ: " << score << endl;
                } else {
                    cout << "��Ŀ�����ڣ�������ӿ�Ŀ" << endl;
                }
                return;
            }
        }
        cout << "δ�ҵ�ѧ��Ϊ " << id << " ��ѧ��" << endl;
    }

    // ��ӿ�Ŀ
    void addSubject(const string& subject) {
        if (find(subjects.begin(), subjects.end(), subject) != subjects.end()) {
            cout << "��Ŀ�Ѵ��ڣ�" << endl;
            return;
        }
        subjects.push_back(subject);
        // ����ѧ������¿�Ŀ����ʼ0�֣�
        for (auto& s : students) {
            s.setScore(subject, 0.0);
        }
        cout << "����ӿ�Ŀ: " << subject << endl;
    }

    // ɾ����Ŀ
    void removeSubject(const string& subject) {
        auto it = find(subjects.begin(), subjects.end(), subject);
        if (it != subjects.end()) {
            subjects.erase(it);
            // ɾ������ѧ���ÿ�Ŀ�ɼ�
            for (auto& s : students) {
                s.removeScore(subject);
            }
            cout << "��ɾ����Ŀ: " << subject << endl;
        } else {
            cout << "��Ŀ�����ڣ�" << endl;
        }
    }

    // չʾ��
    void display(bool showAverage = false) {
        // ��ʾ��ͷ
        cout << "\n��: " << formName << endl;
        cout << left << setw(15) << "����" << setw(15) << "ѧ��";
        for (const auto& sub : subjects) {
            cout << setw(15) << sub;
        }
        cout << setw(15) << "�ܷ�" << endl;
        cout << string(15*(subjects.size()+2), '-') << endl;

        // ��ʾѧ������
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

        // ��ʾƽ����
        if (showAverage && !students.empty()) {
            cout << string(15*(subjects.size()+2), '-') << endl;
            cout << left << setw(30) << "ƽ����"; // ��ռ������+ѧ�Ų۳���
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

    // ����չʾ
    void sortAndDisplay(const string& criteria, bool ascending = true) {
        if (criteria == "ѧ��") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getId() < b.getId() : a.getId() > b.getId();
                });
        } else if (criteria == "����") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getName() < b.getName() : a.getName() > b.getName();
                });
        } else if (criteria == "�ܷ�") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getTotal() < b.getTotal() : a.getTotal() > b.getTotal();
                });
        } else {
            // ����Ŀ����
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    double scoreA = a.getScore(criteria);
                    double scoreB = b.getScore(criteria);
                    return ascending ? scoreA < scoreB : scoreA > scoreB;
                });
        }
        display(true);
    }

    // ���浽CSV
    void saveToCSV(const string& filename) {
        ofstream file(filename);
        if (!file.is_open()) {
            cerr << "�޷����ļ�: " << filename << endl;
            return;
        }

        // ��ͷ
        file << "����,ѧ��";
        for (const auto& sub : subjects) {
            file << "," << sub;
        }
        file << endl;

        // ����
        for (const auto& s : students) {
            file << s.toCSV() << endl;
        }

        cout << "�ɹ����浽 " << filename << endl;
        file.close();
    }

    // ��CSV����
    void loadFromCSV(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            cerr << "�޷����ļ�: " << filename << endl;
            return;
        }

        students.clear();
        subjects.clear();

        string line;
        // ��ͷ
        if (getline(file, line)) {
            stringstream ss(line);
            string cell;
            vector<string> headers;

            while (getline(ss, cell, ',')) {
                headers.push_back(cell);
            }

            // ǰ������������ѧ�ţ������ǿ�Ŀ
            if (headers.size() >= 2) {
                subjects = vector<string>(headers.begin() + 2, headers.end());
            }
        }

        // ����
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
                        // ת��ʧ��ʱ����
                    }
                }
                students.push_back(s);
            }
        }

        cout << "�ɹ��� " << filename << " ���� " << students.size() << " ����¼" << endl;
        file.close();
    }

    const string& getName() const { return formName; }
    const vector<string>& getSubjects() const { return subjects; }
};

// �ɼ�����ϵͳ
class GradeSystem {
private:
    vector<GradeForm> forms;

    // ���ұ�����
    int findFormIndex(const string& name) {
        for (int i = 0; i < forms.size(); i++) {
            if (forms[i].getName() == name) {
                return i;
            }
        }
        return -1;
    }

public:
    // �����±�
    void createForm(const string& name) {
        if (findFormIndex(name) != -1) {
            cout << "���Ѵ��ڣ�" << endl;
            return;
        }
        forms.emplace_back(name);
        cout << "�Ѵ�����: " << name << endl;
    }

    // ɾ����
    void removeForm(const string& name) {
        int index = findFormIndex(name);
        if (index != -1) {
            forms.erase(forms.begin() + index);
            cout << "��ɾ����: " << name << endl;
        } else {
            cout << "�������ڣ�" << endl;
        }
    }

    // ��ȡ��
    GradeForm* getForm(const string& name) {
        int index = findFormIndex(name);
        if (index != -1) {
            // ���ﴫ��ָ��ȽϺã�������find���ص�����
            return &forms[index];
        }
        return nullptr;
    }

    // ��ʾ���б�
    void listForms() {
        if (forms.empty()) {
            cout << "��ǰû�б�" << endl;
            return;
        }

        cout << "\n���ñ�:" << endl;
        for (const auto& form : forms) {
            cout << "- " << form.getName() << " (��Ŀ��: " << form.getSubjects().size() << ")" << endl;
        }
    }
};

// ��ʾ���˵�
void displayMainMenu() {
    cout << "\n===== ѧ���ɼ�����ϵͳ =====";
    cout << "\n1. ������";
    cout << "\n2. ɾ����";
    cout << "\n3. �����";
    cout << "\n4. �г����б�";
    cout << "\n5. ��CSV����";
    cout << "\n6. ������CSV";
    cout << "\n0. �˳�";
    cout << "\n=========================";
    cout << "\n��ѡ�����: ";
}

// ��ʾ������˵�
void displayFormMenu() {
    cout << "\n===== ������ =====";
    cout << "\n1. ���ѧ��";
    cout << "\n2. ɾ��ѧ��";
    cout << "\n3. ��ѯѧ��";
    cout << "\n4. �޸ĳɼ�";
    cout << "\n5. ��ӿ�Ŀ";
    cout << "\n6. ɾ����Ŀ";
    cout << "\n7. չʾ��";
    cout << "\n8. ����չʾ";
    cout << "\n0. �������˵�";
    cout << "\n==================";
    cout << "\n��ѡ�����: ";
}

int main() {
    GradeSystem system;

    while (true) {
        displayMainMenu();
        int choice;
        cin >> choice;
        if (choice == 0) break;
        switch (choice) {
            case 1: { // ������
                string name;
                cout << "�����±�����: ";
                cin >> name;
                system.createForm(name);
                break;
            }
            case 2: { // ɾ����
                string name;
                cout << "����Ҫɾ���ı�����: ";
                cin >> name;
                system.removeForm(name);
                break;
            }
            case 3: { // �����
                string sheet_name;
                cout << "����Ҫ����ı�����: ";
                cin >> sheet_name;
                GradeForm* form = system.getForm(sheet_name);
                if (!form) {
                    cout << "�������ڣ�" << endl;
                    break;
                }
                while (true) {
                    displayFormMenu();
                    int formChoice;
                    cin >> formChoice;
                    if (formChoice == 0) break;
                    switch (formChoice) {
                        case 1: { // ���ѧ��
                            string stu_name, id;
                            cout << "����ѧ������: ";
                            cin >> stu_name;
                            cout << "����ѧ��ѧ��: ";
                            cin >> id;
                            form->addStudent(Student(stu_name, id));
                            break;
                        }
                        case 2: { // ɾ��ѧ��
                            string id;
                            cout << "����Ҫɾ����ѧ��ѧ��: ";
                            cin >> id;
                            form->removeStudent(id);
                            break;
                        }
                        case 3: { // ��ѯѧ��
                            string keyword;
                            cout << "����������ѧ��: ";
                            cin >> keyword;
                            form->queryStudent(keyword);
                            break;
                        }
                        case 4: { // �޸ĳɼ�
                            string id, subject;
                            double score;
                            cout << "����ѧ��ѧ��: ";
                            cin >> id;
                            cout << "�����Ŀ����: ";
                            cin >> subject;
                            cout << "�����³ɼ�: ";
                            cin >> score;
                            form->modifyScore(id, subject, score);
                            break;
                        }
                        case 5: { // ��ӿ�Ŀ
                            string subject;
                            cout << "�����¿�Ŀ����: ";
                            cin >> subject;
                            form->addSubject(subject);
                            break;
                        }
                        case 6: { // ɾ����Ŀ
                            string subject;
                            cout << "����Ҫɾ���Ŀ�Ŀ����: ";
                            cin >> subject;
                            form->removeSubject(subject);
                            break;
                        }
                        case 7: // չʾ��
                            form->display(true);
                            break;
                        case 8: { // ����չʾ
                            string criteria;
                            cout << "������������(����/ѧ��/�ܷ�/��Ŀ��): ";
                            cin >> criteria;
                            form->sortAndDisplay(criteria);
                            break;
                        }
                        default:
                            cout << "��Чѡ��" << endl;
                    }
                }
                break;
            }
            case 4: // �г����б�
                system.listForms();
                break;
            case 5: { // ��CSV����
                string formName, filename;
                cout << "���������: ";
                cin >> formName;
                cout << "����CSV�ļ���: ";
                cin >> filename;
                system.createForm(formName);
                GradeForm* form = system.getForm(formName);
                if (form) {
                    form->loadFromCSV(filename);
                }
                break;
            }
            case 6: { // ������CSV
                string formName, filename;
                cout << "���������: ";
                cin >> formName;
                GradeForm* form = system.getForm(formName);
                if (!form) {
                    cout << "�������ڣ�" << endl;
                    break;
                }
                cout << "���뱣���ļ���: ";
                cin >> filename;
                form->saveToCSV(filename);
                break;
            }
            default:
                cout << "��Чѡ��" << endl;
        }
    }

    cout << "ϵͳ���˳�" << endl;
    return 0;
}