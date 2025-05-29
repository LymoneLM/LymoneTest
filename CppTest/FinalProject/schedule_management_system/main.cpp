#include <iostream>
#include <vector>
#include <memory>
#include <algorithm>
#include <ctime>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <map>

// ���ࣺ�ճ�
class Schedule {
protected:
    std::string type;
    std::string content;
    std::time_t time;

public:
    Schedule(const std::string& t, const std::string& c, std::time_t tm)
        : type(t), content(c), time(tm) {}

    virtual ~Schedule() = default;

    // ����<�������������
    bool operator<(const Schedule& other) const {
        return time < other.time;
    }

    // ����<<������������
    friend std::ostream& operator<<(std::ostream& os, const Schedule& s) {
        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M", std::localtime(&s.time));
        os << "[" << s.type << "] " << buffer << " - " << s.content;
        s.printDetails(os);
        return os;
    }

    // ��̬����
    virtual void printDetails(std::ostream& os) const = 0;
    virtual std::string getSpecificInfo() const = 0;
    virtual std::string toJSON() const = 0;

    // ��ȡ��
    std::time_t getTime() const { return time; }
    std::string getType() const { return type; }
    std::string getContent() const { return content; }
};

// ����
class Meeting : public Schedule {
    std::string location;

public:
    Meeting(const std::string& c, std::time_t tm, const std::string& loc)
        : Schedule("����", c, tm), location(loc) {}

    void printDetails(std::ostream& os) const override {
        os << " (�ص�: " << location << ")";
    }

    std::string getSpecificInfo() const override {
        return location;
    }

    std::string toJSON() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"����\","
            << "\"content\":\"" << content << "\","
            << "\"time\":" << time << ","
            << "\"location\":\"" << location << "\""
            << "}";
        return oss.str();
    }
};

// ����
class Reminder : public Schedule {
    std::string frequency;

public:
    Reminder(const std::string& c, std::time_t tm, const std::string& freq)
        : Schedule("����", c, tm), frequency(freq) {}

    void printDetails(std::ostream& os) const override {
        os << " (Ƶ��: " << frequency << ")";
    }

    std::string getSpecificInfo() const override {
        return frequency;
    }

    std::string toJSON() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"����\","
            << "\"content\":\"" << content << "\","
            << "\"time\":" << time << ","
            << "\"frequency\":\"" << frequency << "\""
            << "}";
        return oss.str();
    }
};

// ����
class Task : public Schedule {
    std::string priority;

public:
    Task(const std::string& c, std::time_t tm, const std::string& pri)
        : Schedule("����", c, tm), priority(pri) {}

    void printDetails(std::ostream& os) const override {
        os << " (���ȼ�: " << priority << ")";
    }

    std::string getSpecificInfo() const override {
        return priority;
    }

    std::string toJSON() const override {
        std::ostringstream oss;
        oss << "{"
            << "\"type\":\"����\","
            << "\"content\":\"" << content << "\","
            << "\"time\":" << time << ","
            << "\"priority\":\"" << priority << "\""
            << "}";
        return oss.str();
    }
};

// �ճ̹���ϵͳ
class ScheduleManager {
private:
    std::vector<std::unique_ptr<Schedule>> schedules;

public:
    // ���ַ�������ʱ��
    static std::time_t parseTime(const std::string& datetime){
        std::tm tm = {};
        std::istringstream ss(datetime);
        ss >> std::get_time(&tm, "%Y-%m-%d %H:%M");
        if (ss.fail()) return -1;
        return std::mktime(&tm);
    }

    // ʱ���ʽ��
    static std::string formatTime(const std::time_t time){
        char buffer[20];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M", std::localtime(&time));
        return buffer;
    }

    // ����ճ�
    void addSchedule(std::unique_ptr<Schedule> s) {
        schedules.push_back(std::move(s));
    }

    // ɾ���ճ�
    bool deleteSchedule(const int index) {
        if (index < 0 || index >= static_cast<int>(schedules.size())) {
            return false;
        }
        schedules.erase(schedules.begin() + index);
        return true;
    }

