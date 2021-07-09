from imports import *

class Table:
    def __init__(self, frame, excel_table):
        self.excel_table = excel_table
        self.cols = len(excel_table.columns)
        self.rows = len(excel_table)

        self.table = tkintertable.TableCanvas(
            frame, read_only=True, data=self.readExcelData())
        self.table.show()

    def destroy(self):
        self.table.destroy()

    def readExcelData(self):
        data = {}
        for i in range(self.rows):
            row_dict = {}
            for col in self.excel_table:
                if pd.isnull(self.excel_table[col][i]):
                    row_dict[col] = ''
                else:
                    row_dict[col] = str(self.excel_table[col][i])
            data[i+1] = row_dict

        return data

if __name__ == '__main__':
    pass
