#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <map>
#include <iomanip>
#include <memory>

using namespace std;

// ������Կ���
#define TEST_MODE 1

// ���ࣺ�ɼ���Ա
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

    string getName() const { return xingming; }
    string getID() const { return xuehao; }

    // ��������أ���ѧ������
    bool operator<(const ChengJiMember& other) const {
        return xuehao < other.xuehao;
    }
};

// ��ͨѧ����
class PuTongStudent : public ChengJiMember {
private:
    map<string, double> chengji; // ��Ŀ-�ɼ�ӳ��
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
        cout << "[��ͨ��]" << endl;
    }

    double getKemuScore(const string& kemu) const override {
        auto it = chengji.find(kemu);
        return (it != chengji.end()) ? it->second : 0.0;
    }

    void xiugaiScore(const string& kemu, double score) override {
        chengji[kemu] = score;
    }

    // ��ӿ�Ŀ�ɼ������ڳ�ʼ����
    void addSubject(const string& kemu) {
        if (chengji.find(kemu) == chengji.end()) {
            chengji[kemu] = 0.0;
        }
    }

    // ɾ����Ŀ
    void removeSubject(const string& kemu) {
        chengji.erase(kemu);
    }
};

// ����ѧ����
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
        cout << "[������]" << endl;
    }

    double getKemuScore(const string& kemu) const override {
        auto it = chengji.find(kemu);
        return (it != chengji.end()) ? it->second : 0.0;
    }

    void xiugaiScore(const string& kemu, double score) override {
        chengji[kemu] = score;
    }

    void addSubject(const string& kemu) {
        if (chengji.find(kemu) == chengji.end()) {
            chengji[kemu] = 0.0;
        }
    }

    void removeSubject(const string& kemu) {
        chengji.erase(kemu);
    }
};

// �ɼ�����ϵͳ
class ChengJiGuanLi {
private:
    vector<unique_ptr<ChengJiMember>> xueshengList; // ѧ���б�
    vector<string> kemuList; // ��Ŀ�б�

public:
    // ���ѧ��
    void addStudent(bool isPutong, const string& name, const string& id) {
        if (isPutong) {
            xueshengList.push_back(make_unique<PuTongStudent>(name, id));
        } else {
            xueshengList.push_back(make_unique<PangTingStudent>(name, id));
        }
        // Ϊ��ѧ����ʼ�����п�Ŀ
        for (const auto& kemu : kemuList) {
            xueshengList.back()->addSubject(kemu);
        }
    }

    // ɾ��ѧ��
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

    // ��ѯѧ��
    ChengJiMember* findStudent(const string& key) {
        for (auto& s : xueshengList) {
            if (s->getID() == key || s->getName() == key) {
                return s.get();
            }
        }
        return nullptr;
    }

    // ��ӿ�Ŀ
    void addSubject(const string& kemu) {
        if (find(kemuList.begin(), kemuList.end(), kemu) == kemuList.end()) {
            kemuList.push_back(kemu);
            // Ϊ����ѧ������¿�Ŀ
            for (auto& s : xueshengList) {
                s->addSubject(kemu);
            }
        }
    }

    // ɾ����Ŀ
    void delSubject(const string& kemu) {
        auto it = find(kemuList.begin(), kemuList.end(), kemu);
        if (it != kemuList.end()) {
            kemuList.erase(it);
            // ������ѧ����ɾ���ÿ�Ŀ
            for (auto& s : xueshengList) {
                s->removeSubject(kemu);
            }
        }
    }

    // �޸ĳɼ�
    void modScore(const string& stuKey, const string& kemu, double score) {
        auto stu = findStudent(stuKey);
        if (stu) {
            // ����Ŀ�Ƿ����
            if (find(kemuList.begin(), kemuList.end(), kemu) != kemuList.end()) {
                stu->xiugaiScore(kemu, score);
            }
        }
    }

