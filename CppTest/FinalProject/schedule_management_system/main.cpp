#include <iostream>
#include <vector>
#include <memory>
#include <algorithm>
#include <ctime>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <map>

// 基类：日程
class Schedule {
protected:
    std::string type;
    std::string content;
    std::time_t time;

public:
    Schedule(const std::string& t, const std::string& c, std::time_t tm)
        : type(t), content(c), time(tm) {}

    virtual ~Schedule() = default;

    // 重载<运算符用于排序
    bool operator<(const Schedule& other) const {
        return time < other.time;
    }

    // 重载<<运算符用于输出
    friend std::ostream& operator<<(std::ostream& os, const Schedule& s) {
        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M", std::localtime(&s.time));
        os << "[" << s.type << "] " << buffer << " - " << s.content;
        s.printDetails(os);
        return os;
    }

    // 多态方法
    virtual void printDetails(std::ostream& os) const = 0;
    virtual std::string getSpecificInfo() const = 0;
    virtual std::string toJSON() const = 0;

    // 获取器
    std::time_t getTime() const { return time; }
    std::string getType() const { return type; }
    std::string getContent() const { return content; }
};

// 会议
class Meeting : public Schedule {
    std::string location;

public:
    Meeting(const std::string& c, std::time_t tm, const std::string& loc)
        : Schedule("会议", c, tm), location(loc) {}

    void printDetails(std::ostream& os) const override {
        os << " (地点: " << location << ")";
    }

    std::string getSpecificInfo() const override {
        return location;
    }

    std::string toJSON() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"会议\","
            << "\"content\":\"" << content << "\","
            << "\"time\":" << time << ","
            << "\"location\":\"" << location << "\""
            << "}";
        return oss.str();
    }
};

// 提醒
class Reminder : public Schedule {
    std::string frequency;

public:
    Reminder(const std::string& c, std::time_t tm, const std::string& freq)
        : Schedule("提醒", c, tm), frequency(freq) {}

    void printDetails(std::ostream& os) const override {
        os << " (频率: " << frequency << ")";
    }

    std::string getSpecificInfo() const override {
        return frequency;
    }

    std::string toJSON() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"提醒\","
            << "\"content\":\"" << content << "\","
            << "\"time\":" << time << ","
            << "\"frequency\":\"" << frequency << "\""
            << "}";
        return oss.str();
    }
};

// 任务
class Task : public Schedule {
    std::string priority;

public:
    Task(const std::string& c, std::time_t tm, const std::string& pri)
        : Schedule("任务", c, tm), priority(pri) {}

    void printDetails(std::ostream& os) const override {
        os << " (优先级: " << priority << ")";
    }

    std::string getSpecificInfo() const override {
        return priority;
    }

    std::string toJSON() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"任务\","
            << "\"content\":\"" << content << "\","
            << "\"time\":" << time << ","
            << "\"priority\":\"" << priority << "\""
            << "}";
        return oss.str();
    }
};

// 日程管理系统
class ScheduleManager {
private:
    std::vector<std::unique_ptr<Schedule>> schedules;

public:
    // 从字符串解析时间
    static std::time_t parseTime(const std::string& datetime){
        std::tm tm = {};
        std::istringstream ss(datetime);
        ss >> std::get_time(&tm, "%Y-%m-%d %H:%M");
        if (ss.fail()) return -1;
        return std::mktime(&tm);
    }

    // 时间格式化
    static std::string formatTime(const std::time_t time){
        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M", std::localtime(&time));
        return buffer;
    }

    // 添加日程
    void addSchedule(std::unique_ptr<Schedule> s) {
        schedules.push_back(std::move(s));
    }

    // 删除日程
    bool deleteSchedule(const int index) {
        if (index < 0 || index >= static_cast<int>(schedules.size())) {
            return false;
        }
        schedules.erase(schedules.begin() + index);
        return true;
    }

    // 查询日程
    std::vector<Schedule*> querySchedules(const std::string& date = "",
                                         std::time_t start = 0,
                                         std::time_t end = 0) {
        std::vector<Schedule*> results;

        for (auto& s : schedules) {
            bool match = true;
            if (!date.empty()) {
                std::string sdate = formatTime(s->getTime()).substr(0, 10);
                if (sdate != date) match = false;
            }

            if (start != 0 && end != 0) {
                if (s->getTime() < start || s->getTime() > end) match = false;
            }

            if (match) results.push_back(s.get());
        }

        return results;
    }

