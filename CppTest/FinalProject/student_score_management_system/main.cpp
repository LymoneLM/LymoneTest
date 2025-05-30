#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <map>

using namespace std;

class shujuxiang {
public:
    virtual ~shujuxiang() {}
    virtual void xianshi() const = 0;
    virtual string geshihuacsv() const = 0;
    virtual bool baohan(const string& s) const = 0;
};

class xuesheng : public shujuxiang {
private:
    string xingming;
    string xuehao;
    map<string, double> chengji;

public:
    xuesheng(string m, string h) : xingming(m), xuehao(h) {}

    bool operator==(const xuesheng& o) const {
        return xuehao == o.xuehao;
    }

    void xiugaicj(const string& k, double f) {
        chengji[k] = f;
    }

    void shanchukm(const string& k) {
        chengji.erase(k);
    }

    double jisuanzf() const {
        double z = 0.0;
        for (const auto& g : chengji) {
            z += g.second;
        }
        return z;
    }

    double huodecj(const string& k) const {
        auto it = chengji.find(k);
        return (it != chengji.end()) ? it->second : -1.0;
    }

    void xianshi() const override {
        cout << left << setw(15) << xingming << setw(15) << xuehao;
        for (const auto& g : chengji) {
            cout << setw(10) << g.first << ":" << setw(5) << g.second;
        }
        cout << "�ܷ�:" << setw(6) << jisuanzf() << endl;
    }

    string geshihuacsv() const override {
        ostringstream oss;
        oss << xingming << "," << xuehao;
        for (const auto& g : chengji) {
            oss << "," << g.second;
        }
        return oss.str();
    }

    bool baohan(const string& s) const override {
        return xingming.find(s) != string::npos || xuehao.find(s) != string::npos;
    }

    const string& huodeming() const { return xingming; }
    const string& huodehao() const { return xuehao; }
    const map<string, double>& huodecjmap() const { return chengji; }
};

class chengjidan {
private:
    string biaotiming;
    vector<xuesheng> xueshenglist;
    vector<string> kemulist;

public:
    chengjidan(string bt) : biaotiming(bt) {}

    void tianjiaxuesheng(const xuesheng& xs) {
        auto it = find(xueshenglist.begin(), xueshenglist.end(), xs);
        if (it != xueshenglist.end()) {
            cout << "����ѧ�� " << xs.huodehao() << " �Ѵ��ڣ�" << endl;
            return;
        }
        xueshenglist.push_back(xs);
        cout << "�����ѧ��: " << xs.huodeming() << endl;
    }

    void shanchuxs(const string& h) {
        auto it = find_if(xueshenglist.begin(), xueshenglist.end(),
                         [&](const xuesheng& s) { return s.huodehao() == h; });

        if (it != xueshenglist.end()) {
            cout << "ɾ��ѧ��: " << it->huodeming() << " (" << it->huodehao() << ")" << endl;
            xueshenglist.erase(it);
        } else {
            cout << "δ�ҵ�ѧ��: " << h << endl;
        }
    }

    void chaxunxs(const string& s) {
        bool zhaodao = false;
        for (const auto& xs : xueshenglist) {
            if (xs.baohan(s)) {
                xs.xianshi();
                zhaodao = true;
            }
        }
        if (!zhaodao) {
            cout << "δ�ҵ�ƥ���ѧ����¼" << endl;
        }
    }

    void genggaicj(const string& h, const string& k, double f) {
        bool zhaodao = false;

        for (auto& xs : xueshenglist) {
            if (xs.huodehao() == h) {
                zhaodao = true;
                auto subIt = find(kemulist.begin(), kemulist.end(), k);
                if (subIt != kemulist.end()) {
                    xs.xiugaicj(k, f);
                    cout << "�Ѹ��� " << xs.huodeming() << " ��" << k << "�ɼ�: " << f << endl;
                } else {
                    cout << "���󣺿�Ŀ '" << k << "' ������" << endl;
                }
                break;
            }
        }

        if (!zhaodao) {
            cout << "δ�ҵ�ѧ��: " << h << endl;
        }
    }

    void tianjiakm(const string& k) {
        if (find(kemulist.begin(), kemulist.end(), k) != kemulist.end()) {
            cout << "��Ŀ�Ѵ��ڣ�" << endl;
            return;
        }
        kemulist.push_back(k);

        for (auto& xs : xueshenglist) {
            xs.xiugaicj(k, 0.0);
        }
        cout << "����ӿ�Ŀ: " << k << endl;
    }

