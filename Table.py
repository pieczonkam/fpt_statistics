from imports import *
import tkintertable
import random


class Table:
    def __init__(self, frame, excel_table):
        self.excel_table = excel_table
        self.cols = len(excel_table.columns)
        self.rows = len(excel_table)

        self.table = tkintertable.TableCanvas(
            frame, rows=self.rows, cols=self.cols)
        self.table.show()

    def destroy(self):
        self.table.destroy()


if __name__ == '__main__':
    pass
