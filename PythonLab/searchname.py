import openpyxl


def search_in_column(file_path, column_index, search_text):
    # 打开xlsx文件
    workbook = openpyxl.load_workbook(file_path)

    # 获取第一个工作表
    sheet = workbook.active

    # 获取D列的所有单元格
    column_data = sheet[f'D{column_index}:D{sheet.max_row}']

    # 遍历D列的每个单元格
    for cell in column_data:
        cell_value = cell[0].value

        # 检查单元格的值是否包含搜索文本
        if cell_value  not in search_text:
            print(f"找到未包含搜索文本的值：{cell_value}")

    # 关闭工作簿
    workbook.close()


# 输入文件路径和搜索文本
file_path = '2.xlsx'  # 将 'your_file.xlsx' 替换为你的文件路径
search_text = input("请输入要搜索的文本：")

# 搜索D列并输出未包含搜索文本的值
search_in_column(file_path, 1, search_text)
