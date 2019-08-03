import xlrd


class ExcelParser:

    def __init__(self, excelpath):
        self.workBook = xlrd.open_workbook(excelpath)
        self.sheet = self.workBook.sheet_by_index(0)
        self.sheet_rows = self.sheet.nrows
        self.sheet_cols = self.sheet.ncols

    def parse_excel(self):
        result = []

        # 创建二维list
        for i in range(1, self.sheet_rows):
            result.append([])

        # 读取每一行
        for i in range(1, self.sheet_rows):
            result[i - 1] = self.sheet.row_values(i)

        return result



