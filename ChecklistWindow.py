from imports import *


class ChecklistWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

    def show(self, language, col_list, already_selected_list, page_len=500):
        self.showLoadingCursor(self.root)
        self.col_list = col_list
        self.already_selected_list = already_selected_list
        self.selected_list = already_selected_list.copy()
        self.page_len = page_len if len(col_list) > page_len else len(col_list)
        self.pages = math.ceil(len(col_list) / page_len)
        self.page_nmb = 1
        self.vars = [tkinter.IntVar(value=i) for i in already_selected_list]
        self.button_frames_height = 100 if self.pages > 1 else 70
        height = self.height if self.pages > 1 else self.height - 30

        self.checklist_window = tkinter.Toplevel(self.root)
        self.posx = self.root.winfo_x() + (self.root.winfo_width() - self.width) / 2
        self.posy = self.root.winfo_y() + (self.root.winfo_height() - height) / 2
        self.checklist_window.geometry(
            '%dx%d+%d+%d' % (self.width, height, self.posx, self.posy))
        self.checklist_window.resizable(0, 0)
        self.checklist_window.title('PMS DA')
        self.checklist_window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.checklist_window.grab_set()

        self.button_frame_top1 = ttk.Frame(
            self.checklist_window, width=self.width, height=30)
        self.button_frame_top2 = ttk.Frame(
            self.checklist_window, width=self.width, height=30)
        self.checklist_frame = ttk.Frame(
            self.checklist_window, width=self.width, height=height - self.button_frames_height)
        self.button_frame_bottom = ttk.Frame(
            self.checklist_window, width=self.width, height=40)
        self.button_frame_top1.pack(side=tkinter.TOP)
        if self.pages > 1:
            self.button_frame_top2.pack(side=tkinter.TOP)
        self.checklist_frame.pack(side=tkinter.TOP)
        self.button_frame_bottom.pack(side=tkinter.TOP)

        if self.pages > 1:
            ttk.Separator(self.button_frame_top2, orient='horizontal').place(
                relx=0, rely=0.98, relwidth=1)
        else:
            ttk.Separator(self.button_frame_top1, orient='horizontal').place(
                relx=0, rely=0.98, relwidth=1)
        ttk.Separator(self.button_frame_bottom, orient='horizontal').place(
            relx=0, rely=0, relwidth=1)

        self.ok_button = ttk.Button(
            self.button_frame_bottom, text='OK', command=self.overwriteSelected)
        self.ok_button.place(relx=0.05, rely=0.16,
                             relwidth=0.4, relheight=0.70)
        ttk.Button(self.button_frame_bottom, text=utils.setLabel(language, 'Anuluj', 'Cancel'),
                   command=self.checklist_window.destroy).place(relx=0.55, rely=0.16, relwidth=0.4, relheight=0.70)

        self.select_all_var = tkinter.IntVar(
            value=1 if self.areAllSelected() else 0)
        self.select_page_var = tkinter.IntVar(
            value=1 if self.isPageSelected() else 0)
        ttk.Checkbutton(self.button_frame_top1, text=utils.setLabel(
            language, 'Zaznacz wszystko', 'Select all'), variable=self.select_all_var, command=self.handleSelectAll).place(relx=0.015, rely=0.1, relwidth=0.49, relheight=0.78)
        ttk.Checkbutton(self.button_frame_top2, text=utils.setLabel(
            language, 'Zaznacz stronę', 'Select page'), variable=self.select_page_var, command=self.handleSelectPage).place(relx=0.015, rely=0.1, relwidth=0.49, relheight=0.78)
        self.page_choice_var = tkinter.StringVar(
            value=str(self.page_nmb) + '/' + str(self.pages) + (u' \u25fc' if self.isPageSelected() else u' \u25fb' if self.isPageNotSelected() else u' \u25e7'))
        self.page_choice_menu = ttk.Combobox(self.button_frame_top1, textvariable=self.page_choice_var, values=list(
            str(i) + '/' + str(self.pages) + (u' \u25fc' if self.isPageSelected(i) else u' \u25fb' if self.isPageNotSelected(i) else u' \u25e7') for i in range(1, self.pages + 1)), state='readonly')
        self.page_choice_menu.bind(
            '<<ComboboxSelected>>', lambda event: self.handlePageChange())
        if self.pages > 1:
            self.total_selected_label = ttk.Label(self.button_frame_top2, text=str(
                self.getNumberOfSelected()) + '/' + str(len(self.selected_list)))
        else:
            self.total_selected_label = ttk.Label(self.button_frame_top1, text=str(
                self.getNumberOfSelected()) + '/' + str(len(self.selected_list)))
        Hovertip(self.page_choice_menu, utils.setLabel(
            language, 'Numer strony', 'Page number'))
        Hovertip(self.total_selected_label, utils.setLabel(
            language, 'Liczba wybranych pozycji', 'Number of selected items'))
        self.page_choice_menu.place(
            relx=0.6, rely=0.1, relwidth=0.385, relheight=0.78)
        self.total_selected_label.place(
            relx=0.6, rely=0.1, relwidth=0.385, relheight=0.78)

        self.canvas = tkinter.Canvas(
            self.checklist_frame, borderwidth=0, highlightthickness=0)
        self.inner_frame = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(
            self.checklist_frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.inner_frame)
        self.inner_frame.bind('<Configure>', lambda event: self.canvas.configure(
            scrollregion=self.canvas.bbox('all'), width=self.width - 25, height=height - self.button_frames_height))
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.canvas.pack(side=tkinter.LEFT)

        self.reloadChecklist()
        self.inner_frame.update()
        self.canvas.update()
        if self.inner_frame.winfo_height() > self.canvas.winfo_height():
            self.canvas.bind('<Enter>', lambda _: self.canvas.bind_all(
                '<MouseWheel>', lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')))
            self.canvas.bind(
                '<Leave>', lambda _: self.canvas.unbind_all('<MouseWheel>'))
        self.hideLoadingCursor(self.root)

    def reloadChecklist(self):
        for child in self.inner_frame.winfo_children():
            child.destroy()
        self.checkbutton_list = [None for _ in range(self.page_len)]
        offset = (self.page_nmb - 1) * self.page_len
        for i, j in zip(range(offset, self.page_len + offset), range(self.page_len)):
            if i < len(self.col_list):
                self.checkbutton_list[j] = ttk.Checkbutton(
                    self.inner_frame, text=self.col_list[i], variable=self.vars[i], command=self.handleSelectItem)
                self.checkbutton_list[j].pack(side=tkinter.TOP, anchor='w')
            else:
                ttk.Label(self.inner_frame, text='').pack(
                    side=tkinter.TOP, anchor='w')
        self.handleSelectItem(show_loading_cursor=False)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(0)

    def handleSelectAll(self):
        self.showLoadingCursor(self.checklist_window, 10000)
        if self.select_all_var.get() == 0:
            self.setVars(0)
        else:
            self.setVars(1)
        self.handleSelectItem(show_loading_cursor=False)
        self.hideLoadingCursor(self.checklist_window)

    def handleSelectPage(self):
        self.showLoadingCursor(self.checklist_window, 10000)
        offset = (self.page_nmb - 1) * self.page_len
        if self.select_page_var.get() == 0:
            self.setVars(0, offset, self.page_len + offset)
        else:
            self.setVars(1, offset, self.page_len + offset)
        self.handleSelectItem(show_loading_cursor=False)
        self.hideLoadingCursor(self.checklist_window)

    def handleSelectItem(self, show_loading_cursor=True):
        if show_loading_cursor:
            self.showLoadingCursor(self.checklist_window, 100000)
        self.selected_list = self.getVars()
        self.total_selected_label['text'] = str(
            self.getNumberOfSelected()) + '/' + str(len(self.selected_list))
        self.page_choice_var.set(str(self.page_nmb) + '/' + str(self.pages) + (
            u' \u25fc' if self.isPageSelected() else u' \u25fb' if self.isPageNotSelected() else u' \u25e7'))
        self.page_choice_menu['values'] = list(
            str(i) + '/' + str(self.pages) + (u' \u25fc' if self.isPageSelected(i) else u' \u25fb' if self.isPageNotSelected(i) else u' \u25e7') for i in range(1, self.pages + 1))
        if not self.isAnySelected():
            self.ok_button['state'] = 'disabled'
        else:
            self.ok_button['state'] = 'normal'
        if not self.areAllSelected():
            self.select_all_var.set(0)
        else:
            self.select_all_var.set(1)
        if not self.isPageSelected():
            self.select_page_var.set(0)
        else:
            self.select_page_var.set(1)
        if show_loading_cursor:
            self.hideLoadingCursor(self.checklist_window)

    def handlePageChange(self):
        current_page = int(self.page_choice_var.get().split('/')[0])
        if self.page_nmb != current_page:
            self.showLoadingCursor(self.checklist_window)
            self.page_nmb = current_page
            self.reloadChecklist()
            self.hideLoadingCursor(self.checklist_window)

    def getVars(self, i=None, j=None):
        vars = []
        i = i if not isinstance(i, type(None)) else 0
        j = j if not isinstance(j, type(None)) else len(self.vars)
        for n in range(i, j):
            if n < len(self.vars):
                vars.append(self.vars[n].get())
        return vars

    def setVars(self, val, i=None, j=None):
        i = i if not isinstance(i, type(None)) else 0
        j = j if not isinstance(j, type(None)) else len(self.vars)
        for n in range(i, j):
            if n < len(self.vars):
                self.vars[n].set(val)

    def getNumberOfSelected(self):
        selected_nmb = 0
        for i in self.selected_list:
            if i != 0:
                selected_nmb += 1
        return selected_nmb

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

    def isPageSelected(self, page_nmb=None):
        if isinstance(page_nmb, type(None)):
            page_nmb = self.page_nmb
        offset = (page_nmb - 1) * self.page_len
        for i in range(offset, self.page_len + offset):
            if i < len(self.selected_list) and self.selected_list[i] == 0:
                return False
        return True

    def isPageNotSelected(self, page_nmb=None):
        if isinstance(page_nmb, type(None)):
            page_nmb = self.page_nmb
        offset = (page_nmb - 1) * self.page_len
        for i in range(offset, self.page_len + offset):
            if i < len(self.selected_list) and self.selected_list[i] == 1:
                return False
        return True

    def overwriteSelected(self):
        self.showLoadingCursor(self.checklist_window)
        for i in range(len(self.already_selected_list)):
            self.already_selected_list[i] = self.selected_list[i]
        self.hideLoadingCursor(self.checklist_window)
        self.checklist_window.destroy()

    def showLoadingCursor(self, window, min=None):
        if isinstance(min, type(None)) or len(self.selected_list) > min:
            window.configure(cursor='wait')
            time.sleep(0.1)
            window.update()

    def hideLoadingCursor(self, window):
        window.configure(cursor='')


if __name__ == '__main__':
    pass
