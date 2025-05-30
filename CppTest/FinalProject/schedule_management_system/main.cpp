#include <iostream>
#include <vector>
#include <memory>
#include <algorithm>
#include <ctime>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <map>

class ScheduleA {
protected:
    std::string leixing;
    std::string xinxi;
    std::time_t shijian;

public:
    ScheduleA(const std::string& a, const std::string& b, std::time_t c)
        : leixing(a), xinxi(b), shijian(c) {}

    virtual ~ScheduleA() = default;

    bool operator<(const ScheduleA& aa) const {
        return shijian < aa.shijian;
    }

    friend std::ostream& operator<<(std::ostream& os, const ScheduleA& ss) {
        char bf[20];
        std::strftime(bf, sizeof(bf), "%Y-%m-%d %H:%M", std::localtime(&ss.shijian));
        os << "[" << ss.leixing << "] " << bf << " - " << ss.xinxi;
        ss.xq(os);
        return os;
    }

    virtual void xq(std::ostream& os) const = 0;
    virtual std::string tjs() const = 0;
    virtual std::string toJ() const = 0;

    std::time_t getT() const { return shijian; }
    std::string getL() const { return leixing; }
    std::string getX() const { return xinxi; }
};

class MeetingA : public ScheduleA {
    std::string didian;

public:
    MeetingA(const std::string& a, std::time_t b, const std::string& c)
        : ScheduleA("会议", a, b), didian(c) {}

    void xq(std::ostream& os) const override {
        os << " (地点: " << didian << ")";
    }

    std::string tjs() const override {
        return didian;
    }

    std::string toJ() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"会议\","
            << "\"content\":\"" << xinxi << "\","
            << "\"time\":" << shijian << ","
            << "\"location\":\"" << didian << "\""
            << "}";
        return oss.str();
    }
};

class ReminderA : public ScheduleA {
    std::string pinlv;

public:
    ReminderA(const std::string& a, std::time_t b, const std::string& c)
        : ScheduleA("提醒", a, b), pinlv(c) {}

    void xq(std::ostream& os) const override {
        os << " (频率: " << pinlv << ")";
    }

    std::string tjs() const override {
        return pinlv;
    }

    std::string toJ() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"提醒\","
            << "\"content\":\"" << xinxi << "\","
            << "\"time\":" << shijian << ","
            << "\"frequency\":\"" << pinlv << "\""
            << "}";
        return oss.str();
    }
};

class TaskA : public ScheduleA {
    std::string youxianji;

public:
    TaskA(const std::string& a, std::time_t b, const std::string& c)
        : ScheduleA("任务", a, b), youxianji(c) {}

    void xq(std::ostream& os) const override {
        os << " (优先级: " << youxianji << ")";
    }

    std::string tjs() const override {
        return youxianji;
    }

    std::string toJ() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"任务\","
            << "\"content\":\"" << xinxi << "\","
            << "\"time\":" << shijian << ","
            << "\"priority\":\"" << youxianji << "\""
            << "}";
        return oss.str();
    }
};

class ManagerA {
private:
    std::vector<std::unique_ptr<ScheduleA>> rcb;

public:
    static std::time_t parseT(const std::string& dt){
        std::tm tm = {};
        std::istringstream ss(dt);
        ss >> std::get_time(&tm, "%Y-%m-%d %H:%M");
        if (ss.fail()) return -1;
        return std::mktime(&tm);
    }

    static std::string formatT(const std::time_t t){
        char bf[20];
        std::strftime(bf, sizeof(bf), "%Y-%m-%d %H:%M", std::localtime(&t));
        return bf;
    }

    void addS(std::unique_ptr<ScheduleA> s) {
        rcb.push_back(std::move(s));
    }

    bool delS(const int idx) {
        if (idx < 0 || idx >= static_cast<int>(rcb.size())) {
            return false;
        }
        rcb.erase(rcb.begin() + idx);
        return true;
    }

    std::vector<ScheduleA*> findS(const std::string& d = "",
                                         std::time_t s1 = 0,
                                         std::time_t s2 = 0) {
        std::vector<ScheduleA*> res;

        for (auto& r : rcb) {
            bool m = true;
            if (!d.empty()) {
                std::string rd = formatT(r->getT()).substr(0, 10);
                if (rd != d) m = false;
            }

            if (s1 != 0 && s2 != 0) {
                if (r->getT() < s1 || r->getT() > s2) m = false;
            }

            if (m) res.push_back(r.get());
        }

        return res;
    }

