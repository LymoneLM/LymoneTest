# 写图数据库
# 写入歌曲的相似信息

from py2neo import *
import json

data_path = "../data/origin"
output_path = "../output"

# 使用py2neo的函数API效率太低
# 本文件中的插入操作使用CQL实现

def write_similar(graph):
    file = open(data_path +"/similar.txt", encoding="utf-8")
    i = 0
    for line in file:
        simi_info = json.loads(line)
        id1 = simi_info['source']
        id2 = simi_info['target']
        CQL = "MATCH (s1:Song),(s2:Song) \
                WHERE s1.uid={} and s2.uid={}   \
                CREATE (s1)-[simi:SimilarTo]->(s2)".format(id1, id2)
        graph.run(CQL)
        i += 1
        if i%100==0:
            print("No.{}".format(i))


if __name__ == '__main__':
    graph =Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    write_similar(graph)
        

