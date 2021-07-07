import tkinter
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import pandas

filename = ''
excel_file = None


def chooseFile():
    global filename
    filename = filedialog.askopenfilename(
        initialdir='..', title='Wybierz plik', filetypes=(
            ('Pliki programu Excel', '*.xlsx *.xls',), ('Wszystkie pliki', '*.*')))

    if filename == '':
        pass
    elif not (filename.endswith('.xlsx')
              or filename.endswith('.xls')):
        tkinter.messagebox.showinfo(
            title='Błąd formatu',
            message='Wybrano plik o nieobsługiwanym rozszerzeniu')
        filename = ''
    else:
        tkinter.messagebox.showinfo(message='Plik załadowany pomyślnie')


def showTable():
    global filename
    global excel_file
    if filename != '':
        excel_file = pandas.read_excel(filename)
        print(excel_file)


window = tkinter.Tk()
window.title('PMS Data Analysis')
window.geometry('800x600')

btn1 = ttk.Button(window, text='Załaduj plik', command=chooseFile, width=15)
btn2 = ttk.Button(window, text='Tabela', command=showTable, width=15)

btn1.pack(pady=5)
btn2.pack()

window.mainloop()