    void shanchukm(const string& k) {
        auto it = find(kemulist.begin(), kemulist.end(), k);
        if (it != kemulist.end()) {
            kemulist.erase(it);
            for (auto& xs : xueshenglist) {
                xs.shanchukm(k);
            }
            cout << "���Ƴ���Ŀ: " << k << endl;
        } else {
            cout << "���󣺿�Ŀ������" << endl;
        }
    }

    void xianshibd(bool showAvg = true) {
        cout << "\n=== " << biaotiming << " ===" << endl;
        cout << left << setw(15) << "����" << setw(15) << "ѧ��";
        for (const auto& km : kemulist) {
            cout << setw(15) << km;
        }
        cout << setw(15) << "�ܷ�" << endl;
        cout << string(15*(kemulist.size()+2), '-') << endl;

        for (const auto& xs : xueshenglist) {
            cout << left << setw(15) << xs.huodeming() << setw(15) << xs.huodehao();
            for (const auto& km : kemulist) {
                double f = xs.huodecj(km);
                if (f >= 0) {
                    cout << setw(15) << f;
                } else {
                    cout << setw(15) << "N/A";
                }
            }
            cout << setw(15) << xs.jisuanzf() << endl;
        }

        if (showAvg && !xueshenglist.empty()) {
            cout << string(15*(kemulist.size()+2), '-') << endl;
            cout << left << setw(30) << "ƽ����";
            for (const auto& km : kemulist) {
                double z = 0.0;
                int gs = 0;
                for (const auto& xs : xueshenglist) {
                    double f = xs.huodecj(km);
                    if (f >= 0) {
                        z += f;
                        gs++;
                    }
                }
                double pj = (gs > 0) ? z / gs : 0.0;
                cout << setw(15) << fixed << setprecision(1) << pj;
            }
            cout << endl;
        }
    }

    void paixuxianshi(const string& z, bool asc = true) {
        if (z == "ѧ��") {
            sort(xueshenglist.begin(), xueshenglist.end(),
                [&](const xuesheng& a, const xuesheng& b) {
                    return asc ? a.huodehao() < b.huodehao() : a.huodehao() > b.huodehao();
                });
        } else if (z == "����") {
            sort(xueshenglist.begin(), xueshenglist.end(),
                [&](const xuesheng& a, const xuesheng& b) {
                    return asc ? a.huodeming() < b.huodeming() : a.huodeming() > b.huodeming();
                });
        } else if (z == "�ܷ�") {
            sort(xueshenglist.begin(), xueshenglist.end(),
                [&](const xuesheng& a, const xuesheng& b) {
                    return asc ? a.jisuanzf() < b.jisuanzf()
                                     : a.jisuanzf() > b.jisuanzf();
                });
        } else {
            sort(xueshenglist.begin(), xueshenglist.end(),
                [&](const xuesheng& a, const xuesheng& b) {
                    double fa = a.huodecj(z);
                    double fb = b.huodecj(z);
                    return asc ? fa < fb : fa > fb;
                });
        }
        xianshibd(true);
    }

    void daochucsv(const string& w) {
        ofstream outFile(w);
        if (!outFile) {
            cerr << "�ļ���ʧ��: " << w << endl;
            return;
        }

        outFile << "����,ѧ��";
        for (const auto& km : kemulist) {
            outFile << "," << km;
        }
        outFile << endl;

        for (const auto& xs : xueshenglist) {
            outFile << xs.geshihuacsv() << endl;
        }

        cout << "�����ѵ�����: " << w << endl;
        outFile.close();
    }

    void daorucsv(const string& w) {
        ifstream inFile(w);
        if (!inFile) {
            cerr << "�޷����ļ�: " << w << endl;
            return;
        }

        xueshenglist.clear();
        kemulist.clear();

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

            kemulist = vector<string>(headers.begin() + 2, headers.end());
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

            xuesheng xs(rowData[0], rowData[1]);
            for (int i = 0; i < kemulist.size() && i + 2 < rowData.size(); i++) {
                try {
                    double f = stod(rowData[i + 2]);
                    xs.xiugaicj(kemulist[i], f);
                } catch (...) {
                    cerr << "�ɼ�ת������: " << rowData[i+2] << endl;
                }
            }
            xueshenglist.push_back(xs);
        }

        cout << "�ѵ��� " << xueshenglist.size() << " ����¼" << endl;
        inFile.close();
    }

    const string& huodebt() const { return biaotiming; }
    const vector<string>& huodekm() const { return kemulist; }
};

class guanliqi {
private:
    vector<chengjidan> danlist;

