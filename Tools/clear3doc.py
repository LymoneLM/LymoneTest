import os
import argparse


def delete_doc_with_txt(folder_path):
    """删除存在同名txt文件的doc和docx文件（包括子目录）"""
    extensions = ('.doc', '.docx')

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(extensions):
                file_path = os.path.join(root, filename)
                name = os.path.splitext(filename)[0]
                txt_path = os.path.join(root, f"{name}.txt")

                if os.path.exists(txt_path):
                    try:
                        os.remove(file_path)
                        print(f"已删除: {file_path} (存在同名txt文件)")
                    except Exception as e:
                        print(f"删除失败: {file_path} - {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='递归删除存在同名txt的doc/docx文件')
    parser.add_argument('folder', help='目标文件夹路径')

    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"错误: 路径 '{args.folder}' 不是有效文件夹")
        exit(1)

    print(f"开始处理文件夹: {args.folder}")
    print("=" * 50)
    delete_doc_with_txt(args.folder)
    print("=" * 50)
    print("处理完成")