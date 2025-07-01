# -*- coding: utf-8 -*-
"""
脚本功能：将指定目录中的所有.doc和.docx文件转换为.txt格式，并清理隐藏文字和空白行
使用方法：python doc_to_txt.py [目录路径]
"""

import os
import sys
import re
import pythoncom
from win32com import client as wc
import tempfile

try:
    from docx import Document

    HAS_DOCX_SUPPORT = True
except ImportError:
    HAS_DOCX_SUPPORT = False


def clean_text(text):
    """
    清理文本：
    1. 删除每行末尾的隐藏字符（乱码）
    2. 删除完全空白的行
    3. 删除孤立的不含中文字符的行
    4. 删除连续多个空行

    参数:
        text: 原始文本
    返回:
        清理后的文本
    """
    lines = text.splitlines()
    cleaned_lines = []

    # 1. 删除行末乱码（至少4个ASCII字符，且包含特殊字符）
    for line in lines:
        # 匹配行末乱码（前面有非ASCII字符，后面是至少4个可打印ASCII字符）
        match = re.search(r'([^\x00-\x7F])([\x20-\x7E]{4,})$', line)
        if match:
            prefix, junk = match.groups()
            # 检查是否只包含英文/数字/空格
            if not re.fullmatch(r'[\sA-Za-z0-9]*', junk):
                # 保留前缀字符，删除乱码部分
                line = line[:match.start(1)] + prefix

        cleaned_lines.append(line)

    # 2. 过滤空白行和无效行
    final_lines = []
    for line in cleaned_lines:
        # 跳过完全空白行
        if re.fullmatch(r'\s*$', line):
            continue

        # 检查是否包含中文字符
        has_chinese = re.search(r'[\u4e00-\u9fa5]', line)

        # 检查是否有实际内容（至少3个连续字母/数字）
        has_content = re.search(r'\w{3,}', line)

        # 保留有中文字符或有实际内容的行
        if has_chinese or has_content:
            final_lines.append(line)

    # 3. 删除连续空行（保留最多一个空行）
    result_lines = []
    prev_empty = False
    for line in final_lines:
        is_empty = re.match(r'^\s*$', line)
        if is_empty:
            if not prev_empty:
                result_lines.append('')
            prev_empty = True
        else:
            result_lines.append(line)
            prev_empty = False

    return '\n'.join(result_lines)


def get_unique_txt_path(doc_path):
    """
    根据文档路径生成唯一的txt文件路径

    参数:
        doc_path: 原始文档路径
    返回:
        唯一的txt文件路径
    """
    dirname = os.path.dirname(doc_path)
    base_name = os.path.splitext(os.path.basename(doc_path))[0]
    ext = '.txt'
    txt_path = os.path.join(dirname, base_name + ext)

    # 处理文件名冲突
    counter = 1
    while os.path.exists(txt_path):
        new_name = f"{base_name}_{counter}{ext}"
        txt_path = os.path.join(dirname, new_name)
        counter += 1

    return txt_path


def extract_text_using_docx(docx_path):
    """
    使用python-docx提取.docx文件文本内容

    参数:
        docx_path: .docx文件路径
    返回:
        提取的文本内容
    """
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def convert_doc_to_txt(directory_path):
    """
    将指定目录中的所有.doc和.docx文件转换为.txt格式并清理文本

    参数:
        directory_path: 要处理的目录路径
    """
    # 收集所有.doc和.docx文件
    doc_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.doc', '.docx')):
                full_path = os.path.join(root, file)
                doc_files.append(full_path)

    if not doc_files:
        print(f"在目录 {directory_path} 中没有找到.doc或.docx文件")
        return

    print(f"找到 {len(doc_files)} 个文档文件，开始转换...")

    # 初始化COM库
    pythoncom.CoInitialize()

    try:
        # 启动Word应用程序（仅用于处理.doc文件）
        word_app = wc.gencache.EnsureDispatch('Word.Application') if any(
            f.lower().endswith('.doc') for f in doc_files) else None
        if word_app:
            word_app.Visible = False  # 不显示Word界面

        success_count = 0
        error_count = 0

        for i, doc_path in enumerate(doc_files, 1):
            print(f"正在处理 ({i}/{len(doc_files)}): {os.path.basename(doc_path)}")
            file_ext = os.path.splitext(doc_path)[1].lower()

            try:
                txt_path = get_unique_txt_path(doc_path)
                default_path = os.path.join(os.path.dirname(doc_path),
                                            os.path.splitext(os.path.basename(doc_path))[0] + '.txt')
                if txt_path != default_path:
                    print(f"  注意: 文件已存在，将保存为: {os.path.basename(txt_path)}")

                content = ""

                # 处理.doc文件
                if file_ext == '.doc':
                    # 创建临时文件保存转换结果
                    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
                        temp_path = temp_file.name

                    try:
                        doc = word_app.Documents.Open(doc_path)
                        doc.SaveAs(temp_path, FileFormat=7, Encoding=65001)  # 7 = txt格式, 65001 = UTF-8编码
                        doc.Close(SaveChanges=False)

                        # 读取转换后的内容
                        with open(temp_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    finally:
                        # 删除临时文件
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)

                # 处理.docx文件
                elif file_ext == '.docx':
                    if HAS_DOCX_SUPPORT:
                        content = extract_text_using_docx(doc_path)
                    else:
                        # 没有python-docx库时使用Word COM对象
                        if not word_app:
                            word_app = wc.gencache.EnsureDispatch('Word.Application')
                            word_app.Visible = False

                        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
                            temp_path = temp_file.name

                        try:
                            doc = word_app.Documents.Open(doc_path)
                            doc.SaveAs(temp_path, FileFormat=7, Encoding=65001)
                            doc.Close(SaveChanges=False)

                            with open(temp_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                        finally:
                            if os.path.exists(temp_path):
                                os.unlink(temp_path)

                # 清理文本并保存
                cleaned_content = clean_text(content)
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

                print(f"  转换成功 -> {os.path.basename(txt_path)} (已清理)")
                success_count += 1

            except Exception as e:
                print(f"  转换失败: {str(e)}")
                error_count += 1

        print("\n转换完成!")
        print(f"成功: {success_count} 个, 失败: {error_count} 个")

        # 显示python-docx支持状态
        if not HAS_DOCX_SUPPORT:
            print("\n注意: 未安装python-docx库，.docx文件使用Word COM对象转换")
            print("      建议安装: pip install python-docx 以获得更好的性能")

    except Exception as e:
        print(f"初始化Word应用程序失败: {str(e)}")
    finally:
        # 清理资源
        try:
            if word_app:
                word_app.Quit()
        except:
            pass
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    # 获取命令行参数
    if len(sys.argv) < 2:
        print("请指定要处理的目录路径")
        print("用法: python doc_to_txt.py [目录路径]")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"错误: '{directory}' 不是有效的目录")
        sys.exit(1)

    convert_doc_to_txt(directory)