#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define ROW 9
#define COL 9
#define ROWS ROW+2
#define COLS COL+2
#define EASY_COUNT 20

//声明
void test();
void menu();
void game();
void InitBoard(char board[ROWS][COLS],int rows,int cols,char set);
void DisplayBoard(char board[ROWS][COLS],int row,int col);
void SetMine(char mine[ROWS][COLS],int row,int col);
void FindMine(char mine[ROWS][COLS],char show[ROWS][COLS],int row,int col);
int  get_mine_count(char mine[ROWS][COLS],int x,int y);
void Open(char mine[ROWS][COLS],char show[ROWS][COLS],int x,int y);

//定义
void Open(char mine[ROWS][COLS],char show[ROWS][COLS],int x,int y)
{ 
    for(int i=x-1;i<=x+1;i++)
    {
        for(int j=y-1;j<=y+1;j++)
        {
            if(show[i][j]=='*')
            {
                show[i][j]=get_mine_count(mine,i,j)+'0';
                if(show[i][j]=='0')
                {
                    Open(mine,show,i,j);
                }
            }
        }
    }
}

int  get_mine_count(char mine[ROWS][COLS],int x,int y)
{
    return (mine[x-1][y]+mine[x-1][y-1]+mine[x-1][y+1]+
            mine[x][y-1]+mine[x][y+1]+mine[x+1][y-1]+
            mine[x+1][y]+mine[x+1][y+1]-8*'0');
}

void FindMine(char mine[ROWS][COLS],char show[ROWS][COLS],int row,int col)
{
    int x=0;
    int y=0;
    int win=0;

    while(win<row*col-EASY_COUNT)
    {
        printf("请输入要排查的坐标");
        scanf("%d %d",&x,&y);
        if(x>=1&&x<=row&&y>=1&&y<=col)
        {
            if(show[x][y]!='*')
            {
                printf("改坐标已被排查,");
                continue;
            }
            if(mine[x][y]=='1')
            {
                printf("你踩雷了，失败了\n");
                DisplayBoard(mine,ROW,COL);
                break;
            }
            else
            {
                show[x][y]=get_mine_count(mine,x,y)+'0';
                if(show[x][y]=='0')
                {
                    Open(mine,show,x,y);
                }
                DisplayBoard(show,ROW,COL);
                win++;
            }
        }
        else
        {
            printf("坐标非法,重新输入\n");
        }
    }
    if (win==(row*col-EASY_COUNT))
    {
        printf("恭喜你,排雷成功\n");
    }
    
}

void SetMine(char mine[ROWS][COLS],int row,int col)
{
    int count=EASY_COUNT;
    while(count)
    {
        int x=rand()%row+1;
        int y=rand()%col+1;
        
        if(mine[x][y]=='0')
        {
            mine[x][y]='1';
            count--;
        }
    }
}

void DisplayBoard(char board[ROWS][COLS],int row,int col)
{
    int i=0;
    int j=0;
    printf("-------扫雷--------\n");
    for(j=0;j<=col;j++)
    {
        printf("%d ",j);
    }
    printf("\n");
    for(i=1;i<=row;i++)
    {
        printf("%d ",i);
        for(j=1;j<=col;j++)
        {
            printf("%c ",board[i][j]);
        }
        printf("\n");
    }
}

void InitBoard(char board[ROWS][COLS],int rows,int cols,char set)
{
    int i=0;
    for(;i<rows;i++)
    {
        int j=0;
        for(;j<cols;j++)
        {
            board[i][j]=set;
        }
    }
}

void game()
{
    char mine[ROWS][COLS]={0};//布置好的雷
    char show[ROWS][COLS]={0};//被排查的雷
    //初始化
    InitBoard(mine,ROWS,COLS,'0');
    InitBoard(show,ROWS,COLS,'*');
    //打印
    DisplayBoard(show,ROW,COL);
    //布置雷
    SetMine(mine,ROW,COL);
    //DisplayBoard(mine,ROW,COL);
    //排查雷
    FindMine(mine,show,ROW,COL);


}

void menu()
{
    printf("************************\n");
    printf("*******1. 开始游戏******\n");
    printf("*******0. 退出游戏******\n");
    printf("************************\n");

}

void test()
{
    srand((unsigned int)time(NULL));
    int input=0;
    do
    {
        menu();
        printf("请选择:>");
        scanf("%d",&input);
        switch(input)
        {
        case 1:
            game();
            break;
        case 0:
            printf("退出游戏");
            exit(0);
            break;
        default:
            printf("请重新输入");
            break;
        }
        
    }while (1);
}

int main()
{
    test();
    return 0;
}
