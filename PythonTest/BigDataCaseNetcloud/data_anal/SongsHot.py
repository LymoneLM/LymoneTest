import json
import time
import operator
import pandas as pd
from collections import defaultdict
from pyecharts.charts import Line
from pyecharts import options as opts
from datetime import datetime

data_path = r"../data/origin"
output_path = "../output"


def get_song_data(music_id):
    """
    一次性读取所有相关数据，避免多次读取大文件
    返回: (评论计数, 点赞计数)
    """
    comments_count = defaultdict(int)
    liked_count = defaultdict(int)

    with open(data_path+"/comments_2.txt", 'r', encoding="utf-8") as f:
        for line in f:
            try:
                comment = json.loads(line)
                if comment['song_id'] == music_id:
                    # 转换时间戳为年月格式 (YYYYMM)
                    timestamp = comment['time'] // 1000
                    date_key = time.strftime("%Y%m", time.localtime(timestamp))

                    # 统计评论次数
                    comments_count[date_key] += 1

                    # 统计点赞总数
                    liked_count[date_key] += int(comment.get('likedCount', 0))
            except (json.JSONDecodeError, KeyError) as e:
                print(f"解析错误: {e}, 行内容: {line}")
                continue

    # 排序并转换为列表
    sorted_comments = sorted(comments_count.items(), key=operator.itemgetter(0))
    sorted_liked = sorted(liked_count.items(), key=operator.itemgetter(0))

    return sorted_comments, sorted_liked


def format_dates(date_keys):
    """将YYYYMM格式转换为更易读的格式 (YYYY年MM月)"""
    return [f"{d[:4]}年{d[4:]}月" for d in date_keys]


def create_line_chart(music_id, song_name):
    # 获取数据
    comments_data, liked_data = get_song_data(music_id)

    # 提取日期和数值
    dates = [item[0] for item in comments_data]
    comments_values = [item[1] for item in comments_data]
    liked_values = [item[1] for item in liked_data]

    # 计算热度值 = 评论数 + 点赞数
    hot_values = [c + l for c, l in zip(comments_values, liked_values)]

    # 格式化日期
    formatted_dates = format_dates(dates)

    # 创建折线图
    line = Line(
        init_opts=opts.InitOpts(width="1200px", height="600px")
    )

    # 添加三条线
    line.add_xaxis(formatted_dates)
    line.add_yaxis(
        "评论数",
        comments_values,
        is_smooth=True,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        linestyle_opts=opts.LineStyleOpts(width=3),
        itemstyle_opts=opts.ItemStyleOpts(color="#5793f3")
    )

    line.add_yaxis(
        "点赞数",
        liked_values,
        is_smooth=True,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        linestyle_opts=opts.LineStyleOpts(width=3, type_="dashed"),
        itemstyle_opts=opts.ItemStyleOpts(color="#d14a61")
    )

    line.add_yaxis(
        "热度值",
        hot_values,
        is_smooth=True,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="峰值热度"),
                opts.MarkPointItem(type_="min", name="低谷热度"),
            ]
        ),
        linestyle_opts=opts.LineStyleOpts(width=4),
        itemstyle_opts=opts.ItemStyleOpts(color="#675bba")
    )

    # 设置全局选项
    line.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"歌曲《{song_name}》热度变化趋势",
            subtitle=f"数据统计周期: {formatted_dates[0]} 至 {formatted_dates[-1]}",
            pos_left="center"
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(
            is_show=True,
            feature={
                "saveAsImage": {},
                "dataView": {"readOnly": False},
                "restore": {},
                "dataZoom": {}
            }
        ),
        legend_opts=opts.LegendOpts(
            pos_top="5%",
            pos_left="center",
            orient="horizontal"
        ),
        yaxis_opts=opts.AxisOpts(
            name="数量",
            name_location="end",
            name_gap=15,
            axislabel_opts=opts.LabelOpts(formatter="{value} 次")
        ),
        xaxis_opts=opts.AxisOpts(
            name="时间",
            name_location="end",
            name_gap=30,
            axislabel_opts=opts.LabelOpts(rotate=45)
        )
    )

    # 生成HTML文件
    output_file = f"{output_path}/{song_name}_热度变化.html"
    line.render(output_file)
    print(f"图表已生成: {output_file}")

    # 返回数据用于调试
    return {
        "dates": dates,
        "comments": comments_values,
        "liked": liked_values,
        "hot": hot_values
    }


if __name__ == '__main__':
    # 歌曲信息
    song_id = 569200210  # 一荤一素
    song_name = "一荤一素"

    # 创建图表并获取数据
    data = create_line_chart(song_id, song_name)

    # 打印数据摘要
    print("\n数据摘要:")
    print(f"统计周期: {data['dates'][0]} 至 {data['dates'][-1]}")
    print(f"总评论数: {sum(data['comments'])}")
    print(f"总点赞数: {sum(data['liked'])}")
    print(f"最高热度值: {max(data['hot'])} (出现在 {data['dates'][data['hot'].index(max(data['hot']))]})")

    # 创建数据表格 (可选)
    df = pd.DataFrame({
        "日期": format_dates(data['dates']),
        "评论数": data['comments'],
        "点赞数": data['liked'],
        "热度值": data['hot']
    })
    print("\n月度数据表:")
    print(df)