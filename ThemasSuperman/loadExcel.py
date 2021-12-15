import xlrd
from xlutils.copy import copy

from downloadPhoto import generate
from pinyin import pinyin

startNo = 1
url = "https://m.imitui.com/manhua/"


def load_excel(path:str):
    read_book = xlrd.open_workbook(r'template.xls')
    sheet = read_book.sheet_by_name('result')
    line = sheet.nrows - startNo
    copy_book = copy(read_book)
    copy_sheet = copy_book.get_sheet(0)
    for i in range(line):
        if sheet.cell_value(i + startNo, 2) == '否':
            continue
        num = generate(url+pinyin(sheet.cell_value(i + startNo, 0)),
                       int(sheet.cell_value(i + startNo, 1)),
                       path+pinyin(sheet.cell_value(i + startNo, 0)))
        copy_sheet.write(i + 1, 1, num)
    copy_book.save('template.xls')