    // չʾ��
    void display(bool byID = true, const string& sortKemu = "") {
        // ����ָ����������
        vector<ChengJiMember*> tempList;
        for (auto& s : xueshengList) {
            tempList.push_back(s.get());
        }

        // �����߼�
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

        // ��ӡ��ͷ
        cout << "\nѧ��      ����      ";
        for (const auto& k : kemuList) {
            cout << setw(10) << k;
        }
        cout << "����" << endl;
        cout << string(20 + kemuList.size()*10, '-') << endl;

        // ��ӡѧ������
        for (auto s : tempList) {
            s->xianshi(kemuList);
        }

        // ����ƽ����
        cout << "\nƽ����:   ";
        for (const auto& k : kemuList) {
            double sum = 0;
            for (auto s : tempList) {
                sum += s->getKemuScore(k);
            }
            cout << setw(10) << fixed << setprecision(1) << (sum / tempList.size());
        }
        cout << endl << endl;
    }

    // ���ɲ�������
    void generateTestData() {
        addSubject("����");
        addSubject("��ѧ");
        addSubject("Ӣ��");

        addStudent(true, "����", "2023001");
        modScore("2023001", "����", 85.5);
        modScore("2023001", "��ѧ", 92.0);
        modScore("2023001", "Ӣ��", 78.5);

        addStudent(true, "����", "2023002");
        modScore("2023002", "����", 76.0);
        modScore("2023002", "��ѧ", 88.5);
        modScore("2023002", "Ӣ��", 92.5);

        addStudent(false, "����", "2023003");
        modScore("2023003", "����", 92.5);
        modScore("2023003", "��ѧ", 65.0);
        modScore("2023003", "Ӣ��", 85.0);
    }
};

// �û������˵�
void userMenu() {
    ChengJiGuanLi manager;

#if TEST_MODE
    manager.generateTestData();
    cout << "�Ѽ��ز�������\n";
#endif

    while (true) {
        cout << "\n===== ѧ���ɼ�����ϵͳ =====\n";
        cout << "1. ����ѧ��\n";
        cout << "2. ɾ��ѧ��\n";
        cout << "3. ��ѯѧ��\n";
        cout << "4. �޸ĳɼ�\n";
        cout << "5. չʾ��\n";
        cout << "6. ��ӿ�Ŀ\n";
        cout << "7. ɾ����Ŀ\n";
        cout << "0. �˳�ϵͳ\n";
        cout << "��ѡ�����: ";

        int choice;
        cin >> choice;

        string name, id, kemu;
        double score;
        ChengJiMember* stu;

        switch (choice) {
            case 1: {
                cout << "ѧ������ (1.��ͨ 2.����): ";
                int type;
                cin >> type;
                cout << "����: ";
                cin >> name;
                cout << "ѧ��: ";
                cin >> id;
                manager.addStudent(type == 1, name, id);
                cout << "��ӳɹ�!\n";
                break;
            }
            case 2: {
                cout << "����ѧ��: ";
                cin >> id;
                if (manager.delStudent(id)) {
                    cout << "ɾ���ɹ�!\n";
                } else {
                    cout << "ѧ�Ų�����!\n";
                }
                break;
            }
            case 3: {
                cout << "����ѧ�Ż�����: ";
                cin >> id;
                stu = manager.findStudent(id);
                if (stu) {
                    cout << "�ҵ�ѧ��: " << stu->getName()
                         << "(" << stu->getID() << ")\n";
                } else {
                    cout << "δ�ҵ�ѧ��!\n";
                }
                break;
            }
            case 4: {
                cout << "����ѧ�Ż�����: ";
                cin >> id;
                cout << "�����Ŀ: ";
                cin >> kemu;
                cout << "�����³ɼ�: ";
                cin >> score;
                manager.modScore(id, kemu, score);
                cout << "�޸ĳɹ�!\n";
                break;
            }
            case 5: {
                cout << "����ʽ (1.ѧ�� 2.��Ŀ�ɼ�): ";
                int sortType;
                cin >> sortType;
                if (sortType == 2) {
                    cout << "���������Ŀ: ";
                    cin >> kemu;
                    manager.display(false, kemu);
                } else {
                    manager.display();
                }
                break;
            }
            case 6: {
                cout << "�����¿�Ŀ����: ";
                cin >> kemu;
                manager.addSubject(kemu);
                cout << "��ӳɹ�!\n";
                break;
            }
            case 7: {
                cout << "����ɾ����Ŀ����: ";
                cin >> kemu;
                manager.delSubject(kemu);
                cout << "ɾ���ɹ�!\n";
                break;
            }
            case 0:
                cout << "ϵͳ���˳�!\n";
                return;
            default:
                cout << "��Чѡ������������!\n";
        }
    }
}

int main() {
    userMenu();
    return 0;
}