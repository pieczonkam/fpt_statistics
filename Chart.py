from imports import *
from ChecklistWindow import *
from ComboboxWindow import *


class Chart:
    def __init__(self, root, frame, refresh_button_frame, excel_table, language):
        self.frame = frame
        self.refresh_button_frame = refresh_button_frame
        self.checklist_window = ChecklistWindow(root, 250, 480)
        self.combobox_window = ComboboxWindow(root, 220, 120)
        self.excel_table = excel_table
        self.language = language
        self.cols = len(excel_table.columns)
        self.rows = len(excel_table)
        self.figure = None
        self.bars_nmb = None

        # ChartA
        self.chartA_drawn = False
        self.chartA_first_draw = True
        self.A_serial_number_selected = None
        self.A_station_selected = None
        self.A_operator_name_selected = None
        self.A_date_selected = None

        # chartB
        self.chartB_drawn = False
        self.chartB_first_draw = True
        self.B_station_selected = None
        self.B_date_selected = None
        self.B_shift_selected = None
        self.B_cycle_selected = None
        self.B_part_number_selected = None

        self.B_engines_nmb = None
        self.B_transition_time = None

    def setLanguage(self, language):
        self.language = language

    def getColumn(self, column_name, optional_name, col_index):
        try:
            col = self.excel_table[column_name]
        except Exception:
            try:
                col = self.excel_table[optional_name]
            except Exception:
                try:
                    col = self.excel_table.iloc[:, col_index]
                except Exception:
                    col = pd.Series()
        finally:
            return col

    def getColumnUniqueList(self, column_name, optional_name=None, col_index=None):
        return list(set(self.getColumn(column_name, optional_name, col_index).tolist()))

    def clearFrame(self):
        for child in self.frame.winfo_children():
            if child != self.refresh_button_frame:
                child.destroy()
            else:
                child.place_forget()

    @utils.threadpool
    def drawChart(self, chart='A', chart_drawn=None):
        def chartChoice(chart):
            return {
                'A': self.drawChartA,
                'B': self.drawChartB,
                'C': self.drawChartC,
                'D': self.drawChartD,
                'E': self.drawChartE
            }.get(chart, self.drawChartA)

        chartChoice(chart)(chart_drawn)

    @utils.threadpool
    def saveChart(self, filename):
        if not self.figure is None:
            self.figure.savefig(filename)

    def zerosListWithOne(self, length):
        data_list = [0 for _ in range(length)]
        try:
            data_list[0] = 1
        except Exception:
            pass
        return data_list

    def onesList(self, length):
        return [1 for _ in range(length)]

    def getCDF(self, data_list):
        cdf = [0 for _ in range(len(data_list))]
        for i in range(len(data_list)):
            for j in range(i, len(cdf)):
                cdf[j] += data_list[i]
        data_list_sum = sum(data_list)
        if data_list_sum == 0:
            return [0 for _ in range(self.bars_nmb)]
        for i in range(len(cdf)):
            cdf[i] = (cdf[i] / data_list_sum) * 100
        return cdf

    def drawChartA(self, chart_drawn=None):
        if not chart_drawn is None:
            self.chartA_drawn = chart_drawn

        serial_number = sorted(self.getColumnUniqueList(
            'Numer seryjny', 'Serial Number', 10))
        station = sorted(self.getColumnUniqueList('Stacja', 'Station', 1))
        operator_name = sorted(self.getColumnUniqueList(
            'Operator Name', 'Operator Name', 4))
        date = sorted(self.getColumnUniqueList('Date', 'Date', 2))

        if self.chartA_first_draw:
            self.A_serial_number_selected = self.zerosListWithOne(len(serial_number))
            self.A_station_selected = self.zerosListWithOne(len(station))
            self.A_operator_name_selected = self.zerosListWithOne(len(operator_name))
            self.A_date_selected = self.zerosListWithOne(len(date))           
            self.chartA_first_draw = False
            
        #######################################################################################################

        self.clearFrame()
        options_frame = ttk.Frame(self.frame)
        chart_frame = ttk.Frame(self.frame)
        options_frame.place(relx=0, rely=0, relwidth=0.85, relheight=0.05)
        self.refresh_button_frame.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.05)
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

        #######################################################################################################

        # To be done

    def drawChartB(self, chart_drawn=None):
        if not chart_drawn is None:
            self.chartB_drawn = chart_drawn

        station = sorted(self.getColumnUniqueList('Stacja', 'Station', 1))
        date = sorted(self.getColumnUniqueList('Date', 'Date', 2))
        shift = sorted(self.getColumnUniqueList('Przesunięcie', 'Shift', 11))
        cycle = sorted(self.getColumnUniqueList('Cycle', 'Cycle', 5))
        part_number = sorted(self.getColumnUniqueList('Numer części', 'Part number', 9))

        if self.chartB_first_draw:
            self.B_station_selected = [0, len(station) - 1]
            self.B_date_selected = self.onesList(len(date))
            self.B_shift_selected = self.onesList(len(shift))
            self.B_cycle_selected = self.onesList(len(cycle))
            self.B_part_number_selected = self.onesList(len(part_number))
            self.chartB_first_draw = False

        if not self.chartB_drawn:      
            self.bars_nmb = 29
            self.B_engines_nmb = [0 for _ in range(self.bars_nmb)]
            self.B_transition_time = ['' for i in range(self.bars_nmb)]

            time_elapsed = {}
            for sn in self.getColumnUniqueList('Numer seryjny', 'Serial Number', 10):
                engine_date = self.getColumn('Date', 'Date', 2)[self.getColumn('Numer seryjny', 'Serial Number', 10) == sn].values
                delta_time = np.float64(self.getColumn('Aktualny czas trwania [s]', 'Actual duration [s]', 6)[(self.getColumn('Numer seryjny', 'Serial Number', 10) == sn) & (self.getColumn('Date', 'Date', 2) == np.max(engine_date))].values[0])
                time_elapsed[sn] = (np.max(engine_date) - np.min(engine_date)) / np.timedelta64(1, 's') + delta_time
            time_elapsed_cpy = dict(time_elapsed)

            for i in range(self.bars_nmb - 1):
                m, s = divmod(390 + i * 15, 60) # 390s = 6min 30s
                self.B_transition_time[i] = f'{m:02d}:{s:02d}'
                for key, value in time_elapsed.items():
                    if value <= 390 + i * 15 and key in time_elapsed_cpy:
                        self.B_engines_nmb[i] += 1
                        time_elapsed_cpy.pop(key, 'None')
            self.B_engines_nmb[-1] = len(time_elapsed_cpy.keys())
            self.cdf_data = self.getCDF(self.B_engines_nmb)
            self.chartB_drawn = True
        self.B_transition_time[-1] = utils.setLabel(self.language, 'Więcej', 'More')

        #######################################################################################################

        self.clearFrame()
        options_frame = ttk.Frame(self.frame)
        chart_frame = ttk.Frame(self.frame)
        options_frame.place(relx=0, rely=0, relwidth=0.85, relheight=0.05)
        self.refresh_button_frame.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.05)
        chart_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)
        ttk.Separator(options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        station_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Stacja \u25bc', u'Station \u25bc'), command=lambda: self.combobox_window.show(self.language, station, self.B_station_selected))
        date_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Data \u25bc', u'Date \u25bc'), command=lambda: self.checklist_window.show(self.language, date, self.B_date_selected, page_len=250))
        shift_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Zmiana \u25bc', u'Shift \u25bc'), command=lambda: self.checklist_window.show(self.language, shift, self.B_shift_selected, page_len=250))
        cycle_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Cykl \u25bc', u'Cycle \u25bc'), command=lambda: self.checklist_window.show(self.language, cycle, self.B_cycle_selected, page_len=250))
        part_number_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, u'Numer części \u25bc', u'Part number \u25bc'), command=lambda: self.checklist_window.show(self.language, part_number, self.B_part_number_selected, page_len=250))
        station_btn.pack(side=tkinter.LEFT, padx=15)
        date_btn.pack(side=tkinter.LEFT)
        shift_btn.pack(side=tkinter.LEFT, padx=15)
        cycle_btn.pack(side=tkinter.LEFT)
        part_number_btn.pack(side=tkinter.LEFT, padx=15)
        
        #######################################################################################################

        B_engines_nmb_str = utils.setLabel(self.language, 'Liczba silników', 'Number of engines')
        B_transition_time_str = utils.setLabel(self.language, 'Czas przejścia', 'Transition time')
        B_cdf_str = utils.setLabel(self.language, 'Dystrybuanta', 'CDF')
        self.figure = plt.Figure()
        self.figure.set_tight_layout(True)
        
        ax1 = self.figure.add_subplot(111)
        hist = ax1.bar(self.B_transition_time, self.B_engines_nmb, align='edge', width=-0.8)
        ax1.set_title(utils.setLabel(self.language, 'Histogram czasu przepływu\n' + str(sum(self.B_engines_nmb)) + ' silników', 'Transition time histogram\n' + str(sum(self.B_engines_nmb)) + ' engines'), pad=15, weight='bold')
        ax1.tick_params(labelrotation=90)
        ax1.set_xlabel(B_transition_time_str)
        ax2 = ax1.twinx()
        cdf = ax2.plot(self.B_transition_time, self.cdf_data, 'rs-')
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax2.set_ylim(0, 101)
        for bar, label1, label2 in zip(ax1.patches, self.B_engines_nmb, self.cdf_data):
            if label1 > 0:
                rotation = 0 if len(str(label1)) < 4 else 45
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (0.01 * max(self.B_engines_nmb) if rotation == 45 else 0), str(label1), ha='center', va='bottom', rotation=rotation)
            ax2.text(bar.get_x(), label2, str(round(label2)) + '%', ha='right', va='bottom', color='red', weight='semibold')
        ax1.legend([hist, cdf[0]], [B_engines_nmb_str, B_cdf_str], bbox_to_anchor=(1, 0.9))

        canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.draw()
        
    def drawChartC(self, chart_drawn=None):
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

    def drawChartD(self, chart_drawn=None):
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

    def drawChartE(self, chart_drawn=None):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        time.sleep(2)
        print('Chart E')


if __name__ == '__main__':
    pass