import argparse
import os
from os import mkdir

def main():
    parser = argparse.ArgumentParser(description='Generate Markdown documentation from code files')
    parser.add_argument('folder', help='Target directory path')
    parser.add_argument('--head', help='Header Markdown file path')
    parser.add_argument('--tail', help='Footer Markdown file path')
    parser.add_argument('--output', help='Output directory path')
    args = parser.parse_args()

    # 处理目标文件夹路径
    target_folder = os.path.abspath(args.folder)
    output_folder = os.path.abspath(os.path.join(__file__, '..', "output"))
    if args.output:
        output_folder = os.path.abspath(args.output)

    if not os.path.isdir(target_folder):
        print(f"Error: '{args.folder}' is not a valid directory")
        return
    folder_name = os.path.basename(target_folder)

    try:
        if not os.path.isdir(output_folder):
            mkdir(output_folder)
    except Exception as e:
        print(f"Error: {str(e)} when touch folder '{output_folder}'")
    output_path = os.path.join(output_folder, f"{folder_name}.md")


    # 收集代码文件
    code_entries = []
    for root, dirs, files in os.walk(target_folder):
        dirs.sort()
        files.sort()
        for file in files:
            if file.endswith(('.cpp', '.py')):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, start=target_folder)
                code_entries.append((rel_path, abs_path))
    
    code_entries.sort(key=lambda x: x[0])

    # 生成主内容
    content_blocks = []
    for rel_path, abs_path in code_entries:
        lang = 'cpp' if rel_path.endswith('.cpp') else 'python'
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                code_content = f.read().rstrip('\n')
        except Exception as e:
            code_content = f"// Error reading file: {str(e)}"
        
        content_blocks.append(f"### {rel_path}\n\n```{lang}\n{code_content}\n```")

    # 处理头尾内容
    header = ""
    if args.head:
        try:
            with open(args.head, 'r', encoding='utf-8') as f:
                header = f.read().strip()
        except Exception as e:
            print(f"Warning: Header file error - {str(e)}")

    footer = ""
    if args.tail:
        try:
            with open(args.tail, 'r', encoding='utf-8') as f:
                footer = f.read().strip()
        except Exception as e:
            print(f"Warning: Footer file error - {str(e)}")

    # 合并内容
    final_content = []
    if header:
        final_content.append(header)
    final_content.append('\n\n'.join(content_blocks))
    if footer:
        final_content.append(footer)

    # 写入输出文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(final_content))
        print(f"Documentation generated: {output_path}")
    except Exception as e:
        print(f"Error writing output: {str(e)}")

if __name__ == '__main__':
    main()