    // ��ѯ�ճ�
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

    // �޸��ճ�
    bool modifySchedule(int index, const std::string& content,
                       const std::string& datetime,
                       const std::string& specific) {
        if (index < 0 || index >= static_cast<int>(schedules.size())) {
            return false;
        }

        std::time_t newTime = parseTime(datetime);
        if (newTime == -1) return false;

        std::string type = schedules[index]->getType();

        if (type == "����") {
            schedules[index] = std::make_unique<Meeting>(content, newTime, specific);
        } else if (type == "����") {
            schedules[index] = std::make_unique<Reminder>(content, newTime, specific);
        } else if (type == "����") {
            schedules[index] = std::make_unique<Task>(content, newTime, specific);
        }

        return true;
    }

    // �����չʾ�����ճ�
    void displayAll() {
        std::sort(schedules.begin(), schedules.end(),
                 [](const auto& a, const auto& b) { return *a < *b; });

        for (size_t i = 0; i < schedules.size(); ++i) {
            std::cout << i << ": " << *schedules[i] << std::endl;
        }
    }

    // ���浽JSON�ļ�
    void saveToJSON(const std::string& filename) {
        std::ofstream file(filename);
        if (!file) {
            std::cerr << "�޷����ļ�: " << filename << std::endl;
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

    // ��JSON�ļ�����
    void loadFromJSON(const std::string& filename) {
        std::ifstream file(filename);
        if (!file) {
            std::cerr << "�޷����ļ�: " << filename << std::endl;
            return;
        }

        schedules.clear();
        std::string line, json;
        while (std::getline(file, line)) {
            json += line;
        }

        // JSON����
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
                if (fields["type"] == "����") {
                    schedules.push_back(std::make_unique<Meeting>(
                        fields["content"], t, fields["location"]
                    ));
                } else if (fields["type"] == "����") {
                    schedules.push_back(std::make_unique<Reminder>(
                        fields["content"], t, fields["frequency"]
                    ));
                } else if (fields["type"] == "����") {
                    schedules.push_back(std::make_unique<Task>(
                        fields["content"], t, fields["priority"]
                    ));
                }
            }
            pos = end + 1;
        }
    }
};

