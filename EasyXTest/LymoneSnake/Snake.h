
//#define DEBUG
//#define DEBUG_TESTDATA

#ifndef SNAKEDRAW_H
#define SNAKEDRAW_H

namespace LSD
{
	/*棋盘绘制*/
	void drawNet();
	void drawMap();
	void cleanmap();
	/*文字绘制*/
	void drawTitle();
	void drawScore(int score);
	/*特殊画面*/
	void drawdeath();
}

#endif 


#ifndef SNAKECHECK_H
#define SNAKECHECK_H

namespace LSC
{
	/*Random*/
	void initrand(int);
	void initrand();
	void randapple();
	void randhead();
	/*Check*/
	void initwall();
	bool directionCheck();
	bool deathCheck();
	bool lengthCheck();

}

#endif


#ifndef SNAKEDATA_H
#define SNAKEDATA_H

class sNode
{
public:
	int x, y;
	sNode* snext;
};

class Linkqueue
{
	//链队列-逆
	//删尾加头 
public:
	void initQ();
	void enQ(sNode);
	sNode deQ();
	void destoryQ();
	void printQ();//devOnly 
	short countQ();
	bool pmapQ();
private:
	sNode* front;
	sNode* rear;
};

#endif
