//Draw Frame
#include <stdio.h>
#include <easyx.h>
#include "Snake.h"

extern char map[20][20];

void LSD::drawNet()
{
#ifdef DEBUG
    printf("PrintNet\n");
#endif // DEBUG


    setlinecolor(0xFFFFFF);
    for (int i = 0; i <= 20; i++)
        line(25 * i, 0, 25 * i, 500);
    for (int i = 0; i <= 20; i++)
        line(0, 25 * i, 500, 25 * i);
    return;
}

void LSD::drawMap()
{
#ifdef DEBUG
    printf("PrintMap\n");
#endif // DEBUG


    for (int xi = 0; xi < 20; xi++)
        for (int yi = 0; yi < 20; yi++)
        {
            short x = 25 * xi, y = 25 * yi;
            switch (map[xi][yi])
            {
            case 'w':
            case 'W':
                setfillcolor(0x2a2aa5);
                setlinecolor(0x2a2aa5);
                fillrectangle(x + 1, y + 1, x + 24, y + 24);
                break;
            case 'h':
            case 'H':
                setfillcolor(0x0000ff);
                setlinecolor(0x0000ff);
                fillcircle(x + 13, y + 13, 11);
                break;
            case 's':
            case 'S':
                setfillcolor(0xffffff);
                setlinecolor(0xffffff);
                fillcircle(x + 13, y + 13, 11);
                break;
            case 'a':
            case 'A':
                setfillcolor(0x6600aa);
                setlinecolor(0x00ff00);
                fillcircle(x + 13, y + 13, 11);
                break;
            }
        }
    return;
}
//cleardevice();//清空绘版
void LSD::cleanmap()
{
    for (int xi = 0; xi < 20; xi++)
        for (int yi = 0; yi < 20; yi++)
        {
            if (map[xi][yi] == 'S')
                map[xi][yi] = 0;
            if (map[xi][yi] == 'H')
                map[xi][yi] = 0;
        }
    return;
}

void LSD::drawdeath()
{
    settextcolor(0x0000FF);
    settextstyle(40, 40, L"Minecraft");
    printf("WASTED\n");
    RECT r = { 0, 0, 699, 504 };
    drawtext(_T("WASTED"), &r, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    
    return;
}
void LSD::drawTitle()
{
    settextcolor(0xFFFFFF);
    settextstyle(14, 14, L"Minecraft");
    RECT r = { 500, 10, 699, 30 };
    drawtext(_T("LymoneSnake"), &r, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    r = { 500, 30, 699, 50 };
    drawtext(_T("按↑↓←→开始"), &r, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    settextstyle(20, 20, L"Minecraft");
    r = { 500, 50, 699, 90 };
    drawtext(_T("当前分数："), &r, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    return;
}
void LSD::drawScore(int score)
{
    TCHAR s[5];
    _stprintf_s(s, _T("%d"), score);

    settextcolor(0xFFFFFF);
    settextstyle(30, 30, L"Minecraft");
    RECT r = { 500, 90, 699, 140 };
    drawtext(s, &r, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    return;
}