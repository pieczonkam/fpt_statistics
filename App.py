from utils import threadpool
from imports import *
from MenuBar import *
from Table import *
from Chart import *
from Loading import *


class App:
    def __init__(self):
        self.language = 'polish'
        self.filepath = ''
        self.filename = ''
        self.excel_table_cols_nmb = 12
        self.excel_table = None
        self.table_prev_excel_table = None
        self.chart_prev_excel_table = None

        self.window = tkinter.Tk()
        self.window.title('PMS Data Analysis')
        self.window.state('zoomed')
        self.window.minsize(1200, 700)
        self.window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.window.protocol('WM_DELETE_WINDOW', self.exitApp)
    
        self.show_empty = True
        self.show_table = False
        self.show_chart = False
        self.show_chartA = False
        self.show_chartB = False
        self.show_chartC = False
        self.show_chartD = False
        self.show_chartE = False

        self.is_loading = False

        # Frames
        self.frame1 = ttk.Frame(self.window)
        self.frame2_empty = ttk.Frame(self.window)
        self.frame2_table = ttk.Frame(self.window)
        self.frame2_chart = ttk.Frame(self.window)
        self.frame2_chart_buttons = ttk.Frame(self.frame2_chart)
        self.frame3 = ttk.Frame(self.window)
        self.frame4 = ttk.Frame(self.window)
        self.frame5 = ttk.Frame(self.window)
        self.frame1.place(relx=0, rely=0, relwidth=0.85, relheight=0.05)
        self.frame2_empty.place(
            relx=0, rely=0.05, relwidth=0.85, relheight=0.92)
        self.frame3.place(relx=0, rely=0.97, relwidth=0.85, relheight=0.03)
        self.frame4.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.94)
        self.frame5.place(relx=0.85, rely=0.94, relwidth=0.15, relheight=0.06)

        # Widgets
        ttk.Separator(self.frame4, orient='vertical').place(
            relx=0, rely=0, relheight=1)
        ttk.Separator(self.frame1, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)
        ttk.Separator(self.frame3, orient='horizontal').place(
            relx=0, rely=0, relwidth=1)
        ttk.Separator(self.frame5, orient='vertical').place(
            relx=0, rely=0, relheight=1)
        ttk.Separator(self.frame2_chart_buttons, orient='horizontal').place(
            relx=0, rely=0.98, relwidth=1)

        self.style = ttk.Style()
        self.style.configure('TButton', font=(None, 9))
        self.style.configure('TLabel', font=(None, 9))
        self.style.configure('TMenubutton', font=(None, 9))
        self.style.configure('TCheckbutton', font=(None, 9))
        
        self.refresh_btn = ttk.Button(self.frame2_chart_buttons, text=self.setLabel(
            u'\u27f3 Odśwież', u'\u27f3 Refresh'), command=lambda: self.redrawChart(False))
        self.reset_filters_btn = ttk.Button(self.frame2_chart_buttons, text=self.setLabel('Reset filtrów', 'Reset filters'), command=self.resetFilters)
        self.refresh_btn.pack(side=tkinter.RIGHT, padx=15)
        self.reset_filters_btn.pack(side=tkinter.RIGHT)

        self.btn1 = None
        self.btn2 = None
        self.btn3 = None
        self.btn4 = None
        self.btn5 = None
        self.btn6 = None
        self.btn7 = None

        self.label1 = None
        self.label2 = None

        self.opt_menu1 = None

        # Classes
        self.table = None
        self.chart = None
        self.menubar = None
        self.loading = Loading(self.window, self.frame5, self.language)

    ##########################################################################
    # Menu bar commands

    # File commands
    def loadFile(self):
        if not self.is_loading:
            prev_filepath = self.filepath
            self.filepath = filedialog.askopenfilename(initialdir='/',
                                                       title=self.setLabel(
                                                           'Wybierz plik', 'Choose file'),
                                                       filetypes=((self.setLabel('Pliki programu Excel', 'Excel files'), '*.xlsx *.xls'), (self.setLabel('Wszystkie pliki', 'All files'), '*.*')))

            if self.filepath == '':
                self.filepath = prev_filepath
            elif not (self.filepath.endswith('.xlsx') or self.filepath.endswith('.xls')):
                tkinter.messagebox.showerror(
                    message=self.setLabel('Wybrano plik o nieobsługiwanym rozszerzeniu.', 'Selected file of unsupported extension.'))
                self.filepath = prev_filepath
            else:
                self.filename = os.path.basename(self.filepath)
                self.excel_all_sheets = pd.ExcelFile(self.filepath).sheet_names
                self.excel_all_sheets = [self.excel_all_sheets[0] if len(
                    self.excel_all_sheets) > 0 else self.setLabel('Brak', 'None')] + self.excel_all_sheets
                if len(self.excel_all_sheets) > 1:
                    self.excel_sheet = self.excel_all_sheets[1]
                else:
                    self.excel_sheet = None
                self.reloadWidgets()
                self.excel_table = self.runWithLoading(
                    self.readExcel, 'Wczytywanie arkusza...', 'Loading sheet...')
                self.validateTable()
                self.reloadChart()
                self.reloadTable()
        else:
            tkinter.messagebox.showerror(message=self.setLabel(
                'Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))

    def saveChart(self):
        if not self.is_loading:
            if self.show_chart and not isinstance(self.chart, type(None)):
                filename = filedialog.asksaveasfilename(initialdir='/', title=self.setLabel('Zapisz wykres', 'Save chart'), filetypes=((self.setLabel(
                    'Plik PNG', 'PNG file'), '*.png'), (self.setLabel('Plik PDF', 'PDF file'), '*.pdf'), (self.setLabel('Plik EPS', 'EPS file'), '*.eps')), defaultextension='*.png')
                self.runWithLoading(
                    self.chart.saveChart, 'Zapisywanie wykresu...', 'Saving chart...', filename)
            else:
                tkinter.messagebox.showerror(message=self.setLabel(
                    'Proszę wybrać wykres do zapisania.', 'Please select a chart to save.'))
        else:
            tkinter.messagebox.showerror(message=self.setLabel(
                'Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))

    # Help commands
    def printInfo(self):
        tkinter.messagebox.showinfo(
            message=self.setLabel('Instrukcja obsługi.', 'Manual.'))

    # Language commands
    def setPolish(self):
        if self.language != 'polish':
            if not (self.is_loading and self.show_chart):
                self.language = 'polish'
                self.reloadMenuBar()
                self.reloadWidgets()
                self.switchButtonsState()
                self.refresh_btn['text'] = self.setLabel(u'\u27f3 Odśwież', u'\u27f3 Refresh')
                self.reset_filters_btn['text'] = self.setLabel('Reset filtrów', 'Reset filters')
                if not isinstance(self.chart, type(None)):
                    self.chart.setLanguage(self.language)
                    self.redrawChart(False)
                self.loading.setText(self.language)
            else:
                tkinter.messagebox.showerror(message=self.setLabel(
                    'Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))

    def setEnglish(self):
        if self.language != 'english':
            if not (self.is_loading and self.show_chart):
                self.language = 'english'
                self.reloadMenuBar()
                self.reloadWidgets()
                self.switchButtonsState()
                self.refresh_btn['text'] = self.setLabel(u'\u27f3 Odśwież', u'\u27f3 Refresh')
                self.reset_filters_btn['text'] = self.setLabel('Reset filtrów', 'Reset filters')
                if not isinstance(self.chart, type(None)):
                    self.chart.setLanguage(self.language)
                    self.redrawChart(False)
                self.loading.setText(self.language)
            else:
                tkinter.messagebox.showerror(message=self.setLabel(
                    'Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))

    def setLabel(self, polish, english):
        if self.language == 'polish':
            return polish
        return english

    # Exit command
    def exitApp(self):
        if self.is_loading:
            tkinter.messagebox.showerror(message=self.setLabel('Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))
        else:
            if tkinter.messagebox.askquestion(message=self.setLabel('Czy na pewno chcesz zakończyć?', 'Are you sure you want to exit?')) == 'yes':
                self.window.destroy()    
        
    ##########################################################################
    # Other methods

    # opt_menu1
    def selectSheet(self, selected_sheet):
        if self.excel_sheet != selected_sheet:
            if not self.is_loading:
                self.excel_sheet = selected_sheet
                self.excel_table = self.runWithLoading(
                    self.readExcel, 'Wczytywanie arkusza...', 'Loading sheet...')
                self.validateTable()
                self.reloadChart()
                self.reloadTable()
            else:
                tkinter.messagebox.showerror(message=self.setLabel(
                    'Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))
                self.opt.set(self.excel_sheet)

    def reloadMenuBar(self):
        if not isinstance(self.menubar, type(None)):
            self.menubar.clear()
        self.menubar = MenuBar(self.window)
        self.menubar.addMenu(self.setLabel('Plik', 'File'), labels=[self.setLabel(
            'Wczytaj arkusz', 'Load sheet'), self.setLabel('Zapisz wykres', 'Save chart')], commands=[self.loadFile, self.saveChart])
        self.menubar.addMenu(self.setLabel('Pomoc', 'Help'), labels=[self.setLabel(
            'Instrukcja obsługi', 'Manual')], commands=[self.printInfo])
        self.menubar.addMenu(self.setLabel('Język', 'Language'), labels=[self.setLabel(u'\u2713 Polski', '     Polish'), self.setLabel(
            '     Angielski', u'\u2713 English')], commands=[self.setPolish, self.setEnglish])
        self.menubar.addMenu(self.setLabel(
            'Zakończ', 'Exit'), main_command=self.exitApp)

    def reloadTable(self):
        if self.show_table:
            if self.filepath != '':
                if isinstance(self.table_prev_excel_table, type(None)) or not self.excel_table.equals(self.table_prev_excel_table):
                    self.table_prev_excel_table = self.excel_table
                    prev_table = self.table
                    self.table = self.runWithLoading(Table(
                        self.frame2_table, self.excel_table).prepareTable, 'Wczytywanie tabeli...', 'Loading table...')
                    self.table.grid(row=0, column=0, sticky='nswe')
                    if not isinstance(prev_table, type(None)):
                        prev_table.destroy()
            else:
                tkinter.messagebox.showerror(
                    message=self.setLabel('Aby wyświetlić tabelę, proszę wczytać plik.', 'In order to show a table load a file first.'))
                self.showEmpty()

    @utils.threadpool
    def setChartObject(self, chart_is_loading):
        self.chart = Chart(self.window, self.frame2_chart,
                            self.frame2_chart_buttons, self.excel_table, self.language, chart_is_loading)

    def reloadChart(self):
        if isinstance(self.chart_prev_excel_table, type(None)) or not self.excel_table.equals(self.chart_prev_excel_table):
            self.chart_prev_excel_table = self.excel_table
            chart_is_loading = True if self.show_chart else False
            if chart_is_loading:
                self.chart.setIsLoading(True)
                self.chart.switchButtonsState()
            self.runWithLoading(self.setChartObject, 'Wczytywanie arkusza...', 'Loading sheet...', chart_is_loading)
        if self.show_chart:
            self.redrawChart()

    def redrawChart(self, chart_drawn=None):
        if not isinstance(self.chart, type(None)):
            self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', self.getCurrentChartName(), chart_drawn) 

    def reloadWidgets(self):
        # Destroy widgets if they exist
        # Buttons
        self.destroyWidget(self.btn1)
        self.destroyWidget(self.btn2)
        self.destroyWidget(self.btn3)
        self.destroyWidget(self.btn4)
        self.destroyWidget(self.btn5)
        self.destroyWidget(self.btn6)
        self.destroyWidget(self.btn7)
        # Labels
        self.destroyWidget(self.label1)
        self.destroyWidget(self.label2)
        # OptionMenus
        self.destroyWidget(self.opt_menu1)

        # Create widgets
        # Frame1
        if self.filename != '':
            visible_len = 60
            if len(' ' + self.filename) > visible_len - 3:
                fname_string = ' ' + self.filename[:visible_len - 5] + '...'
            else:
                fname_string = ' ' + self.filename
            excel_logo = tkinter.PhotoImage(
                file=utils.resourcePath('excellogo.png'))
            self.label1 = ttk.Label(self.frame1, image=excel_logo,
                                    text=fname_string, compound='left')
            self.label1.image = excel_logo
            self.label2 = ttk.Label(
                self.frame1, text=self.setLabel('Arkusz:', 'Sheet:'))
            self.opt = tkinter.StringVar()
            self.opt_menu1 = ttk.OptionMenu(
                self.frame1, self.opt, *self.excel_all_sheets, command=self.selectSheet)
            self.opt.set(self.excel_sheet if not self.excel_sheet is
                         None else self.setLabel('Brak', 'None'))
            self.label1.pack(side=tkinter.LEFT, padx=15)
            self.label2.pack(side=tkinter.LEFT)
            self.opt_menu1.pack(side=tkinter.LEFT)
        else:
            self.label1 = ttk.Label(self.frame1, text=self.setLabel(
                'Nie wczytano arkusza.', 'No sheet loaded.'))
            self.label1.pack(side=tkinter.LEFT, padx=15)

        # Frame4
        self.btn1 = ttk.Button(self.frame4, text=self.setLabel(
            'Tabela', 'Table'), command=self.showTable, style='B1.TButton')
        self.btn2 = ttk.Button(self.frame4, text=self.setLabel(
            'Wykres 3D', '3D Chart'), command=self.showChartA, style='B2.TButton')
        self.btn3 = ttk.Button(self.frame4, text=self.setLabel(
            'Histogram Czasu Przejścia', 'Transition Time Histogram'), command=self.showChartB, style='B3.TButton')
        self.btn4 = ttk.Button(self.frame4, text=self.setLabel(
            '% Czas Przejścia OK', '% Transition Time OK'), command=self.showChartC, style='B4.TButton')
        self.btn5 = ttk.Button(self.frame4, text=self.setLabel(
            'Wykres D', 'Chart D'), command=self.showChartD, style='B5.TButton')
        self.btn6 = ttk.Button(self.frame4, text=self.setLabel(
            'Wykres E', 'Chart E'), command=self.showChartE, style='B6.TButton')
        self.btn7 = ttk.Button(self.frame4, text=self.setLabel(
            'Wyczyść', 'Clear'), command=self.showEmpty)
        # 0.02 for vertical separator
        self.btn1.place(relx=0.05, rely=0.01, relwidth=0.92)
        self.btn4.place(relx=0.05, rely=0.05, relwidth=0.92)
        self.btn3.place(relx=0.05, rely=0.09, relwidth=0.92)
        self.btn2.place(relx=0.05, rely=0.13, relwidth=0.92)
        self.btn5.place(relx=0.05, rely=0.17, relwidth=0.92)
        self.btn6.place(relx=0.05, rely=0.21, relwidth=0.92)
        self.btn7.place(relx=0.05, rely=0.25, relwidth=0.92)

    def destroyWidget(self, widget):
        if not isinstance(widget, type(None)):
            widget.destroy()

    def switchButtons(self, active_btn=None):
        for i in range(1, 8):
            self.style.configure(f'B{i}.TButton', font=(None, 9, 'normal'))
        if not isinstance(active_btn, type(None)):
            self.style.configure(active_btn + '.TButton', font=(None, 9, 'bold'))

    @utils.threadpool
    def readExcel(self):
        return pd.read_excel(self.filepath, sheet_name=self.excel_sheet)

    def runWithLoading(self, fun, text_pl, text_eng, *args):
        self.is_loading = True
        self.switchButtonsState()
        if not isinstance(self.chart, type(None)):
            self.chart.setIsLoading(True)
            self.chart.switchButtonsState()
        self.loading.setText(self.language, text_pl, text_eng)
        self.loading.show()
        fun_future = fun(*args)
        while not fun_future.done():
            self.window.update()
        self.loading.hide()
        self.loading.setText(self.language, 'Wczytywanie...', 'Loading...')
        self.is_loading = False
        self.switchButtonsState()
        if not isinstance(self.chart, type(None)):
            self.chart.setIsLoading(False)
            self.chart.switchButtonsState()
        return fun_future.result()

    def validateTable(self):
        if not isinstance(self.excel_table, type(None)):
            if len(self.excel_table.columns) != self.excel_table_cols_nmb:
                tkinter.messagebox.showwarning(message=utils.setLabel(self.language, 'Wybrany arkusz ma nieprawidłowy format. Niektóre funkcjonalności mogą nie zadziałać poprawnie.',
                                               'Selected sheet has incorrect format. Some functionalities may not work properly.'))

    def switchButtonsState(self):
        if self.is_loading:
            self.disableButtons()
        else:
            self.enableButtons()

    def disableButtons(self):
        buttons = [self.btn1, self.btn2, self.btn3,
                   self.btn4, self.btn5, self.btn6, self.btn7, self.refresh_btn, self.reset_filters_btn]
        for button in buttons:
            if not isinstance(button, type(None)):
                button.configure(state=tkinter.DISABLED)

    def enableButtons(self):
        buttons = [self.btn1, self.btn2, self.btn3,
                   self.btn4, self.btn5, self.btn6, self.btn7, self.refresh_btn, self.reset_filters_btn]
        for button in buttons:
            if not isinstance(button, type(None)):
                button.configure(state=tkinter.NORMAL)

    def getCurrentChartName(self):
        if self.show_chartA:
            return 'A'
        if self.show_chartB:
            return 'B'
        if self.show_chartC:
            return 'C'
        if self.show_chartD:
            return 'D'
        if self.show_chartE:
            return 'E'
        return 'None'

    def resetFilters(self):
        if not isinstance(self.chart, type(None)):
            self.runWithLoading(self.chart.resetFilters, 'Wczytywanie wykresu...', 'Loading chart...', self.getCurrentChartName())
            self.redrawChart(False)

    ##########################################################################
    # Content display controllers

    def showTable(self):
        if not self.is_loading and not self.show_table:
            self.show_table = True
            self.show_empty = False
            self.show_chart = self.show_chartA = self.show_chartB = self.show_chartC = self.show_chartD = self.show_chartE = False
            self.reloadTable()
            if not self.show_empty:
                self.switchButtons('B1')
                if not isinstance(self.chart, type(None)):
                    self.chart.clearFrame()
                self.frame2_empty.place_forget()
                self.frame2_chart.place_forget()
                self.frame2_table.place(
                    relx=0, rely=0.05, relwidth=0.85, relheight=0.92)
                self.frame2_table.grid_columnconfigure(0, weight=1)
                self.frame2_table.grid_rowconfigure(0, weight=1)

    def showChart(self):
        if isinstance(self.chart, type(None)):
            tkinter.messagebox.showerror(
                message=self.setLabel('Aby wyświetlić wykres, proszę wczytać plik.', 'In order to show a chart load a file first.'))
            self.showEmpty()
        else:
            self.show_chart = True
            self.show_empty = self.show_table = False
            self.show_chartA = self.show_chartB = self.show_chartC = self.show_chartD = self.show_chartE = False
            self.frame2_empty.place_forget()
            self.frame2_table.place_forget()
            self.frame2_chart.place(
                relx=0, rely=0.05, relwidth=0.85, relheight=0.92)

    def showChartA(self):
        if not self.is_loading and not self.show_chartA:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B2')
                self.show_chartA = True
                self.runWithLoading(
                    self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'A')

    def showChartB(self):
        if not self.is_loading and not self.show_chartB:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B3')
                self.show_chartB = True
                self.runWithLoading(
                    self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'B')

    def showChartC(self):
        if not self.is_loading and not self.show_chartC:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B4')
                self.show_chartC = True
                self.runWithLoading(
                    self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'C')

    def showChartD(self):
        if not self.is_loading and not self.show_chartD:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B5')
                self.show_chartD = True
                self.runWithLoading(
                    self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'D')

    def showChartE(self):
        if not self.is_loading and not self.show_chartE:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B6')
                self.show_chartE = True
                self.runWithLoading(
                    self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'E')

    def showEmpty(self):
        if not self.is_loading and not self.show_empty:
            self.switchButtons()
            self.show_empty = True
            self.show_table = False
            self.show_chart = self.show_chartA = self.show_chartB = self.show_chartC = self.show_chartD = self.show_chartE = False
            if not isinstance(self.chart, type(None)):
                self.chart.clearFrame()
            self.frame2_table.place_forget()
            self.frame2_chart.place_forget()
            self.frame2_empty.place(
                relx=0, rely=0.05, relwidth=0.85, relheight=0.92)


if __name__ == '__main__':
    pass
