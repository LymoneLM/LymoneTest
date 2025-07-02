import os
import json
import argparse
from glob import glob

def create_notebook(input_dir, output_file):
    # 获取所有.py文件并按数字顺序排序
    files = glob(os.path.join(input_dir, "*.py"))
    files.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))

    # 初始化Notebook结构
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    for file_path in files:
        # 获取原始文件名
        filename = os.path.basename(file_path)
        
        # 添加Markdown单元格显示文件名
        notebook["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"### {filename}"]
        })

        # 添加代码单元格
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        notebook["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code_content
        })

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='合并Python文件到Jupyter Notebook')
    parser.add_argument('-i', '--input', required=True, help='输入目录路径')
    parser.add_argument('-o', '--output', required=True, help='输出Notebook路径')
    args = parser.parse_args()

    create_notebook(args.input, args.output)
    print(f"Notebook已生成: {args.output}")