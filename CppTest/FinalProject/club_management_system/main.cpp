#include <iostream>
#include <vector>
#include <algorithm>
#include <cctype>
#include <iomanip>
#include <memory>
#include <set>

using namespace std;

// ��Ա����
class ChengYuan {
protected:
    string xuehao;      // ѧ��
    string mingzi;      // ����
    string zhiwei;      // ְλ
    int weidaoCount = 0; // δ������

public:
    ChengYuan(const string& xh, const string& mz, const string& zw)
        : xuehao(xh), mingzi(mz), zhiwei(zw) {}

    virtual ~ChengYuan() {}

    // �麯��չʾ��Ϣ
    virtual void xianshi() const {
        cout << left << setw(12) << xuehao
             << setw(10) << mingzi
             << setw(10) << zhiwei
             << "ȱϯ:" << weidaoCount << "��";
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

// ��ͨ��Ա��
class PuTong : public ChengYuan {
public:
    PuTong(const string& xh, const string& mz)
        : ChengYuan(xh, mz, "��ͨ��Ա") {}

    void xianshi() const override {
        cout << "[��ͨ] ";
        ChengYuan::xianshi();
    }

    int getType() const override { return 1; }
};

// �ɲ���Ա��
class GanBu : public ChengYuan {
public:
    GanBu(const string& xh, const string& mz, const string& zw)
        : ChengYuan(xh, mz, zw) {}

    void xianshi() const override {
        cout << "[�ɲ�] ";
        ChengYuan::xianshi();
    }

    int getType() const override { return 2; }
};

// ���Ź�����
class SheTuan {
private:
    vector<unique_ptr<ChengYuan>> chengyuanList;

public:
    // ���� += ��ӳ�Ա
    SheTuan& operator+=(unique_ptr<ChengYuan> cy) {
        chengyuanList.push_back(move(cy));
        return *this;
    }

    // ���� -= ɾ����Ա
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

    // ���� << ������г�Ա
    friend ostream& operator<<(ostream& os, const SheTuan& st) {
        if (st.chengyuanList.empty()) {
            os << "���޳�Ա��Ϣ\n";
            return os;
        }

        // �����Ȱ������ٰ�ѧ��
        vector<ChengYuan*> temp;
        for (const auto& c : st.chengyuanList) {
            temp.push_back(c.get());
        }

        sort(temp.begin(), temp.end(), [](ChengYuan* a, ChengYuan* b) {
            if (a->getType() != b->getType())
                return a->getType() > b->getType();
            return a->getXuehao() < b->getXuehao();
        });

        os << "======== ���ų�Ա�б� ========\n";
        for (const auto& c : temp) {
            c->xianshi();
            os << endl;
        }
        return os;
    }

    // ���ҳ�Ա
    ChengYuan* find(const string& key) {
        for (auto& c : chengyuanList) {
            if (c->getXuehao() == key ||
                c->getMingzi().find(key) != string::npos) {
                return c.get();
            }
        }
        return nullptr;
    }

    // ���ѧ���Ƿ����
    bool xuehaoExists(const string& xh) {
        return any_of(chengyuanList.begin(), chengyuanList.end(),
            [&](const unique_ptr<ChengYuan>& c) {
                return c->getXuehao() == xh;
            });
    }

    // ��ȡ���г�Ա
    vector<ChengYuan*> getAll() const {
        vector<ChengYuan*> result;
        for (const auto& c : chengyuanList) {
            result.push_back(c.get());
        }
        return result;
    }
};

// �ǩ������
void huodongCheck(SheTuan& st) {
    set<string> qiandaoSet;
    string input;

    cout << "\n==== �ǩ�� ====\n"
         << "����ѧ��ǩ�� (exit����)\n";

    while (true) {
        cout << "> ";
        cin >> input;
        if (input == "exit") break;

        ChengYuan* c = st.find(input);
        if (c) {
            qiandaoSet.insert(c->getXuehao());
            cout << c->getMingzi() << " ǩ���ɹ�\n";
        } else {
            cout << "δ�ҵ���Ա������������\n";
        }
    }

    // ͳ��δ����Ա
    vector<ChengYuan*> weidaoList;
    for (auto c : st.getAll()) {
        if (qiandaoSet.find(c->getXuehao()) == qiandaoSet.end()) {
            weidaoList.push_back(c);
            c->addWeidao();
        }
    }

    // ���������ͺ�ѧ��
    sort(weidaoList.begin(), weidaoList.end(),
        [](ChengYuan* a, ChengYuan* b) {
            if (a->getType() != b->getType())
                return a->getType() > b->getType();
            return a->getXuehao() < b->getXuehao();
        });

    // ��ʾδ����Ա
    if (weidaoList.empty()) {
        cout << "���г�Ա���ѵ���!\n";
    } else {
        cout << "\n==== δ����Ա ====\n";
        for (auto c : weidaoList) {
            c->xianshi();
            cout << endl;
        }
    }
}

// ��ʾ���˵�
void showMenu() {
    cout << "\n==== ���Ź���ϵͳ ====\n"
         << "1. ������Ա\n"
         << "2. ɾ����Ա\n"
         << "3. ��ѯ��Ա\n"
         << "4. �޸ĳ�Ա\n"
         << "5. չʾ���г�Ա\n"
         << "6. �ǩ��\n"
         << "0. �˳�\n"
         << "��ѡ��: ";
}

// ������Ա
void addMember(SheTuan& st) {
    string xh, mz, zw;
    int type;

    cout << "����ѧ��: ";
    cin >> xh;
    if (st.xuehaoExists(xh)) {
        cout << "ѧ���Ѵ���!\n";
        return;
    }

    cout << "��������: ";
    cin >> mz;

    cout << "ѡ������ (1-��ͨ��Ա 2-�ɲ�): ";
    cin >> type;

    if (type == 1) {
        st += make_unique<PuTong>(xh, mz);
    } else if (type == 2) {
        cout << "����ɲ�ְλ: ";
        cin >> zw;
        st += make_unique<GanBu>(xh, mz, zw);
    } else {
        cout << "��Ч����!\n";
        return;
    }
    cout << "��ӳɹ�!\n";
}

// ��ѯ��Ա
void searchMember(const SheTuan& st) {
    string key;
    cout << "����ѧ�Ż�����: ";
    cin >> key;

    vector<ChengYuan*> result;
    for (auto c : st.getAll()) {
        if (c->getXuehao().find(key) != string::npos ||
            c->getMingzi().find(key) != string::npos) {
            result.push_back(c);
        }
    }

    if (result.empty()) {
        cout << "δ�ҵ�ƥ���Ա\n";
        return;
    }

    cout << "==== ��ѯ��� ====\n";
    for (auto c : result) {
        c->xianshi();
        cout << endl;
    }
}

// �޸ĳ�Ա
void modifyMember(SheTuan& st) {
    string xh;
    cout << "����Ҫ�޸ĵ�ѧ��: ";
    cin >> xh;

    ChengYuan* c = st.find(xh);
    if (!c) {
        cout << "��Ա������\n";
        return;
    }

    string mz, zw;
    cout << "���������� (���ղ��޸�): ";
    cin.ignore();
    getline(cin, mz);
    if (mz.empty()) mz = c->getMingzi();

    if (c->getType() == 2) {
        cout << "������ְλ (���ղ��޸�): ";
        getline(cin, zw);
        if (zw.empty()) zw = dynamic_cast<GanBu*>(c)->getMingzi();
    } else {
        zw = "��ͨ��Ա";
    }

    c->setXinxi(mz, zw);
    cout << "�޸ĳɹ�!\n";
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
                cout << "����Ҫɾ����ѧ��: ";
                cin >> xh;
                if (shetuan -= xh) {
                    cout << "ɾ���ɹ�\n";
                } else {
                    cout << "��Ա������\n";
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
                cout << "ϵͳ���˳�\n";
                break;
            default:
                cout << "��Чѡ������������\n";
        }
    } while (choice != 0);

    return 0;
}