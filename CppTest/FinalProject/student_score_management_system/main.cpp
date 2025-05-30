#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <map>

using namespace std;

// ������������
class DataItem {
public:
    virtual ~DataItem() {}
    virtual void show() const = 0;
    virtual string csvFormat() const = 0;
    virtual bool contains(const string& term) const = 0;
};

// ѧ���ɼ���
class Student : public DataItem {
private:
    string fullName;
    string studentID;
    map<string, double> grades;

public:
    Student(string name, string id) : fullName(name), studentID(id) {}

    // �Ƚ��������������find
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
        cout << "�ܷ�:" << setw(6) << calculateTotal() << endl;
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

// �ɼ�����
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
            cout << "����ѧ�� " << student.getID() << " �Ѵ��ڣ�" << endl;
            return;
        }
        students.push_back(student);
        cout << "�����ѧ��: " << student.getName() << endl;
    }

    void removeStudent(const string& id) {
        auto it = find_if(students.begin(), students.end(),
                         [&](const Student& s) { return s.getID() == id; });

        if (it != students.end()) {
            cout << "ɾ��ѧ��: " << it->getName() << " (" << it->getID() << ")" << endl;
            students.erase(it);
        } else {
            cout << "δ�ҵ�ѧ��: " << id << endl;
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
            cout << "δ�ҵ�ƥ���ѧ����¼" << endl;
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
                    cout << "�Ѹ��� " << s.getName() << " ��" << subject << "�ɼ�: " << score << endl;
                } else {
                    cout << "���󣺿�Ŀ '" << subject << "' ������" << endl;
                }
                break;
            }
        }

        if (!studentFound) {
            cout << "δ�ҵ�ѧ��: " << id << endl;
        }
    }

    void addSubject(const string& subject) {
        if (find(subjectsList.begin(), subjectsList.end(), subject) != subjectsList.end()) {
            cout << "��Ŀ�Ѵ��ڣ�" << endl;
            return;
        }
        subjectsList.push_back(subject);

        // ��ʼ��
        for (auto& s : students) {
            s.updateGrade(subject, 0.0);
        }
        cout << "����ӿ�Ŀ: " << subject << endl;
    }

    void removeSubject(const string& subject) {
        auto it = find(subjectsList.begin(), subjectsList.end(), subject);
        if (it != subjectsList.end()) {
            subjectsList.erase(it);
            for (auto& s : students) {
                s.removeSubjectGrade(subject);
            }
            cout << "���Ƴ���Ŀ: " << subject << endl;
        } else {
            cout << "���󣺿�Ŀ������" << endl;
        }
    }

    void display(bool showAvg = true) {
        cout << "\n=== " << sheetTitle << " ===" << endl;
        cout << left << setw(15) << "����" << setw(15) << "ѧ��";
        for (const auto& sub : subjectsList) {
            cout << setw(15) << sub;
        }
        cout << setw(15) << "�ܷ�" << endl;
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
            cout << left << setw(30) << "ƽ����";
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
        // ����
        if (field == "ѧ��") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getID() < b.getID() : a.getID() > b.getID();
                });
        } else if (field == "����") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.getName() < b.getName() : a.getName() > b.getName();
                });
        } else if (field == "�ܷ�") {
            sort(students.begin(), students.end(),
                [&](const Student& a, const Student& b) {
                    return ascending ? a.calculateTotal() < b.calculateTotal()
                                     : a.calculateTotal() > b.calculateTotal();
                });
        } else {
            // ��Ŀ
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
            cerr << "�ļ���ʧ��: " << filename << endl;
            return;
        }

        outFile << "����,ѧ��";
        for (const auto& sub : subjectsList) {
            outFile << "," << sub;
        }
        outFile << endl;

        for (const auto& s : students) {
            outFile << s.csvFormat() << endl;
        }

        cout << "�����ѵ�����: " << filename << endl;
        outFile.close();
    }

    void importFromCSV(const string& filename) {
        ifstream inFile(filename);
        if (!inFile) {
            cerr << "�޷����ļ�: " << filename << endl;
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
                cerr << "��Ч�ļ���ʽ" << endl;
                return;
            }

            // ����\ѧ��+N*��Ŀ
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
                    cerr << "�ɼ�ת������: " << rowData[i+2] << endl;
                }
            }
            students.push_back(s);
        }

        cout << "�ѵ��� " << students.size() << " ����¼" << endl;
        inFile.close();
    }

    const string& getTitle() const { return sheetTitle; }
    const vector<string>& getSubjects() const { return subjectsList; }
};

// �ɼ�����ϵͳ
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
            cout << "���Ѵ��ڣ�" << endl;
            return;
        }
        sheets.emplace_back(title);
        cout << "�Ѵ�����: " << title << endl;
    }

    void removeSheet(const string& title) {
        int index = findSheetIndex(title);
        if (index != -1) {
            sheets.erase(sheets.begin() + index);
            cout << "��ɾ����: " << title << endl;
        } else {
            cout << "�������ڣ�" << endl;
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
            cout << "��ǰû�б�" << endl;
            return;
        }

        cout << "\n���б�:" << endl;
        for (const auto& sheet : sheets) {
            cout << "- " << sheet.getTitle() << " (" << sheet.getSubjects().size() << "����Ŀ)" << endl;
        }
    }
};

