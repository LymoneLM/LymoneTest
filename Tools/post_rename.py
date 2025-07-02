# 给Hexo贴文文件重命名，头部附加YYYYMMDD日期
import os
import re
import argparse
from datetime import datetime


def extract_date_from_header(file_path):
    """从Markdown文件的元数据头中提取date字段值"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式匹配YAML元数据头
        header_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not header_match:
            return None

        header = header_match.group(1)
        # 在元数据头中查找date字段
        date_match = re.search(r'^date:\s*(.*)$', header, re.MULTILINE)
        if not date_match:
            return None

        date_str = date_match.group(1).strip()
        # 清理可能的引号
        return date_str.strip('"').strip("'")
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None


def format_date(date_str):
    """将各种日期格式转换为YYYYMMDD格式"""
    # 尝试解析常见日期格式
    formats = [
        "%Y-%m-%d %H:%M:%S",  # 2023-04-02 18:20:00
        "%Y-%m-%d %H:%M",  # 2023-04-02 18:20
        "%Y-%m-%d",  # 2023-04-02
        "%Y/%m/%d %H:%M:%S",  # 2023/04/02 18:20:00
        "%Y/%m/%d"  # 2023/04/02
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y%m%d")
        except ValueError:
            continue

    return None  # 无法解析的格式


def process_md_files(directory):
    """处理目录中的所有Markdown文件"""
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue

        # 检查文件名是否以8位数字开头
        if re.match(r'^\d{8}', filename):
            print(f"Skipping {filename} (already has date prefix)")
            continue

        file_path = os.path.join(directory, filename)
        date_str = extract_date_from_header(file_path)
        if not date_str:
            print(f"Skipping {filename} (no date found in metadata)")
            continue

        formatted_date = format_date(date_str)
        if not formatted_date:
            print(f"Skipping {filename} (unrecognized date format: {date_str})")
            continue

        # 构建新文件名并重命名
        new_filename = f"{formatted_date}{filename}"
        new_path = os.path.join(directory, new_filename)

        # 避免覆盖现有文件
        counter = 1
        while os.path.exists(new_path):
            new_filename = f"{formatted_date}{filename}_{counter}"
            new_path = os.path.join(directory, new_filename)
            counter += 1

        os.rename(file_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add date prefixes to Markdown files based on metadata')
    parser.add_argument('directory', help='Directory containing Markdown files')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        exit(1)

    process_md_files(args.directory)
    print("Processing complete.")