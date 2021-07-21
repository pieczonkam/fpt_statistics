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
        self.excel_all_sheets = [self.setLabel('Brak', 'None')]
        self.excel_sheet = None
        self.excel_table = None
        self.table_prev_excel_table = None
        self.chart_prev_excel_table = None
        self.excel_table_cols_nmb = 12

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
        self.frame3 = ttk.Frame(self.window)
        self.frame4 = ttk.Frame(self.window)
        self.frame5 = ttk.Frame(self.window)
        self.frame1.place(relx=0, rely=0, relwidth=0.85, relheight=0.05)
        self.frame2_empty.place(
            relx=0, rely=0.05, relwidth=0.85, relheight=0.92)
        self.frame3.place(relx=0, rely=0.97, relwidth=0.85, relheight=0.03)
        self.frame4.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.94)
        self.frame5.place(relx=0.85, rely=0.94, relwidth=0.15, relheight=0.06)

        # Separators
        self.sep1 = ttk.Separator(self.frame4, orient='vertical')
        self.sep2 = ttk.Separator(self.frame1, orient='horizontal')
        self.sep3 = ttk.Separator(self.frame3, orient='horizontal')
        self.sep4 = ttk.Separator(self.frame5, orient='vertical')
        self.sep1.place(relx=0, rely=0, relheight=1)
        self.sep2.place(relx=0, rely=0.98, relwidth=1)
        self.sep3.place(relx=0, rely=0, relwidth=1)
        self.sep4.place(relx=0, rely=0, relheight=1)

        # Buttons
        self.btn1 = None
        self.btn2 = None
        self.btn3 = None
        self.btn4 = None
        self.btn5 = None
        self.btn6 = None
        self.btn7 = None
        # Labels
        self.label1 = None
        self.label2 = None
        self.label3 = None
        # OptionMenus
        self.opt_menu1 = None
        self.opt = None

        # Classes
        self.menubar = None
        self.table = None
        self.chart = None
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
                self.reloadTable()
                self.reloadChart()
        else:
            tkinter.messagebox.showerror(message=self.setLabel(
                'Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))

    def saveChart(self):
        if not self.is_loading:
            if self.show_chart and not self.chart is None:
                filename = 'aaa.png'
                self.runWithLoading(self.chart.saveChart, 'Zapisywanie wykresu...', 'Saving chart...', filename)
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
                if not self.chart is None:
                    self.chart.setLanguage(self.language)
                    self.redrawChart()
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
                if not self.chart is None:
                    self.chart.setLanguage(self.language)
                    self.redrawChart()
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
        if not self.is_loading:
            if tkinter.messagebox.askquestion(
                    message=self.setLabel('Czy na pewno chcesz zakończyć?', 'Are you sure you want to exit?')) == 'yes':
                self.window.destroy()
        else:
            tkinter.messagebox.showerror(message=self.setLabel(
                'Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))

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
                self.reloadTable()
                self.reloadChart()
            else:
                tkinter.messagebox.showerror(message=self.setLabel(
                    'Proszę zaczekać na ukończenie wczytywania.', 'Please wait until loading is finished.'))
                self.opt.set(self.excel_sheet)

    def reloadMenuBar(self):
        if not self.menubar is None:
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
                if self.table_prev_excel_table is None or not self.excel_table.equals(self.table_prev_excel_table):
                    self.table_prev_excel_table = self.excel_table
                    prev_table = self.table
                    self.table = self.runWithLoading(Table(
                        self.frame2_table, self.excel_table).prepareTable, 'Wczytywanie tabeli...', 'Loading table...')
                    self.table.grid(row=0, column=0, sticky='nswe')
                    if not prev_table is None:
                        prev_table.destroy()
            else:
                tkinter.messagebox.showerror(
                    message=self.setLabel('Aby wyświetlić tabelę, proszę wczytać plik.', 'In order to show a table load a file first.'))
                self.showEmpty()

    def reloadChart(self):
        if self.chart_prev_excel_table is None or not self.excel_table.equals(self.chart_prev_excel_table):
            self.chart_prev_excel_table = self.excel_table
            self.chart = Chart(self.window, self.frame2_chart, self.excel_table, self.language)
        self.redrawChart()

    def redrawChart(self):
        if self.show_chartA:
            self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'A')
        elif self.show_chartB:
            self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'B')
        elif self.show_chartC:
            self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'C')
        elif self.show_chartD:
            self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'D')
        elif self.show_chartE:
            self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'E')

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
        self.destroyWidget(self.label3)
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
            'Wykres A', 'Chart A'), command=self.showChartA, style='B2.TButton')
        self.btn3 = ttk.Button(self.frame4, text=self.setLabel(
            'Wykres B', 'Chart B'), command=self.showChartB, style='B3.TButton')
        self.btn4 = ttk.Button(self.frame4, text=self.setLabel(
            'Wykres C', 'Chart C'), command=self.showChartC, style='B4.TButton')
        self.btn5 = ttk.Button(self.frame4, text=self.setLabel(
            'Wykres D', 'Chart D'), command=self.showChartD, style='B5.TButton')
        self.btn6 = ttk.Button(self.frame4, text=self.setLabel(
            'Wykres E', 'Chart E'), command=self.showChartE, style='B6.TButton')
        self.btn7 = ttk.Button(self.frame4, text=self.setLabel(
            'Wyczyść', 'Clear'), command=self.showEmpty)
        # 0.02 for vertical separator
        self.btn1.place(relx=0.05, rely=0.01, relwidth=0.92)
        self.btn2.place(relx=0.05, rely=0.05, relwidth=0.92)
        self.btn3.place(relx=0.05, rely=0.09, relwidth=0.92)
        self.btn4.place(relx=0.05, rely=0.13, relwidth=0.92)
        self.btn5.place(relx=0.05, rely=0.17, relwidth=0.92)
        self.btn6.place(relx=0.05, rely=0.21, relwidth=0.92)
        self.btn7.place(relx=0.05, rely=0.25, relwidth=0.92)

    def destroyWidget(self, widget):
        if not widget is None:
            widget.destroy()

    def switchButtons(self, active_btn=None):
        s = ttk.Style()
        for i in range(1, 8):
            s.configure(f'B{i}.TButton', font=font.nametofont('TkDefaultFont'))
        if not active_btn is None:
            s.configure(active_btn + '.TButton', font=('Arial', 10, 'bold'))

    @utils.threadpool
    def readExcel(self):
        return pd.read_excel(self.filepath, sheet_name=self.excel_sheet)

    def runWithLoading(self, fun, text_pl, text_eng, *args):
        self.is_loading = True
        self.loading.setText(self.language, text_pl, text_eng)
        self.loading.show()
        fun_future = fun(*args)
        while not fun_future.done():
            self.window.update()
        self.loading.hide()
        self.loading.setText(self.language, 'Wczytywanie...', 'Loading...')
        self.is_loading = False
        return fun_future.result()

    def validateTable(self):
        if not self.excel_table is None:
            if len(self.excel_table.columns) != self.excel_table_cols_nmb:
                tkinter.messagebox.showwarning(message=utils.setLabel(self.language, 'Wybrany arkusz ma nieprawidłowy format. Niektóre funkcjonalności mogą nie zadziałać poprawnie.', 'Selected sheet has incorrect format. Some functionalities may not work properly.'))

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
                self.frame2_empty.place_forget()
                self.frame2_chart.place_forget()
                self.frame2_table.place(
                    relx=0, rely=0.05, relwidth=0.85, relheight=0.92)
                self.frame2_table.grid_columnconfigure(0, weight=1)
                self.frame2_table.grid_rowconfigure(0, weight=1)

    def showChart(self):
        if self.chart is None:
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
                self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'A')

    def showChartB(self):
        if not self.is_loading and not self.show_chartB:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B3')
                self.show_chartB = True
                self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'B')

    def showChartC(self):
        if not self.is_loading and not self.show_chartC:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B4')
                self.show_chartC = True
                self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'C')

    def showChartD(self):
        if not self.is_loading and not self.show_chartD:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B5')
                self.show_chartD = True
                self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'D')

    def showChartE(self):
        if not self.is_loading and not self.show_chartE:
            self.showChart()
            if not self.show_empty:
                self.switchButtons('B6')
                self.show_chartE = True
                self.runWithLoading(self.chart.drawChart, 'Wczytywanie wykresu...', 'Loading chart...', 'E')

    def showEmpty(self):
        if not self.is_loading and not self.show_empty:
            self.switchButtons()
            self.show_empty = True
            self.show_table = False
            self.show_chart = self.show_chartA = self.show_chartB = self.show_chartC = self.show_chartD = self.show_chartE = False
            self.frame2_table.place_forget()
            self.frame2_chart.place_forget()
            self.frame2_empty.place(
                relx=0, rely=0.05, relwidth=0.85, relheight=0.92)


if __name__ == '__main__':
    pass
