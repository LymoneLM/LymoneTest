import json
import urllib.request
import urllib.parse
import time
import operator
from pyecharts.charts import Bar, Map, Geo
from pyecharts import options as opts

data_path = "../data/origin"
output_path = "../output"
prefix = 'http://163api.qijieya.cn/'
f1 = open(data_path + '/songs.txt', 'r', encoding="utf-8")
f2 = open(data_path + '/comments_1.txt', 'r', encoding="utf-8")


# 进行get请求并将JSON解码  加入自动重试
def doGet(url):
    i = 1
    while True:
        try:
            req = urllib.request.Request(url=prefix + url, method="GET")
            response = urllib.request.urlopen(req)
            res = response.read().decode('utf-8')
            return json.loads(res)
        except:
            print("异常URL：{}".format(url))
            if i < 4:
                time.sleep(10)
                i += 1
            else:
                return 0


# 获取歌手的歌曲
def get_singerSongs(singerName):
    f1.seek(0)  # 重置文件指针到开头
    records = f1.readline()
    songsList = list()
    while records:
        try:
            records_dict = json.loads(records)
            if records_dict['ar'][0]['name'] == singerName:
                songsList.append(records_dict['id'])
            records = f1.readline()
        except json.JSONDecodeError:
            records = f1.readline()
            continue
    return songsList


# 获取歌曲的评论用户
def get_comments_users(songList):
    f2.seek(0)  # 重置文件指针到开头
    comments = f2.readline()
    userList = list()
    while comments:
        try:
            comments_dict = json.loads(comments)
            if comments_dict['song_id'] in songList:
                user_id = comments_dict['user']['userId']
                # 去重处理
                if user_id not in userList:
                    userList.append(user_id)
            comments = f2.readline()
        except json.JSONDecodeError:
            comments = f2.readline()
            continue
    return userList


# 获取粉丝的地区分布
def get_fans_distribution(fansList):
    data = {}
    i = 1
    total_users = len(fansList)

    for uId in fansList:
        url = f'/user/detail?uid={uId}'
        user_detail = doGet(url)

        if user_detail == 0 or 'profile' not in user_detail:
            print(f"跳过无效用户: {uId}")
            continue

        address = user_detail['profile'].get('city', 0)
        # 转换为省级行政区代码
        province_code = address // 10000 * 10000

        # 省份映射
        province_map = {
            110000: '北京', 120000: '天津', 130000: '河北', 140000: '山西', 150000: '内蒙古',
            210000: '辽宁', 220000: '吉林', 230000: '黑龙江', 310000: '上海', 320000: '江苏',
            330000: '浙江', 340000: '安徽', 350000: '福建', 360000: '江西', 370000: '山东',
            410000: '河南', 420000: '湖北', 430000: '湖南', 440000: '广东', 450000: '广西',
            460000: '海南', 510000: '四川', 520000: '贵州', 530000: '云南', 540000: '西藏',
            500000: '重庆', 610000: '陕西', 620000: '甘肃', 630000: '青海', 640000: '宁夏',
            650000: '新疆', 710000: '台湾', 810000: '香港', 820000: '澳门'
        }

        province_name = province_map.get(province_code, "未知")

        if province_name == "未知":
            print(f"未知省份代码: {province_code} (原始地址: {address})")
            continue

        data[province_name] = data.get(province_name, 0) + 1

        # 打印进度
        print(f"处理进度: {i}/{total_users} - 当前省份: {province_name}")
        i += 1

    # 按粉丝数排序并只保留前十
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
    return dict(sorted_data)


if __name__ == '__main__':
    singerName = "毛不易"

    # 1. 获取歌手的所有歌曲ID
    songList = get_singerSongs(singerName)
    print(f"找到歌曲数量: {len(songList)}")

    # 2. 获取这些歌曲的评论用户
    fansList = get_comments_users(songList)
    print(f"获取用户数量: {len(fansList)}")

    # 3. 获取粉丝地区分布
    fansDist = get_fans_distribution(fansList)
    print("粉丝地区分布:")
    for province, count in fansDist.items():
        print(f"{province}: {count}")

    # 4. 使用真实数据绘制地图
    # 初始化地图
    map_chart = Map(init_opts=opts.InitOpts(
        width="1000px",
        height="800px",
        bg_color="#404a59"
    ))

    # 准备数据对
    data_pair = [(province, count) for province, count in fansDist.items()]

    # 设置全局选项
    map_chart.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{singerName}粉丝地区分布",
            subtitle="数据来源: 网易云音乐API",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=20),
            subtitle_textstyle_opts=opts.TextStyleOpts(color="#ccc", font_size=14)
        ),
        visualmap_opts=opts.VisualMapOpts(
            min_=min(fansDist.values()),
            max_=max(fansDist.values()),
            is_piecewise=True,  # 分段显示
            range_text=["高", "低"],
            pos_left="10px",
            pos_bottom="20px",
            textstyle_opts=opts.TextStyleOpts(color="#ddd")
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{b}: {c} 人"
        )
    )

    # 添加数据系列
    map_chart.add(
        series_name="粉丝数量",
        maptype="china",
        data_pair=data_pair,
        is_map_symbol_show=False,  # 不显示标记点
        label_opts=opts.LabelOpts(
            is_show=True,
            color="#333",
            formatter="{b}: {c}"
        ),
        itemstyle_opts=opts.ItemStyleOpts(
            border_color="#111",
            border_width=0.5
        )
    )

    # 设置系列特效选项
    map_chart.set_series_opts(
        markpoint_opts=opts.MarkPointOpts(
            symbol="pin",
            symbol_size=40,
            label_opts=opts.LabelOpts(
                formatter="{b}: {c}",
                color="#fff",
                position="inside"
            )
        )
    )

    # 渲染地图
    output_file = f"{output_path}/{singerName}_fans_distribution.html"
    map_chart.render(output_file)
    print(f"地图已保存为: {output_file}")

    # 关闭文件
    f1.close()
    f2.close()