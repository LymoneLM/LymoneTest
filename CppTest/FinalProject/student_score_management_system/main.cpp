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
        cout << "总分:" << setw(6) << jisuanzf() << endl;
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
            cout << "错误：学号 " << xs.huodehao() << " 已存在！" << endl;
            return;
        }
        xueshenglist.push_back(xs);
        cout << "已添加学生: " << xs.huodeming() << endl;
    }

    void shanchuxs(const string& h) {
        auto it = find_if(xueshenglist.begin(), xueshenglist.end(),
                         [&](const xuesheng& s) { return s.huodehao() == h; });

        if (it != xueshenglist.end()) {
            cout << "删除学生: " << it->huodeming() << " (" << it->huodehao() << ")" << endl;
            xueshenglist.erase(it);
        } else {
            cout << "未找到学号: " << h << endl;
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
            cout << "未找到匹配的学生记录" << endl;
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
                    cout << "已更新 " << xs.huodeming() << " 的" << k << "成绩: " << f << endl;
                } else {
                    cout << "错误：科目 '" << k << "' 不存在" << endl;
                }
                break;
            }
        }

        if (!zhaodao) {
            cout << "未找到学号: " << h << endl;
        }
    }

    void tianjiakm(const string& k) {
        if (find(kemulist.begin(), kemulist.end(), k) != kemulist.end()) {
            cout << "科目已存在！" << endl;
            return;
        }
        kemulist.push_back(k);

        for (auto& xs : xueshenglist) {
            xs.xiugaicj(k, 0.0);
        }
        cout << "已添加科目: " << k << endl;
    }

    void shanchukm(const string& k) {
        auto it = find(kemulist.begin(), kemulist.end(), k);
        if (it != kemulist.end()) {
            kemulist.erase(it);
            for (auto& xs : xueshenglist) {
                xs.shanchukm(k);
            }
            cout << "已移除科目: " << k << endl;
        } else {
            cout << "错误：科目不存在" << endl;
        }
    }

    void xianshibd(bool showAvg = true) {
        cout << "\n=== " << biaotiming << " ===" << endl;
        cout << left << setw(15) << "姓名" << setw(15) << "学号";
        for (const auto& km : kemulist) {
            cout << setw(15) << km;
        }
        cout << setw(15) << "总分" << endl;
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
            cout << left << setw(30) << "平均分";
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
        if (z == "学号") {
            sort(xueshenglist.begin(), xueshenglist.end(),
                [&](const xuesheng& a, const xuesheng& b) {
                    return asc ? a.huodehao() < b.huodehao() : a.huodehao() > b.huodehao();
                });
        } else if (z == "姓名") {
            sort(xueshenglist.begin(), xueshenglist.end(),
                [&](const xuesheng& a, const xuesheng& b) {
                    return asc ? a.huodeming() < b.huodeming() : a.huodeming() > b.huodeming();
                });
        } else if (z == "总分") {
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
            cerr << "文件打开失败: " << w << endl;
            return;
        }

        outFile << "姓名,学号";
        for (const auto& km : kemulist) {
            outFile << "," << km;
        }
        outFile << endl;

        for (const auto& xs : xueshenglist) {
            outFile << xs.geshihuacsv() << endl;
        }

        cout << "数据已导出到: " << w << endl;
        outFile.close();
    }

    void daorucsv(const string& w) {
        ifstream inFile(w);
        if (!inFile) {
            cerr << "无法打开文件: " << w << endl;
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
                cerr << "无效文件格式" << endl;
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
                    cerr << "成绩转换错误: " << rowData[i+2] << endl;
                }
            }
            xueshenglist.push_back(xs);
        }

        cout << "已导入 " << xueshenglist.size() << " 条记录" << endl;
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
            cout << "表单已存在！" << endl;
            return;
        }
        danlist.emplace_back(bt);
        cout << "已创建表单: " << bt << endl;
    }

    void shanchudan(const string& bt) {
        int idx = zhaobiao(bt);
        if (idx != -1) {
            danlist.erase(danlist.begin() + idx);
            cout << "已删除表单: " << bt << endl;
        } else {
            cout << "表单不存在！" << endl;
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
            cout << "当前没有表单" << endl;
            return;
        }

        cout << "\n表单列表:" << endl;
        for (const auto& d : danlist) {
            cout << "- " << d.huodebt() << " (" << d.huodekm().size() << "个科目)" << endl;
        }
    }
};

void xianshicaidan() {
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

void xianshibiaodan() {
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
    guanliqi glq;

    while (true) {
        xianshicaidan();
        int xz;
        cin >> xz;

        if (xz == 0) {
            cout << "系统已退出" << endl;
            break;
        }

        switch (xz) {
            case 1: {
                string bt;
                cout << "输入表单名称: ";
                cin >> bt;
                glq.chuangjiandan(bt);
                break;
            }
            case 2: {
                string bt;
                cout << "输入要删除的表单名称: ";
                cin >> bt;
                glq.shanchudan(bt);
                break;
            }
            case 3: {
                string bt;
                cout << "输入表单名称: ";
                cin >> bt;
                chengjidan* d = glq.huodedan(bt);

                if (!d) {
                    cout << "表单不存在！" << endl;
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
                            cout << "学生姓名: ";
                            cin >> m;
                            cout << "学生学号: ";
                            cin >> h;
                            d->tianjiaxuesheng(xuesheng(m, h));
                            break;
                        }
                        case 2: {
                            string h;
                            cout << "输入学号: ";
                            cin >> h;
                            d->shanchuxs(h);
                            break;
                        }
                        case 3: {
                            string s;
                            cout << "输入姓名或学号: ";
                            cin >> s;
                            d->chaxunxs(s);
                            break;
                        }
                        case 4: {
                            string h, k;
                            double f;
                            cout << "学生学号: ";
                            cin >> h;
                            cout << "科目名称: ";
                            cin >> k;
                            cout << "新成绩: ";
                            cin >> f;
                            d->genggaicj(h, k, f);
                            break;
                        }
                        case 5: {
                            string k;
                            cout << "新科目名称: ";
                            cin >> k;
                            d->tianjiakm(k);
                            break;
                        }
                        case 6: {
                            string k;
                            cout << "要删除的科目: ";
                            cin >> k;
                            d->shanchukm(k);
                            break;
                        }
                        case 7:
                            d->xianshibd(true);
                            break;
                        case 8: {
                            string z;
                            cout << "排序依据(姓名/学号/总分/科目): ";
                            cin >> z;
                            d->paixuxianshi(z);
                            break;
                        }
                        default:
                            cout << "无效操作！" << endl;
                    }
                }
                break;
            }
            case 4:
                glq.liebiaodan();
                break;
            case 5: {
                string bt, w;
                cout << "表单名称: ";
                cin >> bt;
                cout << "CSV文件名: ";
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
                cout << "表单名称: ";
                cin >> bt;
                chengjidan* d = glq.huodedan(bt);
                if (!d) {
                    cout << "表单不存在！" << endl;
                    break;
                }
                cout << "导出文件名: ";
                cin >> w;
                d->daochucsv(w);
                break;
            }
            default:
                cout << "无效选择！" << endl;
        }
    }

    return 0;
}