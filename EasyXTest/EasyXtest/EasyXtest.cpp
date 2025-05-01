#include <iostream>
#include <Easyx.h>

int main()
{
	// 初始化图形窗口
	initgraph(640, 480);

	ExMessage m;		// 定义消息变量

	while (true) 
	{
		// 获取一条鼠标或按键消息
		m = getmessage(EM_MOUSE | EM_KEY);

		switch (m.message)
		{
		case WM_MOUSEMOVE:
			// 鼠标移动的时候画红色的小点
			putpixel(m.x, m.y, RED);
			break;

		case WM_LBUTTONDOWN:
			// 如果点左键的同时按下了 Ctrl 键
			if (m.ctrl)
				// 画一个大方块
				rectangle(m.x - 10, m.y - 10, m.x + 10, m.y + 10);
			else
				// 画一个小方块
				rectangle(m.x - 5, m.y - 5, m.x + 5, m.y + 5);
			break;

		case WM_KEYDOWN:
			if (m.vkcode == VK_ESCAPE)
				return 0;	// 按 ESC 键退出程序
		}
	}

	// 关闭图形窗口
	closegraph();
	return 0;
}