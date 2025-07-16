import sys


def process_file(input_file, output_file=None):
    # 如果未提供输出文件，则覆盖原文件
    if output_file is None:
        output_file = input_file

    processed_lines = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 检查是否非空行（去除空白字符后）
            if line.strip():
                # 在行首添加两个中文全角空格
                processed_lines.append("　　" + line)
            else:
                # 空行保持不变
                processed_lines.append(line)

    # 写入处理结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python add_spaces.py <输入文件> [输出文件]")
        print("示例: python add_spaces.py input.txt output.txt")
        print("注意: 若不指定输出文件，将直接修改输入文件")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        process_file(input_file, output_file)
        print(f"处理完成! {'结果已保存到: ' + output_file if output_file else '文件已直接修改'}")
    except Exception as e:
        print(f"处理出错: {str(e)}")
        sys.exit(1)