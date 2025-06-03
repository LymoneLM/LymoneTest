import json
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Line
from collections import defaultdict
from matplotlib import font_manager

# 设置数据路径
data_path = "../data/origin"
output_path = "../output"


# 模拟SongsHot模块的函数（实际项目中应替换为真实实现）
class SongsHot:
    @staticmethod
    def get_commentsCount(song_id):
        """模拟获取歌曲评论数（按日期）"""
        # 实际项目中应替换为真实API调用
        # 这里返回模拟数据
        days = 30
        base_date = datetime.date.today() - datetime.timedelta(days=days)
        comments_data = []
        for i in range(days):
            date_str = (base_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            # 生成随机但递减的数据
            count = max(100, 500 - i * 10 + np.random.randint(-20, 30))
            comments_data.append([date_str, count])
        return comments_data

    @staticmethod
    def get_likedCount(song_id):
        """模拟获取歌曲点赞数（按日期）"""
        # 实际项目中应替换为真实API调用
        days = 30
        base_date = datetime.date.today() - datetime.timedelta(days=days)
        likes_data = []
        for i in range(days):
            date_str = (base_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            # 生成随机但递减的数据
            count = max(50, 300 - i * 5 + np.random.randint(-15, 25))
            likes_data.append([date_str, count])
        return likes_data

    @staticmethod
    def get_sumCount(comments_data, likes_data):
        """合并评论数和点赞数为热度值"""
        # 创建一个字典来按日期聚合数据
        date_dict = defaultdict(int)

        # 处理评论数据
        for date, count in comments_data:
            date_dict[date] += count * 0.7  # 评论权重为0.7

        # 处理点赞数据
        for date, count in likes_data:
            date_dict[date] += count * 0.3  # 点赞权重为0.3

        # 转换为列表并排序
        result = [[date, date_dict[date]] for date in date_dict]
        result.sort(key=lambda x: x[0])  # 按日期排序

        return result


# 获取歌手的所有歌曲
def get_singerSongs(singerName):
    songsList = []
    songs_file = os.path.join(data_path, 'songs.txt')

    if not os.path.exists(songs_file):
        print(f"警告: 歌曲文件不存在: {songs_file}")
        return songsList

    try:
        with open(songs_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    song_data = json.loads(line.strip())
                    # 检查是否有歌手信息
                    if 'ar' in song_data and song_data['ar'] and song_data['ar'][0]['name'] == singerName:
                        songsList.append(song_data['id'])
                except json.JSONDecodeError:
                    print(f"JSON解析错误: {line[:50]}...")
                    continue
    except Exception as e:
        print(f"读取歌曲文件时出错: {e}")

    return songsList


if __name__ == '__main__':
    singerName = "毛不易"

    # 获取歌手的所有歌曲
    songList = get_singerSongs(singerName)
    print(f"找到 {len(songList)} 首歌曲")

    # 如果没有找到歌曲，使用模拟数据
    if not songList:
        print("未找到歌曲，使用模拟歌曲ID")
        songList = [123456, 789012, 345678]  # 模拟歌曲ID

    # 初始化日期热度字典
    date_hot_dict = defaultdict(float)

    # 统计每首歌的热度
    for songid in songList:
        print(f"处理歌曲: {songid}")

        # 获取评论数据
        comments_data = SongsHot.get_commentsCount(songid)
        # 获取点赞数据
        likes_data = SongsHot.get_likedCount(songid)
        # 合并为热度值
        song_hot_data = SongsHot.get_sumCount(comments_data, likes_data)

        # 累加到总热度
        for date, hot_value in song_hot_data:
            date_hot_dict[date] += hot_value

    # 转换为列表并排序
    singer_HotSum = [[date, date_hot_dict[date]] for date in date_hot_dict]
    singer_HotSum.sort(key=lambda x: x[0])  # 按日期排序

    # 提取日期和热度值
    dates = [item[0] for item in singer_HotSum]
    hot_values = [item[1] for item in singer_HotSum]

    print("日期\t\t热度值")
    for date, value in zip(dates, hot_values):
        print(f"{date}\t{value:.2f}")

    # 创建折线图
    line = Line()
    line.add_xaxis(dates)
    line.add_yaxis(
        series_name="热度值",
        y_axis=hot_values,
        is_smooth=True,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
                opts.MarkPointItem(type_="average", name="平均值")
            ]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]
        ),
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=3),
        itemstyle_opts=opts.ItemStyleOpts(color="#d14a61"),
        areastyle_opts=opts.AreaStyleOpts(opacity=0.3, color="#d14a61")
    )

    line.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{singerName}热度随时间变化",
            subtitle="数据来源: 网易云音乐",
            pos_left="center"
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axislabel_opts=opts.LabelOpts(rotate=45),
            name="日期"
        ),
        yaxis_opts=opts.AxisOpts(
            name="热度值",
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        datazoom_opts=opts.DataZoomOpts(is_show=True, type_="slider"),
        legend_opts=opts.LegendOpts(is_show=False)
    )

    # 渲染图表
    output_file = os.path.join(output_path, f"{singerName}_hot_trend.html")
    line.render(output_file)
    print(f"图表已生成: {output_file}")

    # 设置中文字体支持
    try:
        # 尝试使用系统自带的中文字体
        font_list = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        chinese_fonts = [f for f in font_list if any(
            keyword in f.lower() for keyword in ['simhei', 'simsun', 'microsoft yahei', 'noto sans cjk'])]

        if chinese_fonts:
            # 使用找到的第一个中文字体
            font_path = chinese_fonts[0]
            zh_font = font_manager.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = zh_font.get_name()
        else:
            # 如果找不到中文字体，使用默认字体并显示警告
            print("警告: 未找到系统中文字体，图表中文可能显示为方块")
            plt.rcParams['font.family'] = 'sans-serif'

        # 确保负号正常显示
        plt.rcParams['axes.unicode_minus'] = False
    except Exception as e:
        print(f"设置中文字体时出错: {e}")
        # 回退到默认设置
        plt.rcParams['font.family'] = 'sans-serif'

    # 同时生成matplotlib图表作为备份
    plt.figure(figsize=(12, 6))
    plt.plot(dates, hot_values, 'o-', color='#d14a61', linewidth=2)
    plt.title(f"{singerName}热度随时间变化", fontsize=14)
    plt.xlabel("日期", fontsize=12)
    plt.ylabel("热度值", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # 保存图片
    img_file = os.path.join(output_path, f"{singerName}_hot_trend.png")
    plt.savefig(img_file, dpi=300)
    print(f"备份图片已生成: {img_file}")