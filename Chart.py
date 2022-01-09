from imports import *
from ChecklistWindow import *
from ComboboxWindow import *
from TextWindow import *
from CalendarWindow import *
from ChartPreview import *


class Chart:
    def __init__(self, root, frame, buttons_frame, language, rwlFun):
        self.root = root
        self.frame = frame
        self.buttons_frame = buttons_frame
        self.checklist_window = ChecklistWindow(root, 250, 520)
        self.combobox_window = ComboboxWindow(root, 220, 120)
        self.text_window = TextWindow(root, 700, 450)
        self.calendar_window = CalendarWindow(root, 220, 120)
        self.chart_preview = ChartPreview(root)
        self.language = language
        self.rwlFun = rwlFun

        self.excel_table = None
        self.show_cdf = True

        # ChartA
        self.A_axis_choice_var = tkinter.StringVar()
        self.A_axis_choice_prev_var = tkinter.StringVar()
        self.A_axis_choice_nmb = 0
        self.A_axis_choice_list = [
            utils.setLabel(
                self.language, 'Stacje', 'Stations'), utils.setLabel(
                self.language, 'Pracownicy', 'Employees')]
        self.A_axis_choice_var.trace_id = None

        self.A_mode_choice_var = tkinter.StringVar()
        self.A_mode_choice_prev_var = tkinter.StringVar()
        self.A_mode_choice_nmb = 0
        self.A_mode_choice_list = [
            utils.setLabel(
                self.language,
                'Czas przejścia',
                'Transition time'),
            utils.setLabel(
                self.language,
                'Czas operacji',
                'Operation time')]
        self.A_mode_choice_var.trace_id = None

        self.A_chart_data = None

        self.A_options_frame = ttk.Frame(self.frame)
        self.A_filters_frame = ttk.Frame(self.frame)
        self.A_chart_frame = ttk.Frame(self.frame)

        ttk.Separator(self.A_options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)
        ttk.Separator(self.A_filters_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)
        self.A_sep = ttk.Separator(self.A_filters_frame, orient='vertical')

        self.A_filters_btn = ttk.Button(self.A_options_frame, text=utils.setLabel(self.language, u'Filtry \u25bc', u'Filters \u25bc'),
                                        command=lambda: self.switchFilters('A', self.A_chart_frame, self.A_filters_btn))
        self.A_details_btn = ttk.Button(self.A_options_frame, text=utils.setLabel(
            self.language, 'Szczegóły', 'Details'), command=lambda: self.text_window.show(self.A_details_data, self.language, utils.setLabel(self.language, 'Szczegóły', 'Details')))
        self.A_preview_btn = ttk.Button(
            self.A_options_frame, text=utils.setLabel(
                self.language, 'Podgląd', 'Preview'), command=lambda: self.chart_preview.show(
                self.language, 'A', self.A_chart_data))
        self.A_station_btn = ttk.Button(self.A_filters_frame, text=utils.setLabel(self.language, 'Stacja', 'Station'), command=lambda: self.checklist_window.show(
            self.language, self.station, self.A_station_selected, page_len=250))
        self.A_employee_btn = ttk.Button(self.A_filters_frame, text=utils.setLabel(self.language, 'Pracownik', 'Employee'), command=lambda: self.checklist_window.show(
            self.language, self.operator_name, self.A_employee_selected, page_len=250))
        self.A_date_btn = ttk.Button(self.A_filters_frame, text=utils.setLabel(self.language, 'Data', 'Date'),
                                     command=lambda: self.calendar_window.show(self.language, self.date, self.A_date_selected, 'A'))
        self.A_shift_btn = ttk.Button(self.A_filters_frame, text=utils.setLabel(self.language, 'Zmiana', 'Shift'), command=lambda: self.checklist_window.show(
            self.language, self.shift, self.A_shift_selected, page_len=250))
        self.A_cycle_btn = ttk.Button(self.A_filters_frame, text=utils.setLabel(self.language, 'Cykl', 'Cycle'), command=lambda: self.checklist_window.show(
            self.language, self.cycle, self.A_cycle_selected, page_len=250))
        self.A_part_number_btn = ttk.Button(self.A_filters_frame, text=utils.setLabel(self.language, 'Numer części', 'Part number'), command=lambda: self.checklist_window.show(
            self.language, self.part_number, self.A_part_number_selected, page_len=250))
        self.A_serial_number_btn = ttk.Button(self.A_filters_frame, text=utils.setLabel(self.language, 'Numer seryjny', 'Serial number'), command=lambda: self.checklist_window.show(
            self.language, self.serial_number, self.A_serial_number_selected, page_len=250))
        self.A_filters_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_details_btn.pack(side=tkinter.LEFT)
        self.A_preview_btn.pack(side=tkinter.LEFT, padx=15)
        if self.A_axis_choice_nmb == 0:
            self.A_station_btn.pack(side=tkinter.LEFT, padx=15)
        else:
            self.A_employee_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_date_btn.pack(side=tkinter.LEFT)
        self.A_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_cycle_btn.pack(side=tkinter.LEFT)
        self.A_part_number_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_serial_number_btn.pack(side=tkinter.LEFT, padx=(0, 15))
        self.A_sep.pack(side=tkinter.LEFT, fill=tkinter.Y)

        self.A_label = ttk.Label(self.A_options_frame, text=utils.setLabel(
            self.language, 'Oś X:', 'X Axis:'))
        self.A_option_menu = ttk.OptionMenu(
            self.A_options_frame,
            self.A_axis_choice_var,
            utils.setLabel(
                self.language,
                'Stacje',
                'Stations'),
            *self.A_axis_choice_list)
        self.A_label2 = ttk.Label(
            self.A_options_frame, text=utils.setLabel(
                self.language, 'Oś Z:', 'Z Axis:'))
        self.A_option_menu2 = ttk.OptionMenu(
            self.A_options_frame,
            self.A_mode_choice_var,
            utils.setLabel(
                self.language,
                'Czas przejścia',
                'Transition time'),
            *self.A_mode_choice_list)

        self.A_figure = Figure()
        self.A_canvas = FigureCanvasTkAgg(self.A_figure, self.A_chart_frame)
        self.A_canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        # ChartB
        self.B_two_color = False

        self.B_axis_choice_var = tkinter.StringVar()
        self.B_axis_choice_prev_var = tkinter.StringVar()
        self.B_axis_choice_nmb = 0
        self.B_axis_choice_list = [
            utils.setLabel(
                self.language,
                'Czas przejścia',
                'Transition time'),
            utils.setLabel(
                self.language,
                'Czas operacji',
                'Operation time')]
        self.B_axis_choice_var.trace_id = None

        self.B_options_frame = ttk.Frame(self.frame)
        self.B_filters_frame = ttk.Frame(self.frame)
        self.B_chart_frame = ttk.Frame(self.frame)

        ttk.Separator(self.B_options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)
        ttk.Separator(self.B_filters_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        self.B_filters_btn = ttk.Button(self.B_options_frame, text=utils.setLabel(self.language, u'Filtry \u25bc', u'Filters \u25bc'),
                                        command=lambda: self.switchFilters('B', self.B_chart_frame, self.B_filters_btn))
        self.B_details_btn = ttk.Button(self.B_options_frame, text=utils.setLabel(self.language, 'Szczegóły',
                                                                                  'Details'), command=lambda: self.text_window.show(self.B_details_data, self.language, utils.setLabel(self.language, 'Szczegóły', 'Details')))
        self.show_cdf_var = tkinter.IntVar(value=1 if self.show_cdf else 0)
        self.B_cdf_checkbtn = ttk.Checkbutton(self.B_options_frame, text=utils.setLabel(self.language, 'Pokaż dystrybuantę', 'Show CDF'),
                                              variable=self.show_cdf_var, command=lambda: self.switchShowCDFVar('B'))
        self.B_two_color_var = tkinter.IntVar(value=1 if self.B_two_color else 0)
        self.B_two_color_checkbtn = ttk.Checkbutton(self.B_options_frame, text=utils.setLabel(self.language, 'Tryb dwukolorowy', 'Two-color mode'), variable=self.B_two_color_var, command=lambda: self.switchTwoColorMode('B'))
        self.B_station_btn = ttk.Button(self.B_filters_frame, text=utils.setLabel(self.language, 'Stacja', 'Station'),
                                        command=lambda: self.combobox_window.show(self.language, self.station, self.B_station_selected))
        self.B_date_btn = ttk.Button(self.B_filters_frame, text=utils.setLabel(self.language, 'Data', 'Date'),
                                     command=lambda: self.calendar_window.show(self.language, self.date, self.B_date_selected, 'B'))
        self.B_shift_btn = ttk.Button(self.B_filters_frame, text=utils.setLabel(self.language, 'Zmiana', 'Shift'),
                                      command=lambda: self.checklist_window.show(self.language, self.shift, self.B_shift_selected, page_len=250))
        self.B_cycle_btn = ttk.Button(self.B_filters_frame, text=utils.setLabel(self.language, 'Cykl', 'Cycle'),
                                      command=lambda: self.checklist_window.show(self.language, self.cycle, self.B_cycle_selected, page_len=250))
        self.B_part_number_btn = ttk.Button(self.B_filters_frame, text=utils.setLabel(self.language, 'Numer części', 'Part number'),
                                            command=lambda: self.checklist_window.show(self.language, self.part_number, self.B_part_number_selected, page_len=250))
        self.B_serial_number_btn = ttk.Button(self.B_filters_frame, text=utils.setLabel(self.language, 'Numer seryjny', 'Serial number'), command=lambda: self.checklist_window.show(
            self.language, self.serial_number, self.B_serial_number_selected, page_len=250))
        self.B_filters_btn.pack(side=tkinter.LEFT, padx=15)
        self.B_details_btn.pack(side=tkinter.LEFT)
        self.B_cdf_checkbtn.pack(side=tkinter.LEFT, padx=15)
        self.B_two_color_checkbtn.pack(side=tkinter.LEFT)
        self.B_station_btn.pack(side=tkinter.LEFT, padx=15)
        self.B_date_btn.pack(side=tkinter.LEFT)
        self.B_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.B_cycle_btn.pack(side=tkinter.LEFT)
        self.B_part_number_btn.pack(side=tkinter.LEFT, padx=15)
        self.B_serial_number_btn.pack(side=tkinter.LEFT, padx=(0, 15))
        ttk.Separator(self.B_filters_frame, orient='vertical').pack(
            side=tkinter.LEFT, fill=tkinter.Y)

        self.B_label = ttk.Label(self.B_options_frame, text=utils.setLabel(
            self.language, 'Tryb:', 'Mode:'))
        self.B_option_menu = ttk.OptionMenu(
            self.B_options_frame,
            self.B_axis_choice_var,
            utils.setLabel(
                self.language,
                'Czas przejścia',
                'Transition time'),
            *self.B_axis_choice_list)

        self.B_figure = Figure()
        self.B_canvas = FigureCanvasTkAgg(self.B_figure, self.B_chart_frame)
        self.B_canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        # ChartC
        self.C_options_frame = ttk.Frame(self.frame)
        self.C_filters_frame = ttk.Frame(self.frame)
        self.C_chart_frame = ttk.Frame(self.frame)

        ttk.Separator(self.C_options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)
        ttk.Separator(self.C_filters_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        self.C_filters_btn = ttk.Button(self.C_options_frame, text=utils.setLabel(self.language, u'Filtry \u25bc', u'Filters \u25bc'),
                                        command=lambda: self.switchFilters('C', self.C_chart_frame, self.C_filters_btn))
        self.C_details_btn = ttk.Button(self.C_options_frame, text=utils.setLabel(self.language, 'Szczegóły',
                                                                                  'Details'), command=lambda: self.text_window.show(self.C_details_data, self.language, utils.setLabel(self.language, 'Szczegóły', 'Details')))
        self.C_station_btn = ttk.Button(self.C_filters_frame, text=utils.setLabel(self.language, 'Stacja', 'Station'),
                                        command=lambda: self.checklist_window.show(self.language, self.station, self.C_station_selected, page_len=250))
        self.C_date_btn = ttk.Button(self.C_filters_frame, text=utils.setLabel(self.language, 'Data', 'Date'),
                                     command=lambda: self.calendar_window.show(self.language, self.date, self.C_date_selected, 'C'))
        self.C_shift_btn = ttk.Button(self.C_filters_frame, text=utils.setLabel(self.language, 'Zmiana', 'Shift'),
                                      command=lambda: self.checklist_window.show(self.language, self.shift, self.C_shift_selected, page_len=250))
        self.C_cycle_btn = ttk.Button(self.C_filters_frame, text=utils.setLabel(self.language, 'Cykl', 'Cycle'),
                                      command=lambda: self.checklist_window.show(self.language, self.cycle, self.C_cycle_selected, page_len=250))
        self.C_part_number_btn = ttk.Button(self.C_filters_frame, text=utils.setLabel(self.language, 'Numer części', 'Part number'),
                                            command=lambda: self.checklist_window.show(self.language, self.part_number, self.C_part_number_selected, page_len=250))
        self.C_serial_number_btn = ttk.Button(self.C_filters_frame, text=utils.setLabel(self.language, 'Numer seryjny', 'Serial number'), command=lambda: self.checklist_window.show(
            self.language, self.serial_number, self.C_serial_number_selected, page_len=250))
        self.C_filters_btn.pack(side=tkinter.LEFT, padx=15)
        self.C_details_btn.pack(side=tkinter.LEFT)
        self.C_station_btn.pack(side=tkinter.LEFT, padx=15)
        self.C_date_btn.pack(side=tkinter.LEFT)
        self.C_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.C_cycle_btn.pack(side=tkinter.LEFT)
        self.C_part_number_btn.pack(side=tkinter.LEFT, padx=15)
        self.C_serial_number_btn.pack(side=tkinter.LEFT, padx=(0, 15))
        ttk.Separator(self.C_filters_frame, orient='vertical').pack(
            side=tkinter.LEFT, fill=tkinter.Y)

        self.C_figure = Figure()
        self.C_canvas = FigureCanvasTkAgg(self.C_figure, self.C_chart_frame)
        self.C_canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        # ChartD
        self.D_options_frame = ttk.Frame(self.frame)
        self.D_filters_frame = ttk.Frame(self.frame)
        self.D_chart_frame = ttk.Frame(self.frame)

        ttk.Separator(self.D_options_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)
        ttk.Separator(self.D_filters_frame, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        self.D_filters_btn = ttk.Button(self.D_options_frame, text=utils.setLabel(self.language, u'Filtry \u25bc', u'Filters \u25bc'),
                                        command=lambda: self.switchFilters('D', self.D_chart_frame, self.D_filters_btn))
        self.D_details_btn = ttk.Button(self.D_options_frame, text=utils.setLabel(self.language, 'Szczegóły',
                                                                                  'Details'), command=lambda: self.text_window.show(self.D_details_data, self.language, utils.setLabel(self.language, 'Szczegóły', 'Details')))
        self.D_station_btn = ttk.Button(self.D_filters_frame, text=utils.setLabel(self.language, 'Stacja', 'Station'),
                                        command=lambda: self.checklist_window.show(self.language, self.station, self.D_station_selected, page_len=250))
        self.D_date_btn = ttk.Button(self.D_filters_frame, text=utils.setLabel(self.language, 'Data', 'Date'),
                                     command=lambda: self.calendar_window.show(self.language, self.date, self.D_date_selected, 'D'))
        self.D_shift_btn = ttk.Button(self.D_filters_frame, text=utils.setLabel(self.language, 'Zmiana', 'Shift'),
                                      command=lambda: self.checklist_window.show(self.language, self.shift, self.D_shift_selected, page_len=250))
        self.D_cycle_btn = ttk.Button(self.D_filters_frame, text=utils.setLabel(self.language, 'Cykl', 'Cycle'),
                                      command=lambda: self.checklist_window.show(self.language, self.cycle, self.D_cycle_selected, page_len=250))
        self.D_part_number_btn = ttk.Button(self.D_filters_frame, text=utils.setLabel(self.language, 'Numer części', 'Part number'),
                                            command=lambda: self.checklist_window.show(self.language, self.part_number, self.D_part_number_selected, page_len=250))
        self.D_serial_number_btn = ttk.Button(self.D_filters_frame, text=utils.setLabel(self.language, 'Numer seryjny', 'Serial number'), command=lambda: self.checklist_window.show(
            self.language, self.serial_number, self.D_serial_number_selected, page_len=250))
        self.D_filters_btn.pack(side=tkinter.LEFT, padx=15)
        self.D_details_btn.pack(side=tkinter.LEFT)
        self.D_station_btn.pack(side=tkinter.LEFT, padx=15)
        self.D_date_btn.pack(side=tkinter.LEFT)
        self.D_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.D_cycle_btn.pack(side=tkinter.LEFT)
        self.D_part_number_btn.pack(side=tkinter.LEFT, padx=15)
        self.D_serial_number_btn.pack(side=tkinter.LEFT, padx=(0, 15))
        ttk.Separator(self.D_filters_frame, orient='vertical').pack(
            side=tkinter.LEFT, fill=tkinter.Y)

        self.D_figure = Figure()
        self.D_canvas = FigureCanvasTkAgg(self.D_figure, self.D_chart_frame)
        self.D_canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        # ChartE
        self.E_mode_choice_var = tkinter.StringVar()
        self.E_mode_choice_prev_var = tkinter.StringVar()
        self.E_mode_choice_nmb = 0
        self.E_mode_choice_list = [
            utils.setLabel(
                self.language, 'Stacje', 'Stations'), utils.setLabel(
                self.language, 'Pracownicy', 'Employees')]
        self.E_mode_choice_var.trace_id = None

        self.E_options_frame = ttk.Frame(self.frame)
        self.E_filters_frame = ttk.Frame(self.frame)
        self.E_chart_frame = ttk.Frame(self.frame)

        ttk.Separator(
            self.E_options_frame,
            orient='horizontal').place(
            relx=0,
            rely=0.98,
            relwidth=1)
        ttk.Separator(
            self.E_filters_frame,
            orient='horizontal').place(
            relx=0,
            rely=0.98,
            relwidth=1)
        self.E_sep = ttk.Separator(self.E_filters_frame, orient='vertical')

        self.E_filters_btn = ttk.Button(
            self.E_options_frame,
            text=utils.setLabel(
                self.language,
                u'Filtry \u25bc',
                u'Filters \u25bc'),
            command=lambda: self.switchFilters(
                'E',
                self.E_chart_frame,
                self.E_filters_btn))
        self.E_details_btn = ttk.Button(
            self.E_options_frame, text=utils.setLabel(
                self.language, 'Szczegóły', 'Details'), command=lambda: self.text_window.show(
                self.E_details_data, self.language, utils.setLabel(self.language, 'Szczegóły', 'Details')))
        self.E_station_btn = ttk.Button(
            self.E_filters_frame, text=utils.setLabel(
                self.language, 'Stacja', 'Station'), command=lambda: self.checklist_window.show(
                self.language, self.station, self.E_station_selected, page_len=250))
        self.E_employee_btn = ttk.Button(
            self.E_filters_frame,
            text=utils.setLabel(
                self.language,
                'Pracownik',
                'Employee'),
            command=lambda: self.checklist_window.show(
                self.language,
                self.operator_name,
                self.E_employee_selected,
                page_len=250))
        self.E_date_btn = ttk.Button(
            self.E_filters_frame, text=utils.setLabel(
                self.language, 'Data', 'Date'), command=lambda: self.calendar_window.show(
                self.language, self.date, self.E_date_selected, 'E'))
        self.E_shift_btn = ttk.Button(
            self.E_filters_frame, text=utils.setLabel(
                self.language, 'Zmiana', 'Shift'), command=lambda: self.checklist_window.show(
                self.language, self.shift, self.E_shift_selected, page_len=250))
        self.E_cycle_btn = ttk.Button(
            self.E_filters_frame, text=utils.setLabel(
                self.language, 'Cykl', 'Cycle'), command=lambda: self.checklist_window.show(
                self.language, self.cycle, self.E_cycle_selected, page_len=250))
        self.E_part_number_btn = ttk.Button(
            self.E_filters_frame,
            text=utils.setLabel(
                self.language,
                'Numer części',
                'Part number'),
            command=lambda: self.checklist_window.show(
                self.language,
                self.part_number,
                self.E_part_number_selected,
                page_len=250))
        self.E_serial_number_btn = ttk.Button(self.E_filters_frame, text=utils.setLabel(self.language, 'Numer seryjny', 'Serial number'), command=lambda: self.checklist_window.show(
            self.language, self.serial_number, self.E_serial_number_selected, page_len=250))
        self.E_filters_btn.pack(side=tkinter.LEFT, padx=15)
        self.E_details_btn.pack(side=tkinter.LEFT)
        if self.E_mode_choice_nmb == 0:
            self.E_station_btn.pack(side=tkinter.LEFT, padx=15)
        else:
            self.E_employee_btn.pack(side=tkinter.LEFT, padx=15)
        self.E_date_btn.pack(side=tkinter.LEFT)
        self.E_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.E_cycle_btn.pack(side=tkinter.LEFT)
        self.E_part_number_btn.pack(side=tkinter.LEFT, padx=15)
        self.E_serial_number_btn.pack(side=tkinter.LEFT, padx=(0, 15))
        self.E_sep.pack(side=tkinter.LEFT, fill=tkinter.Y)

        self.E_label = ttk.Label(
            self.E_options_frame, text=utils.setLabel(
                self.language, 'Tryb:', 'Mode:'))
        self.E_option_menu = ttk.OptionMenu(
            self.E_options_frame,
            self.E_mode_choice_var,
            utils.setLabel(
                self.language,
                'Stacje',
                'Stations'),
            *self.E_mode_choice_list)

        self.E_figure = Figure()
        self.E_canvas = FigureCanvasTkAgg(self.E_figure, self.E_chart_frame)
        self.E_canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

    @utils.threadpool
    def setExcelTable(self, excel_table, language, is_loading):
        self.excel_table = excel_table
        self.language = language
        self.is_loading = is_loading

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

        engines_stations = self.getColumns(['Numer seryjny', 'Stacja'], [
                                           'Serial Number', 'Station'], [10, 1])
        engines_stations = engines_stations.sort_values(
            by=[engines_stations.columns[0], engines_stations.columns[1]]).values.tolist()

        engines_stations_dict = {}
        prev_engine = ''
        for i in range(len(engines_stations)):
            engine = engines_stations[i][0]
            station = engines_stations[i][1]
            if engine != prev_engine:
                engines_stations_dict[engine] = []
            engines_stations_dict[engine].append(station)
            prev_engine = engine
        engines_stations_dict_cpy = dict(engines_stations_dict)

        for key, value in engines_stations_dict_cpy.items():
            if sorted(value) != sorted(self.station):
                engines_stations_dict.pop(key, None)
                self.wrong_transition_count += 1
        self.serial_number = list(engines_stations_dict).copy()

        # Charts
        self.show_cdf = True
        self.B_two_color = False

        self.show_cdf_var.set(1)
        self.B_two_color_var.set(0)

        self.chartA_drawn = False
        self.chartA_first_draw = True
        self.chartA_show_filters = False

        self.chartB_drawn = False
        self.chartB_first_draw = True
        self.chartB_show_filters = False

        self.chartC_drawn = False
        self.chartC_first_draw = True
        self.chartC_show_filters = False

        self.chartD_drawn = False
        self.chartD_first_draw = True
        self.chartD_show_filters = False

        self.chartE_drawn = False
        self.chartE_first_draw = True
        self.chartE_show_filters = False

        self.A_axis_choice_nmb = 0
        self.A_mode_choice_nmb = 0
        self.B_axis_choice_nmb = 0
        self.E_mode_choice_nmb = 0

        if not isinstance(self.A_axis_choice_var.trace_id, type(None)):
            self.A_axis_choice_var.trace_vdelete(
                'w', self.A_axis_choice_var.trace_id)
        if not isinstance(self.A_mode_choice_var.trace_id, type(None)):
            self.A_mode_choice_var.trace_vdelete(
                'w', self.A_mode_choice_var.trace_id)
        if not isinstance(self.B_axis_choice_var.trace_id, type(None)):
            self.B_axis_choice_var.trace_vdelete(
                'w', self.B_axis_choice_var.trace_id)
        if not isinstance(self.E_mode_choice_var.trace_id, type(None)):
            self.E_mode_choice_var.trace_vdelete(
                'w', self.E_mode_choice_var.trace_id)
        self.A_axis_choice_var.trace_id = self.A_axis_choice_var.trace(
            'w', lambda *args: self.switchChartAAxisX())
        self.A_mode_choice_var.trace_id = self.A_mode_choice_var.trace(
            'w', lambda *args: self.switchChartAMode())
        self.B_axis_choice_var.trace_id = self.B_axis_choice_var.trace(
            'w', lambda *args: self.switchChartBMode())
        self.E_mode_choice_var.trace_id = self.E_mode_choice_var.trace(
            'w', lambda *args: self.switchChartEMode())

        Globals.chartA_start_date = None
        Globals.chartA_end_date = None
        Globals.chartB_start_date = None
        Globals.chartB_end_date = None
        Globals.chartC_start_date = None
        Globals.chartC_end_date = None
        Globals.chartD_start_date = None
        Globals.chartD_end_date = None
        Globals.chartE_start_date = None
        Globals.chartE_end_date = None

    def setLanguage(self, language):
        self.language = language

    def setIsLoading(self, is_loading):
        self.is_loading = is_loading

    def getIsLoading(self):
        return self.is_loading

    def getColumn(self, column_name=None, optional_name=None, col_index=None):
        try:
            col = self.excel_table[column_name].copy()
        except Exception:
            try:
                col = self.excel_table[optional_name].copy()
            except Exception:
                try:
                    col = self.excel_table.iloc[:, col_index].copy()
                except Exception:
                    col = pd.Series()
        finally:
            return col

    def getColumns(self, column_names=None,
                   optional_names=None, col_indexes=None):
        try:
            cols = self.excel_table[column_names].copy()
        except Exception:
            try:
                cols = self.excel_table[optional_names].copy()
            except Exception:
                try:
                    cols = self.excel_table.iloc[:, col_indexes].copy()
                except Exception:
                    cols = pd.DataFrame()
        finally:
            return cols

    def getColumnUniqueList(self, column_name=None,
                            optional_name=None, col_index=None):
        return list(
            set(self.getColumn(column_name, optional_name, col_index).tolist()))

    def clearFrame(self, chart_name):
        self.buttons_frame.place_forget()

        # ChartA
        if not chart_name == 'A':
            self.A_options_frame.place_forget()
            self.A_filters_frame.place_forget()
            self.A_chart_frame.place_forget()

            self.A_station_btn.pack_forget()
            self.A_employee_btn.pack_forget()
            self.A_date_btn.pack_forget()
            self.A_shift_btn.pack_forget()
            self.A_cycle_btn.pack_forget()
            self.A_part_number_btn.pack_forget()
            self.A_serial_number_btn.pack_forget()
            self.A_sep.pack_forget()

            self.A_label.pack_forget()
            self.A_option_menu.pack_forget()
            self.A_label2.pack_forget()
            self.A_option_menu2.pack_forget()

        # ChartB
        if not chart_name == 'B':
            self.B_options_frame.place_forget()
            self.B_filters_frame.place_forget()
            self.B_chart_frame.place_forget()

            self.B_label.pack_forget()
            self.B_option_menu.pack_forget()

        # ChartC
        if not chart_name == 'C':
            self.C_options_frame.place_forget()
            self.C_filters_frame.place_forget()
            self.C_chart_frame.place_forget()

        # ChartD
        if not chart_name == 'D':
            self.D_options_frame.place_forget()
            self.D_filters_frame.place_forget()
            self.D_chart_frame.place_forget()

        # ChartE
        if not chart_name == 'E':
            self.E_options_frame.place_forget()
            self.E_filters_frame.place_forget()
            self.E_chart_frame.place_forget()

            self.E_station_btn.pack_forget()
            self.E_employee_btn.pack_forget()
            self.E_date_btn.pack_forget()
            self.E_shift_btn.pack_forget()
            self.E_cycle_btn.pack_forget()
            self.E_part_number_btn.pack_forget()
            self.E_serial_number_btn.pack_forget()
            self.E_sep.pack_forget()

            self.E_label.pack_forget()
            self.E_option_menu.pack_forget()

        if chart_name == 'A':
            self.A_options_frame.place_forget()
            self.A_filters_frame.place_forget()
            self.A_chart_frame.place_forget()

            self.A_station_btn.pack_forget()
            self.A_employee_btn.pack_forget()
            self.A_date_btn.pack_forget()
            self.A_shift_btn.pack_forget()
            self.A_cycle_btn.pack_forget()
            self.A_part_number_btn.pack_forget()
            self.A_serial_number_btn.pack_forget()
            self.A_sep.pack_forget()

            self.A_label.pack_forget()
            self.A_option_menu.pack_forget()
            self.A_label2.pack_forget()
            self.A_option_menu2.pack_forget()
        elif chart_name == 'B':
            self.B_options_frame.place_forget()
            self.B_filters_frame.place_forget()
            self.B_chart_frame.place_forget()

            self.B_label.pack_forget()
            self.B_option_menu.pack_forget()
        elif chart_name == 'C':
            self.C_options_frame.place_forget()
            self.C_filters_frame.place_forget()
            self.C_chart_frame.place_forget()
        elif chart_name == 'D':
            self.D_options_frame.place_forget()
            self.D_filters_frame.place_forget()
            self.D_chart_frame.place_forget()
        elif chart_name == 'E':
            self.E_options_frame.place_forget()
            self.E_filters_frame.place_forget()
            self.E_chart_frame.place_forget()

            self.E_station_btn.pack_forget()
            self.E_employee_btn.pack_forget()
            self.E_date_btn.pack_forget()
            self.E_shift_btn.pack_forget()
            self.E_cycle_btn.pack_forget()
            self.E_part_number_btn.pack_forget()
            self.E_serial_number_btn.pack_forget()
            self.E_sep.pack_forget()

            self.E_label.pack_forget()
            self.E_option_menu.pack_forget()

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
            return [0 for _ in range(Globals.bars_nmb)]
        for i in range(len(cdf)):
            cdf[i] = round((cdf[i] / data_list_sum) * 100, 2)
        return cdf

    @utils.threadpool
    def drawChart(self, chart_name='A', chart_drawn=None, mode='single'):
        def chartChoice(chart):
            return {
                'A': self.drawChartA,
                'B': self.drawChartB,
                'C': self.drawChartC,
                'D': self.drawChartD,
                'E': self.drawChartE
            }.get(chart, self.drawChartA)

        if mode == 'all':
            self.chartA_drawn = False
            self.chartB_drawn = False
            self.chartC_drawn = False
            self.chartD_drawn = False
            self.chartE_drawn = False

        if chart_name != 'None':
            chartChoice(chart_name)(chart_drawn)

    @utils.threadpool
    def saveChart(self, figure, filename):
        if figure == 'A':
            self.A_figure.savefig(filename)
        elif figure == 'B':
            self.B_figure.savefig(filename)
        elif figure == 'C':
            self.C_figure.savefig(filename)
        elif figure == 'D':
            self.D_figure.savefig(filename)
        elif figure == 'E':
            self.E_figure.savefig(filename)

    @utils.threadpool
    def resetFilters(self, chart_name):
        if chart_name == 'A':
            self.A_station_selected = self.onesList(len(self.station))
            self.A_employee_selected = self.onesList(len(self.operator_name))
            self.A_date_selected = [0, len(self.date) - 1]
            self.A_shift_selected = self.onesList(len(self.shift))
            self.A_cycle_selected = self.onesList(len(self.cycle))
            self.A_part_number_selected = self.onesList(len(self.part_number))
            self.A_serial_number_selected = self.onesList(len(self.serial_number))

            Globals.chartA_start_date = None
            Globals.chartA_end_date = None
        elif chart_name == 'B':
            self.B_station_selected = [0, len(self.station) - 1]
            self.B_date_selected = [0, len(self.date) - 1]
            self.B_shift_selected = self.onesList(len(self.shift))
            self.B_cycle_selected = self.onesList(len(self.cycle))
            self.B_part_number_selected = self.onesList(len(self.part_number))
            self.B_serial_number_selected = self.onesList(len(self.serial_number))

            Globals.chartB_start_date = None
            Globals.chartB_end_date = None
        elif chart_name == 'C':
            self.C_station_selected = self.onesList(len(self.station))
            self.C_date_selected = [0, len(self.date) - 1]
            self.C_shift_selected = self.onesList(len(self.shift))
            self.C_cycle_selected = self.onesList(len(self.cycle))
            self.C_part_number_selected = self.onesList(len(self.part_number))
            self.C_serial_number_selected = self.onesList(len(self.serial_number))

            Globals.chartC_start_date = None
            Globals.chartC_end_date = None
        elif chart_name == 'D':
            self.D_station_selected = self.onesList(len(self.station))
            self.D_date_selected = [0, len(self.date) - 1]
            self.D_shift_selected = self.onesList(len(self.shift))
            self.D_cycle_selected = self.onesList(len(self.cycle))
            self.D_part_number_selected = self.onesList(len(self.part_number))
            self.D_serial_number_selected = self.onesList(len(self.serial_number))

            Globals.chartD_start_date = None
            Globals.chartD_end_date = None
        elif chart_name == 'E':
            self.E_station_selected = self.onesList(len(self.station))
            self.E_employee_selected = self.onesList(len(self.operator_name))
            self.E_date_selected = [0, len(self.date) - 1]
            self.E_shift_selected = self.onesList(len(self.shift))
            self.E_cycle_selected = self.onesList(len(self.cycle))
            self.E_part_number_selected = self.onesList(len(self.part_number))
            self.E_serial_number_selected = self.onesList(len(self.serial_number))

            Globals.chartE_start_date = None
            Globals.chartE_end_date = None
        else:
            pass

    def disableButtons(self, buttons):
        for button in buttons:
            if not isinstance(button, type(None)):
                button.configure(state=tkinter.DISABLED)

    def enableButtons(self, buttons):
        for button in buttons:
            if not isinstance(button, type(None)):
                button.configure(state=tkinter.NORMAL)

    ##########################################################################
    # Switches

    def switchButtonsState(self):
        buttons = [self.A_filters_btn, self.A_details_btn, self.A_preview_btn, self.A_station_btn, self.A_employee_btn, self.A_date_btn, self.A_shift_btn, self.A_cycle_btn, self.A_part_number_btn, self.A_serial_number_btn, self.A_label, self.A_option_menu, self.A_label2, self.A_option_menu2,
                   self.B_filters_btn, self.B_details_btn, self.B_cdf_checkbtn, self.B_two_color_checkbtn, self.B_station_btn, self.B_date_btn, self.B_shift_btn, self.B_cycle_btn, self.B_part_number_btn, self.B_serial_number_btn, self.B_label, self.B_option_menu,
                   self.C_filters_btn, self.C_details_btn, self.C_station_btn, self.C_date_btn, self.C_shift_btn, self.C_cycle_btn, self.C_part_number_btn, self.C_serial_number_btn,
                   self.D_filters_btn, self.D_details_btn, self.D_station_btn, self.D_date_btn, self.D_shift_btn, self.D_cycle_btn, self.D_part_number_btn, self.D_serial_number_btn,
                   self.E_filters_btn, self.E_details_btn, self.E_station_btn, self.E_employee_btn, self.E_date_btn, self.E_shift_btn, self.E_cycle_btn, self.E_part_number_btn, self.E_serial_number_btn, self.E_label, self.E_option_menu]
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
            self.chartC_show_filters = not self.chartC_show_filters
            show_filters = self.chartC_show_filters
        elif chart_name == 'D':
            self.chartD_show_filters = not self.chartD_show_filters
            show_filters = self.chartD_show_filters
        elif chart_name == 'E':
            self.chartE_show_filters = not self.chartE_show_filters
            show_filters = self.chartE_show_filters
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

    def switchTwoColorMode(self, chart_name):
        if chart_name == 'B':
            self.B_two_color = not self.B_two_color
        self.drawChart(chart_name)

    def switchChartAAxisX(self):
        if self.A_axis_choice_var.get() != self.A_axis_choice_prev_var.get():
            self.A_axis_choice_prev_var.set(self.A_axis_choice_var.get())
            self.A_axis_choice_nmb = (self.A_axis_choice_nmb + 1) % 2
            if not self.is_loading:
                self.rwlFun(
                    self.drawChart,
                    'Wczytywanie wykresu...',
                    'Loading chart...',
                    'A',
                    False)

    def switchChartAMode(self):
        if self.A_mode_choice_var.get() != self.A_mode_choice_prev_var.get():
            self.A_mode_choice_prev_var.set(self.A_mode_choice_var.get())
            self.A_mode_choice_nmb = (self.A_mode_choice_nmb + 1) % 2
            if not self.is_loading:
                self.rwlFun(
                    self.drawChart,
                    'Wczytywanie wykresu...',
                    'Loading chart...',
                    'A',
                    False)

    def switchChartBMode(self):
        if self.B_axis_choice_var.get() != self.B_axis_choice_prev_var.get():
            self.B_axis_choice_prev_var.set(self.B_axis_choice_var.get())
            self.B_axis_choice_nmb = (self.B_axis_choice_nmb + 1) % 2
            if not self.is_loading:
                self.rwlFun(
                    self.drawChart,
                    'Wczytywanie wykresu...',
                    'Loading chart...',
                    'B',
                    False)

    def switchChartEMode(self):
        if self.E_mode_choice_var.get() != self.E_mode_choice_prev_var.get():
            self.E_mode_choice_prev_var.set(self.E_mode_choice_var.get())
            self.E_mode_choice_nmb = (self.E_mode_choice_nmb + 1) % 2
            if not self.is_loading:
                self.rwlFun(
                    self.drawChart,
                    'Wczytywanie wykresu...',
                    'Loading chart...',
                    'E',
                    False)

    ##########################################################################

    def drawChartA(self, chart_drawn=None):
        if not isinstance(chart_drawn, type(None)):
            self.chartA_drawn = chart_drawn

        if self.chartA_first_draw:
            self.A_station_selected = self.onesList(len(self.station))
            self.A_employee_selected = self.onesList(len(self.operator_name))
            self.A_date_selected = [0, len(self.date) - 1]
            self.A_shift_selected = self.onesList(len(self.shift))
            self.A_cycle_selected = self.onesList(len(self.cycle))
            self.A_part_number_selected = self.onesList(len(self.part_number))
            self.A_serial_number_selected = self.onesList(len(self.serial_number))
            self.chartA_first_draw = False

        if not self.chartA_drawn:
            self.A_stations = [self.station[i] for i in range(
                len(self.A_station_selected)) if self.A_station_selected[i] != 0]
            self.A_station_nmb = len(self.A_stations)
            self.A_employees = [self.operator_name[i] for i in range(
                len(self.A_employee_selected)) if self.A_employee_selected[i] != 0]
            self.A_employee_nmb = len(self.A_employees)
            self.A_dates = self.date[self.A_date_selected[0]
                :self.A_date_selected[1] + 1]
            self.A_shifts = [self.shift[i] for i in range(
                len(self.A_shift_selected)) if self.A_shift_selected[i] != 0]
            self.A_cycles = [self.cycle[i] for i in range(
                len(self.A_cycle_selected)) if self.A_cycle_selected[i] != 0]
            self.A_part_numbers = [self.part_number[i] for i in range(
                len(self.A_part_number_selected)) if self.A_part_number_selected[i] != 0]
            self.A_serial_numbers = [self.serial_number[i] for i in range(
                len(self.A_serial_number_selected)) if self.A_serial_number_selected[i] != 0]

            engines_data = self.getColumns(['Numer seryjny', 'Date', 'Stacja', 'Operator Name', 'Aktualny czas trwania [s]'], ['Serial Number', 'Date', 'Station', 'Operator Name', 'Actual duration [s]'], [10, 2, 1, 4, 6])[(self.getColumn('Date', 'Date', 2).isin(self.A_dates))
                                                                                                                                                                                                                              & (self.getColumn('Przesunięcie', 'Shift', 11).isin(self.A_shifts))
                                                                                                                                                                                                                              & (self.getColumn('Cycle', 'Cycle', 5).isin(self.A_cycles))
                                                                                                                                                                                                                              & (self.getColumn('Numer części', 'Part Number', 9).isin(self.A_part_numbers))
                                                                                                                                                                                                                              & (self.getColumn('Numer seryjny', 'Serial Number', 10).isin(self.A_serial_numbers))]

            engines_data = engines_data.sort_values(
                by=[engines_data.columns[0], engines_data.columns[1]]).values.tolist()

            engines_data_dict = {}
            prev_engine = ''
            for i in range(len(engines_data)):
                engine = engines_data[i][0]
                date = engines_data[i][1]
                station = engines_data[i][2]
                employee = engines_data[i][3]
                duration = engines_data[i][4]
                if engine != prev_engine:
                    engines_data_dict[engine] = ([], [], [], [])
                engines_data_dict[engine][0].append(date)
                engines_data_dict[engine][1].append(station)
                engines_data_dict[engine][2].append(employee)
                engines_data_dict[engine][3].append(duration)
                prev_engine = engine
            engines_data_dict_cpy = dict(engines_data_dict)

            for key, value in engines_data_dict_cpy.items():
                if len(value[0]) != len(
                        self.station) or not key in self.serial_number:
                    engines_data_dict.pop(key, None)

            if self.A_mode_choice_nmb == 1:
                if self.A_axis_choice_nmb == 0:
                    stations_data_dict = {}
                    for station in self.A_stations:
                        stations_data_dict[station] = ([], [], [])
                    for data in engines_data_dict.values():
                        dates = data[0]
                        durations = data[3]
                        for i in range(len(data[1])):
                            station = data[1][i]
                            if station in self.A_stations:
                                stations_data_dict[station][0].append(dates[i])
                                stations_data_dict[station][1].append(
                                    durations[i])
                                stations_data_dict[station][2].append(station)

                    stations_data_dict_cpy = dict(stations_data_dict)
                    for station, data in stations_data_dict_cpy.items():
                        stations_data_dict[station] = []
                        dates = data[0]
                        durations = data[1]
                        stations = data[2]
                        for i in range(len(dates)):
                            stations_data_dict[station].append(
                                [dates[i], durations[i], stations[i]])
                        stations_data_dict[station].sort(key=itemgetter(0))
                    chart_data_dict = dict(stations_data_dict)
                else:
                    employees_data_dict = {}
                    for employee in self.A_employees:
                        employees_data_dict[employee] = ([], [], [])
                    for data in engines_data_dict.values():
                        dates = data[0]
                        durations = data[3]
                        for i in range(len(data[2])):
                            employee = data[2][i]
                            if employee in self.A_employees:
                                employees_data_dict[employee][0].append(
                                    dates[i])
                                employees_data_dict[employee][1].append(
                                    durations[i])
                                employees_data_dict[employee][2].append(
                                    employee)

                    employees_data_dict_cpy = dict(employees_data_dict)
                    for employee, data in employees_data_dict_cpy.items():
                        employees_data_dict[employee] = []
                        dates = data[0]
                        durations = data[1]
                        employees = data[2]
                        for i in range(len(dates)):
                            employees_data_dict[employee].append(
                                [dates[i], durations[i], employees[i]])
                        employees_data_dict[employee].sort(key=itemgetter(0))
                    chart_data_dict = dict(employees_data_dict)
            else:
                if self.A_axis_choice_nmb == 0:
                    stations_data_dict = {}
                    for station in self.A_stations:
                        stations_data_dict[station] = ([], [], [])
                    for engine, data in engines_data_dict.items():
                        durations = []
                        dates = data[0]
                        for i in range(len(dates) - 1):
                            durations.append(
                                (dates[i + 1] - dates[i]) / np.timedelta64(1, 's'))
                        durations.append(data[3][-1])
                        for i in range(len(data[1])):
                            station = data[1][i]
                            if station in self.A_stations:
                                stations_data_dict[station][0].append(dates[i])
                                stations_data_dict[station][1].append(
                                    durations[i])
                                stations_data_dict[station][2].append(station)

                    stations_data_dict_cpy = dict(stations_data_dict)
                    for station, data in stations_data_dict_cpy.items():
                        stations_data_dict[station] = []
                        dates = data[0]
                        durations = data[1]
                        stations = data[2]
                        for i in range(len(dates)):
                            stations_data_dict[station].append(
                                [dates[i], durations[i], stations[i]])
                        stations_data_dict[station].sort(key=itemgetter(0))
                    chart_data_dict = dict(stations_data_dict)
                else:
                    employees_data_dict = {}
                    for employee in self.A_employees:
                        employees_data_dict[employee] = ([], [], [])
                    for engine, data in engines_data_dict.items():
                        durations = []
                        dates = data[0]
                        for i in range(len(dates) - 1):
                            durations.append(
                                (dates[i + 1] - dates[i]) / np.timedelta64(1, 's'))
                        durations.append(data[3][-1])
                        for i in range(len(data[2])):
                            employee = data[2][i]
                            if employee in self.A_employees:
                                employees_data_dict[employee][0].append(
                                    dates[i])
                                employees_data_dict[employee][1].append(
                                    durations[i])
                                employees_data_dict[employee][2].append(
                                    employee)

                    employees_data_dict_cpy = dict(employees_data_dict)
                    for employee, data in employees_data_dict_cpy.items():
                        employees_data_dict[employee] = []
                        dates = data[0]
                        durations = data[1]
                        employees = data[2]
                        for i in range(len(dates)):
                            employees_data_dict[employee].append(
                                [dates[i], durations[i], employees[i]])
                        employees_data_dict[employee].sort(key=itemgetter(0))
                    chart_data_dict = dict(employees_data_dict)

            first_date = None
            last_date = None
            for value in chart_data_dict.values():
                if len(value) > 0:
                    if isinstance(first_date, type(
                            None)) or value[0][0] < first_date:
                        first_date = value[0][0]
                    if isinstance(last_date, type(
                            None)) or value[-1][0] > last_date:
                        last_date = value[-1][0]

            self.A_dates_list = []
            self.A_avg_data_dict = {}
            current_date = first_date

            if not isinstance(current_date, type(None)):
                self.A_resolution = np.ceil(
                    (last_date -
                     first_date) /
                    np.timedelta64(
                        1,
                        's') /
                    Globals.chartA_bars_nmb)

                while current_date < last_date:
                    self.A_dates_list.append(current_date)
                    current_date += pd.Timedelta(seconds=self.A_resolution)
                self.A_dates_list.append(current_date)

                for key, value in chart_data_dict.items():
                    self.A_avg_data_dict[key] = []

                    for i in range(len(self.A_dates_list) - 1):
                        avg_dates = []
                        start = self.A_dates_list[i]
                        end = self.A_dates_list[i + 1]
                        for j in range(len(value)):
                            if value[j][0] >= start and value[j][0] < end:
                                avg_dates.append(value[j][1])
                        if len(avg_dates) > 0:
                            avg_date = sum(avg_dates) / len(avg_dates)
                        else:
                            avg_date = 0
                        self.A_avg_data_dict[key].append(
                            [self.A_dates_list[i], round(avg_date, 1), key])

            self.chartA_drawn = True

            ###############
            # Details data
            self.A_details_data = {}
            if self.A_axis_choice_nmb == 0:
                self.A_details_data[utils.setLabel(
                    self.language, 'Ilość stacji', 'Number of stations')] = self.A_station_nmb
                self.A_details_data[utils.setLabel(
                    self.language, 'Wybrane stacje', 'Selected stations')] = self.A_stations
            else:
                self.A_details_data[utils.setLabel(
                    self.language, 'Ilość pracowników', 'Number of employees')] = self.A_employee_nmb
                self.A_details_data[utils.setLabel(
                    self.language, 'Wybrani pracownicy', 'Selected employees')] = self.A_employees
            self.A_details_data[utils.setLabel(
                self.language, 'Data początkowa (z pliku)', 'Start date (from file)')] = self.date[0]
            self.A_details_data[utils.setLabel(
                self.language, 'Data końcowa (z pliku)', 'End date (from file)')] = self.date[-1]
            self.A_details_data[' '] = ''
            self.A_details_data[utils.setLabel(
                self.language, 'Wybrana data początkowa', 'Chosen start date')] = self.date[self.A_date_selected[0]] if isinstance(Globals.chartA_start_date, type(None)) else Globals.chartA_start_date
            self.A_details_data[utils.setLabel(
                self.language, 'Wybrana data końcowa', 'Chosen end date')] = self.date[self.A_date_selected[1]] if isinstance(Globals.chartA_end_date, type(None)) else Globals.chartA_end_date
            self.A_details_data['  '] = ''
            self.A_details_data[utils.setLabel(
                self.language, 'Wybrane zmiany', 'Selected shifts')] = self.A_shifts
            self.A_details_data[utils.setLabel(
                self.language, 'Wybrane cykle', 'Selected cycles')] = self.A_cycles
            self.A_details_data[utils.setLabel(
                self.language, 'Wybrane numery części', 'Selected part numbers')] = self.A_part_numbers
            self.A_details_data[utils.setLabel(self.language,
                                               'Rozdzielczość słupków na wykresie [s]',
                                               'Bars resolution on the chart [s]')] = self.A_resolution
            self.A_details_data['   '] = ''
            self.A_details_data[utils.setLabel(
                self.language, 'Całkowita ilość silników', 'Total number of engines')] = self.serial_number_nmb
            self.A_details_data[utils.setLabel(
                self.language, 'Silniki z brakującymi danymi', 'Engines with missing data')] = self.wrong_transition_count
            self.A_details_data[utils.setLabel(self.language, 'Silniki z poprawnymi danymi',
                                               'Engines with valid data')] = self.serial_number_nmb - self.wrong_transition_count
            self.A_details_data['    '] = ''
            self.A_details_data[utils.setLabel(self.language,
                                               'Ilość wybranych silników',
                                               'Number of selected engines')] = len(engines_data_dict)
            if len(engines_data_dict.keys()) <= 20:
                self.A_details_data[utils.setLabel(self.language,
                                                    'Wybrane silniki',
                                                    'Selected engines')] = [i for i in engines_data_dict.keys()]                                                    
            ###############

            self.A_axis_choice_list = [
                utils.setLabel(
                    self.language, 'Stacje', 'Stations'), utils.setLabel(
                    self.language, 'Pracownicy', 'Employees')]
            self.A_label['text'] = utils.setLabel(
                self.language, 'Oś X:', 'X Axis:')
            self.A_mode_choice_list = [
                utils.setLabel(
                    self.language,
                    'Czas przejścia',
                    'Transition time'),
                utils.setLabel(
                    self.language,
                    'Czas operacji',
                    'Operation time')]
            self.A_label2['text'] = utils.setLabel(
                self.language, 'Oś Z:', 'Z Axis:')

            self.A_axis_choice_var.trace_vdelete(
                'w', self.A_axis_choice_var.trace_id)
            self.A_axis_choice_var.set(
                self.A_axis_choice_list[self.A_axis_choice_nmb])
            self.A_axis_choice_prev_var.set(
                self.A_axis_choice_list[self.A_axis_choice_nmb])
            self.A_axis_choice_var.trace_id = self.A_axis_choice_var.trace(
                'w', lambda *args: self.switchChartAAxisX())

            self.A_mode_choice_var.trace_vdelete(
                'w', self.A_mode_choice_var.trace_id)
            self.A_mode_choice_var.set(
                self.A_mode_choice_list[self.A_mode_choice_nmb])
            self.A_mode_choice_prev_var.set(
                self.A_mode_choice_list[self.A_mode_choice_nmb])
            self.A_mode_choice_var.trace_id = self.A_mode_choice_var.trace(
                'w', lambda *args: self.switchChartAMode())

            menu = self.A_option_menu['menu']
            menu.delete(0, 'end')
            for s in self.A_axis_choice_list:
                menu.add_radiobutton(label=s, variable=self.A_axis_choice_var)

            menu = self.A_option_menu2['menu']
            menu.delete(0, 'end')
            for s in self.A_mode_choice_list:
                menu.add_radiobutton(label=s, variable=self.A_mode_choice_var)

        #######################################################################

        self.clearFrame('A')
        self.A_options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        self.A_filters_frame.place(
            relx=0, rely=0.05, relwidth=0.7, relheight=0.05)
        self.buttons_frame.place(
            relx=0.7,
            rely=0.05,
            relwidth=0.3,
            relheight=0.05)
        if self.chartA_show_filters:
            self.A_chart_frame.place(
                relx=0, rely=0.1, relwidth=1, relheight=0.90)
        else:
            self.A_chart_frame.place(
                relx=0, rely=0.05, relwidth=1, relheight=0.95)

        if self.chartA_show_filters:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25b2', u'Filters \u25b2')
        else:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25bc', u'Filters \u25bc')
        buttons_state = tkinter.DISABLED if self.is_loading else tkinter.NORMAL

        self.A_label.pack(side=tkinter.LEFT)
        self.A_option_menu.pack(side=tkinter.LEFT)
        self.A_label2.pack(side=tkinter.LEFT, padx=(15, 0))
        self.A_option_menu2.pack(side=tkinter.LEFT)

        self.A_filters_btn['text'] = filters_btn_text
        self.A_details_btn['text'] = utils.setLabel(
            self.language, 'Szczegóły', 'Details')
        self.A_preview_btn['text'] = utils.setLabel(
            self.language, 'Podgląd', 'Preview')
        self.A_station_btn['text'] = utils.setLabel(
            self.language, 'Stacja', 'Station')
        self.A_employee_btn['text'] = utils.setLabel(
            self.language, 'Pracownik', 'Employee')
        self.A_date_btn['text'] = utils.setLabel(self.language, 'Data', 'Date')
        self.A_shift_btn['text'] = utils.setLabel(
            self.language, 'Zmiana', 'Shift')
        self.A_cycle_btn['text'] = utils.setLabel(
            self.language, 'Cykl', 'Cycle')
        self.A_part_number_btn['text'] = utils.setLabel(
            self.language, 'Numer części', 'Part number')
        self.A_serial_number_btn['text'] = utils.setLabel(
            self.language, 'Numer seryjny', 'Serial number')

        self.A_filters_btn['state'] = buttons_state
        self.A_details_btn['state'] = buttons_state
        self.A_preview_btn['state'] = buttons_state
        self.A_station_btn['state'] = buttons_state
        self.A_employee_btn['state'] = buttons_state
        self.A_date_btn['state'] = buttons_state
        self.A_shift_btn['state'] = buttons_state
        self.A_cycle_btn['state'] = buttons_state
        self.A_part_number_btn['state'] = buttons_state
        self.A_serial_number_btn['state'] = buttons_state

        if self.A_axis_choice_nmb == 0:
            self.A_station_btn.pack(side=tkinter.LEFT, padx=15)
        else:
            self.A_employee_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_date_btn.pack(side=tkinter.LEFT)
        self.A_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_cycle_btn.pack(side=tkinter.LEFT)
        self.A_part_number_btn.pack(side=tkinter.LEFT, padx=15)
        self.A_serial_number_btn.pack(side=tkinter.LEFT, padx=(0, 15))
        self.A_sep.pack(side=tkinter.LEFT, fill=tkinter.Y)

        #######################################################################

        self.A_figure.clear()

        ax = self.A_figure.add_subplot(111, projection='3d')

        X_labels = list(self.A_avg_data_dict.keys())
        Y_labels = [str(d) for d in self.A_dates_list[:-1]]

        if len(Y_labels) <= 17:
            Y_labels_chosen_nmb = list(range(len(Y_labels)))
        elif len(Y_labels) > 17:
            nmb_of_internal_labels = 7
            step = int(len(Y_labels) / (nmb_of_internal_labels + 1))

            Y_labels_chosen_nmb = [0]
            i = 1
            while i * step < len(Y_labels) - 1:
                Y_labels_chosen_nmb.append(i * step)
                i += 1
            Y_labels_chosen_nmb.append(len(Y_labels) - 1)

        Y_labels_chosen = [Y_labels[i] for i in Y_labels_chosen_nmb]

        for i in range(len(Y_labels_chosen)):
            if len(Y_labels_chosen[i].split('-')[0]) == 4:
                Y_labels_chosen[i] = Y_labels_chosen[i][5:]

        _X = np.arange(0, len(X_labels), 1)
        _Y = np.arange(0, len(Y_labels), 1)
        _XX, _YY = np.meshgrid(_X, _Y)
        X, Y = _XX.ravel(), _YY.ravel()

        Z = []
        X_cleared = []
        Y_cleared = []

        j = 0
        for i in range(len(Y_labels)):
            for value in self.A_avg_data_dict.values():
                if value[i][1] > 0.0:
                    X_cleared.append(X[j])
                    Y_cleared.append(Y[j])
                    Z.append(value[i][1])
                j += 1

        if len(X) > 0 and len(Y) > 0 and len(Z) > 0:
            self.A_poly3d = ax.bar3d(
                X_cleared, Y_cleared, np.zeros_like(Z), 0.9, 1, Z, shade=True, color=Globals.primary_color)
            self.A_poly3d._facecolors2d = self.A_poly3d._facecolor3d
            self.A_poly3d._edgecolors2d = self.A_poly3d._edgecolor3d

            ax.set_xticks(np.arange(0.5, len(X_labels), 1))
            ax.set_xticklabels(X_labels, rotation=90)

            ax.set_yticks(Y_labels_chosen_nmb)
            ax.set_yticklabels(Y_labels_chosen, rotation=90)

            if self.A_axis_choice_nmb == 0:
                ax.set_xlabel(
                    utils.setLabel(
                        self.language,
                        '\n\n\n\n\nStacje',
                        '\n\n\n\n\nStations'))
            else:
                ax.set_xlabel(utils.setLabel(
                    self.language, '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nPracownicy', '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nEmployees'))
            ax.set_ylabel(
                utils.setLabel(
                    self.language,
                    '\n\n\n\n\n\n\n\n\n\n\n\n\nData',
                    '\n\n\n\n\n\n\n\n\n\n\n\n\nDate'))
            ax.set_zlabel(self.A_mode_choice_list[self.A_mode_choice_nmb] + ' [s]')
        else:
            ax.set_xticks([])
            ax.set_xticklabels([])
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_zticks([])
            ax.set_zticklabels([])

            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_zlabel('')

        ax.set_box_aspect((2, 2, 1), zoom=1.2)
        ax.set_title(utils.setLabel(self.language, 'Wykres 3D',
                                    '3D Chart'), pad=15, weight='bold')
        self.A_figure.text(0.99, 0.02, utils.setLabel(self.language, 'LPM - obrót\nŚPM - przesunięcie\nPPM - przybliżenie/oddalenie',
                           'LMB - rotate\nMMB - move\nRMB - zoom in/out'), horizontalalignment='right')

        self.A_canvas.draw()

        self.A_chart_data = {}
        self.A_chart_data['X'] = X_cleared
        self.A_chart_data['Y'] = Y_cleared
        self.A_chart_data['Z'] = Z
        self.A_chart_data['X_labels'] = X_labels
        self.A_chart_data['Y_labels'] = Y_labels_chosen
        self.A_chart_data['Y_labels_nmb'] = Y_labels_chosen_nmb
        self.A_chart_data['xlabel'] = utils.setLabel(
            self.language,
            '\n\n\n\n\nStacje',
            '\n\n\n\n\nStations') if self.A_axis_choice_nmb == 0 else utils.setLabel(
            self.language,
            '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nPracownicy',
            '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nEmployees')
        self.A_chart_data['ylabel'] = utils.setLabel(
            self.language,
            '\n\n\n\n\n\n\n\n\n\n\n\n\nData',
            '\n\n\n\n\n\n\n\n\n\n\n\n\nDate')
        self.A_chart_data['zlabel'] = self.A_mode_choice_list[self.A_mode_choice_nmb] + ' [s]'

    def drawChartB(self, chart_drawn=None):
        if not isinstance(chart_drawn, type(None)):
            self.chartB_drawn = chart_drawn

        if self.chartB_first_draw:
            self.B_station_selected = [0, len(self.station) - 1]
            self.B_date_selected = [0, len(self.date) - 1]
            self.B_shift_selected = self.onesList(len(self.shift))
            self.B_cycle_selected = self.onesList(len(self.cycle))
            self.B_part_number_selected = self.onesList(len(self.part_number))
            self.B_serial_number_selected = self.onesList(len(self.serial_number))
            self.chartB_first_draw = False

        if not self.chartB_drawn:
            self.B_engines_nmb = [0 for _ in range(Globals.bars_nmb)]
            self.B_transition_time = ['' for _ in range(Globals.bars_nmb)]

            self.B_station_nmb = self.B_station_selected[1] - \
                self.B_station_selected[0] + 1
            self.B_stations = self.station[self.B_station_selected[0]                                           :self.B_station_selected[1] + 1]
            self.B_dates = self.date[self.B_date_selected[0]                                     :self.B_date_selected[1] + 1]
            self.B_shifts = [self.shift[i] for i in range(
                len(self.B_shift_selected)) if self.B_shift_selected[i] != 0]
            self.B_cycles = [self.cycle[i] for i in range(
                len(self.B_cycle_selected)) if self.B_cycle_selected[i] != 0]
            self.B_part_numbers = [self.part_number[i] for i in range(
                len(self.B_part_number_selected)) if self.B_part_number_selected[i] != 0]
            self.B_serial_numbers = [self.serial_number[i] for i in range(
                len(self.B_serial_number_selected)) if self.B_serial_number_selected[i] != 0]

            engines_data = self.getColumns(['Numer seryjny', 'Date', 'Aktualny czas trwania [s]'], ['Serial Number', 'Date', 'Actual duration [s]'], [10, 2, 6])[(self.getColumn('Date', 'Date', 2).isin(self.B_dates))
                                                                                                                                                                 & (self.getColumn('Przesunięcie', 'Shift', 11).isin(self.B_shifts))
                                                                                                                                                                 & (self.getColumn('Cycle', 'Cycle', 5).isin(self.B_cycles))
                                                                                                                                                                 & (self.getColumn('Numer części', 'Part Number', 9).isin(self.B_part_numbers))
                                                                                                                                                                 & (self.getColumn('Numer seryjny', 'Serial Number', 10).isin(self.B_serial_numbers))]
            engines_data = engines_data.sort_values(
                by=[engines_data.columns[0], engines_data.columns[1]]).values.tolist()

            engines_data_dict = {}
            prev_engine = ''
            for i in range(len(engines_data)):
                engine = engines_data[i][0]
                date = engines_data[i][1]
                duration = engines_data[i][2]
                if engine != prev_engine:
                    engines_data_dict[engine] = ([], [])
                engines_data_dict[engine][0].append(date)
                engines_data_dict[engine][1].append(duration)
                prev_engine = engine
            engines_data_dict_cpy = dict(engines_data_dict)

            for key, value in engines_data_dict_cpy.items():
                if len(value[0]) != len(
                        self.station) or not key in self.serial_number:
                    engines_data_dict.pop(key, None)

            time_elapsed = {}
            for engine, engine_data in engines_data_dict.items():
                if self.B_station_nmb > 1:
                    engine_date = [engine_data[0][i] for i in range(
                        len(engine_data[0])) if self.station[i] in self.B_stations]
                    delta_time = np.float64([engine_data[1][i] for i in range(
                        len(engine_data[1])) if self.station[i] in self.B_stations][-1])
                    time_elapsed[engine] = (
                        np.max(engine_date) - np.min(engine_date)) / np.timedelta64(1, 's') + delta_time
                elif self.B_station_nmb == 1:
                    if self.B_axis_choice_nmb == 0:
                        if self.B_stations[0] != self.station[-1]:
                            current_stations = [
                                self.B_stations[0]] + [self.station[self.B_station_selected[0] + 1]]
                            engine_date = [engine_data[0][i] for i in range(
                                len(engine_data[0])) if self.station[i] in current_stations]
                            time_elapsed[engine] = (
                                np.max(engine_date) - np.min(engine_date)) / np.timedelta64(1, 's')
                        else:
                            time_elapsed[engine] = np.float64([engine_data[1][i] for i in range(
                                len(engine_data[1])) if self.station[i] in self.B_stations][-1])
                    elif self.B_axis_choice_nmb == 1:
                        time_elapsed[engine] = np.float64([engine_data[1][i] for i in range(
                            len(engine_data[1])) if self.station[i] in self.B_stations][-1])
            time_elapsed_cpy = dict(time_elapsed)

            if self.B_station_nmb == 1 and self.B_axis_choice_nmb == 1:
                time_expected = Globals.operation_expected_time
            else:
                time_expected = Globals.transition_expected_time

            for i in range(Globals.bars_nmb - 1):
                m, s = divmod(self.B_station_nmb * time_expected + i * Globals.bars_resolution -
                              (self.B_station_nmb // 3) * Globals.bars_resolution, 60)
                self.B_transition_time[i] = f'{m:02d}:{s:02d}'
                for key, value in time_elapsed.items():
                    if value <= self.B_station_nmb * time_expected + i * Globals.bars_resolution - \
                            (self.B_station_nmb // 3) * Globals.bars_resolution and key in time_elapsed_cpy:
                        self.B_engines_nmb[i] += 1
                        time_elapsed_cpy.pop(key, 'None')
            self.B_engines_nmb[-1] = len(time_elapsed_cpy.keys())
            self.cdf_data = self.getCDF(self.B_engines_nmb)
            self.chartB_drawn = True

            ###############
            # Details data
            self.B_details_data = {}
            self.B_details_data[utils.setLabel(
                self.language, 'Ilość stacji', 'Number of stations')] = self.B_station_nmb
            self.B_details_data[utils.setLabel(
                self.language, 'Wybrane stacje', 'Selected stations')] = self.B_stations
            self.B_details_data[utils.setLabel(
                self.language, 'Data początkowa (z pliku)', 'Start date (from file)')] = self.date[0]
            self.B_details_data[utils.setLabel(
                self.language, 'Data końcowa (z pliku)', 'End date (from file)')] = self.date[-1]
            self.B_details_data[''] = ''
            self.B_details_data[utils.setLabel(
                self.language, 'Wybrana data początkowa', 'Chosen start date')] = self.date[self.B_date_selected[0]] if isinstance(Globals.chartB_start_date, type(None)) else Globals.chartB_start_date
            self.B_details_data[utils.setLabel(
                self.language, 'Wybrana data końcowa', 'Chosen end date')] = self.date[self.B_date_selected[1]] if isinstance(Globals.chartB_end_date, type(None)) else Globals.chartB_end_date
            self.B_details_data[' '] = ''
            self.B_details_data[utils.setLabel(
                self.language, 'Wybrane zmiany', 'Selected shifts')] = self.B_shifts
            self.B_details_data[utils.setLabel(
                self.language, 'Wybrane cykle', 'Selected cycles')] = self.B_cycles
            self.B_details_data[utils.setLabel(
                self.language, 'Wybrane numery części', 'Selected part numbers')] = self.B_part_numbers
            self.B_details_data[utils.setLabel(
                self.language, 'Całkowita ilość silników', 'Total number of engines')] = self.serial_number_nmb
            self.B_details_data[utils.setLabel(
                self.language, 'Silniki z brakującymi danymi', 'Engines with missing data')] = self.wrong_transition_count
            self.B_details_data[utils.setLabel(self.language, 'Silniki z poprawnymi danymi',
                                               'Engines with valid data')] = self.serial_number_nmb - self.wrong_transition_count
            self.B_details_data['  '] = ''
            self.B_details_data[utils.setLabel(
                self.language, 'Ilość wybranych silników', 'Number of selected engines')] = len(engines_data_dict)
            if len(engines_data_dict.keys()) <= 20:
                self.B_details_data[utils.setLabel(self.language,
                                                    'Wybrane silniki',
                                                    'Selected engines')] = [i for i in engines_data_dict.keys()]
            ###############

            self.B_axis_choice_list = [
                utils.setLabel(
                    self.language,
                    'Czas przejścia',
                    'Transition time'),
                utils.setLabel(
                    self.language,
                    'Czas operacji',
                    'Operation time')]
            self.B_label['text'] = utils.setLabel(
                self.language, 'Tryb:', 'Mode:')

            self.B_axis_choice_var.trace_vdelete(
                'w', self.B_axis_choice_var.trace_id)
            self.B_axis_choice_var.set(
                self.B_axis_choice_list[self.B_axis_choice_nmb])
            self.B_axis_choice_prev_var.set(
                self.B_axis_choice_list[self.B_axis_choice_nmb])
            self.B_axis_choice_var.trace_id = self.B_axis_choice_var.trace(
                'w', lambda *args: self.switchChartBMode())

            menu = self.B_option_menu['menu']
            menu.delete(0, 'end')
            for s in self.B_axis_choice_list:
                menu.add_radiobutton(label=s, variable=self.B_axis_choice_var)

        self.B_transition_time[-1] = utils.setLabel(
            self.language, 'Więcej', 'More')
        self.B_engines_nmb_str = utils.setLabel(
            self.language, 'Liczba silników', 'Number of engines')
        if self.B_station_nmb == 1 and self.B_axis_choice_nmb == 1:
            self.B_transition_time_str = utils.setLabel(
                self.language, 'Czas operacji', 'Operation time')
        else:
            self.B_transition_time_str = utils.setLabel(
                self.language, 'Czas przejścia', 'Transition time')
        self.B_cdf_str = utils.setLabel(self.language, 'Dystrybuanta', 'CDF')
        self.B_expected_time_str = utils.setLabel(
            self.language, 'Czas projektowy', 'Expected time')

        #######################################################################

        self.clearFrame('B')
        self.B_options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        self.B_filters_frame.place(
            relx=0, rely=0.05, relwidth=0.7, relheight=0.05)
        self.buttons_frame.place(
            relx=0.7,
            rely=0.05,
            relwidth=0.3,
            relheight=0.05)
        if self.chartB_show_filters:
            self.B_chart_frame.place(
                relx=0, rely=0.1, relwidth=1, relheight=0.90)
        else:
            self.B_chart_frame.place(
                relx=0, rely=0.05, relwidth=1, relheight=0.95)

        if self.chartB_show_filters:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25b2', u'Filters \u25b2')
        else:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25bc', u'Filters \u25bc')
        buttons_state = tkinter.DISABLED if self.is_loading else tkinter.NORMAL

        if self.B_station_nmb == 1:
            self.B_label.pack(side=tkinter.LEFT, padx=(15, 0))
            self.B_option_menu.pack(side=tkinter.LEFT)

        self.B_filters_btn['text'] = filters_btn_text
        self.B_details_btn['text'] = utils.setLabel(
            self.language, 'Szczegóły', 'Details')
        self.B_cdf_checkbtn['text'] = utils.setLabel(
            self.language, 'Pokaż dystrybuantę', 'Show CDF')
        self.B_two_color_checkbtn['text'] = utils.setLabel(self.language, 'Tryb dwukolorowy', 'Two-color mode')
        self.B_station_btn['text'] = utils.setLabel(
            self.language, 'Stacja', 'Station')
        self.B_date_btn['text'] = utils.setLabel(self.language, 'Data', 'Date')
        self.B_shift_btn['text'] = utils.setLabel(
            self.language, 'Zmiana', 'Shift')
        self.B_cycle_btn['text'] = utils.setLabel(
            self.language, 'Cykl', 'Cycle')
        self.B_part_number_btn['text'] = utils.setLabel(
            self.language, 'Numer części', 'Part number')
        self.B_serial_number_btn['text'] = utils.setLabel(
            self.language, 'Numer seryjny', 'Serial number')

        self.B_filters_btn['state'] = buttons_state
        self.B_details_btn['state'] = buttons_state
        self.B_cdf_checkbtn['state'] = buttons_state
        self.B_two_color_checkbtn['state'] = buttons_state
        self.B_station_btn['state'] = buttons_state
        self.B_date_btn['state'] = buttons_state
        self.B_shift_btn['state'] = buttons_state
        self.B_cycle_btn['state'] = buttons_state
        self.B_part_number_btn['state'] = buttons_state
        self.B_serial_number_btn['state'] = buttons_state

        #######################################################################

        self.B_figure.clear()

        self.B_figure.set_tight_layout(True)
        ax1 = self.B_figure.add_subplot(111)

        hist = ax1.bar(self.B_transition_time,
                       self.B_engines_nmb, align='edge', width=-0.8, edgecolor='k', color=Globals.primary_color)
        expected_time = ax1.axvline(x=self.B_station_nmb // 3, color='grey')
        if self.B_station_nmb == 1 and self.B_axis_choice_nmb == 1:
            ax1.set_title(
                utils.setLabel(
                    self.language,
                    'Histogram czasu operacji',
                    'Operation time histogram'),
                pad=15,
                weight='bold')
        else:
            ax1.set_title(
                utils.setLabel(
                    self.language,
                    'Histogram czasu przejścia',
                    'Transition time histogram'),
                pad=15,
                weight='bold')
        ax1.tick_params(labelrotation=90)
        ax1.set_xlabel(self.B_transition_time_str)
        if self.B_details_data[utils.setLabel(
                self.language, 'Ilość wybranych silników', 'Number of selected engines')] == 0:
            ax1.yaxis.set_major_formatter(mtick.NullFormatter())

        if self.B_two_color:
            for bar, i in zip(ax1.patches, range(len(ax1.patches))):
                if i % 2 == 1:
                    bar.set_facecolor(Globals.secondary_color)

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
            legend_handles = [hist, cdf[0], expected_time]
            legend_labels = [self.B_engines_nmb_str,
                             self.B_cdf_str, self.B_expected_time_str]
        else:
            legend_handles = [hist, expected_time]
            legend_labels = [self.B_engines_nmb_str, self.B_expected_time_str]
        ax1.legend(legend_handles, legend_labels, bbox_to_anchor=(
            1, 0.92 + 0.02 * len(legend_handles)))

        self.B_canvas.draw()

    def drawChartC(self, chart_drawn=None):
        if not isinstance(chart_drawn, type(None)):
            self.chartC_drawn = chart_drawn

        if self.chartC_first_draw:
            self.C_station_selected = self.onesList(len(self.station))
            self.C_date_selected = [0, len(self.date) - 1]
            self.C_shift_selected = self.onesList(len(self.shift))
            self.C_cycle_selected = self.onesList(len(self.cycle))
            self.C_part_number_selected = self.onesList(len(self.part_number))
            self.C_serial_number_selected = self.onesList(len(self.serial_number))
            self.chartC_first_draw = False

        if not self.chartC_drawn:
            self.C_stations = [self.station[i] for i in range(
                len(self.C_station_selected)) if self.C_station_selected[i] != 0]
            self.C_station_nmb = len(self.C_stations)
            self.C_dates = self.date[self.C_date_selected[0]                                     :self.C_date_selected[1] + 1]
            self.C_shifts = [self.shift[i] for i in range(
                len(self.C_shift_selected)) if self.C_shift_selected[i] != 0]
            self.C_cycles = [self.cycle[i] for i in range(
                len(self.C_cycle_selected)) if self.C_cycle_selected[i] != 0]
            self.C_part_numbers = [self.part_number[i] for i in range(
                len(self.C_part_number_selected)) if self.C_part_number_selected[i] != 0]
            self.C_serial_numbers = [self.serial_number[i] for i in range(
                len(self.C_serial_number_selected)) if self.C_serial_number_selected[i] != 0]

            self.C_engines_ok_percentage = [
                0 for _ in range(self.C_station_nmb)]

            engines_data = self.getColumns(['Numer seryjny', 'Date', 'Aktualny czas trwania [s]'], ['Serial Number', 'Date', 'Actual duration [s]'], [10, 2, 6])[(self.getColumn('Date', 'Date', 2).isin(self.C_dates))
                                                                                                                                                                 & (self.getColumn('Przesunięcie', 'Shift', 11).isin(self.C_shifts))
                                                                                                                                                                 & (self.getColumn('Cycle', 'Cycle', 5).isin(self.C_cycles))
                                                                                                                                                                 & (self.getColumn('Numer części', 'Part Number', 9).isin(self.C_part_numbers))
                                                                                                                                                                 & (self.getColumn('Numer seryjny', 'Serial Number', 10).isin(self.C_serial_numbers))]
            engines_data = engines_data.sort_values(
                by=[engines_data.columns[0], engines_data.columns[1]]).values.tolist()

            engines_data_dict = {}
            prev_engine = ''
            for i in range(len(engines_data)):
                engine = engines_data[i][0]
                duration = engines_data[i][2]
                if engine != prev_engine:
                    engines_data_dict[engine] = []
                engines_data_dict[engine].append(duration)
                prev_engine = engine
            engines_data_dict_cpy = dict(engines_data_dict)

            for key, value in engines_data_dict_cpy.items():
                if len(value) != len(
                        self.station) or not key in self.serial_number:
                    engines_data_dict.pop(key, None)

            delta_time = {}
            for engine, engine_duration in engines_data_dict.items():
                delta_time[engine] = [engine_duration[i] for i in range(
                    len(engine_duration)) if self.station[i] in self.C_stations]

            if len(engines_data_dict) > 0:
                for i in range(self.C_station_nmb):
                    for engine in engines_data_dict.keys():
                        if delta_time[engine][i] <= Globals.operation_expected_time:
                            self.C_engines_ok_percentage[i] += 1
                    self.C_engines_ok_percentage[i] = round((
                        self.C_engines_ok_percentage[i] / len(engines_data_dict)) * 100, 2)

            self.chartC_drawn = True

            ###############
            # Details data
            self.C_details_data = {}
            self.C_details_data[utils.setLabel(
                self.language, 'Ilość stacji', 'Number of stations')] = self.C_station_nmb
            self.C_details_data[utils.setLabel(
                self.language, 'Wybrane stacje', 'Selected stations')] = self.C_stations
            self.C_details_data[utils.setLabel(
                self.language, 'Data początkowa (z pliku)', 'Start date (from file)')] = self.date[0]
            self.C_details_data[utils.setLabel(
                self.language, 'Data końcowa (z pliku)', 'End date (from file)')] = self.date[-1]
            self.C_details_data[''] = ''
            self.C_details_data[utils.setLabel(
                self.language, 'Wybrana data początkowa', 'Chosen start date')] = self.date[self.C_date_selected[0]] if isinstance(Globals.chartC_start_date, type(None)) else Globals.chartC_start_date
            self.C_details_data[utils.setLabel(
                self.language, 'Wybrana data końcowa', 'Chosen end date')] = self.date[self.C_date_selected[1]] if isinstance(Globals.chartC_end_date, type(None)) else Globals.chartC_end_date
            self.C_details_data[' '] = ''
            self.C_details_data[utils.setLabel(
                self.language, 'Wybrane zmiany', 'Selected shifts')] = self.C_shifts
            self.C_details_data[utils.setLabel(
                self.language, 'Wybrane cykle', 'Selected cycles')] = self.C_cycles
            self.C_details_data[utils.setLabel(
                self.language, 'Wybrane numery części', 'Selected part numbers')] = self.C_part_numbers
            self.C_details_data[utils.setLabel(
                self.language, 'Całkowita ilość silników', 'Total number of engines')] = self.serial_number_nmb
            self.C_details_data[utils.setLabel(
                self.language, 'Silniki z brakującymi danymi', 'Engines with missing data')] = self.wrong_transition_count
            self.C_details_data[utils.setLabel(self.language, 'Silniki z poprawnymi danymi',
                                               'Engines with valid data')] = self.serial_number_nmb - self.wrong_transition_count
            self.C_details_data['  '] = ''
            self.C_details_data[utils.setLabel(
                self.language, 'Ilość wybranych silników', 'Number of selected engines')] = len(engines_data_dict)
            if len(engines_data_dict.keys()) <= 20:
                self.C_details_data[utils.setLabel(self.language,
                                                    'Wybrane silniki',
                                                    'Selected engines')] = [i for i in engines_data_dict.keys()]
            ###############

        self.C_station_str = utils.setLabel(
            self.language, 'Stacje', 'Stations')

        #######################################################################

        self.clearFrame('C')
        self.C_options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        self.C_filters_frame.place(
            relx=0, rely=0.05, relwidth=0.7, relheight=0.05)
        self.buttons_frame.place(
            relx=0.7,
            rely=0.05,
            relwidth=0.3,
            relheight=0.05)
        if self.chartC_show_filters:
            self.C_chart_frame.place(
                relx=0, rely=0.1, relwidth=1, relheight=0.90)
        else:
            self.C_chart_frame.place(
                relx=0, rely=0.05, relwidth=1, relheight=0.95)

        if self.chartC_show_filters:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25b2', u'Filters \u25b2')
        else:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25bc', u'Filters \u25bc')
        buttons_state = tkinter.DISABLED if self.is_loading else tkinter.NORMAL

        self.C_filters_btn['text'] = filters_btn_text
        self.C_details_btn['text'] = utils.setLabel(
            self.language, 'Szczegóły', 'Details')
        self.C_station_btn['text'] = utils.setLabel(
            self.language, 'Stacja', 'Station')
        self.C_date_btn['text'] = utils.setLabel(self.language, 'Data', 'Date')
        self.C_shift_btn['text'] = utils.setLabel(
            self.language, 'Zmiana', 'Shift')
        self.C_cycle_btn['text'] = utils.setLabel(
            self.language, 'Cykl', 'Cycle')
        self.C_part_number_btn['text'] = utils.setLabel(
            self.language, 'Numer części', 'Part number')
        self.C_serial_number_btn['text'] = utils.setLabel(
            self.language, 'Numer seryjny', 'Serial number')

        self.C_filters_btn['state'] = buttons_state
        self.C_details_btn['state'] = buttons_state
        self.C_station_btn['state'] = buttons_state
        self.C_date_btn['state'] = buttons_state
        self.C_shift_btn['state'] = buttons_state
        self.C_cycle_btn['state'] = buttons_state
        self.C_part_number_btn['state'] = buttons_state
        self.C_serial_number_btn['state'] = buttons_state

        #######################################################################

        self.C_figure.clear()

        self.C_figure.set_tight_layout(True)
        ax = self.C_figure.add_subplot(111)

        ax.bar(self.C_stations, self.C_engines_ok_percentage, width=0.8, edgecolor='k', color=Globals.primary_color)
        ax.set_title(utils.setLabel(self.language, f'Procentowy udział silników z czasem OPERACJI \u2264 {Globals.operation_expected_time}s dla poszczególnych stacji',
                     f'Percentage of engines with OPERATION time \u2264 {Globals.operation_expected_time}s grouped by stations'), pad=15, weight='bold')
        ax.set_xlabel(self.C_station_str)
        ax.set_ylim(0, 105)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        for bar, label in zip(ax.patches, self.C_engines_ok_percentage):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    str(round(label, 2)) + '%', weight='semibold', ha='center', va='bottom')

        self.C_canvas.draw()

    def drawChartD(self, chart_drawn=None):
        if not isinstance(chart_drawn, type(None)):
            self.chartD_drawn = chart_drawn

        if self.chartD_first_draw:
            self.D_station_selected = self.onesList(len(self.station))
            self.D_date_selected = [0, len(self.date) - 1]
            self.D_shift_selected = self.onesList(len(self.shift))
            self.D_cycle_selected = self.onesList(len(self.cycle))
            self.D_part_number_selected = self.onesList(len(self.part_number))
            self.D_serial_number_selected = self.onesList(len(self.serial_number))
            self.chartD_first_draw = False

        if not self.chartD_drawn:
            self.D_stations = [self.station[i] for i in range(
                len(self.D_station_selected)) if self.D_station_selected[i] != 0]
            self.D_station_nmb = len(self.D_stations)
            self.D_dates = self.date[self.D_date_selected[0]                                     :self.D_date_selected[1] + 1]
            self.D_shifts = [self.shift[i] for i in range(
                len(self.D_shift_selected)) if self.D_shift_selected[i] != 0]
            self.D_cycles = [self.cycle[i] for i in range(
                len(self.D_cycle_selected)) if self.D_cycle_selected[i] != 0]
            self.D_part_numbers = [self.part_number[i] for i in range(
                len(self.D_part_number_selected)) if self.D_part_number_selected[i] != 0]
            self.D_serial_numbers = [self.serial_number[i] for i in range(
                len(self.D_serial_number_selected)) if self.D_serial_number_selected[i] != 0]

            self.D_engines_ok_percentage = [
                0 for _ in range(self.D_station_nmb)]

            engines_data = self.getColumns(['Numer seryjny', 'Date', 'Aktualny czas trwania [s]'], ['Serial Number', 'Date', 'Actual duration [s]'], [10, 2, 6])[(self.getColumn('Date', 'Date', 2).isin(self.D_dates))
                                                                                                                                                                 & (self.getColumn('Przesunięcie', 'Shift', 11).isin(self.D_shifts))
                                                                                                                                                                 & (self.getColumn('Cycle', 'Cycle', 5).isin(self.D_cycles))
                                                                                                                                                                 & (self.getColumn('Numer części', 'Part Number', 9).isin(self.D_part_numbers))
                                                                                                                                                                 & (self.getColumn('Numer seryjny', 'Serial Number', 10).isin(self.D_serial_numbers))]
            engines_data = engines_data.sort_values(
                by=[engines_data.columns[0], engines_data.columns[1]]).values.tolist()

            engines_data_dict = {}
            prev_engine = ''
            for i in range(len(engines_data)):
                engine = engines_data[i][0]
                date = engines_data[i][1]
                duration = engines_data[i][2]
                if engine != prev_engine:
                    engines_data_dict[engine] = ([], [])
                engines_data_dict[engine][0].append(date)
                engines_data_dict[engine][1].append(duration)
                prev_engine = engine
            engines_data_dict_cpy = dict(engines_data_dict)

            for key, value in engines_data_dict_cpy.items():
                if len(value[0]) != len(
                        self.station) or not key in self.serial_number:
                    engines_data_dict.pop(key, None)

            delta_time = {}
            for engine, engine_data in engines_data_dict.items():
                engine_station_time = [(engine_data[0][i + 1] - engine_data[0][i]) /
                                       np.timedelta64(1, 's') for i in range(len(engine_data[0]) - 1)]
                engine_station_time.append(engine_data[1][-1])
                delta_time[engine] = [engine_station_time[i] for i in range(
                    len(engine_station_time)) if self.station[i] in self.D_stations]

            if len(engines_data_dict) > 0:
                for i in range(self.D_station_nmb):
                    for engine in engines_data_dict.keys():
                        if delta_time[engine][i] <= Globals.transition_expected_time:
                            self.D_engines_ok_percentage[i] += 1
                    self.D_engines_ok_percentage[i] = round((
                        self.D_engines_ok_percentage[i] / len(engines_data_dict)) * 100, 2)

            self.chartD_drawn = True

            ###############
            # Details data
            self.D_details_data = {}
            self.D_details_data[utils.setLabel(
                self.language, 'Ilość stacji', 'Number of stations')] = self.D_station_nmb
            self.D_details_data[utils.setLabel(
                self.language, 'Wybrane stacje', 'Selected stations')] = self.D_stations
            self.D_details_data[utils.setLabel(
                self.language, 'Data początkowa (z pliku)', 'Start date (from file)')] = self.date[0]
            self.D_details_data[utils.setLabel(
                self.language, 'Data końcowa (z pliku)', 'End date (from file)')] = self.date[-1]
            self.D_details_data[''] = ''
            self.D_details_data[utils.setLabel(
                self.language, 'Wybrana data początkowa', 'Chosen start date')] = self.date[self.D_date_selected[0]] if isinstance(Globals.chartD_start_date, type(None)) else Globals.chartD_start_date
            self.D_details_data[utils.setLabel(
                self.language, 'Wybrana data końcowa', 'Chosen end date')] = self.date[self.D_date_selected[1]] if isinstance(Globals.chartD_end_date, type(None)) else Globals.chartD_end_date
            self.D_details_data[' '] = ''
            self.D_details_data[utils.setLabel(
                self.language, 'Wybrane zmiany', 'Selected shifts')] = self.D_shifts
            self.D_details_data[utils.setLabel(
                self.language, 'Wybrane cykle', 'Selected cycles')] = self.D_cycles
            self.D_details_data[utils.setLabel(
                self.language, 'Wybrane numery części', 'Selected part numbers')] = self.D_part_numbers
            self.D_details_data[utils.setLabel(
                self.language, 'Całkowita ilość silników', 'Total number of engines')] = self.serial_number_nmb
            self.D_details_data[utils.setLabel(
                self.language, 'Silniki z brakującymi danymi', 'Engines with missing data')] = self.wrong_transition_count
            self.D_details_data[utils.setLabel(self.language, 'Silniki z poprawnymi danymi',
                                               'Engines with valid data')] = self.serial_number_nmb - self.wrong_transition_count
            self.D_details_data['  '] = ''
            self.D_details_data[utils.setLabel(
                self.language, 'Ilość wybranych silników', 'Number of selected engines')] = len(engines_data_dict)
            if len(engines_data_dict.keys()) <= 20:
                self.D_details_data[utils.setLabel(self.language,
                                                    'Wybrane silniki',
                                                    'Selected engines')] = [i for i in engines_data_dict.keys()]
            ###############

        self.D_station_str = utils.setLabel(
            self.language, 'Stacje', 'Stations')

        #######################################################################

        self.clearFrame('D')
        self.D_options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        self.D_filters_frame.place(
            relx=0, rely=0.05, relwidth=0.7, relheight=0.05)
        self.buttons_frame.place(
            relx=0.7,
            rely=0.05,
            relwidth=0.3,
            relheight=0.05)
        if self.chartD_show_filters:
            self.D_chart_frame.place(
                relx=0, rely=0.1, relwidth=1, relheight=0.90)
        else:
            self.D_chart_frame.place(
                relx=0, rely=0.05, relwidth=1, relheight=0.95)

        if self.chartD_show_filters:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25b2', u'Filters \u25b2')
        else:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25bc', u'Filters \u25bc')
        buttons_state = tkinter.DISABLED if self.is_loading else tkinter.NORMAL

        self.D_filters_btn['text'] = filters_btn_text
        self.D_details_btn['text'] = utils.setLabel(
            self.language, 'Szczegóły', 'Details')
        self.D_station_btn['text'] = utils.setLabel(
            self.language, 'Stacja', 'Station')
        self.D_date_btn['text'] = utils.setLabel(self.language, 'Data', 'Date')
        self.D_shift_btn['text'] = utils.setLabel(
            self.language, 'Zmiana', 'Shift')
        self.D_cycle_btn['text'] = utils.setLabel(
            self.language, 'Cykl', 'Cycle')
        self.D_part_number_btn['text'] = utils.setLabel(
            self.language, 'Numer części', 'Part number')
        self.D_serial_number_btn['text'] = utils.setLabel(
            self.language, 'Numer seryjny', 'Serial number')

        self.D_filters_btn['state'] = buttons_state
        self.D_details_btn['state'] = buttons_state
        self.D_station_btn['state'] = buttons_state
        self.D_date_btn['state'] = buttons_state
        self.D_shift_btn['state'] = buttons_state
        self.D_cycle_btn['state'] = buttons_state
        self.D_part_number_btn['state'] = buttons_state
        self.D_serial_number_btn['state'] = buttons_state

        #######################################################################

        self.D_figure.clear()

        self.D_figure.set_tight_layout(True)
        ax = self.D_figure.add_subplot(111)

        ax.bar(self.D_stations, self.D_engines_ok_percentage, width=0.8, edgecolor='k', color=Globals.primary_color)
        ax.set_title(utils.setLabel(self.language, f'Procentowy udział silników z czasem PRZEJŚCIA \u2264 {Globals.transition_expected_time}s dla poszczególnych stacji',
                     f'Percentage of engines with TRANSITION time \u2264 {Globals.transition_expected_time}s grouped by stations'), pad=15, weight='bold')
        ax.set_xlabel(self.D_station_str)
        ax.set_ylim(0, 105)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        for bar, label in zip(ax.patches, self.D_engines_ok_percentage):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    str(round(label, 2)) + '%', weight='semibold', ha='center', va='bottom')

        self.D_canvas.draw()

    def drawChartE(self, chart_drawn=None):
        if not isinstance(chart_drawn, type(None)):
            self.chartE_drawn = chart_drawn

        if self.chartE_first_draw:
            self.E_station_selected = self.onesList(len(self.station))
            self.E_employee_selected = self.onesList(len(self.operator_name))
            self.E_date_selected = [0, len(self.date) - 1]
            self.E_shift_selected = self.onesList(len(self.shift))
            self.E_cycle_selected = self.onesList(len(self.cycle))
            self.E_part_number_selected = self.onesList(len(self.part_number))
            self.E_serial_number_selected = self.onesList(len(self.serial_number))
            self.chartE_first_draw = False

        if not self.chartE_drawn:
            self.E_stations = [self.station[i] for i in range(
                len(self.E_station_selected)) if self.E_station_selected[i] != 0]
            self.E_station_nmb = len(self.E_stations)
            self.E_employees = [self.operator_name[i] for i in range(
                len(self.E_employee_selected)) if self.E_employee_selected[i] != 0]
            self.E_employee_nmb = len(self.E_employees)
            self.E_dates = self.date[self.E_date_selected[0]
                :self.E_date_selected[1] + 1]
            self.E_shifts = [self.shift[i] for i in range(
                len(self.E_shift_selected)) if self.E_shift_selected[i] != 0]
            self.E_cycles = [self.cycle[i] for i in range(
                len(self.E_cycle_selected)) if self.E_cycle_selected[i] != 0]
            self.E_part_numbers = [self.part_number[i] for i in range(
                len(self.E_part_number_selected)) if self.E_part_number_selected[i] != 0]
            self.E_serial_numbers = [self.serial_number[i] for i in range(
                len(self.E_serial_number_selected)) if self.E_serial_number_selected[i] != 0]

            engines_data = self.getColumns(['Numer seryjny', 'Date', 'Stacja', 'Operator Name', 'Aktualny czas trwania [s]'], ['Serial Number', 'Date', 'Station', 'Operator Name', 'Actual duration [s]'], [10, 2, 1, 4, 6])[(self.getColumn('Date', 'Date', 2).isin(self.E_dates))
                                                                                                                                                                                                                              & (self.getColumn('Przesunięcie', 'Shift', 11).isin(self.E_shifts))
                                                                                                                                                                                                                              & (self.getColumn('Cycle', 'Cycle', 5).isin(self.E_cycles))
                                                                                                                                                                                                                              & (self.getColumn('Numer części', 'Part Number', 9).isin(self.E_part_numbers))
                                                                                                                                                                                                                              & (self.getColumn('Numer seryjny', 'Serial Number', 10).isin(self.E_serial_numbers))]

            engines_data = engines_data.sort_values(by=[engines_data.columns[0], engines_data.columns[1]]).values.tolist()

            engines_data_dict = {}
            prev_engine = ''
            for i in range(len(engines_data)):
                engine = engines_data[i][0]
                date = engines_data[i][1]
                station = engines_data[i][2]
                employee = engines_data[i][3]
                duration = engines_data[i][4]
                if engine != prev_engine:
                    engines_data_dict[engine] = ([], [], [], [])
                engines_data_dict[engine][0].append(date)
                engines_data_dict[engine][1].append(station)
                engines_data_dict[engine][2].append(employee)
                engines_data_dict[engine][3].append(duration)
                prev_engine = engine
            engines_data_dict_cpy = dict(engines_data_dict)

            for key, value in engines_data_dict_cpy.items():
                if len(value[0]) != len(self.station) or not key in self.serial_number:
                    engines_data_dict.pop(key, None)

            self.E_chart_data_dict = {}
            if self.E_mode_choice_nmb == 0:
                for station in self.E_stations:
                    self.E_chart_data_dict[station] = [0, 0, 0, 0] # operation time sum | operation time len | transition time sum | transition time len
            else:
                for employee in self.E_employees:
                    self.E_chart_data_dict[employee] = [0, 0, 0, 0] # operation time sum | operation time len | transition time sum | transition time len

            for data in engines_data_dict.values():
                dates = data[0]
                durations = data[3]
                if self.E_mode_choice_nmb == 0:
                    keys = data[1]
                else:
                    keys = data[2]
                for i in range(len(keys)):
                    if keys[i] in self.E_chart_data_dict.keys():
                        # Operation time
                        self.E_chart_data_dict[keys[i]][0] += durations[i]
                        self.E_chart_data_dict[keys[i]][1] += 1
                        # Transition time
                        if i == len(keys) - 1:
                            self.E_chart_data_dict[keys[i]][2] += durations[i]
                            self.E_chart_data_dict[keys[i]][3] += 1
                        else:
                            self.E_chart_data_dict[keys[i]][2] += (dates[i + 1] - dates[i]) / np.timedelta64(1, 's')
                            self.E_chart_data_dict[keys[i]][3] += 1

            for data in self.E_chart_data_dict.values():
                if data[1] != 0:
                    data[0] = round(data[0] / data[1], 2)
                if data[3] != 0:
                    data[2] = round(data[2] / data[3], 2)

            self.chartE_drawn = True

            ###############
            # Details data
            self.E_details_data = {}
            if self.E_mode_choice_nmb == 0:
                self.E_details_data[utils.setLabel(
                    self.language, 'Ilość stacji', 'Number of stations')] = self.E_station_nmb
                self.E_details_data[utils.setLabel(
                    self.language, 'Wybrane stacje', 'Selected stations')] = self.E_stations
            else:
                self.E_details_data[utils.setLabel(
                    self.language, 'Ilość pracowników', 'Number of employees')] = self.E_employee_nmb
                self.E_details_data[utils.setLabel(
                    self.language, 'Wybrani pracownicy', 'Selected employees')] = self.E_employees
            self.E_details_data[utils.setLabel(
                self.language, 'Data początkowa (z pliku)', 'Start date (from file)')] = self.date[0]
            self.E_details_data[utils.setLabel(
                self.language, 'Data końcowa (z pliku)', 'End date (from file)')] = self.date[-1]
            self.E_details_data[' '] = ''
            self.E_details_data[utils.setLabel(self.language, 'Wybrana data początkowa', 'Chosen start date')] = self.date[self.E_date_selected[0]] if isinstance(
                Globals.chartE_start_date, type(None)) else Globals.chartE_start_date
            self.E_details_data[utils.setLabel(self.language, 'Wybrana data końcowa', 'Chosen end date')] = self.date[self.E_date_selected[1]] if isinstance(
                Globals.chartE_end_date, type(None)) else Globals.chartE_end_date
            self.E_details_data['  '] = ''
            self.E_details_data[utils.setLabel(
                self.language, 'Wybrane zmiany', 'Selected shifts')] = self.E_shifts
            self.E_details_data[utils.setLabel(
                self.language, 'Wybrane cykle', 'Selected cycles')] = self.E_cycles
            self.E_details_data[utils.setLabel(
                self.language, 'Wybrane numery części', 'Selected part numbers')] = self.E_part_numbers
            self.E_details_data[utils.setLabel(self.language,
                                               'Całkowita ilość silników',
                                               'Total number of engines')] = self.serial_number_nmb
            self.E_details_data[utils.setLabel(self.language,
                                               'Silniki z brakującymi danymi',
                                               'Engines with missing data')] = self.wrong_transition_count
            self.E_details_data[utils.setLabel(self.language, 'Silniki z poprawnymi danymi',
                                               'Engines with valid data')] = self.serial_number_nmb - self.wrong_transition_count
            self.E_details_data['   '] = ''
            self.E_details_data[utils.setLabel(self.language,
                                               'Ilość wybranych silników',
                                               'Number of selected engines')] = len(engines_data_dict)
            if len(engines_data_dict.keys()) <= 20:
                self.E_details_data[utils.setLabel(self.language,
                                                    'Wybrane silniki',
                                                    'Selected engines')] = [i for i in engines_data_dict.keys()]
            ###############

            self.E_mode_choice_list = [
                utils.setLabel(
                    self.language, 'Stacje', 'Stations'), utils.setLabel(
                    self.language, 'Pracownicy', 'Employees')]
            self.E_label['text'] = utils.setLabel(
                self.language, 'Tryb:', 'Mode:')

            self.E_mode_choice_var.trace_vdelete(
                'w', self.E_mode_choice_var.trace_id)
            self.E_mode_choice_var.set(
                self.E_mode_choice_list[self.E_mode_choice_nmb])
            self.E_mode_choice_prev_var.set(
                self.E_mode_choice_list[self.E_mode_choice_nmb])
            self.E_mode_choice_var.trace_id = self.E_mode_choice_var.trace(
                'w', lambda *args: self.switchChartEMode())

            menu = self.E_option_menu['menu']
            menu.delete(0, 'end')
            for s in self.E_mode_choice_list:
                menu.add_radiobutton(label=s, variable=self.E_mode_choice_var)

        #######################################################################

        self.clearFrame('E')
        self.E_options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        self.E_filters_frame.place(
            relx=0, rely=0.05, relwidth=0.7, relheight=0.05)
        self.buttons_frame.place(
            relx=0.7,
            rely=0.05,
            relwidth=0.3,
            relheight=0.05)
        if self.chartE_show_filters:
            self.E_chart_frame.place(
                relx=0, rely=0.1, relwidth=1, relheight=0.9)
        else:
            self.E_chart_frame.place(
                relx=0, rely=0.05, relwidth=1, relheight=0.95)

        if self.chartE_show_filters:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25b2', u'Filters \u25b2')
        else:
            filters_btn_text = utils.setLabel(
                self.language, u'Filtry \u25bc', u'Filters \u25bc')
        buttons_state = tkinter.DISABLED if self.is_loading else tkinter.NORMAL

        self.E_label.pack(side=tkinter.LEFT, padx=(15, 0))
        self.E_option_menu.pack(side=tkinter.LEFT)

        self.E_filters_btn['text'] = filters_btn_text
        self.E_details_btn['text'] = utils.setLabel(
            self.language, 'Szczegóły', 'Details')
        self.E_station_btn['text'] = utils.setLabel(
            self.language, 'Stacja', 'Station')
        self.E_employee_btn['text'] = utils.setLabel(
            self.language, 'Pracownik', 'Employee')
        self.E_date_btn['text'] = utils.setLabel(self.language, 'Data', 'Date')
        self.E_shift_btn['text'] = utils.setLabel(
            self.language, 'Zmiana', 'Shift')
        self.E_cycle_btn['text'] = utils.setLabel(
            self.language, 'Cykl', 'Cycle')
        self.E_part_number_btn['text'] = utils.setLabel(
            self.language, 'Numer części', 'Part number')
        self.E_serial_number_btn['text'] = utils.setLabel(
            self.language, 'Numer seryjny', 'Serial number')

        self.E_filters_btn['state'] = buttons_state
        self.E_details_btn['state'] = buttons_state
        self.E_station_btn['state'] = buttons_state
        self.E_employee_btn['state'] = buttons_state
        self.E_date_btn['state'] = buttons_state
        self.E_shift_btn['state'] = buttons_state
        self.E_cycle_btn['state'] = buttons_state
        self.E_part_number_btn['state'] = buttons_state
        self.E_serial_number_btn['state'] = buttons_state

        if self.E_mode_choice_nmb == 0:
            self.E_station_btn.pack(side=tkinter.LEFT, padx=15)
        else:
            self.E_employee_btn.pack(side=tkinter.LEFT, padx=15)
        self.E_date_btn.pack(side=tkinter.LEFT)
        self.E_shift_btn.pack(side=tkinter.LEFT, padx=15)
        self.E_cycle_btn.pack(side=tkinter.LEFT)
        self.E_part_number_btn.pack(side=tkinter.LEFT, padx=15)
        self.E_serial_number_btn.pack(side=tkinter.LEFT, padx=(0, 15))
        self.E_sep.pack(side=tkinter.LEFT, fill=tkinter.Y)

        #######################################################################

        self.E_figure.clear()

        self.E_figure.set_tight_layout(True)
        ax = self.E_figure.add_subplot(111)

        keys_list = []
        operation_time_list = []
        transition_time_list = []
        passive_time_list = []
        for key, data in self.E_chart_data_dict.items():
            keys_list.append(key)
            operation_time_list.append(data[0])
            transition_time_list.append(data[2])
            passive_time_list.append(round(data[2] - data[0], 2))

        ax.bar(keys_list, operation_time_list, width=0.8, edgecolor='k', label=utils.setLabel(self.language, 'Czas operacji [s]', 'Operation time [s]'), color=Globals.primary_color)
        ax.bar(keys_list, passive_time_list, bottom=operation_time_list, width=0.8, edgecolor='k', label=utils.setLabel(self.language, 'Czas pasywny [s]', 'Passive time [s]'), color=Globals.secondary_color)
        if self.E_mode_choice_nmb == 1 and len(self.E_chart_data_dict.keys()) > 5:
            if len(self.E_chart_data_dict.keys()) <= 15:
                ax.tick_params(labelrotation=45)
                ax.legend(loc='upper right', bbox_to_anchor=(1, 1.1))
            else:
                ax.tick_params(labelrotation=90)
                ax.legend(loc='upper right', bbox_to_anchor=(1, 1.12))
        else:
            ax.legend(loc='upper right', bbox_to_anchor=(1, 1.08))
        ax.set_xlabel(self.E_mode_choice_list[self.E_mode_choice_nmb])
       
        if self.E_details_data[utils.setLabel(
                    self.language, 'Ilość wybranych silników', 'Number of selected engines')] == 0:
                ax.yaxis.set_major_formatter(mtick.NullFormatter())

        for bar, label, height in zip(ax.patches, operation_time_list + passive_time_list, operation_time_list + transition_time_list):
            if self.E_mode_choice_nmb == 1:
                rotation = 0 if len(keys_list) <= 5 else 45 if len(keys_list) <= 15 else 90
                offset = 0 if len(keys_list) <= 5 else 0.01 * max(transition_time_list)
            else:
                rotation = 0
                offset = 0
            if label > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, height + offset, str(label) + ' s', weight='semibold', ha='center', va='bottom', rotation=rotation)

        ax.set_title(
            utils.setLabel(
                self.language,
                'Czas operacji vs czas pasywny',
                'Operation time vs passive time'),
            pad=15,
            weight='bold')

        self.E_canvas.draw()


if __name__ == '__main__':
    pass
