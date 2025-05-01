#include <stdio.h>
#include "Snake.h"

extern char map[20][20];

void Linkqueue::initQ()
{
	sNode* p = new sNode;
	front = p;
	rear = p;
	p->snext = NULL;
	return;
}
void Linkqueue::enQ(sNode node)
{
	sNode* p = new sNode;
	p->x = node.x;
	p->y = node.y;
	rear->snext = p;
	rear = p;
	p->x = node.x;
	p->y = node.y;
	return;
}
sNode Linkqueue::deQ()
{
	sNode rearNode;
	if (rear == front)
	{
		rearNode.x = -1;
		rearNode.y = -1;
	}
	sNode* p;
	p = front->snext;
	front->snext = p->snext;
	rearNode.x = p->x;
	rearNode.y = p->y;
	delete p;
	return rearNode;
}
void Linkqueue::destoryQ()
{
	while (rear != front)
		Linkqueue::deQ();
	delete front;
	return;
}
void Linkqueue::printQ()
{
	if (rear == front)
		return;
	sNode* p = front;
	do
	{
		p = p->snext;
		//std::cout << "X=" << p->x << "Y=" << p->y << std::endl;
	} while (p != rear);
	return;
}
short Linkqueue::countQ()
{
	if (rear == front)
		return 0;
	short num = 0;
	sNode* p = front;
	do
	{
		p = p->snext;
		++num;
	} while (p != rear);
	return num;
}
bool Linkqueue::pmapQ()
{
	if (rear == front)
		return false;
	LSD::cleanmap();
	sNode* p = front;
	do
	{
		p = p->snext;
		map[p->x][p->y] = 'S';
	} while (p != rear);
	map[p->x][p->y] = 'H';
	return true;
}
