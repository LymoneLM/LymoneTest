#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
import time

base_target_dir = "classes_data/"
base_source_dir = "files/"


def generate_singer_json():
    singers_target_path = os.path.join(base_target_dir, "singers.json")
    singers_source_path = os.path.join(base_source_dir, "singers.txt")

    singers_dict = {}
    with open(singers_source_path, 'r', encoding='utf-8') as f:
        for line in f:
            json_item = json.loads(line)
            print(json_item['name'])
            singers_dict[json_item['id']] = json_item['name']

    with open(singers_target_path, 'w') as f:
        json.dump(singers_dict, f)


def generate_song_json():
    songs_target_path = os.path.join(base_target_dir, "songs.json")
    songs_source_path = os.path.join(base_source_dir, "songs.txt")
    songs_dict = {}
    with open(songs_source_path, 'r', encoding='utf-8') as f:
        for line in f:
            json_item = json.loads(line)
            temp_dict = {}
            temp_dict['name'] = json_item['name']
            temp_dict['singer'] = json_item['ar'][0]['id']
            songs_dict[json_item['id']] = temp_dict

    with open(songs_target_path, 'w') as f:
        json.dump(songs_dict, f)


def timestamp2hour(timestamp):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    print(time_local)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    # dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    dt = time.strftime("%H", time_local)
    return dt


if __name__ == '__main__':
    dict = {"6": {"da": "chen", "xiao": "xiang"}, "5": {"da": "chen5", "xiao": "xiang"}}
    for i in dict:
        print(i)
