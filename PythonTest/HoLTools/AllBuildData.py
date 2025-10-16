"""
python list2csv.py input.txt
需要先行处理文件，删除数据头
"""
import csv
import re
import os
import sys


def parse_data_string(s):
    # 移除所有空白字符（包括换行和空格）
    s = re.sub(r'\s+', '', s)

    # 移除外层的大括号
    s = s.strip('{}')

    # 分割每个内部数组
    arrays = re.findall(r'\{([^}]*)\}', s)

    data = []
    for arr_str in arrays:
        # 分割数组中的元素
        elements = re.findall(r'\"([^\"]*)\"', arr_str)
        data.append(elements)

    return data


def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # 创建标题行
        headers = ['Index'] + [str(i) for i in range(len(data[0]))]
        writer.writerow(headers)

        # 写入数据行
        for idx, row in enumerate(data):
            writer.writerow([idx] + row)


def main():
    # 检查命令行参数
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("请输入输入文件路径: ")

    # 检查文件是否存在
    if not os.path.isfile(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        return

    # 读取输入文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data_str = f.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return

    # 解析数据
    try:
        data = parse_data_string(data_str)
    except Exception as e:
        print(f"解析数据时出错: {e}")
        return

    # 生成输出文件名
    base_name = os.path.splitext(input_file)[0]
    output_file = base_name + ".csv"

    # 写入CSV文件
    try:
        write_to_csv(data, output_file)
        print(f"CSV文件已成功创建: {output_file}")
    except Exception as e:
        print(f"写入CSV文件时出错: {e}")


if __name__ == "__main__":
    main()