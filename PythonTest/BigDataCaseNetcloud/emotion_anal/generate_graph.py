import os
import json
from pyecharts.charts import Bar
from pyecharts import options as opts

if __name__ == '__main__':
    base_dir = "classes_data"
    singers_file = os.path.join(base_dir, "singers_info.json")
    songs_file = os.path.join(base_dir, "songs_info.json")
    time_file = os.path.join(base_dir, "time_info.json")

    # # plot time info
    with open(time_file) as f:
        time_dict = json.load(f)
        name_list = []
        len_list = []
        score_list = []
        for key, value in time_dict.items():
            name = key
            name_list.append(name)
            len = value['len']
            len_list.append(len)
            score = round(value['score'], 2)
            score_list.append(score)
        bar = (Bar().add_xaxis(name_list).add_yaxis(
            "评论热度", len_list).add_yaxis("评论抑郁度", score_list).set_global_opts(
                title_opts=opts.TitleOpts(title="一天时间内的评论分布"),
                xaxis_opts=opts.AxisOpts(name="时间")))
        bar.render('time.html')

    # plot singers info
    with open(singers_file, 'r') as f:
        well_known_singers = ['薛之谦', '毛不易', '陈奕迅', '李荣浩', '林俊杰', '谢春花', '华晨宇', '花粥', 'G.E.M.邓紫棋', '房东的猫', '陈粒', '赵雷', '张国荣', '五月天', '蔡徐坤']
        singer_dict = json.load(f)
        name_list = []
        len_list = []
        score_list = []
        # singer_sorted_list是一个元组列表
        # singer_dict.items() 返回一个元组列表，然后通过key进行排序
        singer_sorted_list = sorted(singer_dict.items(), key=lambda item: item[1]['len'], reverse=True)
        songs_num = 0
        for item in singer_sorted_list:
            if songs_num > 20:
                break
            name = item[0]
            if name not in well_known_singers:
                continue
            name_list.append(name)
            len = item[1]['len']
            len_list.append(len)
            score = round(item[1]['score'], 2)
            score_list.append(score)
            songs_num = songs_num+1
        bar = (Bar().add_xaxis(name_list).add_yaxis(
            "评论热度", len_list).add_yaxis("评论抑郁度", score_list).set_global_opts(
                title_opts=opts.TitleOpts(title="歌手最热评论排行榜"),
                xaxis_opts=opts.AxisOpts(name="歌手姓名",
                                         axislabel_opts={"rotate": 30})))
        bar.render('singers.html')

    # plot songs info
    with open(songs_file, 'r') as f:
        song_dict = json.load(f)
        name_list = []
        len_list = []
        score_list = []
        song_sorted_list = sorted(song_dict.items(), key=lambda item: item[1]['len'], reverse=True)
        songs_num = 0
        for item in song_sorted_list:
            if songs_num > 20:
                break
            name = item[0]
            name_list.append(name)
            len = item[1]['len']
            len_list.append(len)
            score = round(item[1]['score'], 2)
            score_list.append(score)
            songs_num = songs_num + 1
        bar = (Bar().add_xaxis(name_list).add_yaxis(
            "评论热度", len_list).add_yaxis("评论抑郁度", score_list).set_global_opts(
                title_opts=opts.TitleOpts(title="歌曲最热评论排行榜"),
                xaxis_opts=opts.AxisOpts(name="歌曲名",
                                         axislabel_opts={"rotate": 30})))
        bar.render('songs.html')
