import numpy as np
import matplotlib.pyplot as plt

Ln = 100
Xit = np.zeros(Ln)

y = np.zeros(Ln)
u = np.zeros(Ln)
u = np.linspace(-2 * np.pi, 2 * np.pi, Ln)  # 范围内等分Ln分。
Xit = np.arange(1, Ln + 1)
y1 = np.sin(u)
y2 = y1 * 2

########画图##################################################################################################

# 画图，可以命名，图标，大小，像素，背景色，
plt.figure(num='fig1', figsize=(9, 5), dpi=80, facecolor='m', edgecolor='y', linewidth=10, frameon=True)
# 设置图片位置占比
left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
plt.axes([left, bottom, width, height])

# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['STSong']
plt.rcParams['font.size'] = 20
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False

# 图片分割线
plt.grid(color='r', linestyle='--', linewidth=1, alpha=0.3)
##########################################################################
# 放两张图一个绿色点，一个红线
PL1 = plt.plot(u, y1, 'g:', label='Quxian', linewidth=3)
PL2 = plt.plot(u, y2, 'r', label='曲线', linewidth=3)
plt.legend(loc='lower right', fontsize=20, ncol=1)  # 图内标识的图片标识的位置，放在右侧，一列

# labelss = plt.legend(loc='right',fontsize=20,ncol=1).get_texts()
# [label.set_fontname('Times New Roman') for label in labelss]
# label = labelss[0]
# label.set_fontproperties('STSong')


#############################################################################
# 表头名字
plt.title('Python', fontsize=30, fontname='Times New Roman')
# 限制轴范围
plt.axis([-8, 8, -6, 6])  # 等价

# 标识横轴纵轴
plt.xlabel('姓名:', fontproperties='STSong', fontsize=20, color='black')
plt.ylabel('Xuehao:12345678', fontname='Times New Roman', fontsize=20, color='g')

# 坐标轴字符大小调整
plt.tick_params(labelsize=30)

# 定义的位置增加标号
# plt.text(-2, 4, "矿大",fontproperties = 'simHei',  fontdict={'size': 50, 'color': 'r'},ha='center', va='bottom')
plt.scatter(-2, 4, s=100, c='b', marker='*')
plt.text(-2, 4, "矿大", fontproperties='simHei', fontdict={'size': 20, 'color': 'k'}, ha='right', va='top')
# ha有三个选择：right,center,left
# va有四个选择：'top', 'bottom', 'center', 'baseline'
# 画箭头
plt.annotate("标记", xy=(3, 4), xytext=(-3, -4), arrowprops=dict(facecolor='black', shrink=0, width=2))

# width表示箭头宽度

# 显示图片
plt.savefig('Tupian.png')
plt.show()
# 关闭图片
plt.close