// ��ӡ�˵�
void displayMenu() {
    std::cout << "\n=====�ճ̹���ϵͳ=====\n";
    std::cout << "1. ����ճ�\n";
    std::cout << "2. ɾ���ճ�\n";
    std::cout << "3. ��ѯ�ճ�\n";
    std::cout << "4. �޸��ճ�\n";
    std::cout << "5. չʾ�����ճ�\n";
    std::cout << "6. ���浽�ļ�\n";
    std::cout << "7. ���ļ�����\n";
    std::cout << "0. �˳�\n";
    std::cout << "====================\n";
    std::cout << "��ѡ�����: ";
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
            case 1: {  // ����ճ�
                std::string type, content, specific, datetime;

                std::cout << "ѡ������ (1.���� 2.���� 3.����): ";
                int typeChoice;
                std::cin >> typeChoice;
                std::cin.ignore();

                if (typeChoice < 1 || typeChoice > 3) {
                    std::cout << "��Чѡ��!\n";
                    break;
                }

                std::cout << "��������: ";
                std::getline(std::cin, content);

                std::cout << "����ʱ�� (YYYY-MM-DD HH:MM): ";
                std::getline(std::cin, datetime);

                if (typeChoice == 1) {
                    std::cout << "����ص�: ";
                    std::getline(std::cin, specific);
                    type = "����";
                } else if (typeChoice == 2) {
                    std::cout << "����Ƶ��: ";
                    std::getline(std::cin, specific);
                    type = "����";
                } else {
                    std::cout << "�������ȼ�: ";
                    std::getline(std::cin, specific);
                    type = "����";
                }

                std::time_t t = manager.parseTime(datetime);
                if (t == -1) {
                    std::cout << "ʱ���ʽ����!\n";
                    break;
                }

                if (type == "����") {
                    manager.addSchedule(std::make_unique<Meeting>(content, t, specific));
                } else if (type == "����") {
                    manager.addSchedule(std::make_unique<Reminder>(content, t, specific));
                } else {
                    manager.addSchedule(std::make_unique<Task>(content, t, specific));
                }

                std::cout << "�ճ���ӳɹ�!\n";
                break;
            }

            case 2: {  // ɾ���ճ�
                manager.displayAll();
                int index;
                std::cout << "����Ҫɾ�����ճ̱��: ";
                std::cin >> index;

                if (manager.deleteSchedule(index)) {
                    std::cout << "�ճ�ɾ���ɹ�!\n";
                } else {
                    std::cout << "��Ч���!\n";
                }
                break;
            }

            case 3: {  // ��ѯ�ճ�
                int queryType;
                std::cout << "��ѯ��ʽ (1.������ 2.��ʱ�䷶Χ): ";
                std::cin >> queryType;
                std::cin.ignore();

                std::vector<Schedule*> results;

                if (queryType == 1) {
                    std::string date;
                    std::cout << "�������� (YYYY-MM-DD): ";
                    std::getline(std::cin, date);
                    results = manager.querySchedules(date);
                } else if (queryType == 2) {
                    std::string startStr, endStr;
                    std::cout << "������ʼʱ�� (YYYY-MM-DD HH:MM): ";
                    std::getline(std::cin, startStr);
                    std::cout << "�������ʱ�� (YYYY-MM-DD HH:MM): ";
                    std::getline(std::cin, endStr);

                    std::time_t start = manager.parseTime(startStr);
                    std::time_t end = manager.parseTime(endStr);

                    if (start == -1 || end == -1) {
                        std::cout << "ʱ���ʽ����!\n";
                        break;
                    }

                    results = manager.querySchedules("", start, end);
                } else {
                    std::cout << "��Чѡ��!\n";
                    break;
                }

                if (results.empty()) {
                    std::cout << "δ�ҵ�ƥ���ճ�\n";
                } else {
                    for (auto s : results) {
                        std::cout << *s << std::endl;
                    }
                }
                break;
            }

            case 4: {  // �޸��ճ�
                manager.displayAll();
                int index;
                std::cout << "����Ҫ�޸ĵ��ճ̱��: ";
                std::cin >> index;
                std::cin.ignore();

                std::string content, datetime, specific;
                std::cout << "���������� (ֱ�ӻس�����ԭ����): ";
                std::getline(std::cin, content);

                std::cout << "������ʱ�� (YYYY-MM-DD HH:MM) (ֱ�ӻس�����ԭʱ��): ";
                std::getline(std::cin, datetime);

                if (!datetime.empty() && manager.parseTime(datetime) == -1) {
                    std::cout << "ʱ���ʽ����!\n";
                    break;
                }

                std::cout << "�������ض���Ϣ (ֱ�ӻس�����ԭ��Ϣ): ";
                std::getline(std::cin, specific);

                if (manager.modifySchedule(index,
                    content.empty() ? manager.querySchedules()[index]->getContent() : content,
                    datetime.empty() ? manager.formatTime(manager.querySchedules()[index]->getTime()) : datetime,
                    specific.empty() ? manager.querySchedules()[index]->getSpecificInfo() : specific)) {
                    std::cout << "�ճ��޸ĳɹ�!\n";
                } else {
                    std::cout << "�޸�ʧ��!\n";
                }
                break;
            }

            case 5:  // չʾ�����ճ�
                manager.displayAll();
                break;

            case 6:  // ���浽�ļ�
                manager.saveToJSON(filename);
                std::cout << "�ճ��ѱ��浽 " << filename << std::endl;
                break;

            case 7:  // ���ļ�����
                manager.loadFromJSON(filename);
                std::cout << "�ճ��Ѵ� " << filename << " ����" << std::endl;
                break;

            case 0:  // �˳�
                std::cout << "��лʹ���ճ̹���ϵͳ!\n";
                break;

            default:
                std::cout << "��Чѡ������������!\n";
        }
    } while (choice != 0);

    return 0;
}