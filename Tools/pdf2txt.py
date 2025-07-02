# PDF转TXT
import os
import argparse
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError


def convert_pdf_to_txt(pdf_path, txt_path):
    """将单个PDF文件转换为TXT文件"""
    try:
        text = extract_text(pdf_path)
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        return True
    except PDFSyntaxError:
        print(f"错误：文件损坏或加密 - {pdf_path}")
    except Exception as e:
        print(f"转换失败 {pdf_path}: {str(e)}")
    return False


def process_directory(input_dir, output_dir):
    """处理目录中的所有PDF文件"""
    count = 0
    success = 0

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                count += 1
                pdf_path = os.path.join(root, file)

                # 创建输出目录结构
                rel_path = os.path.relpath(root, input_dir)
                out_dir = os.path.join(output_dir, rel_path)
                os.makedirs(out_dir, exist_ok=True)

                # 生成输出路径
                txt_file = os.path.splitext(file)[0] + '.txt'
                txt_path = os.path.join(out_dir, txt_file)

                print(f"正在处理 ({count}): {pdf_path}")
                if convert_pdf_to_txt(pdf_path, txt_path):
                    success += 1

    print(f"\n转换完成! 成功: {success}/{count} 个文件")
    if count > success:
        print("注意：部分文件可能因加密或损坏而未能转换")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF转TXT转换器')
    parser.add_argument('input_dir', help='输入目录路径')
    args = parser.parse_args()

    process_directory(args.input_dir, args.input_dir)