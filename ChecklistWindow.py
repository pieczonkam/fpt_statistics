from imports import *

class ChechlistWindow:
    pass

def data(frame):
    for i in range(1000):
        ttk.Checkbutton(frame, text=i, variable=vars[i]).pack(side=tkinter.TOP)

def printVars():
    print(vars)


def button_click():
    height = 300
    width = 200
    popup_window = tkinter.Toplevel(root)
    posx = root.winfo_x() + (root.winfo_width() - width) / 2
    posy = root.winfo_y() + (root.winfo_height() - height) / 2
    popup_window.geometry('%dx%d+%d+%d' % (width, height, posx, posy))
    popup_window.resizable(0, 0)   
    popup_window.grab_set()

    checklist_frame = ttk.Frame(popup_window, width=250, height=250, style='A.TFrame')
    button_frame = ttk.Frame(popup_window, width=250, height=50, style='B.TFrame')
    checklist_frame.pack(side=tkinter.TOP)
    button_frame.pack(side=tkinter.BOTTOM)

    # canvas = tkinter.Canvas(checklist_frame, bg='blue', borderwidth=0, highlightthickness=0)
    # inner_frame = ttk.Frame(canvas, width=canvas.winfo_width(), height=canvas.winfo_height())
    canvas = tkinter.Canvas(checklist_frame)
    inner_frame = ttk.Frame(canvas)
    scrollbar = tkinter.Scrollbar(checklist_frame, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    canvas.pack(side=tkinter.LEFT)

    # canvas.place(relx=0, rely=0, relwidth=0.9, relheight=1)
    # scrollbar.place(relx=0.9, rely=0, relwidth=0.1, relheight=1)

    canvas.create_window((0, 0), window=inner_frame)
    inner_frame.bind('<Configure>', lambda event : canvas.configure(scrollregion=canvas.bbox('all'), width=225, height=250))
    data(inner_frame)

    ttk.Separator(button_frame, orient='horizontal').place(relx=0, rely=0, relwidth=1)
    ttk.Button(button_frame, text='OK', command=printVars).place(relx=0.05, rely=0.15, relwidth=0.4, relheight=0.7)
    ttk.Button(button_frame, text='Anuluj', command=popup_window.destroy).place(relx=0.55, rely=0.15, relwidth=0.4, relheight=0.7)

root = tkinter.Tk()
vars = [tkinter.IntVar() for _ in range(1000)]
root.geometry('600x600')
ttk.Button(root, text='Klik!', command=button_click).pack()

root.mainloop()