#!/usr/bin/python3
# -*-coding: utf-8-*-
import os
import re
import json
import time


def timestamp2hour(timestamp):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    # dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    dt = time.strftime("%H", time_local)
    return dt


def delete_file(del_path):
    for file in os.listdir(del_path):
        file_path = os.path.join(del_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    # os.rmdir(del_path)


origin_txt_path = "files/comments.txt"
song_json_path = "classes_data/songs.json"
singer_json_path = "classes_data/singers.json"
songs_forder = "classes_data/songs_data/"
singers_forder = "classes_data/singers_data/"
time_forder = "classes_data/time_data/"


if __name__ == '__main__':
    # songs_dict = {}
    # singers_dict = {}

    delete_file(songs_forder)
    delete_file(singers_forder)
    delete_file(time_forder)

    with open(song_json_path, 'r', encoding='utf-8') as f:
        songs_dict = json.load(f)
    with open(singer_json_path, 'r', encoding='utf-8') as f:
        singers_dict = json.load(f)

    with open(origin_txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            # line = r'{}'.format(line) 无效
            # line = re.sub(r'\\', r'\\\\', line)
            try:
                json_item = json.loads(line)
                content = json_item['content']
                if len(content) < 8:
                    continue
                # print(content)
                song_id = json_item['song_id']
                song_id = str(song_id)
                if song_id in songs_dict:
                    # print("song_id:", song_id)
                    song_name = songs_dict[song_id]['name']
                    song_singer_id = songs_dict[song_id]['singer']
                    song_singer_id = str(song_singer_id)
                    if song_singer_id not in singers_dict:
                        continue

                    hour = timestamp2hour(float(json_item['time']/1000))

                    song_file_path = os.path.join(songs_forder, "{}.txt".format(song_name))
                    singer_file_path = os.path.join(singers_forder, "{}.txt".format(singers_dict[song_singer_id]))
                    hour_file_path = os.path.join(time_forder, "{}.txt".format(hour))

                    with open(song_file_path, 'a', encoding='utf-8') as f:
                        f.write(content)

                    with open(singer_file_path, 'a', encoding='utf-8') as f:
                        f.write(content)

                    with open(hour_file_path, 'a', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                print(e)
