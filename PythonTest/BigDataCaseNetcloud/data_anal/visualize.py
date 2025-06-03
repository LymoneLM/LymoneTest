
import os
from wordcloud import WordCloud
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from pyecharts import options as opts
from pyecharts.charts import Pie

SAVAPATH = '/home/hadoop/Experiment/Ex2_WordCount/results/'

class visualize:

    def rdd2dic(self,resRdd,topK):
        # 提示：SparkRdd有函数可直接转换
        # 【现在你应该完成下面函数编码】
        resDic =  resRdd.collectAsMap()
        # 截取字典前K个
        K = 0
        wordDicK = {}
        for key, value in resDic.items():
            # 完成循环截取字典
            if K < topK:
                wordDicK[key] = value
                K += 1
            else:
                break
        return wordDicK

    def drawWorcCloud(self, wordDic):
        # 生成词云
        #font_path='/usr/share/fonts/dejavu/DejaVuSans-ExtraLight.ttf'
        wc = WordCloud(font_path='/home/hadoop/Experiment/Ex2_WordCount/simkai.ttf',
                       background_color='white',
                       max_words=2000,
                       width=1920, height=1080,
                       margin=5)
        wc.generate_from_frequencies(wordDic)
        # 保存结果
        wc.to_file(os.path.join(SAVAPATH, '词云可视化.png'))

    def drawPie(self, wordDic):

        key_list = wordDic.keys()      # wordDic所有key组成list
        value_list= wordDic.values()   # wordDic所有value组成list
        def pie_position() -> Pie:
            c = (
                Pie()
                    .add
                    (
                    "",
                    [list(z) for z in zip(key_list, value_list)], # dic -> list
                    center=["35%", "50%"],
                    )
                    .set_global_opts
                    (
                    title_opts=opts.TitleOpts(title='饼图可视化'), # 设置标题
                    legend_opts=opts.LegendOpts(pos_left="15%"),
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
            return c
        # 保存结果
        make_snapshot(snapshot, pie_position().render(), SAVAPATH + '饼图可视化.png')
