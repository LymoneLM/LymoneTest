import openpyxl
import requests
import os

# 打开 Excel 文件
workbook = openpyxl.load_workbook('1.xlsx')

# 选择工作表
worksheet = workbook['导出照片与三维数据']  # 请替换为你实际的工作表名称

# 创建目录用于存储下载的图片
os.makedirs('images', exist_ok=True)

# 遍历每个单元格
counter = [0]*32  # 图片计数器
for row in worksheet.iter_rows():
    # 获取链接和文件夹名字的单元格
    link_cell = row[5]  # F列，索引为5（从0开始）
    folder_cell = row[4]  # E列，索引为4（从0开始）

    # 检查链接和文件夹名字是否存在
    if link_cell.value and folder_cell.value:
        link = link_cell.value
        folder_name = folder_cell.value

        # 判断链接是否为图片链接
        if link.endswith('.jpg') or link.endswith('.jpeg') or link.endswith('.png'):
            # 创建文件夹
            folder_path = os.path.join('images', str(folder_name))
            os.makedirs(folder_path, exist_ok=True)

            # 发送 HTTP 请求下载图片
            response = requests.get(link)
            # 提取图片文件扩展名
            extension = link.split('.')[-1]
            # 构造新的文件名
            filename = f'{counter[folder_name]}.{extension}'
            counter[folder_name] += 1
            # 保存图片到文件夹中
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
                print(f'下载图片 {filename} 完成')

# 关闭 Excel 文件
workbook.close()