    bool modS(int idx, const std::string& ct,
                       const std::string& dt,
                       const std::string& sp) {
        if (idx < 0 || idx >= static_cast<int>(rcb.size())) {
            return false;
        }

        std::time_t nt = parseT(dt);
        if (nt == -1) return false;

        std::string tp = rcb[idx]->getL();

        if (tp == "会议") {
            rcb[idx] = std::make_unique<MeetingA>(ct, nt, sp);
        } else if (tp == "提醒") {
            rcb[idx] = std::make_unique<ReminderA>(ct, nt, sp);
        } else if (tp == "任务") {
            rcb[idx] = std::make_unique<TaskA>(ct, nt, sp);
        }

        return true;
    }

    void showA() {
        std::sort(rcb.begin(), rcb.end(),
                 [](const auto& a, const auto& b) { return *a < *b; });

        for (size_t i = 0; i < rcb.size(); ++i) {
            std::cout << i << ": " << *rcb[i] << std::endl;
        }
    }

    void saveJ(const std::string& fn) {
        std::ofstream ff(fn);
        if (!ff) {
            std::cerr << "无法打开文件: " << fn << std::endl;
            return;
        }

        ff << "[\n";
        for (size_t i = 0; i < rcb.size(); ++i) {
            ff << rcb[i]->toJ();
            if (i < rcb.size() - 1) ff << ",";
            ff << "\n";
        }
        ff << "]\n";
    }

    void loadJ(const std::string& fn) {
        std::ifstream ff(fn);
        if (!ff) {
            std::cerr << "无法打开文件: " << fn << std::endl;
            return;
        }

        rcb.clear();
        std::string ln, js;
        while (std::getline(ff, ln)) {
            js += ln;
        }

        size_t p = 0;
        while ((p = js.find('{', p)) != std::string::npos) {
            size_t e = js.find('}', p);
            if (e == std::string::npos) break;

            std::string en = js.substr(p + 1, e - p - 1);
            std::map<std::string, std::string> ff;

            size_t fs = 0;
            while (fs < en.size()) {
                size_t cl = en.find(':', fs);
                if (cl == std::string::npos) break;

                std::string k = en.substr(fs, cl - fs);
                k.erase(std::remove(k.begin(), k.end(), '"'), k.end());
                k.erase(std::remove(k.begin(), k.end(), ' '), k.end());

                size_t vs = cl + 1;
                size_t ve = en.find(',', vs);
                if (ve == std::string::npos) ve = en.size();

                std::string v = en.substr(vs, ve - vs);
                if (v.front() == '"' && v.back() == '"') {
                    v = v.substr(1, v.size() - 2);
                }

                ff[k] = v;
                fs = ve + 1;
            }

            if (ff.count("type") && ff.count("content") &&
                ff.count("time")) {

                std::time_t t = static_cast<std::time_t>(std::stoll(ff["time"]));
                if (ff["type"] == "会议") {
                    rcb.push_back(std::make_unique<MeetingA>(
                        ff["content"], t, ff["location"]
                    ));
                } else if (ff["type"] == "提醒") {
                    rcb.push_back(std::make_unique<ReminderA>(
                        ff["content"], t, ff["frequency"]
                    ));
                } else if (ff["type"] == "任务") {
                    rcb.push_back(std::make_unique<TaskA>(
                        ff["content"], t, ff["priority"]
                    ));
                }
            }
            p = e + 1;
        }
    }
};

void showMenu() {
    std::cout << "\n=====日程管理系统=====\n";
    std::cout << "1. 添加日程\n";
    std::cout << "2. 删除日程\n";
    std::cout << "3. 查询日程\n";
    std::cout << "4. 修改日程\n";
    std::cout << "5. 展示所有日程\n";
    std::cout << "6. 保存到文件\n";
    std::cout << "7. 从文件加载\n";
    std::cout << "0. 退出\n";
    std::cout << "====================\n";
    std::cout << "请选择操作: ";
}

