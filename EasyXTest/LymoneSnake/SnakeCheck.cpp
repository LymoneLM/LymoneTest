//Check Frame
#include <cstdlib>
#include <stdio.h>
#include <EasyX.h>
#include <time.h>
#include "Snake.h"

extern char map[20][20];
extern ExMessage m;
extern char Nextstep;
sNode Head,Rear;
//extern int Head.x, Head.y;
extern int snakelength;
Linkqueue Q;

void LSC::initwall()
{
	//TODO: 墙体检入
}

void LSC::initrand(int seed)
{
	srand(seed);
	return;
}
void LSC::initrand()
{
	srand(time(0));
	return;
}

void LSC::randapple()
{
	short xi, yi;
	loop:
	xi = rand() % 20;
	yi = rand() % 20;
	if (map[xi][yi] == 0)
		map[xi][yi] = 'A';
	else
		goto loop;
	return;
}

void LSC::randhead()
{
	Q.initQ();
	short xi, yi;
loop:
	xi = rand() % 20;
	yi = rand() % 20;
	if (map[xi][yi] == 0)
	{
		map[xi][yi] = 'H';
		Head.x = xi;Head.y = yi;
		Q.enQ(Head);
	}
	else
		goto loop;
	return;
}

/*键盘输入*/
bool LSC::directionCheck()
{
	if (peekmessage(&m, EX_KEY))
	{
		switch (m.message)
		{
		case WM_KEYDOWN:
			if (m.vkcode == VK_UP)
			{
				Nextstep = 'U';
			}
			if (m.vkcode == VK_DOWN)
			{
				Nextstep = 'D';
			}
			if (m.vkcode == VK_LEFT)
			{
				Nextstep = 'L';
			}
			if (m.vkcode == VK_RIGHT)
			{
				Nextstep = 'R';
			}
			if (m.vkcode == VK_ESCAPE)
			{
				return true;
			}
			break;

		}
	}
	return false;
}

bool LSC::deathCheck()
{
	switch (Nextstep)
	{
	case 'U':
		if (Head.y - 1 < 0)
			return true;
		else if (map[Head.x][Head.y - 1] != 0&& map[Head.x][Head.y - 1] != 'A')
			return true;
		break;
	case 'D':
		if (Head.y + 1 >= 20)
			return true;
		else if (map[Head.x][Head.y + 1] != 0&& map[Head.x][Head.y + 1] != 'A')
			return true;
		break;
	case 'L':
		if (Head.x - 1 < 0)
			return true;
		else if (map[Head.x - 1][Head.y] != 0&& map[Head.x - 1][Head.y] != 'A')
			return true;
		break;
	case 'R':
		if (Head.x + 1 >= 20)
			return true;
		else if (map[Head.x + 1][Head.y] != 0&& map[Head.x + 1][Head.y] != 'A')
			return true;
		break;
	default:
		printf("Error:UndefinedDeathCheck\n");
	}
	return false;
}

bool LSC::lengthCheck()
{
	bool isA=false;
	//苹果检定并移动
	switch (Nextstep)
	{
	case 'U':
		if (map[Head.x][--Head.y] == 'A')
			isA = true;
		break;
	case 'D':
		if (map[Head.x][++Head.y] == 'A')
			isA = true;
		break;
	case 'L':
		if (map[--Head.x][Head.y] == 'A')
			isA = true;
		break;
	case 'R':
		if (map[++Head.x][Head.y] == 'A')
			isA = true;
		break;
	default:
		printf("Error:UndefinedLengthCheck\n");
	}
	if (isA)
	{
		snakelength++;
		LSC::randapple();
	}
	Q.enQ(Head);
		
	//长度检定
	int length = Q.countQ();
	if (length > snakelength)
	{
		Rear=Q.deQ();
		setfillcolor(0x000000);
		setlinecolor(0x000000);
		#ifdef DEBUG
		printf("%d,%d\n", Rear.x, Rear.y);
		#endif // DEBUG		
		fillcircle(25*Rear.x + 13, 25*Rear.y + 13, 11);
	}
	Q.pmapQ();
	return true;
}