    // 修改日程
    bool modifySchedule(int index, const std::string& content,
                       const std::string& datetime,
                       const std::string& specific) {
        if (index < 0 || index >= static_cast<int>(schedules.size())) {
            return false;
        }

        std::time_t newTime = parseTime(datetime);
        if (newTime == -1) return false;

        std::string type = schedules[index]->getType();

        if (type == "会议") {
            schedules[index] = std::make_unique<Meeting>(content, newTime, specific);
        } else if (type == "提醒") {
            schedules[index] = std::make_unique<Reminder>(content, newTime, specific);
        } else if (type == "任务") {
            schedules[index] = std::make_unique<Task>(content, newTime, specific);
        }

        return true;
    }

    // 排序后展示所有日程
    void displayAll() {
        std::sort(schedules.begin(), schedules.end(),
                 [](const auto& a, const auto& b) { return *a < *b; });

        for (size_t i = 0; i < schedules.size(); ++i) {
            std::cout << i << ": " << *schedules[i] << std::endl;
        }
    }

    // 保存到JSON文件
    void saveToJSON(const std::string& filename) {
        std::ofstream file(filename);
        if (!file) {
            std::cerr << "无法打开文件: " << filename << std::endl;
            return;
        }

        file << "[\n";
        for (size_t i = 0; i < schedules.size(); ++i) {
            file << schedules[i]->toJSON();
            if (i < schedules.size() - 1) file << ",";
            file << "\n";
        }
        file << "]\n";
    }

    // 从JSON文件加载
    void loadFromJSON(const std::string& filename) {
        std::ifstream file(filename);
        if (!file) {
            std::cerr << "无法打开文件: " << filename << std::endl;
            return;
        }

        schedules.clear();
        std::string line, json;
        while (std::getline(file, line)) {
            json += line;
        }

        // JSON解析
        size_t pos = 0;
        while ((pos = json.find('{', pos)) != std::string::npos) {
            size_t end = json.find('}', pos);
            if (end == std::string::npos) break;

            std::string entry = json.substr(pos + 1, end - pos - 1);
            std::map<std::string, std::string> fields;

            size_t fieldStart = 0;
            while (fieldStart < entry.size()) {
                size_t colon = entry.find(':', fieldStart);
                if (colon == std::string::npos) break;

                std::string key = entry.substr(fieldStart, colon - fieldStart);
                key.erase(std::remove(key.begin(), key.end(), '"'), key.end());
                key.erase(std::remove(key.begin(), key.end(), ' '), key.end());

                size_t valueStart = colon + 1;
                size_t valueEnd = entry.find(',', valueStart);
                if (valueEnd == std::string::npos) valueEnd = entry.size();

                std::string value = entry.substr(valueStart, valueEnd - valueStart);
                if (value.front() == '"' && value.back() == '"') {
                    value = value.substr(1, value.size() - 2);
                }

                fields[key] = value;
                fieldStart = valueEnd + 1;
            }

            if (fields.count("type") && fields.count("content") &&
                fields.count("time")) {

                std::time_t t = static_cast<std::time_t>(std::stoll(fields["time"]));
                if (fields["type"] == "会议") {
                    schedules.push_back(std::make_unique<Meeting>(
                        fields["content"], t, fields["location"]
                    ));
                } else if (fields["type"] == "提醒") {
                    schedules.push_back(std::make_unique<Reminder>(
                        fields["content"], t, fields["frequency"]
                    ));
                } else if (fields["type"] == "任务") {
                    schedules.push_back(std::make_unique<Task>(
                        fields["content"], t, fields["priority"]
                    ));
                }
            }
            pos = end + 1;
        }
    }
};

