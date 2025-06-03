# 写图数据库
# 写入Comment与user信息

from py2neo import *
import json

data_path = "../data/origin"
output_path = "../output"

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


def write_comments(graph):
    file = open(data_path +"/comments_1.txt", encoding="utf-8")
    i = 0
    for line in file:
        comment = json.loads(line)
        user = comment['user']
        song_id = comment['song_id']
        # 创建用户节点 MERGE 不重复创建用户
        r_user = {"uid": user['userId'], 'name': user['nickname'], 'vipType': user['vipType']}
        insert_cql = "MERGE  (user:User{}) RETURN user".format(dict2cql(r_user))
        graph.run(insert_cql)
        # 创建comment节点 以及联系
        r_comment = {"uid": comment['commentId'],
                     'time': comment['time'],
                     'likedCount': comment['likedCount'],
                     'content': comment['content'].replace("\"", "")
                     }
        insert_cql = "MATCH (song:Song),(user:User) WHERE song.uid={} AND user.uid={} " \
                     "CREATE (user) - [:Publish] -> (comment:Comment{}) - [:Belong] -> (song)".format(song_id, user['userId'], dict2cql(r_comment))

        # print(insert_cql)
        graph.run(insert_cql)

        i += 1
        print(i)


if __name__ == '__main__':
    graph =Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    write_comments(graph)
