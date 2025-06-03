import json
import numpy as np
from pyecharts.charts import Pie
from pyecharts import options as opts
from collections import defaultdict

data_path = "../data/origin"
output_path = "../output"
prefix = 'http://163api.qijieya.cn/'


# 获取歌手所有歌曲
def get_singerSongs(singerName):
    songsList = []
    with open(f"{data_path}/songs.txt", 'r', encoding="utf-8") as f:
        for line in f:
            song_data = json.loads(line)
            # 检查歌手信息是否存在
            if 'ar' in song_data and len(song_data['ar']) > 0:
                if song_data['ar'][0]['name'] == singerName:
                    songsList.append(song_data['id'])
    return songsList


# 获取不同类型的粉丝数
def get_fansRights(songList):
    # 使用集合存储用户ID，确保唯一性
    all_users = set()
    vip_users = set()

    with open(f"{data_path}/comments_2.txt", 'r', encoding="utf-8") as f:
        for line in f:
            comment = json.loads(line)
            if comment['song_id'] in songList:
                user_id = comment['user']['userId']
                all_users.add(user_id)

                # 更准确的VIP判断
                if 'vipRights' in comment['user'] and isinstance(comment['user']['vipRights'], dict):
                    vip_users.add(user_id)

    # 计算普通用户数
    regular_count = len(all_users) - len(vip_users)
    return [regular_count, len(vip_users)]


if __name__ == '__main__':
    singerName = "毛不易"

    # 获取歌手的所有歌曲ID
    songList = get_singerSongs(singerName)
    print(f"找到 {len(songList)} 首歌曲")

    # 获取粉丝统计数据
    fan_counts = get_fansRights(songList)
    print(f"普通粉丝: {fan_counts[0]}, VIP粉丝: {fan_counts[1]}")

    # 创建饼图
    pie = Pie()
    pie.add(
        series_name="粉丝类型",
        data_pair=[
            ("普通粉丝", fan_counts[0]),
            ("VIP粉丝", fan_counts[1])
        ],
        radius=["30%", "70%"],
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(is_show=True, formatter="{b}: {c} ({d}%)")
    )

    pie.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"歌手粉丝类别 - {singerName}",
            subtitle=f"总计粉丝数: {sum(fan_counts)}"
        ),
        legend_opts=opts.LegendOpts(
            orient="vertical",
            pos_left="left"
        )
    )

    pie.render("singer_fans.html")
    print("图表已生成: singer_fans.html")