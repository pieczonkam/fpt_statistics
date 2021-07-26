from os import stat
from tkinter.constants import S
from imports import *
from ChecklistWindow import *
from ComboboxWindow import *
from TextWindow import *


class Chart:
    def __init__(self, root, frame, refresh_button_frame, excel_table, language, is_loading):
        self.frame = frame
        self.refresh_button_frame = refresh_button_frame
        self.checklist_window = ChecklistWindow(root, 250, 480)
        self.combobox_window = ComboboxWindow(root, 220, 120)
        self.text_window = TextWindow(root, 600, 450)
        self.excel_table = excel_table
        self.language = language
        self.cols = len(excel_table.columns)
        self.rows = len(excel_table)
        self.figure = None

        # Columns data
        self.ute = sorted(self.getColumnUniqueList('UTE', 'UTE', 0))
        self.station = sorted(self.getColumnUniqueList('Stacja', 'Station', 1))
        self.date = sorted(self.getColumnUniqueList('Date', 'Date', 2))
        self.operator_id = sorted(self.getColumnUniqueList(
            'Operator ID', 'Operator ID', 3))
        self.operator_name = sorted(self.getColumnUniqueList(
            'Operator Name', 'Operator Name', 4))
        self.cycle = sorted(self.getColumnUniqueList('Cycle', 'Cycle', 5))
        self.actual_duration = sorted(self.getColumnUniqueList(
            'Aktualny czas trwania [s]', 'Actual duration [s]', 6))
        self.cycle_duration = sorted(self.getColumnUniqueList(
            'Czas trwania cyklu [s]', 'Cycle duration [s]', 7))
        self.time_difference = sorted(self.getColumnUniqueList(
            'Różnica czasu [s]', 'Time differences [s]', 8))
        self.part_number = sorted(self.getColumnUniqueList(
            'Numer części', 'Part Number', 9))
        self.serial_number = sorted(self.getColumnUniqueList(
            'Numer seryjny', 'Serial Number', 10))
        self.shift = sorted(self.getColumnUniqueList(
            'Przesunięcie', 'Shift', 11))

        self.serial_number_nmb = len(self.serial_number)
        self.wrong_transition_count = 0
        for i in range(len(self.serial_number)):
            engine_station = self.getColumn('Stacja', 'Station', 1)[(
                self.getColumn('Numer seryjny', 'Serial Number', 10) == self.serial_number[i])].values
            if sorted(engine_station) != sorted(self.station):
                self.wrong_transition_count += 1
                self.serial_number[i] = None
        self.serial_number = [sn for sn in self.serial_number if not sn is None]

        # Charts
        self.show_cdf = True
        self.is_loading = is_loading
        
        # ChartA
        self.chartA_drawn = False
        self.chartA_first_draw = True
        self.chartA_show_filters = False

        self.A_filters_btn = None
        self.A_details_btn = None
        self.A_station_btn = None
        self.A_date_btn = None
        self.A_shift_btn = None
        self.A_cycle_btn = None
        self.A_part_number_btn = None

        # chartB
        self.chartB_drawn = False
        self.chartB_first_draw = True
        self.chartB_show_filters = False

        self.B_filters_btn = None
        self.B_details_btn = None
        self.B_cdf_checkbtn = None
        self.B_station_btn = None
        self.B_date_btn = None
        self.B_shift_btn = None
        self.B_cycle_btn = None
        self.B_part_number_btn = None

    def setLanguage(self, language):
        self.language = language

    def setIsLoading(self, is_loading):
        self.is_loading = is_loading

    def getIsLoading(self):
        return self.is_loading

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

        self.A_filters_btn = None
        self.A_details_btn = None
        self.A_station_btn = None
        self.A_date_btn = None
        self.A_shift_btn = None
        self.A_cycle_btn = None
        self.A_part_number_btn = None
        self.B_filters_btn = None
        self.B_details_btn = None
        self.B_cdf_checkbtn = None
        self.B_station_btn = None
        self.B_date_btn = None
        self.B_shift_btn = None
        self.B_cycle_btn = None
        self.B_part_number_btn = None
    
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
            cdf[i] = round((cdf[i] / data_list_sum) * 100, 2)
        return cdf

    def contains(self, big_set, small_list):
        for el in small_list:
            if not el in big_set:
                return False
        return True

    @utils.threadpool
    def drawChart(self, chart_name='A', chart_drawn=None):
        def chartChoice(chart):
            return {
                'A': self.drawChartA,
                'B': self.drawChartB,
                'C': self.drawChartC,
                'D': self.drawChartD,
                'E': self.drawChartE
            }.get(chart, self.drawChartA)

        if chart_name != 'None':
            chartChoice(chart_name)(chart_drawn)

    @utils.threadpool
    def saveChart(self, filename):
        if not isinstance(self.figure, type(None)):
            self.figure.savefig(filename)

    def disableButtons(self, buttons):
        for button in buttons:
            if not isinstance(button, type(None)):
                button.configure(state=tkinter.DISABLED)

    def enableButtons(self, buttons):
        for button in buttons:
            if not isinstance(button, type(None)):
                button.configure(state=tkinter.NORMAL)

    ############################################################################################################
    # Switches

    def switchButtonsState(self):
        buttons = [self.A_filters_btn, self.A_details_btn, self.A_station_btn, self.A_date_btn, self.A_shift_btn, self.A_cycle_btn, self.A_part_number_btn,
                   self.B_filters_btn, self.B_details_btn, self.B_cdf_checkbtn, self.B_station_btn, self.B_date_btn, self.B_shift_btn, self.B_cycle_btn, self.B_part_number_btn]
        if self.is_loading:
            self.disableButtons(buttons)
        else:
            self.enableButtons(buttons)            
        
    def switchFilters(self, chart_name, chart_frame, filters_btn):
        if chart_name == 'A':
            self.chartA_show_filters = not self.chartA_show_filters
            show_filters = self.chartA_show_filters
        elif chart_name == 'B':
            self.chartB_show_filters = not self.chartB_show_filters
            show_filters = self.chartB_show_filters
        elif chart_name == 'C':
            pass
        elif chart_name == 'D':
            pass
        elif chart_name == 'E':
            pass
        else:
            pass

        if show_filters:
            chart_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
            filters_btn['text'] = utils.setLabel(
                self.language, u'Filtry \u25b2', u'Filters \u25b2')
        else:
            chart_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)
            filters_btn['text'] = utils.setLabel(
                self.language, u'Filtry \u25bc', u'Filters \u25bc')

    def switchShowCDFVar(self, chart_name):
        self.show_cdf = not self.show_cdf
        self.drawChart(chart_name)

    def switchFigureText(self, text, figure_text, canvas):
        figure_text.set_text(text)
        canvas.draw()

    ############################################################################################################

    def drawChartA(self, chart_drawn=None):
        if not isinstance(chart_drawn, type(None)):
            self.chartA_drawn = chart_drawn

        if self.chartA_first_draw:
            self.A_station_selected = [0, len(self.station) - 1]
            self.A_date_selected = [0, len(self.date) - 1]
            self.A_shift_selected = self.onesList(len(self.shift))
            self.A_cycle_selected = self.onesList(len(self.cycle))
            self.A_part_number_selected = self.onesList(len(self.part_number))
            self.chartA_first_draw = False

        if not self.chartA_drawn:
            self.A_station_nmb = self.A_station_selected[1] - self.A_station_selected[0] + 1
            self.A_stations = self.station[self.A_station_selected[0]:self.A_station_selected[1] + 1]
            self.A_dates = self.date[self.A_date_selected[0]:self.A_date_selected[1] + 1]
            self.A_shifts = [self.shift[i] for i in range(len(self.A_shift_selected)) if self.A_shift_selected[i] != 0]
            self.A_cycles = [self.cycle[i] for i in range(len(self.A_cycle_selected)) if self.A_cycle_selected[i] != 0]
            self.A_part_numbers = [self.part_number[i] for i in range(len(self.A_part_number_selected)) if self.A_part_number_selected[i] != 0]


            ###############
            # Details data
            self.A_details_data = {}
            self.A_details_data[utils.setLabel(self.language, 'Ilość stacji', 'Number of stations')] = self.A_station_nmb
            self.A_details_data[utils.setLabel(self.language, 'Wybrane stacje', 'Selected stations')] = self.A_stations
            self.A_details_data[utils.setLabel(self.language, 'Data początkowa', 'Start date')] = self.date[self.A_date_selected[0]]
            self.A_details_data[utils.setLabel(self.language, 'Data końcowa', 'End date')] = self.date[self.A_date_selected[1]]
            self.A_details_data[''] = ''
            self.A_details_data[utils.setLabel(self.language, 'Wybrane zmiany', 'Selected shifts')] = self.A_shifts
            self.A_details_data[utils.setLabel(self.language, 'Wybrane cykle', 'Selected cycles')] = self.A_cycles
            self.A_details_data[utils.setLabel(self.language, 'Wybrane numery części', 'Selected part numbers')] = self.A_part_numbers
            self.A_details_data[utils.setLabel(self.language, 'Całkowita ilość silników', 'Total number of engines')] = self.serial_number_nmb
            self.A_details_data[utils.setLabel(self.language, 'Silniki z brakującymi danymi', 'Engines with missing data')] = self.wrong_transition_count
            self.A_details_data[utils.setLabel(self.language, 'Silniki z poprawnymi danymi', 'Engines with valid data')] = self.serial_number_nmb - self.wrong_transition_count
            ###############

        #######################################################################################################

        self.clearFrame()
        options_frame = ttk.Frame(self.frame)
        filters_frame = ttk.Frame(self.frame)
        chart_frame = ttk.Frame(self.frame)
        options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        filters_frame.place(relx=0, rely=0.05, relwidth=0.85, relheight=0.05)
        self.refresh_button_frame.place(
            relx=0.85, rely=0.05, relwidth=0.15, relheight=0.05)
        if self.chartA_show_filters:
            chart_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.90)
        else:
            chart_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

        ttk.Separator(options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)
        ttk.Separator(filters_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        if self.chartA_show_filters:
            filters_btn_text = utils.setLabel(self.language, u'Filtry \u25b2', u'Filters \u25b2')
        else:
            filters_btn_text = utils.setLabel(self.language, u'Filtry \u25bc', u'Filters \u25bc')
        buttons_state = tkinter.DISABLED if self.is_loading else tkinter.NORMAL
        self.A_filters_btn = ttk.Button(options_frame, text=filters_btn_text, command=lambda: self.switchFilters('A', chart_frame, self.A_filters_btn), state=buttons_state)
        self.A_details_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, 'Szczegóły', 'Details'), command=lambda: self.text_window.show(self.A_details_data), state=buttons_state)
        self.A_filters_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_details_btn.pack(side=tkinter.LEFT)

        self.A_station_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Stacja', 'Station'), command=lambda: self.combobox_window.show(self.language, self.station, self.A_station_selected), state=buttons_state)
        self.A_date_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Data', 'Date'), command=lambda: self.combobox_window.show(self.language, self.date, self.A_date_selected), state=buttons_state)
        self.A_shift_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Zmiana', 'Shift'), command=lambda: self.checklist_window.show(self.language, self.shift, self.A_shift_selected, page_len=250), state=buttons_state)
        self.A_cycle_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Cykl', 'Cycle'), command=lambda: self.checklist_window.show(self.language, self.cycle, self.A_cycle_selected, page_len=250), state=buttons_state)
        self.A_part_number_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Numer części', 'Part number'), command=lambda: self.checklist_window.show(self.language, self.part_number, self.A_part_number_selected, page_len=250), state=buttons_state)
        self.A_station_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_date_btn.pack(side=tkinter.LEFT)
        self.A_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_cycle_btn.pack(side=tkinter.LEFT)
        self.A_part_number_btn.pack(side=tkinter.LEFT, padx=15)

        #######################################################################################################

        self.figure = plt.Figure()
        self.figure.set_tight_layout(True)
        ax1 = self.figure.add_subplot(111, projection='3d')

        ax1.plot(list(range(100)), list(range(100)), list(range(100)), 'o')
        self.A_ax1_text = self.figure.text(0.99, 0.02, 'abc', horizontalalignment='right')
        self.A_ax1_text.set_text('aaabbbccc')

        canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.draw()

        chart_frame.bind('<Enter>', lambda _: self.A_ax1_text.set_text(utils.setLabel(self.language, 'LPM - obrót\nPPM - przybliżenie/oddalenie', 'LMB - rotate\nRMB - zoom in/out')))
        chart_frame.bind('<Leave>', lambda _: self.switchFigureText('', self.A_ax1_text, canvas))

    def drawChartB(self, chart_drawn=None):
        if not isinstance(chart_drawn, type(None)):
            self.chartB_drawn = chart_drawn

        if self.chartB_first_draw:
            self.B_station_selected = [0, len(self.station) - 1]
            self.B_date_selected = [0, len(self.date) - 1]
            self.B_shift_selected = self.onesList(len(self.shift))
            self.B_cycle_selected = self.onesList(len(self.cycle))
            self.B_part_number_selected = self.onesList(len(self.part_number))
            self.chartB_first_draw = False

        if not self.chartB_drawn:
            self.bars_nmb = 29
            self.B_engines_nmb = [0 for _ in range(self.bars_nmb)]
            self.B_transition_time = ['' for _ in range(self.bars_nmb)]

            self.B_station_nmb = self.B_station_selected[1] - self.B_station_selected[0] + 1
            self.B_stations =  self.station[self.B_station_selected[0]:self.B_station_selected[1] + 1]
            self.B_dates = self.date[self.B_date_selected[0]:self.B_date_selected[1] + 1]
            self.B_shifts = [self.shift[i] for i in range(len(self.B_shift_selected)) if self.B_shift_selected[i] != 0]
            self.B_cycles = [self.cycle[i] for i in range(len(self.B_cycle_selected)) if self.B_cycle_selected[i] != 0]
            self.B_part_numbers = [self.part_number[i] for i in range(len(self.B_part_number_selected)) if self.B_part_number_selected[i] != 0]
            
            self.B_engines = list(set(self.getColumn('Numer seryjny', 'Serial Number', 10)[(self.getColumn('Date', 'Date', 2).isin(self.B_dates))
                            & (self.getColumn('Przesunięcie', 'Shift', 11).isin(self.B_shifts))
                            & (self.getColumn('Cycle', 'Cycle', 5).isin(self.B_cycles)) 
                            & (self.getColumn('Numer części', 'Part Number', 9).isin(self.B_part_numbers))].values))
            self.B_engines = [e for e in self.B_engines if e in self.serial_number]
             
            time_elapsed = {}
            B_dates_set = set(self.B_dates)
            for i in range(len(self.B_engines)):
                engine_date = self.getColumn('Date', 'Date', 2)[(self.getColumn(
                    'Numer seryjny', 'Serial Number', 10) == self.B_engines[i]) & (self.getColumn('Stacja', 'Station', 1).isin(self.B_stations))].tolist()
                if self.contains(B_dates_set, engine_date):
                    delta_time = np.float64(self.getColumn('Aktualny czas trwania [s]', 'Actual duration [s]', 6)[(self.getColumn(
                        'Numer seryjny', 'Serial Number', 10) == self.B_engines[i]) & (self.getColumn('Date', 'Date', 2) == np.max(engine_date))].values[0])
                    time_elapsed[self.B_engines[i]] = (np.max(engine_date) - np.min(engine_date)) / np.timedelta64(1, 's') + delta_time
                else:
                    self.B_engines[i] = None
            self.B_engines = [e for e in self.B_engines if not e is None]
            time_elapsed_cpy = dict(time_elapsed)
            
            for i in range(self.bars_nmb - 1):
                m, s = divmod(self.B_station_nmb * 45 + i * 15 -
                              (self.B_station_nmb // 3) * 15, 60)
                self.B_transition_time[i] = f'{m:02d}:{s:02d}'
                for key, value in time_elapsed.items():
                    if value <= self.B_station_nmb * 45 + i * 15 - (self.B_station_nmb // 3) * 15 and key in time_elapsed_cpy:
                        self.B_engines_nmb[i] += 1
                        time_elapsed_cpy.pop(key, 'None')
            self.B_engines_nmb[-1] = len(time_elapsed_cpy.keys())
            self.cdf_data = self.getCDF(self.B_engines_nmb)
            self.chartB_drawn = True

            ###############
            # Details data
            self.B_details_data = {}
            self.B_details_data[utils.setLabel(self.language, 'Ilość stacji', 'Number of stations')] = self.B_station_nmb
            self.B_details_data[utils.setLabel(self.language, 'Wybrane stacje', 'Selected stations')] = self.B_stations
            self.B_details_data[utils.setLabel(self.language, 'Data początkowa', 'Start date')] = self.date[self.B_date_selected[0]]
            self.B_details_data[utils.setLabel(self.language, 'Data końcowa', 'End date')] = self.date[self.B_date_selected[1]]
            self.B_details_data[''] = ''
            self.B_details_data[utils.setLabel(self.language, 'Wybrane zmiany', 'Selected shifts')] = self.B_shifts
            self.B_details_data[utils.setLabel(self.language, 'Wybrane cykle', 'Selected cycles')] = self.B_cycles
            self.B_details_data[utils.setLabel(self.language, 'Wybrane numery części', 'Selected part numbers')] = self.B_part_numbers
            self.B_details_data[utils.setLabel(self.language, 'Całkowita ilość silników', 'Total number of engines')] = self.serial_number_nmb
            self.B_details_data[utils.setLabel(self.language, 'Silniki z brakującymi danymi', 'Engines with missing data')] = self.wrong_transition_count
            self.B_details_data[utils.setLabel(self.language, 'Silniki z poprawnymi danymi', 'Engines with valid data')] = self.serial_number_nmb - self.wrong_transition_count
            self.B_details_data[' '] = ''
            self.B_details_data[utils.setLabel(self.language, 'Ilość wybranych silników', 'Number of selected engines')] = len(self.B_engines)
            ###############

        self.B_transition_time[-1] = utils.setLabel(
            self.language, 'Więcej', 'More')
        self.B_engines_nmb_str = utils.setLabel(
            self.language, 'Liczba silników', 'Number of engines')
        self.B_transition_time_str = utils.setLabel(
            self.language, 'Czas przejścia', 'Transition time')
        self.B_cdf_str = utils.setLabel(self.language, 'Dystrybuanta', 'CDF')
        self.B_expected_time = utils.setLabel(
            self.language, 'Czas projektowy', 'Expected time')

        #######################################################################################################

        self.clearFrame()
        options_frame = ttk.Frame(self.frame)
        filters_frame = ttk.Frame(self.frame)
        chart_frame = ttk.Frame(self.frame)
        options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        filters_frame.place(relx=0, rely=0.05, relwidth=0.85, relheight=0.05)
        self.refresh_button_frame.place(
            relx=0.85, rely=0.05, relwidth=0.15, relheight=0.05)
        if self.chartB_show_filters:
            chart_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.90)
        else:
            chart_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

        ttk.Separator(options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)
        ttk.Separator(filters_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        if self.chartB_show_filters:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25b2', u'Filters \u25b2')
        else:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25bc', u'Filters \u25bc')
        buttons_state = tkinter.DISABLED if self.is_loading else tkinter.NORMAL
        self.B_filters_btn = ttk.Button(options_frame, text=filters_btn_text,
                                 command=lambda: self.switchFilters('B', chart_frame, self.B_filters_btn), state=buttons_state)
        self.B_details_btn = ttk.Button(options_frame, text=utils.setLabel(self.language, 'Szczegóły',
                   'Details'), command=lambda: self.text_window.show(self.B_details_data), state=buttons_state)
        self.show_cdf_var = tkinter.IntVar(value=1 if self.show_cdf else 0)
        self.B_cdf_checkbtn = ttk.Checkbutton(options_frame, text=utils.setLabel(self.language, 'Pokaż dystrybuantę', 'Show CDF'),
                        variable=self.show_cdf_var, command=lambda: self.switchShowCDFVar('B'), state=buttons_state)
        self.B_filters_btn.pack(side=tkinter.LEFT, padx=15)
        self.B_details_btn.pack(side=tkinter.LEFT)
        self.B_cdf_checkbtn.pack(side=tkinter.LEFT, padx=15)

        self.B_station_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Stacja', 'Station'),
                   command=lambda: self.combobox_window.show(self.language, self.station, self.B_station_selected), state=buttons_state)
        self.B_date_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Data', 'Date'),
                   command=lambda: self.combobox_window.show(self.language, self.date, self.B_date_selected), state=buttons_state)
        self.B_shift_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Zmiana', 'Shift'),
                   command=lambda: self.checklist_window.show(self.language, self.shift, self.B_shift_selected, page_len=250), state=buttons_state)
        self.B_cycle_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Cykl', 'Cycle'),
                   command=lambda: self.checklist_window.show(self.language, self.cycle, self.B_cycle_selected, page_len=250), state=buttons_state)
        self.B_part_number_btn = ttk.Button(filters_frame, text=utils.setLabel(self.language, 'Numer części', 'Part number'),
                   command=lambda: self.checklist_window.show(self.language, self.part_number, self.B_part_number_selected, page_len=250), state=buttons_state)
        self.B_station_btn.pack(side=tkinter.LEFT, padx=15)
        self.B_date_btn.pack(side=tkinter.LEFT)
        self.B_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.B_cycle_btn.pack(side=tkinter.LEFT)
        self.B_part_number_btn.pack(side=tkinter.LEFT, padx=15)

        #######################################################################################################

        self.figure = plt.Figure()
        self.figure.set_tight_layout(True)
        ax1 = self.figure.add_subplot(111)

        hist = ax1.bar(self.B_transition_time,
                       self.B_engines_nmb, align='edge', width=-0.8)
        expected_time = ax1.axvline(x=self.B_station_nmb // 3, color='grey')
        ax1.set_title(utils.setLabel(self.language, 'Histogram czasu przepływu',
                      'Transition time histogram'), pad=15, weight='bold')
        ax1.tick_params(labelrotation=90)
        ax1.set_xlabel(self.B_transition_time_str)
        for bar, label in zip(ax1.patches, self.B_engines_nmb):
            if label > 0:
                rotation = 0 if len(str(label)) < 4 else 45
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (0.01 * max(self.B_engines_nmb)
                                                                                if rotation == 45 else 0), str(label), ha='center', va='bottom', rotation=rotation)

        if self.show_cdf:
            ax2 = ax1.twinx()
            cdf = ax2.plot(self.B_transition_time, self.cdf_data, 'rs-')
            ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
            ax2.set_ylim(0, 101)
            for bar, label in zip(ax1.patches, self.cdf_data):
                ax2.text(bar.get_x(), label, str(round(label)) + '%',
                         ha='right', va='bottom', color='red', weight='semibold', fontsize='small')
            lengend_handles = [hist, cdf[0], expected_time]
            legend_labels = [self.B_engines_nmb_str,
                             self.B_cdf_str, self.B_expected_time]
        else:
            lengend_handles = [hist, expected_time]
            legend_labels = [self.B_engines_nmb_str, self.B_expected_time]
        ax1.legend(lengend_handles, legend_labels, bbox_to_anchor=(
            1, 0.92 + 0.02 * len(lengend_handles)))

        canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.draw()

    def drawChartC(self, chart_drawn=None):
        self.clearFrame()
        print('Empty')

    def drawChartD(self, chart_drawn=None):
        self.clearFrame()
        print('Empty')

    def drawChartE(self, chart_drawn=None):
        self.clearFrame()
        print('Empty')


if __name__ == '__main__':
    pass
