from imports import *


class Table:
    def __init__(self, frame, excel_table):
        self.frame = frame
        self.excel_table = excel_table
        self.cols = len(excel_table.columns)
        self.rows = len(excel_table)
        self.table = None

    def readExcelData(self):
        data = []
        headers = [col for col in self.excel_table]
        for i in range(self.rows):
            row_list = []
            for col in self.excel_table:
                if pd.isnull(self.excel_table[col][i]):
                    row_list.append('')
                else:
                    row_list.append(str(self.excel_table[col][i]))
            data.append(row_list)
        return data, headers

    @utils.threadpool
    def prepareTable(self):
        data, headers = self.readExcelData()
        self.table = tksheet.Sheet(self.frame,
                                   data=data, headers=headers, header_font=('Arial', 12, 'bold'))
        self.table.readonly_columns(columns=list(range(self.cols)))
        self.table.enable_bindings()
        self.table.disable_bindings('paste')
        self.table.disable_bindings('cut')
        self.table.disable_bindings('delete')
        return self.table


if __name__ == '__main__':
    pass
