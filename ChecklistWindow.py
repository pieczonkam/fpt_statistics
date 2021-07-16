from imports import *

class ChechlistWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        
        self.posx = None
        self.posy = None
        self.checklist_window = None
        self.col_list = None
        self.already_selected_list = None
        self.selected_list = None
        self.page_len = None
        self.pages = None
        self.page_nmb = None
        self.vars = None
        self.checkbutton_list = []
        
    def show(self, language, col_list, already_selected_list, page_len=500):
        self.col_list = col_list
        self.already_selected_list = already_selected_list
        self.selected_list = already_selected_list.copy()
        self.page_len = page_len
        self.pages = math.ceil(len(col_list) / page_len)
        self.page_nmb = 1
        self.vars = [tkinter.IntVar(value=i) for i in already_selected_list]

        self.posx = root.winfo_x() + (root.winfo_width() - self.width) / 2
        self.posy = root.winfo_y() + (root.winfo_height() - self.height) / 2
        self.checklist_window = tkinter.Toplevel(self.root) 
        self.checklist_window.geometry('%dx%d+%d+%d' % (self.width, self.height, self.posx, self.posy))
        self.checklist_window.resizable(0, 0)
        self.checklist_window.grab_set()

        self.button_frame_top = ttk.Frame(self.checklist_window, width=self.width, height=30)
        self.checklist_frame = ttk.Frame(self.checklist_window, width=self.width, height=self.height - 70)
        self.button_frame_bottom = ttk.Frame(self.checklist_window, width=self.width, height=40)
        self.button_frame_top.pack(side=tkinter.TOP)
        self.checklist_frame.pack(side=tkinter.TOP)
        self.button_frame_bottom.pack(side=tkinter.TOP)

        self.sep_top = ttk.Separator(self.button_frame_top, orient='horizontal')
        self.sep_bottom = ttk.Separator(self.button_frame_bottom, orient='horizontal')
        self.sep_top.place(relx=0, rely=0.98, relwidth=1)
        self.sep_bottom.place(relx=0, rely=0, relwidth=1)

        self.ok_button = ttk.Button(self.button_frame_bottom, text='OK', command=self.overwriteSelected) 
        self.cancel_button = ttk.Button(self.button_frame_bottom, text=utils.setLabel(language, 'Anuluj', 'Cancel'), command=self.destroy)
        self.ok_button.place(relx=0.05, rely=0.16, relwidth=0.4, relheight=0.70)
        self.cancel_button.place(relx=0.55, rely=0.16, relwidth=0.4, relheight=0.70)

        self.select_all_var = tkinter.IntVar(value=1 if self.areAllSelected() else 0)
        self.select_all_checkbutton = ttk.Checkbutton(self.button_frame_top, text=utils.setLabel(language, 'Zaznacz wszystko', 'Select all'), variable=self.select_all_var, command=self.handleSelectAll)
        self.page_choice_var = tkinter.StringVar(value=str(self.page_nmb) + '/' + str(self.pages))
        self.page_choice_menu = ttk.Combobox(self.button_frame_top, textvariable=self.page_choice_var, values=list(range(1, self.pages + 1)))
        self.select_all_checkbutton.place(relx=0.015, rely=0.1, relwidth=0.49, relheight=0.78)
        self.page_choice_menu.place(relx=0.6, rely=0.1, relwidth=0.385, relheight=0.78)

        self.canvas = tkinter.Canvas(self.checklist_frame, borderwidth=0, highlightthickness=0)
        self.inner_frame = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(self.checklist_frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.inner_frame)
        self.inner_frame.bind('<Configure>', lambda event : self.canvas.configure(scrollregion=self.canvas.bbox('all'), width=self.width - 25, height=self.height - 70))
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.canvas.pack(side=tkinter.LEFT)
    
        self.reloadChecklist()

    def destroy(self):
        if not self.checklist_window is None:
            self.checklist_window.destroy()
        self.posx = None
        self.posy = None
        self.checklist_window = None
        self.col_list = None
        self.already_selected_list = None
        self.selected_list = None
        self.page_len = None
        self.pages = None
        self.page_nmb = None
        self.vars = None
        self.checkbutton_list = []

    def previousPage(self):
        if self.page_nmb > 1:
            self.page_nmb -= 1
            self.reloadChecklist()

    def nextPage(self):
        if self.page_nmb < self.pages:
            self.page_nmb += 1
            self.reloadChecklist()

    def reloadChecklist(self):
        for child in self.inner_frame.winfo_children():
            child.destroy()
        self.checkbutton_list = [None for _ in range(self.page_len)]
        offset = (self.page_nmb - 1) * self.page_len
        for i, j in zip(range(offset, self.page_len + offset), range(self.page_len)):
            if i < len(self.col_list):
                self.checkbutton_list[j] = ttk.Checkbutton(self.inner_frame, text=self.col_list[i], variable=self.vars[i], command=self.handleSelectItem)
                self.checkbutton_list[j].pack(side=tkinter.TOP, anchor='w')
        self.handleSelectItem()
        
    def handleSelectAll(self):
        if self.select_all_var.get() == 0:
            self.setVars(0)
        else:
            self.setVars(1)
        self.handleSelectItem()
    
    def handleSelectItem(self):
        self.selected_list = self.getVars()
        if not self.isAnySelected():
            self.ok_button['state'] = 'disabled'
        else:
            self.ok_button['state'] = 'normal'

    def handlePageChange(self, chosen_page):
        self.page_nmb = chosen_page
        self.reloadChecklist()

    def getVars(self, i=None, j=None):
        vars = []
        i = i if not i is None else 0
        j = j if not j is None else len(self.vars)
        for n in range(i, j):
            vars.append(self.vars[n].get())
        return vars
    
    def setVars(self, val, i=None, j=None):
        i = i if not i is None else 0
        j = j if not j is None else len(self.vars)
        for n in range(i, j):
            self.vars[n].set(val)

    def isAnySelected(self):
        for i in self.selected_list:
            if i != 0:
                return True
        return False

    def areAllSelected(self):
        for i in self.selected_list:
            if i == 0:
                return False
        return True
    
    def overwriteSelected(self):
        for i in range(len(self.already_selected_list)):
            self.already_selected_list[i] = self.selected_list[i]
        self.destroy()

root = tkinter.Tk()
root.geometry('600x600')

l = [str(i) + '.' for i in range(20001)]
selected = [0 for _ in range(20001)]
selected[0] = 1
selected[10] = 1

popup_window = ChechlistWindow(root, 250, 450)
ttk.Button(root, text='Klik!', command=lambda : popup_window.show('polish', l, selected, 250)).pack()

ttk.Button(root, text='Klik2!', command=lambda : print(selected)).pack()

root.mainloop()