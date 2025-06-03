# txt数据写入图数据库v1

from py2neo import Graph, Node, Relationship, NodeMatcher, Subgraph, RelationshipMatcher
import json

data_path = "../data/origin"
output_path = "../output"

def getSinger():
    file = open(data_path+"/singers.txt", encoding="utf-8")
    singers = []
    for line in file:
        singers.append(json.loads(line))
    file.close()
    return singers


def getSongs():
    file = open(data_path+"/songs.txt", encoding="utf-8")
    singers = []
    for line in file:
        singers.append(json.loads(line))
    file.close()
    return singers


def insert_singers():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))

    # graph = Graph("bolt://ip address:port", auth=("user", "password"))  # 建立连接
    tx = graph.begin()    # 开始一次 Transaction
    singers = getSinger()    # 以某种方式获取歌手信息
    for singer in singers:
        node = Node("Singer", **singer)  # 构造结点对象，Label为Singer，属性来自singer(dict类型)
        tx.create(node)     # 在数据库中创建结点
        tx.push(node)       # push到服务器
    tx.commit()  # 提交 Transaction
    print("结束")


def delNoNeedInfo(song):
    del song['ar']  # 去除冗余信息
    del song['al']  # 去除冗余信息
    del song['h']
    del song['l']
    del song['m']
    del song['privilege']
    return song

def clean_node_properties(data):
    """确保所有属性值都是 Neo4j 支持的基本类型"""
    cleaned = {}
    for key, value in data.items():
        # 处理 None 值
        if value is None:
            cleaned[key] = ""  # 转换为空字符串
        # 处理字典和列表
        elif isinstance(value, (dict, list)):
            # 将复杂类型转换为 JSON 字符串
            cleaned[key] = json.dumps(value, ensure_ascii=False)
        # 处理其他非原始类型
        elif not isinstance(value, (str, int, float, bool)):
            # 转换为字符串表示
            cleaned[key] = str(value)
        else:
            # 原始类型直接保留
            cleaned[key] = value
    return cleaned

def insert_songs():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    tx = graph.begin()
    matcher = NodeMatcher(graph)    # 创建匹配器对象
    songs = getSongs()  # 以某种方式获取歌曲信息
    for song in songs:
        # 查找singer结点
        singer_name = song['ar'][0]['name']
        singer_node = matcher.match("Singer", name=singer_name).first()
        # 创建song结点
        song = delNoNeedInfo(song)  # 去除冗余信息
        song = clean_node_properties(song)
        song_node = Node("Song", **song)
        # 创建双向关系
        r1 = Relationship(singer_node, "Create", song_node)
        r2 = Relationship(song_node, "Belong", singer_node)

        tx.create(song_node)     # 在数据库中创建结点
        tx.push(song_node)       # push到服务器
        tx.create(r1)
        tx.create(r2)
        tx.push(r1)
        tx.push(r2)
    tx.commit()


if __name__ == '__main__':
    insert_singers()
    insert_songs()
