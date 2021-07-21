from imports import *
from ChecklistWindow import *


class Chart:
    def __init__(self, root, frame, excel_table, language):
        self.frame = frame
        self.checklist_window = ChecklistWindow(root, 250, 480)
        self.excel_table = excel_table
        self.language = language
        self.cols = len(excel_table.columns)
        self.rows = len(excel_table)
        self.figure = None

        # ChartA
        self.chartA_drawn = False
        self.A_serial_number_selected = None
        self.A_station_selected = None
        self.A_operator_name_selected = None
        self.A_date_selected = None

        # chartB
        self.chartB_drawn = False
        self.B_bars_nmb = 29
        self.B_engines_nmb = [0 for _ in range(self.B_bars_nmb)]
        self.B_transition_time = ['' for i in range(self.B_bars_nmb)]

    def setLanguage(self, language):
        self.language = language

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

    @utils.threadpool
    def saveChart(self, filename):
        if not self.figure is None:
            self.figure.savefig(filename)

    def drawChartA(self):
        serial_number = sorted(self.getColumnUniqueList(
            'Numer seryjny', 'Serial Number', 10))
        station = sorted(self.getColumnUniqueList('Stacja', 'Station', 1))
        operator_name = sorted(self.getColumnUniqueList(
            'Operator Name', 'Operator Name', 4))
        date = sorted(self.getColumnUniqueList('Date', 'Date', 2))

        if not self.chartA_drawn:
            self.A_serial_number_selected = [
                0 for _ in range(len(serial_number))]
            self.A_station_selected = [0 for _ in range(len(station))]
            self.A_operator_name_selected = [
                0 for _ in range(len(operator_name))]
            self.A_date_selected = [0 for _ in range(len(date))]
            try:
                self.A_serial_number_selected[0] = 1
                self.A_station_selected[0] = 1
                self.A_operator_name_selected[0] = 1
                self.A_date_selected[0] = 1
            except:
                pass
            self.chartA_drawn = True
            
        self.clearFrame()
        options_frame = ttk.Frame(self.frame)
        chart_frame = ttk.Frame(self.frame)
        options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        chart_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)
        ttk.Separator(options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        serial_number_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Numer seryjny \u25bc', u'Serial number \u25bc'),
                                       command=lambda: self.checklist_window.show(self.language, serial_number, self.A_serial_number_selected, page_len=250))
        station_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Stacja \u25bc', u'Station \u25bc'),
                                 command=lambda: self.checklist_window.show(self.language, station, self.A_station_selected, page_len=250))
        operator_name_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Operator \u25bc', u'Operator name \u25bc'),
                                       command=lambda: self.checklist_window.show(self.language, operator_name, self.A_operator_name_selected, page_len=250))
        date_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Data \u25bc', u'Date \u25bc'),
                              command=lambda: self.checklist_window.show(self.language, date, self.A_date_selected, page_len=250))
        serial_number_btn.pack(side=tkinter.LEFT, padx=15)
        station_btn.pack(side=tkinter.LEFT)
        operator_name_btn.pack(side=tkinter.LEFT, padx=15)
        date_btn.pack(side=tkinter.LEFT)

    def drawChartB(self):
        if not self.chartB_drawn:
            time_elapsed = {}
            for sn in self.getColumnUniqueList('Numer seryjny', 'Serial Number', 10):
                date = self.getColumn('Date', 'Date', 2)[self.getColumn('Numer seryjny', 'Serial Number', 10) == sn].values
                delta_time = np.float64(self.getColumn('Aktualny czas trwania [s]', 'Actual duration [s]', 6)[(self.getColumn('Numer seryjny', 'Serial Number', 10) == sn) & (self.getColumn('Date', 'Date', 2) == np.max(date))].values[0])
                time_elapsed[sn] = (np.max(date) - np.min(date)) / np.timedelta64(1, 's') + delta_time
            time_elapsed_cpy = dict(time_elapsed)

            for i in range(self.B_bars_nmb - 1):
                m, s = divmod(390 + i * 15, 60) # 390s = 6min 30s
                self.B_transition_time[i] = f'{m:02d}:{s:02d}'
                for key, value in time_elapsed.items():
                    if value <= 390 + i * 15 and key in time_elapsed_cpy:
                        self.B_engines_nmb[i] += 1
                        time_elapsed_cpy.pop(key, 'None')
            self.B_transition_time[-1] = '> ' + self.B_transition_time[-2]
            self.B_engines_nmb[-1] = len(time_elapsed_cpy.keys())
            self.chartB_drawn = True

        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        B_engines_nmb_str = utils.setLabel(self.language, 'Ilość silników', 'Number of engines')
        B_transition_time_str = utils.setLabel(self.language, 'Czas przejścia', 'Transition time')
        
        self.figure = plt.Figure()
        self.figure.set_tight_layout(True)
        ax = self.figure.add_subplot(111)
        ax.bar(self.B_transition_time, self.B_engines_nmb, align='edge',width=-0.8)
        ax.set_title('Histogram', pad=15, weight='bold')
        ax.tick_params(labelrotation=90)
        ax.set_xlabel(B_transition_time_str)
        ax.legend(labels=[B_engines_nmb_str])
        for bar, label in zip(ax.patches, self.B_engines_nmb):
            if label > 0:
                rotation = 0 if len(str(label)) < 4 else 45
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (0.01 * max(self.B_engines_nmb) if rotation == 45 else 0), str(label), ha='center', va='bottom', rotation=rotation)
        canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.draw()
        
    def drawChartC(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        data = {'Interest_Rate': [5, 5.5, 6, 5.5, 5.25, 6.5, 7, 8, 7.5, 8.5],
                'Stock_Index_Price': [1500, 1520, 1525, 1523, 1515, 1540, 1545, 1560, 1555, 1565]
                }
        df = pd.DataFrame(data, columns=['Interest_Rate', 'Stock_Index_Price'])

        self.figure = plt.Figure()
        ax = self.figure.add_subplot(111)
        ax.scatter(df['Interest_Rate'], df['Stock_Index_Price'], color='g')
        scatter = FigureCanvasTkAgg(self.figure, chart_frame)
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

        self.figure = plt.Figure()
        ax = self.figure.add_subplot(111)
        bar = FigureCanvasTkAgg(self.figure, chart_frame)
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
