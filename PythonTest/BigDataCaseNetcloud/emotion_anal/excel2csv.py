import os
import xlrd
import csv


def xlsx_to_csv():
    with open('labeled_data.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for root, dirs, files in os.walk("./excel_data"):
            for filename in files:
                filepath = os.path.join(root, filename)

                workbook = xlrd.open_workbook(filepath)
                table = workbook.sheet_by_index(0)
                for row_num in range(table.nrows):
                    row_value = table.row_values(row_num)
                    writer.writerow(row_value)


if __name__ == '__main__':
    xlsx_to_csv()
