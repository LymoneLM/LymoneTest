#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <ctime>

// ������
class RiQi {
private:
    int nian, yue, ri;
    static int ceshi;  // ��̬�������ڴ洢��������
public:
    RiQi(int n = 0, int y = 0, int r = 0) : nian(n), yue(y), ri(r) {}

    // ����+�����������黹���ڣ�
    RiQi operator+(int days) const {
        RiQi result = *this;
        result.ri += days;
        while (result.ri > 30) {
            result.ri -= 30;
            result.yue++;
            if (result.yue > 12) {
                result.yue = 1;
                result.nian++;
            }
        }
        return result;
    }

    // ����>��������Ƚ����ڣ�
    bool operator>(const RiQi& other) const {
        if (nian != other.nian) return nian > other.nian;
        if (yue != other.yue) return yue > other.yue;
        return ri > other.ri;
    }

    // �������ڲ���ڷ��
    int operator-(const RiQi& other) const {
        int a = (nian * 360) + (yue * 30) + ri;
        int b = (other.nian * 360) + (other.yue * 30) + other.ri;
        return a - b;
    }

    void xianshi() const {
        std::cout << nian << "-" << yue << "-" << ri;
    }

    static RiQi dangqianRiQi() {
        std::time_t t = std::time(0);
        std::tm* now = std::localtime(&t);
        return RiQi(now->tm_year + 1900, now->tm_mon + 1, now->tm_mday) + ceshi;
    }

    // ���Թ���
    static void tianjiaDays(int days) {
        ceshi = ceshi + days;
    }

    // ���ò�������
    static void chongzhiCeshi() {
        ceshi = 0;
    }
};
int RiQi::ceshi = 0;

// ͼ�����Ʒ����
class TushuguanItem {
protected:
    std::string biaoti;
    std::string zuozhe;
    std::string ISBN;
    bool jieyueZhuangtai;
    RiQi jiechuRiqi;
    RiQi yingguihuanRiqi;
public:
    TushuguanItem(const std::string& bt, const std::string& zz, const std::string& isbn)
        : biaoti(bt), zuozhe(zz), ISBN(isbn), jieyueZhuangtai(false) {}

    virtual ~TushuguanItem() {}

    // ��̬��������ȡ��������
    virtual int getJieyueQixian() const = 0;

    // ��̬���������㷣��
    virtual double jisuanFakuan(int chaoguoDays) const {
        return chaoguoDays * 0.5; // Ĭ��ÿ��0.5Ԫ
    }

    void jieyue(const RiQi& jiechu) {
        jieyueZhuangtai = true;
        jiechuRiqi = jiechu;
        yingguihuanRiqi = jiechu + getJieyueQixian();
    }

    double guihuan(const RiQi& guihuanRiqi) {
        if (!jieyueZhuangtai) return 0.0;

        jieyueZhuangtai = false;
        if (guihuanRiqi > yingguihuanRiqi) {
            int chaoguoDays = guihuanRiqi - yingguihuanRiqi;
            return jisuanFakuan(chaoguoDays);
        }
        return 0.0;
    }

    void xujie() {
        if (jieyueZhuangtai) {
            yingguihuanRiqi = yingguihuanRiqi + getJieyueQixian();
        }
    }

    const std::string& getBiaoti() const { return biaoti; }
    const std::string& getZuozhe() const { return zuozhe; }
    const std::string& getISBN() const { return ISBN; }
    bool getJieyueZhuangtai() const { return jieyueZhuangtai; }
    void xianshiXinxi() const {
        std::cout << "����: " << biaoti << " | ����: " << zuozhe
                  << " | ISBN: " << ISBN << " | ״̬: ";
        if (jieyueZhuangtai) {
            std::cout << "�ѽ�� (Ӧ������: ";
            yingguihuanRiqi.xianshi();
            std::cout << ")";
        } else {
            std::cout << "�ɽ���";
        }
    }
};

// ͼ����
class Shu : public TushuguanItem {
public:
    Shu(const std::string& bt, const std::string& zz, const std::string& isbn)
        : TushuguanItem(bt, zz, isbn) {}

    int getJieyueQixian() const override { return 30; } // 30�����
};

// �ڿ���
class Qikan : public TushuguanItem {
public:
    Qikan(const std::string& bt, const std::string& zz, const std::string& isbn)
        : TushuguanItem(bt, zz, isbn) {}

    int getJieyueQixian() const override { return 14; } // 14�����
    double jisuanFakuan(int a) const override {
        return a * 1.0; // �ڿ�����ÿ��1Ԫ
    }
};

// ������
class Lunwen : public TushuguanItem {
public:
    Lunwen(const std::string& bt, const std::string& zz, const std::string& isbn)
        : TushuguanItem(bt, zz, isbn) {}

    int getJieyueQixian() const override { return 7; } // 7�����
    double jisuanFakuan(int b) const override {
        return b * 2.0; // ��������ÿ��2Ԫ
    }
};

// ͼ��ݹ���ϵͳ
class Tushuguan {
private:
    std::vector<TushuguanItem*> wupin;

public:
    ~Tushuguan() {
        for (auto c : wupin) delete c;
    }

    void tianjia(TushuguanItem* a) {
        wupin.push_back(a);
    }

    bool shanchu(const std::string& d) {
        auto it = std::remove_if(wupin.begin(), wupin.end(),
            [&](TushuguanItem* e) {
                if (e->getISBN() == d) {
                    delete e;
                    return true;
                }
                return false;
            });

        if (it != wupin.end()) {
            wupin.erase(it, wupin.end());
            return true;
        }
        return false;
    }