// 打印菜单
void displayMenu() {
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
    ScheduleManager manager;
    int choice;
    const std::string filename = "schedules.json";

    do {
        displayMenu();
        std::cin >> choice;
        std::cin.ignore();

        switch (choice) {
            case 1: {  // 添加日程
                std::string type, content, specific, datetime;

                std::cout << "选择类型 (1.会议 2.提醒 3.任务): ";
                int typeChoice;
                std::cin >> typeChoice;
                std::cin.ignore();

                if (typeChoice < 1 || typeChoice > 3) {
                    std::cout << "无效选择!\n";
                    break;
                }

                std::cout << "输入内容: ";
                std::getline(std::cin, content);

                std::cout << "输入时间 (YYYY-MM-DD HH:MM): ";
                std::getline(std::cin, datetime);

                if (typeChoice == 1) {
                    std::cout << "输入地点: ";
                    std::getline(std::cin, specific);
                    type = "会议";
                } else if (typeChoice == 2) {
                    std::cout << "输入频率: ";
                    std::getline(std::cin, specific);
                    type = "提醒";
                } else {
                    std::cout << "输入优先级: ";
                    std::getline(std::cin, specific);
                    type = "任务";
                }

                std::time_t t = manager.parseTime(datetime);
                if (t == -1) {
                    std::cout << "时间格式错误!\n";
                    break;
                }

                if (type == "会议") {
                    manager.addSchedule(std::make_unique<Meeting>(content, t, specific));
                } else if (type == "提醒") {
                    manager.addSchedule(std::make_unique<Reminder>(content, t, specific));
                } else {
                    manager.addSchedule(std::make_unique<Task>(content, t, specific));
                }

                std::cout << "日程添加成功!\n";
                break;
            }

            case 2: {  // 删除日程
                manager.displayAll();
                int index;
                std::cout << "输入要删除的日程编号: ";
                std::cin >> index;

                if (manager.deleteSchedule(index)) {
                    std::cout << "日程删除成功!\n";
                } else {
                    std::cout << "无效编号!\n";
                }
                break;
            }

            case 3: {  // 查询日程
                int queryType;
                std::cout << "查询方式 (1.按日期 2.按时间范围): ";
                std::cin >> queryType;
                std::cin.ignore();

                std::vector<Schedule*> results;

                if (queryType == 1) {
                    std::string date;
                    std::cout << "输入日期 (YYYY-MM-DD): ";
                    std::getline(std::cin, date);
                    results = manager.querySchedules(date);
                } else if (queryType == 2) {
                    std::string startStr, endStr;
                    std::cout << "输入起始时间 (YYYY-MM-DD HH:MM): ";
                    std::getline(std::cin, startStr);
                    std::cout << "输入结束时间 (YYYY-MM-DD HH:MM): ";
                    std::getline(std::cin, endStr);

                    std::time_t start = manager.parseTime(startStr);
                    std::time_t end = manager.parseTime(endStr);

                    if (start == -1 || end == -1) {
                        std::cout << "时间格式错误!\n";
                        break;
                    }

                    results = manager.querySchedules("", start, end);
                } else {
                    std::cout << "无效选择!\n";
                    break;
                }

                if (results.empty()) {
                    std::cout << "未找到匹配日程\n";
                } else {
                    for (auto s : results) {
                        std::cout << *s << std::endl;
                    }
                }
                break;
            }

            case 4: {  // 修改日程
                manager.displayAll();
                int index;
                std::cout << "输入要修改的日程编号: ";
                std::cin >> index;
                std::cin.ignore();

                std::string content, datetime, specific;
                std::cout << "输入新内容 (直接回车保持原内容): ";
                std::getline(std::cin, content);

                std::cout << "输入新时间 (YYYY-MM-DD HH:MM) (直接回车保持原时间): ";
                std::getline(std::cin, datetime);

                if (!datetime.empty() && manager.parseTime(datetime) == -1) {
                    std::cout << "时间格式错误!\n";
                    break;
                }

                std::cout << "输入新特定信息 (直接回车保持原信息): ";
                std::getline(std::cin, specific);

                if (manager.modifySchedule(index,
                    content.empty() ? manager.querySchedules()[index]->getContent() : content,
                    datetime.empty() ? manager.formatTime(manager.querySchedules()[index]->getTime()) : datetime,
                    specific.empty() ? manager.querySchedules()[index]->getSpecificInfo() : specific)) {
                    std::cout << "日程修改成功!\n";
                } else {
                    std::cout << "修改失败!\n";
                }
                break;
            }

            case 5:  // 展示所有日程
                manager.displayAll();
                break;

            case 6:  // 保存到文件
                manager.saveToJSON(filename);
                std::cout << "日程已保存到 " << filename << std::endl;
                break;

            case 7:  // 从文件加载
                manager.loadFromJSON(filename);
                std::cout << "日程已从 " << filename << " 加载" << std::endl;
                break;

            case 0:  // 退出
                std::cout << "感谢使用日程管理系统!\n";
                break;

            default:
                std::cout << "无效选择，请重新输入!\n";
        }
    } while (choice != 0);

    return 0;
}