// �˵�ϵͳ
void showMainMenu() {
    cout << "\n===== ѧ���ɼ�����ϵͳ =====";
    cout << "\n1. �½���";
    cout << "\n2. ɾ����";
    cout << "\n3. �����";
    cout << "\n4. ���б�";
    cout << "\n5. ����CSV";
    cout << "\n6. ����CSV";
    cout << "\n0. �˳�ϵͳ";
    cout << "\n=========================";
    cout << "\n��ѡ��: ";
}

void showSheetMenu() {
    cout << "\n===== ������ =====";
    cout << "\n1. ���ѧ��";
    cout << "\n2. ɾ��ѧ��";
    cout << "\n3. ����ѧ��";
    cout << "\n4. �޸ĳɼ�";
    cout << "\n5. ��ӿ�Ŀ";
    cout << "\n6. ɾ����Ŀ";
    cout << "\n7. ��ʾ��";
    cout << "\n8. ������ʾ";
    cout << "\n0. �������˵�";
    cout << "\n==================";
    cout << "\n��ѡ�����: ";
}

int main() {
    GradeManager manager;

    while (true) {
        showMainMenu();
        int choice;
        cin >> choice;

        if (choice == 0) {
            cout << "ϵͳ���˳�" << endl;
            break;
        }

        switch (choice) {
            case 1: { // �½���
                string title;
                cout << "���������: ";
                cin >> title;
                manager.createSheet(title);
                break;
            }
            case 2: { // ɾ����
                string title;
                cout << "����Ҫɾ���ı�����: ";
                cin >> title;
                manager.removeSheet(title);
                break;
            }
            case 3: { // �����
                string title;
                cout << "���������: ";
                cin >> title;
                GradeSheet* sheet = manager.getSheet(title);

                if (!sheet) {
                    cout << "�������ڣ�" << endl;
                    break;
                }

                while (true) {
                    showSheetMenu();
                    int sheetChoice;
                    cin >> sheetChoice;

                    if (sheetChoice == 0) break;

                    switch (sheetChoice) {
                        case 1: { // ���ѧ��
                            string name, id;
                            cout << "ѧ������: ";
                            cin >> name;
                            cout << "ѧ��ѧ��: ";
                            cin >> id;
                            sheet->addStudentRecord(Student(name, id));
                            break;
                        }
                        case 2: { // ɾ��ѧ��
                            string id;
                            cout << "����ѧ��: ";
                            cin >> id;
                            sheet->removeStudent(id);
                            break;
                        }
                        case 3: { // ����ѧ��
                            string term;
                            cout << "����������ѧ��: ";
                            cin >> term;
                            sheet->searchStudents(term);
                            break;
                        }
                        case 4: { // �޸ĳɼ�
                            string id, subject;
                            double score;
                            cout << "ѧ��ѧ��: ";
                            cin >> id;
                            cout << "��Ŀ����: ";
                            cin >> subject;
                            cout << "�³ɼ�: ";
                            cin >> score;
                            sheet->updateGrade(id, subject, score);
                            break;
                        }
                        case 5: { // ��ӿ�Ŀ
                            string subject;
                            cout << "�¿�Ŀ����: ";
                            cin >> subject;
                            sheet->addSubject(subject);
                            break;
                        }
                        case 6: { // ɾ����Ŀ
                            string subject;
                            cout << "Ҫɾ���Ŀ�Ŀ: ";
                            cin >> subject;
                            sheet->removeSubject(subject);
                            break;
                        }
                        case 7:
                            sheet->display(true);
                            break;
                        case 8: {
                            string field;
                            cout << "��������(����/ѧ��/�ܷ�/��Ŀ): ";
                            cin >> field;
                            sheet->sortAndShow(field);
                            break;
                        }
                        default:
                            cout << "��Ч������" << endl;
                    }
                }
                break;
            }
            case 4:
                manager.listSheets();
                break;
            case 5: { // ����CSV
                string title, filename;
                cout << "������: ";
                cin >> title;
                cout << "CSV�ļ���: ";
                cin >> filename;
                manager.createSheet(title);
                GradeSheet* sheet = manager.getSheet(title);
                if (sheet) {
                    sheet->importFromCSV(filename);
                }
                break;
            }
            case 6: { // ����CSV
                string title, filename;
                cout << "������: ";
                cin >> title;
                GradeSheet* sheet = manager.getSheet(title);
                if (!sheet) {
                    cout << "�������ڣ�" << endl;
                    break;
                }
                cout << "�����ļ���: ";
                cin >> filename;
                sheet->exportToCSV(filename);
                break;
            }
            default:
                cout << "��Чѡ��" << endl;
        }
    }

    return 0;
}