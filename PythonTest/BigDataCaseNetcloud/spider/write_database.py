# 写图数据库
# 写入歌手与歌曲信息

from py2neo import *
import json

data_path = "../data/origin"
output_path = "../output"

def getData(filename: str, need_info: list = None):
    file = open(filename, encoding="utf-8")
    res = []
    for line in file:
        item = json.loads(line)
        # 信息筛选
        if need_info is not None:
            r_item = dict()
            for attr in need_info:
                r_item[attr] = item[attr]
            res.append(r_item)
        else:
            res.append(item)
    print("数据总量：" + str(len(res)))
    return res


# 写入数据库
def writeSingers(graph):
    need_info = ['id', 'name', 'picUrl']
    singers = getData(data_path +"/singers.txt", need_info)
    nodes = []
    for singer in singers:
        singer['uid'] = singer['id']
        del singer['id']
        node = Node("Singer", **singer)
        nodes.append(node)
    subgraph = Subgraph(nodes)
    graph.create(subgraph)


def dict2cql(dict_: dict):
    res = '{'
    for k in dict_.keys():
        res += (str(k) + ":")
        if type(dict_[k]) == str:
            res += "\"" + dict_[k] + "\""
        else:
            res += str(dict_[k])
        res += ","
    return res[0:len(res) - 1] + '}'


def writeSongs(graph):
    need_info = ['id', 'name', 'ar', 'publishTime']
    songs = getData(data_path +"/songs.txt", need_info)
    rels = []
    matcher = NodeMatcher(graph)
    i = 0
    for song in songs:
        singers = list(song['ar'])
        del song['ar']
        # 插入歌曲节点
        song['uid'] = song['id']
        del song['id']
        insert_cql = "CREATE (:Song {})".format(dict2cql(song))
        try:
            graph.run(insert_cql)
        except Exception as e:
            print(e)
        # 增加歌手与和歌曲的关系
        for singer in singers:
            rel_cql = "MATCH (s1:Singer),(s2:Song) \
                    WHERE s1.uid={} and s2.uid={}   \
                    CREATE (s1)-[:Sing]->(s2)".format(singer['id'], song['uid'])
            try:
                graph.run(rel_cql)
            except Exception as e:
                print(e)
        i += 1
        if i % 100 == 0:
            print("No.{} ".format(i) + song['name'])


if __name__ == '__main__':
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    graph.delete_all()
    writeSingers(graph)
    writeSongs(graph)
    # test
