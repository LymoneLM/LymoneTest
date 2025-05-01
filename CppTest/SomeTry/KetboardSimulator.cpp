#include <windows.h>
#include <iostream>
#include <winuser.h>

using namespace std;

void writeword(char w)
{
    char out = w ;
    cout << out << endl;
    keybd_event(out, 0, 0, 0);
    keybd_event(out, 0, KEYEVENTF_KEYUP, 0);
}

int main()
{
    string input = "HELLO";
    Sleep(1000);
    //win+R
    keybd_event(VK_LWIN, 0,0, 0);
    keybd_event(82, 0, 0, 0);
    Sleep(500);
    keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0);
    keybd_event(82, 0, KEYEVENTF_KEYUP, 0);
    int i = 0;
    while (i != input.length())
    {        
        char a = input[i];
        writeword(toupper(a));
        Sleep(500);
        i++;
    }
    return 0;
}