    int zhaobiao(const string& bt) const{
        for (int i = 0; i < danlist.size(); i++) {
            if (danlist[i].huodebt() == bt) {
                return i;
            }
        }
        return -1;
    }

public:
    void chuangjiandan(const string& bt) {
        if (zhaobiao(bt) != -1) {
            cout << "���Ѵ��ڣ�" << endl;
            return;
        }
        danlist.emplace_back(bt);
        cout << "�Ѵ�����: " << bt << endl;
    }

    void shanchudan(const string& bt) {
        int idx = zhaobiao(bt);
        if (idx != -1) {
            danlist.erase(danlist.begin() + idx);
            cout << "��ɾ����: " << bt << endl;
        } else {
            cout << "�������ڣ�" << endl;
        }
    }

    chengjidan* huodedan(const string& bt) {
        int idx = zhaobiao(bt);
        if (idx != -1) {
            return &danlist[idx];
        }
        return nullptr;
    }

    void liebiaodan() {
        if (danlist.empty()) {
            cout << "��ǰû�б�" << endl;
            return;
        }

        cout << "\n���б�:" << endl;
        for (const auto& d : danlist) {
            cout << "- " << d.huodebt() << " (" << d.huodekm().size() << "����Ŀ)" << endl;
        }
    }
};

void xianshicaidan() {
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

void xianshibiaodan() {
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
    guanliqi glq;

    while (true) {
        xianshicaidan();
        int xz;
        cin >> xz;

        if (xz == 0) {
            cout << "ϵͳ���˳�" << endl;
            break;
        }

        switch (xz) {
            case 1: {
                string bt;
                cout << "���������: ";
                cin >> bt;
                glq.chuangjiandan(bt);
                break;
            }
            case 2: {
                string bt;
                cout << "����Ҫɾ���ı�����: ";
                cin >> bt;
                glq.shanchudan(bt);
                break;
            }
            case 3: {
                string bt;
                cout << "���������: ";
                cin >> bt;
                chengjidan* d = glq.huodedan(bt);

                if (!d) {
                    cout << "�������ڣ�" << endl;
                    break;
                }

                while (true) {
                    xianshibiaodan();
                    int bdxz;
                    cin >> bdxz;

                    if (bdxz == 0) break;

                    switch (bdxz) {
                        case 1: {
                            string m, h;
                            cout << "ѧ������: ";
                            cin >> m;
                            cout << "ѧ��ѧ��: ";
                            cin >> h;
                            d->tianjiaxuesheng(xuesheng(m, h));
                            break;
                        }
                        case 2: {
                            string h;
                            cout << "����ѧ��: ";
                            cin >> h;
                            d->shanchuxs(h);
                            break;
                        }
                        case 3: {
                            string s;
                            cout << "����������ѧ��: ";
                            cin >> s;
                            d->chaxunxs(s);
                            break;
                        }
                        case 4: {
                            string h, k;
                            double f;
                            cout << "ѧ��ѧ��: ";
                            cin >> h;
                            cout << "��Ŀ����: ";
                            cin >> k;
                            cout << "�³ɼ�: ";
                            cin >> f;
                            d->genggaicj(h, k, f);
                            break;
                        }
                        case 5: {
                            string k;
                            cout << "�¿�Ŀ����: ";
                            cin >> k;
                            d->tianjiakm(k);
                            break;
                        }
                        case 6: {
                            string k;
                            cout << "Ҫɾ���Ŀ�Ŀ: ";
                            cin >> k;
                            d->shanchukm(k);
                            break;
                        }
                        case 7:
                            d->xianshibd(true);
                            break;
                        case 8: {
                            string z;
                            cout << "��������(����/ѧ��/�ܷ�/��Ŀ): ";
                            cin >> z;
                            d->paixuxianshi(z);
                            break;
                        }
                        default:
                            cout << "��Ч������" << endl;
                    }
                }
                break;
            }
            case 4:
                glq.liebiaodan();
                break;
            case 5: {
                string bt, w;
                cout << "������: ";
                cin >> bt;
                cout << "CSV�ļ���: ";
                cin >> w;
                glq.chuangjiandan(bt);
                chengjidan* d = glq.huodedan(bt);
                if (d) {
                    d->daorucsv(w);
                }
                break;
            }
            case 6: {
                string bt, w;
                cout << "������: ";
                cin >> bt;
                chengjidan* d = glq.huodedan(bt);
                if (!d) {
                    cout << "�������ڣ�" << endl;
                    break;
                }
                cout << "�����ļ���: ";
                cin >> w;
                d->daochucsv(w);
                break;
            }
            default:
                cout << "��Чѡ��" << endl;
        }
    }

    return 0;
}