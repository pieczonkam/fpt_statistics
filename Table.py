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
                if isinstance(self.excel_table[col][i], pd.Timestamp):
                    row_dict[col] = self.excel_table[col][i].strftime('%Y-%m-%d %X')
                elif isinstance(self.excel_table[col][i], datetime.time):
                    row_dict[col] = self.excel_table[col][i].strftime('%d.%m.%Y %X')
                    print(type(row_dict[col]), ':', row_dict[col])
                elif isinstance(self.excel_table[col][i], np.int64) or isinstance(self.excel_table[col][i], np.float64) or isinstance(self.excel_table[col][i], np.int32) or isinstance(self.excel_table[col][i], np.float32):
                    row_dict[col] = self.excel_table[col][i].item()
                else:
                    row_dict[col] = self.excel_table[col][i]
            data[i+1] = row_dict

        return data

if __name__ == '__main__':
    pass
