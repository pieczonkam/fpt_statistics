from imports import *
from MenuBar import *
from Table import *


class App:
    def __init__(self):
        self.language = 'polish'
        self.filepath = ''
        self.filename = ''
        self.excel_table = None
        self.excel_all_sheets = [self.setLabel('Brak', 'None')]
        self.excel_sheet = None

        self.window = tkinter.Tk()
        self.window.title('PMS Data Analysis')
        self.window.state('zoomed')
        self.window.minsize(1100, 700)
        self.window.iconbitmap(utils.resourcePath('applogo.ico'))

        # Frames
        self.frame1 = ttk.Frame(self.window)
        self.frame2 = ttk.Frame(self.window)
        self.frame3 = ttk.Frame(self.window)
        self.frame1.place(relx=0, rely=0, relwidth=0.85, relheight=0.05)
        self.frame2.place(relx=0, rely=0.05, relwidth=0.85, relheight=0.95)
        self.frame3.place(relx=0.85, rely=0, relwidth=0.15, relheight=1)

        # Separators
        self.sep1 = ttk.Separator(self.frame3, orient='vertical')
        self.sep2 = ttk.Separator(self.frame2, orient='horizontal')
        self.sep1.place(relx=0, rely=0, relheight=1)
        self.sep2.place(relx=0, rely=0, relwidth=1)

        # Buttons
        self.btn1 = None
        self.btn2 = None
        self.btn3 = None
        # Labels
        self.label1 = None
        self.label2 = None
        self.label3 = None
        # OptionMenus
        self.opt_menu1 = None

        # Classes
        self.menubar = None
        self.table = None

    ##########################################################################
    # Menu bar commands

    # File commands
    def loadFile(self):
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
            tkinter.messagebox.showinfo(
                message=self.setLabel('Plik załadowany pomyślnie.', 'File was loaded successfully.'))
            self.excel_all_sheets = pd.ExcelFile(self.filepath).sheet_names
            self.excel_all_sheets = [self.excel_all_sheets[0] if len(
                self.excel_all_sheets) > 0 else self.setLabel('Brak', 'None')] + self.excel_all_sheets
            if len(self.excel_all_sheets) > 1:
                self.excel_sheet = self.excel_all_sheets[1]
            else:
                self.excel_sheet = None
            self.excel_table = None
            self.reloadWidgets()

    # Help commands
    def printInfo(self):
        tkinter.messagebox.showinfo(
            message=self.setLabel('Instrukcja obsługi.', 'Manual.'))

    # Language commands
    def setPolish(self):
        self.language = 'polish'
        self.reloadMenuBar()
        self.reloadWidgets()

    def setEnglish(self):
        self.language = 'english'
        self.reloadMenuBar()
        self.reloadWidgets()

    def setLabel(self, polish, english):
        if self.language == 'polish':
            return polish
        return english

    # Exit command
    def exitApp(self):
        if tkinter.messagebox.askquestion(
                message=self.setLabel('Czy na pewno chcesz zakończyć?', 'Are you sure you want to exit?')) == 'yes':
            self.window.quit()

    ##########################################################################
    # Other commands

    # opt_menu1
    def selectSheet(self, selected_sheet):
        self.excel_sheet = selected_sheet

    def reloadMenuBar(self):
        self.menubar = MenuBar(self.window)
        self.menubar.addMenu(self.setLabel('Plik', 'File'), labels=[self.setLabel(
            'Załaduj', 'Load')], commands=[self.loadFile])
        self.menubar.addMenu(self.setLabel('Pomoc', 'Help'), labels=[self.setLabel(
            'Instrukcja obsługi', 'Manual')], commands=[self.printInfo])
        self.menubar.addMenu(self.setLabel('Język', 'Language'), labels=[self.setLabel(u'\u2713 Polski', '     Polish'), self.setLabel(
            '     Angielski', u'\u2713 English')], commands=[self.setPolish, self.setEnglish])
        self.menubar.addMenu(self.setLabel(
            'Zakończ', 'Exit'), main_command=self.exitApp)

    def reloadTable(self):
        if self.filepath != '':
            if self.table != None:
                self.table.destroy()
            self.excel_table = pd.read_excel(
                self.filepath, sheet_name=self.excel_sheet)
            self.table = Table(self.frame2, self.excel_table)
        else:
            tkinter.messagebox.showerror(
                message=self.setLabel('Aby wyświetlić tabelę, proszę załadować plik.', 'In order to show a table, load a file first.'))

    def reloadWidgets(self):
        # Destroy widgets if they exist
        # Buttons
        self.destroyWidget(self.btn1)
        self.destroyWidget(self.btn2)
        self.destroyWidget(self.btn3)
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
            opt = tkinter.StringVar()
            self.opt_menu1 = ttk.OptionMenu(
                self.frame1, opt, *self.excel_all_sheets, command=self.selectSheet)
            opt.set(self.excel_sheet if self.excel_sheet !=
                    None else self.setLabel('Brak', 'None'))
            self.label1.pack(side=tkinter.LEFT, padx=15)
            self.label2.pack(side=tkinter.LEFT)
            self.opt_menu1.pack(side=tkinter.LEFT)
        else:
            self.label1 = ttk.Label(self.frame1, text=self.setLabel(
                'Nie załadowano pliku.', 'No file loaded.'))
            self.label1.pack(side=tkinter.LEFT, padx=15)

        # Frame3
        self.btn1 = ttk.Button(self.frame3, text=self.setLabel(
            'Tabela', 'Table'), command=self.reloadTable)
        self.btn2 = ttk.Button(self.frame3, text=self.setLabel(
            'Pusty', 'Empty'), command=self.reloadTable)
        self.btn3 = ttk.Button(self.frame3, text=self.setLabel(
            'Pusty', 'Empty'), command=self.reloadTable)
        # 0.02 for vertical separator
        self.btn1.place(relx=0.05, rely=0.01, relwidth=0.92)
        self.btn2.place(relx=0.05, rely=0.05, relwidth=0.92)
        self.btn3.place(relx=0.05, rely=0.09, relwidth=0.92)

    def destroyWidget(self, widget):
        if widget is not None:
            widget.destroy()

    ##########################################################################


if __name__ == '__main__':
    pass
