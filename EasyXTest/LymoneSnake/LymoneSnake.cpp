#include <stdio.h>
#include <easyx.h>
#include "Snake.h"
#include <windows.h>

char map[20][20];
/*Wall-Head-Apple-Snake*/
ExMessage m;

char Nextstep;
/*Up-Down-Left-Right*/
int delay = 400;

int snakelength=1;

void initMap()
{
    for (int xi = 0; xi < 20; xi++)
        for (int yi = 0; yi < 20; yi++)
        {
            map[xi][yi] = 0;
        }
    return;
}

//block 25*25
void testData();
void consolLoaded()
{
    #ifdef DEBUG
    printf("==ConsolLoaded==\n");
    #endif // DEBUG  
    return;
}

int main()
{
/*==初始化==*/
    #ifdef DEBUG
    initgraph(700, 505, EW_SHOWCONSOLE);
    consolLoaded();
    #else
    initgraph(700, 505);
    #endif // DEBUG

    LSD::drawNet();
    LSD::drawTitle();

    #ifdef DEBUG_TESTDATA
    testData();
    #endif // DEBUG_TESTDATA
    LSC::initrand();
    LSC::randhead();
    LSC::randapple();
    LSD::drawMap();
/*开始*/
    while (true)
    {
        //输入检定
        //for (int i = 0; i < 4; i++)
        {
            if (LSC::directionCheck())
            {
                return 0;
            }
            #ifdef DEBUG
            printf("%c", Nextstep);
            #endif // DEBUG
            //Sleep(10);
        }
        #ifdef DEBUG
        printf("\n");
        #endif // DEBUG
        
        //死亡检定
        if (LSC::deathCheck())
        {
            LSD::drawdeath();
            m = getmessage();
            return 0;
        }
        else
        {
            //移动
            LSC::lengthCheck();
            LSD::drawScore(snakelength);
            //cleardevice();
            //LSD::drawNet();
            LSD::drawMap();
        }
        Sleep(delay-snakelength*10);
    }//main while


    closegraph();//关闭绘图窗口
    return 0;
}

void testData()
{
    //testdata devonly
    printf("TestDataLoading\n");
    map[1][1] = 'W';
    map[2][2] = 'S';
    map[3][3] = 'W';
    map[4][4] = 'S';
    map[5][5] = 'W';
    map[6][6] = 'S';
    map[7][7] = 'A';
    map[8][8] = 'H';
    map[9][9] = 'A';
    map[10][10] = 'H';
}