from imports import *
from MenuBar import *
from Table import *


class App:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('PMS Data Analysis')
        self.window.state('zoomed')
        self.window.minsize(800, 600)
        self.window.iconbitmap(os.path.abspath('applogo.ico'))
        #self.window.bind('<Configure>', self.resize)

        self.widnow_width = self.window.winfo_width()

        self.language = 'polish'
        self.filepath = ''
        self.filename = ''
        self.excel_file = None

        self.menubar = None
        self.table = None

        # Separators
        self.sep1 = None
        self.sep2 = None
        # Buttons
        self.btn1 = None
        # Labels
        self.label1 = None
        self.label2 = None
        self.label3 = None

    ##########################################################################
    # Menu bar commands

    # File commands

    def loadFile(self):
        self.filepath = filedialog.askopenfilename(initialdir='/',
                                                   title=self.setLabel(
                                                       'Wybierz plik', 'Choose file'),
                                                   filetypes=((self.setLabel('Pliki programu Excel', 'Excel files'), '*.xlsx *.xls'), (self.setLabel('Wszystkie pliki', 'All files'), '*.*')))

        if self.filepath == '':
            pass
        elif not (self.filepath.endswith('.xlsx') or self.filepath.endswith('.xls')):
            tkinter.messagebox.showerror(
                message=self.setLabel('Wybrano plik o nieobsługiwanym rozszerzeniu.', 'Selected file of unsupported extension.'))
            self.filepath = ''
            self.filename = ''
        else:
            self.filename = os.path.basename(self.filepath)
            tkinter.messagebox.showinfo(
                message=self.setLabel(
                    'Plik załadowany pomyślnie.',
                    'File was loaded successfully.'))
        self.reloadWidgets()

    # Help commands
    def printInfo(self):
        tkinter.messagebox.showinfo(
            message=self.setLabel(
                'Instrukcja obsługi.',
                'Manual.'))

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
    # Buttons commands

    # 'Table' button
    def showTable(self):
        if self.filepath != '':
            self.excel_file = pd.read_excel(self.filepath)
            print(self.excel_file)
        else:
            print("No file loaded")

    ##########################################################################

    def reloadMenuBar(self):
        self.menubar = MenuBar(self.window)
        self.menubar.addMenu(
            self.setLabel(
                'Plik', 'File'), labels=[
                self.setLabel(
                    'Załaduj', 'Load')], commands=[
                    self.loadFile])
        self.menubar.addMenu(
            self.setLabel(
                'Pomoc', 'Help'), labels=[
                self.setLabel(
                    'Instrukcja obsługi', 'Manual')], commands=[
                    self.printInfo])
        self.menubar.addMenu(
            self.setLabel(
                'Język', 'Language'), labels=[
                self.setLabel(
                    u'\u2713 Polski', '     Polish'), self.setLabel(
                    '     Angielski', u'\u2713 English')], commands=[
                        self.setPolish, self.setEnglish])
        self.menubar.addMenu(
            self.setLabel(
                'Zakończ',
                'Exit'),
            main_command=self.exitApp)

    def reloadWidgets(self):
        # Destroy widgets if they exist
        # Separators
        self.destroyWidget(self.sep1)
        self.destroyWidget(self.sep2)
        # Buttons
        self.destroyWidget(self.btn1)
        # Labels
        self.destroyWidget(self.label1)
        self.destroyWidget(self.label2)
        self.destroyWidget(self.label3)

        # Separators
        # sep1
        self.sep1 = ttk.Separator(self.window, orient='vertical')
        self.sep1.place(relx=0.85, rely=0, relheight=1)
        # sep2
        self.sep2 = ttk.Separator(self.window, orient='horizontal')
        self.sep2.place(relx=0.85, rely=0.70, relwidth=0.25)
        # Buttons
        # btn1
        self.btn1 = ttk.Button(
            self.window,
            text=self.setLabel(
                'Tabela',
                'Table'),
            command=self.showTable)
        self.btn1.place(relx=0.855, rely=0.01, relwidth=0.14)
        # Labels
        # label1
        if self.filename != '':
            excel_logo = tkinter.PhotoImage(
                file=os.path.abspath('excellogo.png'))
            self.label1 = tkinter.Label(
                self.window,
                image=excel_logo,
                text=' ' + self.filename,
                compound='left',
                wraplength=self.window.winfo_width() * 0.13)
            self.label1.image = excel_logo
            self.label1.place(relx=0.855, rely=0.71, relwidth=0.14)

    def destroyWidget(self, widget):
        if widget is not None:
            widget.destroy()

    ##########################################################################

    def resize(self, event):
        if self.widnow_width != self.window.winfo_width():
            self.window_width = self.window.winfo_width()
            self.reloadWidgets()


if __name__ == '__main__':
    pass
