from imports import *
from ChecklistWindow import *


class Chart:
    def __init__(self, root, frame, excel_table, language, chartA_data, chartB_data, chartC_data, chartD_data, chartE_data):
        self.frame = frame
        self.checklist_window = ChecklistWindow(root, 250, 480)
        self.excel_table = excel_table
        self.language = language
        self.chartA_data = chartA_data
        self.chartB_data = chartB_data
        self.chartC_data = chartC_data
        self.chartD_data = chartD_data
        self.chartE_data = chartE_data
        self.cols = len(excel_table.columns)
        self.rows = len(excel_table)

        # ChartA
        self.serial_numberA_selected = None
        self.stationA_selected = None
        self.operator_nameA_selected = None
        self.dateA_selected = None

    def __del__(self):
        self.rewriteChartData()

    def rewriteChartData(self):
        # ChartA
        self.chartA_data[0] = self.serial_numberA_selected
        self.chartA_data[1] = self.stationA_selected
        self.chartA_data[2] = self.operator_nameA_selected
        self.chartA_data[3] = self.dateA_selected

    def getColumn(self, column_name, optional_name, col_index):
        try:
            col = self.excel_table[column_name]
        except:
            try:
                col = self.excel_table[optional_name]
            except:
                try:
                    col = self.excel_table.iloc[:, col_index]
                except:
                    col = pd.Series()
        finally:
            return col

    def getColumnUniqueList(self, column_name, optional_name=None, col_index=None):
        return list(set(self.getColumn(column_name, optional_name, col_index).tolist()))

    def clearFrame(self):
        for child in self.frame.winfo_children():
            child.destroy()

    @utils.threadpool
    def drawChart(self, chart='A'):
        def chartChoice(chart):
            return {
                'A': self.drawChartA,
                'B': self.drawChartB,
                'C': self.drawChartC,
                'D': self.drawChartD,
                'E': self.drawChartE
            }.get(chart, self.drawChartA)

        chartChoice(chart)()

    def drawChartA(self):
        self.clearFrame()
        options_frame = ttk.Frame(self.frame)
        chart_frame = ttk.Frame(self.frame)
        options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        chart_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)
        ttk.Separator(options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        serial_number = sorted(self.getColumnUniqueList(
            'Numer seryjny', 'Serial Number', 10))
        station = sorted(self.getColumnUniqueList('Stacja', 'Station', 1))
        operator_name = sorted(self.getColumnUniqueList(
            'Operator Name', 'Operator Name', 4))
        date = sorted(self.getColumnUniqueList('Date', 'Date', 2))

        if self.chartA_data == [None, None, None, None]:
            self.serial_numberA_selected = [
                0 for _ in range(len(serial_number))]
            self.stationA_selected = [0 for _ in range(len(station))]
            self.operator_nameA_selected = [
                0 for _ in range(len(operator_name))]
            self.dateA_selected = [0 for _ in range(len(date))]
            try:
                self.serial_numberA_selected[0] = 1
                self.stationA_selected[0] = 1
                self.operator_nameA_selected[0] = 1
                self.dateA_selected[0] = 1
            except:
                pass
            
            self.rewriteChartData()
        else:
            self.serial_numberA_selected = self.chartA_data[0]
            self.stationA_selected = self.chartA_data[1]
            self.operator_nameA_selected = self.chartA_data[2]
            self.dateA_selected = self.chartA_data[3]

        serial_number_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Numer seryjny \u25bc', u'Serial number \u25bc'),
                                       command=lambda: self.checklist_window.show(self.language, serial_number, self.serial_numberA_selected, page_len=250))
        station_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Stacja \u25bc', u'Station \u25bc'),
                                 command=lambda: self.checklist_window.show(self.language, station, self.stationA_selected, page_len=250))
        operator_name_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Operator \u25bc', u'Operator name \u25bc'),
                                       command=lambda: self.checklist_window.show(self.language, operator_name, self.operator_nameA_selected, page_len=250))
        date_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Data \u25bc', u'Date \u25bc'),
                              command=lambda: self.checklist_window.show(self.language, date, self.dateA_selected, page_len=250))
        serial_number_btn.pack(side=tkinter.LEFT, padx=15)
        station_btn.pack(side=tkinter.LEFT)
        operator_name_btn.pack(side=tkinter.LEFT, padx=15)
        date_btn.pack(side=tkinter.LEFT)

    def drawChartB(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        bars_nmb = 28
        frequency = [0 for _ in range(bars_nmb)]
        time_elapsed = {}
        
        for sn in self.getColumnUniqueList('Numer seryjny', 'Serial Number', 10):
            date = self.getColumn('Date', 'Date', 2)[self.getColumn('Numer seryjny', 'Serial Number', 10) == sn].values
            delta_time = np.float64(self.getColumn('Aktualny czas trwania [s]', 'Actual duration [s]', 6)[(self.getColumn('Numer seryjny', 'Serial Number', 10) == sn) & (self.getColumn('Date', 'Date', 2) == np.max(date))].values[0])
            time_elapsed[sn] = (np.max(date) - np.min(date)) / np.timedelta64(1, 's') + delta_time
        

    def drawChartC(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        data = {'Interest_Rate': [5, 5.5, 6, 5.5, 5.25, 6.5, 7, 8, 7.5, 8.5],
                'Stock_Index_Price': [1500, 1520, 1525, 1523, 1515, 1540, 1545, 1560, 1555, 1565]
                }
        df = pd.DataFrame(data, columns=['Interest_Rate', 'Stock_Index_Price'])

        figure = plt.Figure()
        ax = figure.add_subplot(111)
        ax.scatter(df['Interest_Rate'], df['Stock_Index_Price'], color='g')
        scatter = FigureCanvasTkAgg(figure, chart_frame)
        scatter.get_tk_widget().place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        ax.legend(['Stock_Index_Price'])
        ax.set_xlabel('Interest Rate')
        ax.set_title('Interest Rate Vs. Stock Index Price')

    def drawChartD(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        data = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
                'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]
                }
        df = pd.DataFrame(data, columns=['Country', 'GDP_Per_Capita'])

        figure = plt.Figure()
        ax = figure.add_subplot(111)
        bar = FigureCanvasTkAgg(figure, chart_frame)
        bar.get_tk_widget().place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        df = df[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
        df.plot(kind='bar', legend=True, ax=ax)
        ax.set_title('Country Vs. GDP Per Capita')

    def drawChartE(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        time.sleep(2)
        print('Chart E')


if __name__ == '__main__':
    pass