    void jieyueItem(const std::string& f, const RiQi& g) {
        for (auto h : wupin) {
            if (h->getISBN() == f && !h->getJieyueZhuangtai()) {
                h->jieyue(g);
                return;
            }
        }
    }

    double guihuanItem(const std::string& i, const RiQi& j) {
        for (auto k : wupin) {
            if (k->getISBN() == i && k->getJieyueZhuangtai()) {
                return k->guihuan(j);
            }
        }
        return -1; // δ�ҵ�
    }

    void xujieItem(const std::string& l) {
        for (auto m : wupin) {
            if (m->getISBN() == l && m->getJieyueZhuangtai()) {
                m->xujie();
                return;
            }
        }
    }

    void chaxun(const std::string& n) const {
        for (auto o : wupin) {
            if (o->getBiaoti().find(n) != std::string::npos ||
                o->getZuozhe().find(n) != std::string::npos ||
                o->getISBN() == n) {
                o->xianshiXinxi();
                std::cout << std::endl;
            }
        }
    }

    void xianshiAll() const {
        for (auto p : wupin) {
            p->xianshiXinxi();
            std::cout << std::endl;
        }
    }
};

// �û�����
void showMenu() {
    std::cout << "\n===== ͼ��ݹ���ϵͳ =====";
    std::cout << "\n1. ���ͼ��";
    std::cout << "\n2. ɾ��ͼ��";
    std::cout << "\n3. ����ͼ��";
    std::cout << "\n4. �黹ͼ��";
    std::cout << "\n5. ����ͼ��";
    std::cout << "\n6. ��ѯͼ��";
    std::cout << "\n7. չʾ����ͼ��";
    std::cout << "\n8. �������������ԣ�";
    std::cout << "\n9. �������ڣ����ԣ�";
    std::cout << "\n0. �˳�ϵͳ";
    std::cout << "\n========================";
    std::cout << "\n��ѡ�����: ";
}

int main() {
    Tushuguan library;
    int choice;

    // ���ʾ������
    library.tianjia(new Shu("C++ Primer", "Stanley Lippman", "978711548"));
    library.tianjia(new Qikan("Science Journal", "Nature", "SCI2023"));
    library.tianjia(new Lunwen("Deep Learning", "Yann LeCun", "AI2024"));

    do {
        showMenu();
        std::cin >> choice;
        std::cin.ignore();

        std::string a, b, c;
        RiQi d;

        switch (choice) {
            case 1: {
                int type;
                std::cout << "ѡ������ (1.ͼ�� 2.�ڿ� 3.����): ";
                std::cin >> type;
                std::cin.ignore();

                std::cout << "�������: ";
                std::getline(std::cin, a);
                std::cout << "��������: ";
                std::getline(std::cin, b);
                std::cout << "����ISBN: ";
                std::getline(std::cin, c);

                if (type == 1) library.tianjia(new Shu(a, b, c));
                else if (type == 2) library.tianjia(new Qikan(a, b, c));
                else if (type == 3) library.tianjia(new Lunwen(a, b, c));
                std::cout << "��ӳɹ�!\n";
                break;
            }
            case 2:
                std::cout << "����Ҫɾ����ISBN: ";
                std::getline(std::cin, a);
                if (library.shanchu(a)) {
                    std::cout << "ɾ���ɹ�!\n";
                } else {
                    std::cout << "δ�ҵ���ͼ��!\n";
                }
                break;
            case 3:
                std::cout << "����Ҫ���ĵ�ISBN: ";
                std::getline(std::cin, a);
                d = RiQi::dangqianRiQi();
                library.jieyueItem(a, d);
                std::cout << "���ĳɹ�! �������: ";
                d.xianshi();
                std::cout << std::endl;
                break;
            case 4:
                std::cout << "����Ҫ�黹��ISBN: ";
                std::getline(std::cin, a);
                d = RiQi::dangqianRiQi();
                double fakuan;
                fakuan = library.guihuanItem(a, d);
                if (fakuan >= 0) {
                    if (fakuan > 0) {
                        std::cout << "�黹�ɹ�! ���ڷ���: " << fakuan << "Ԫ\n";
                    } else {
                        std::cout << "�黹�ɹ�! ������\n";
                    }
                } else {
                    std::cout << "δ�ҵ���ͼ���δ���!\n";
                }
                break;
            case 5:
                std::cout << "����Ҫ�����ISBN: ";
                std::getline(std::cin, a);
                library.xujieItem(a);
                std::cout << "����ɹ�!\n";
                break;
            case 6:
                std::cout << "�����ѯ����(����/����/ISBN): ";
                std::getline(std::cin, a);
                library.chaxun(a);
                break;
            case 7:
                library.xianshiAll();
                break;
            case 8:
                int days;
                std::cout << "����Ҫ���ӵ�����: ";
                std::cin >> days;
                RiQi::tianjiaDays(days);
                std::cout << "��ǰ����������Ϊ: ";
                RiQi::dangqianRiQi().xianshi();
                std::cout << std::endl;
                break;
            case 9:
                RiQi::chongzhiCeshi();
                std::cout << "������Ϊ��ʵ����: ";
                RiQi::dangqianRiQi().xianshi();
                std::cout << std::endl;
                break;
            case 0:
                std::cout << "��лʹ�ã��ټ�!\n";
                break;
            default:
                std::cout << "��Чѡ������������!\n";
        }
    } while (choice != 0);

    return 0;
}