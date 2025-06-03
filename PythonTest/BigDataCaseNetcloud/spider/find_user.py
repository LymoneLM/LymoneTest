# 从评论数据集获取用户id集合

import json

data_path = "../data/origin"
output_path = "../output"

if __name__ == '__main__':
    file = open(data_path+"/comments_1.txt", encoding="utf-8")
    out_file = open(output_path+"/userIds.txt", mode="w")
    user_list = []
    for line in file:
        try:
            obj = json.loads(line)
        except:
            continue
        uid = obj['user']['userId']
        user_list.append(uid)
    user_set = set(user_list)
    user_list = list(user_set)
    print(len(user_list))
    for uid in user_set:
        out_file.write(str(uid) + '\n')
    out_file.close()