int main() {
    ManagerA mgr;
    int ch;
    const std::string fn = "schedules.json";

    do {
        showMenu();
        std::cin >> ch;
        std::cin.ignore();

        switch (ch) {
            case 1: {
                std::string tp, ct, sp, dt;

                std::cout << "选择类型 (1.会议 2.提醒 3.任务): ";
                int tch;
                std::cin >> tch;
                std::cin.ignore();

                if (tch < 1 || tch > 3) {
                    std::cout << "无效选择!\n";
                    break;
                }

                std::cout << "输入内容: ";
                std::getline(std::cin, ct);

                std::cout << "输入时间 (YYYY-MM-DD HH:MM): ";
                std::getline(std::cin, dt);

                if (tch == 1) {
                    std::cout << "输入地点: ";
                    std::getline(std::cin, sp);
                    tp = "会议";
                } else if (tch == 2) {
                    std::cout << "输入频率: ";
                    std::getline(std::cin, sp);
                    tp = "提醒";
                } else {
                    std::cout << "输入优先级: ";
                    std::getline(std::cin, sp);
                    tp = "任务";
                }

                std::time_t t = mgr.parseT(dt);
                if (t == -1) {
                    std::cout << "时间格式错误!\n";
                    break;
                }

                if (tp == "会议") {
                    mgr.addS(std::make_unique<MeetingA>(ct, t, sp));
                } else if (tp == "提醒") {
                    mgr.addS(std::make_unique<ReminderA>(ct, t, sp));
                } else {
                    mgr.addS(std::make_unique<TaskA>(ct, t, sp));
                }

                std::cout << "日程添加成功!\n";
                break;
            }

            case 2: {
                mgr.showA();
                int idx;
                std::cout << "输入要删除的日程编号: ";
                std::cin >> idx;

                if (mgr.delS(idx)) {
                    std::cout << "日程删除成功!\n";
                } else {
                    std::cout << "无效编号!\n";
                }
                break;
            }

            case 3: {
                int qtype;
                std::cout << "查询方式 (1.按日期 2.按时间范围): ";
                std::cin >> qtype;
                std::cin.ignore();

                std::vector<ScheduleA*> res;

                if (qtype == 1) {
                    std::string d;
                    std::cout << "输入日期 (YYYY-MM-DD): ";
                    std::getline(std::cin, d);
                    res = mgr.findS(d);
                } else if (qtype == 2) {
                    std::string sstr, estr;
                    std::cout << "输入起始时间 (YYYY-MM-DD HH:MM): ";
                    std::getline(std::cin, sstr);
                    std::cout << "输入结束时间 (YYYY-MM-DD HH:MM): ";
                    std::getline(std::cin, estr);

                    std::time_t st = mgr.parseT(sstr);
                    std::time_t et = mgr.parseT(estr);

                    if (st == -1 || et == -1) {
                        std::cout << "时间格式错误!\n";
                        break;
                    }

                    res = mgr.findS("", st, et);
                } else {
                    std::cout << "无效选择!\n";
                    break;
                }

                if (res.empty()) {
                    std::cout << "未找到匹配日程\n";
                } else {
                    for (auto s : res) {
                        std::cout << *s << std::endl;
                    }
                }
                break;
            }

            case 4: {
                mgr.showA();
                int idx;
                std::cout << "输入要修改的日程编号: ";
                std::cin >> idx;
                std::cin.ignore();

                std::string ct, dt, sp;
                std::cout << "输入新内容 (直接回车保持原内容): ";
                std::getline(std::cin, ct);

                std::cout << "输入新时间 (YYYY-MM-DD HH:MM) (直接回车保持原时间): ";
                std::getline(std::cin, dt);

                if (!dt.empty() && mgr.parseT(dt) == -1) {
                    std::cout << "时间格式错误!\n";
                    break;
                }

                std::cout << "输入新特定信息 (直接回车保持原信息): ";
                std::getline(std::cin, sp);

                std::vector<ScheduleA*> tmp = mgr.findS();
                if (mgr.modS(idx,
                    ct.empty() ? tmp[idx]->getX() : ct,
                    dt.empty() ? mgr.formatT(tmp[idx]->getT()) : dt,
                    sp.empty() ? tmp[idx]->tjs() : sp)) {
                    std::cout << "日程修改成功!\n";
                } else {
                    std::cout << "修改失败!\n";
                }
                break;
            }

            case 5:
                mgr.showA();
                break;

            case 6:
                mgr.saveJ(fn);
                std::cout << "日程已保存到 " << fn << std::endl;
                break;

            case 7:
                mgr.loadJ(fn);
                std::cout << "日程已从 " << fn << " 加载" << std::endl;
                break;

            case 0:
                std::cout << "感谢使用日程管理系统!\n";
                break;

            default:
                std::cout << "无效选择，请重新输入!\n";
        }
    } while (ch != 0);

    return 0;
}