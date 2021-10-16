from imports import *
from EntryWithPlaceholder import *


class ChecklistWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

    def show(self, language, col_list, already_selected_list, page_len=500):
        self.showLoadingCursor(self.root)
        self.language = language

        self.col_list = [str(i) for i in col_list]
        self.col_list_filtered = [(s, i) for s, i in zip(
            self.col_list, range(len(self.col_list)))]
        self.already_selected_list = already_selected_list
        self.selected_list = already_selected_list.copy()
        self.vars = [tkinter.IntVar(value=i) for i in already_selected_list]

        self.page_len = page_len
        self.pages = math.ceil(len(self.col_list_filtered) / self.page_len)
        self.page_nmb = 1
        self.height_adjusted = self.height if self.pages > 1 else self.height - 30

        self.checklist_window = tkinter.Toplevel(self.root)
        self.posx = self.root.winfo_x() + (self.root.winfo_width() - self.width) / 2
        self.posy = self.root.winfo_y() + (self.root.winfo_height() -
                                           self.height_adjusted) / 2
        self.checklist_window.geometry(
            '%dx%d+%d+%d' %
            (self.width, self.height_adjusted, self.posx, self.posy))
        self.checklist_window.resizable(0, 0)
        self.checklist_window.title('PMS DA')
        self.checklist_window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.checklist_window.grab_set()

        self.button_frame_top1 = ttk.Frame(
            self.checklist_window, width=self.width, height=40)
        self.button_frame_top2 = ttk.Frame(
            self.checklist_window, width=self.width, height=30)
        self.button_frame_top3 = ttk.Frame(
            self.checklist_window, width=self.width, height=30)
        self.checklist_frame_no_scroll = ttk.Frame(
            self.checklist_window, width=self.width, height=self.height - 140)
        self.checklist_frame_scroll = ttk.Frame(
            self.checklist_window, width=self.width, height=self.height - 140)
        self.no_records_frame = ttk.Frame(
            self.checklist_window,
            width=self.width,
            height=self.height - 140)
        self.button_frame_bottom = ttk.Frame(
            self.checklist_window, width=self.width, height=40)

        self.no_records_frame.pack_propagate(0)
        self.checklist_frame_no_scroll.pack_propagate(0)
        self.checklist_frame_scroll.pack_propagate(0)

        ttk.Label(
            self.no_records_frame,
            text=utils.setLabel(
                self.language,
                'Brak rekordów',
                'No records')).pack(
            side=tkinter.TOP,
            pady=5)
        self.top_sep_1 = ttk.Separator(
            self.button_frame_top2, orient='horizontal')
        self.top_sep_2 = ttk.Separator(
            self.button_frame_top3, orient='horizontal')
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
        ttk.Checkbutton(self.button_frame_top2, text=utils.setLabel(
            language, 'Zaznacz wszystko', 'Select all'), variable=self.select_all_var, command=self.handleSelectAll).place(relx=0.015, rely=0.1, relwidth=0.49, relheight=0.78)
        ttk.Checkbutton(self.button_frame_top3, text=utils.setLabel(
            language, 'Zaznacz stronę', 'Select page'), variable=self.select_page_var, command=self.handleSelectPage).place(relx=0.015, rely=0.1, relwidth=0.49, relheight=0.78)

        self.page_choice_var = tkinter.StringVar(
            value=str(self.page_nmb) + '/' + str(self.pages) + (u' \u25fc' if self.isPageSelected() else u' \u25fb' if self.isPageNotSelected() else u' \u25e7'))
        self.page_choice_menu = ttk.Combobox(self.button_frame_top2, textvariable=self.page_choice_var, values=list(
            str(i) + '/' + str(self.pages) + (u' \u25fc' if self.isPageSelected(i) else u' \u25fb' if self.isPageNotSelected(i) else u' \u25e7') for i in range(1, self.pages + 1)), state='readonly')
        self.page_choice_menu.bind(
            '<<ComboboxSelected>>',
            lambda event: self.handlePageChange())

        self.total_selected_label_1 = ttk.Label(self.button_frame_top2, text=str(
            self.getNumberOfSelected()) + '/' + str(len(self.col_list_filtered)), anchor=tkinter.E)
        self.total_selected_label_2 = ttk.Label(self.button_frame_top3, text=str(
            self.getNumberOfSelected()) + '/' + str(len(self.col_list_filtered)), anchor=tkinter.E)

        Hovertip(self.page_choice_menu, utils.setLabel(
            language, 'Numer strony', 'Page number'))
        Hovertip(self.total_selected_label_1, utils.setLabel(
            language, 'Liczba wybranych pozycji', 'Number of selected items'))
        Hovertip(self.total_selected_label_2, utils.setLabel(
            language, 'Liczba wybranych pozycji', 'Number of selected items'))

        if self.pages > 1:
            self.top_sep_2.place(relx=0, rely=0.98, relwidth=1)
            self.page_choice_menu.place(
                relx=0.555, rely=0.1, relwidth=0.43, relheight=0.78)
            self.total_selected_label_2.place(
                relx=0.555, rely=0.1, relwidth=0.42, relheight=0.78)
        else:
            self.top_sep_1.place(relx=0, rely=0.98, relwidth=1)
            self.total_selected_label_1.place(
                relx=0.555, rely=0.1, relwidth=0.42, relheight=0.78)

        self.previous_search = None
        self.search_var = tkinter.StringVar()
        self.search_entry = EntryWithPlaceholder(
            self.button_frame_top1,
            self.search_var,
            0.015,
            0.1,
            0.49,
            0.78,
            utils.setLabel(
                language,
                'Szukaj...',
                'Search...'))
        ttk.Button(
            self.button_frame_top1,
            text=utils.setLabel(
                language,
                'Szukaj',
                'Search'),
            command=self.search).place(
            relx=0.555,
            rely=0.1,
            relwidth=0.43,
            relheight=0.78)

        self.canvas_scroll = tkinter.Canvas(
            self.checklist_frame_scroll,
            borderwidth=0,
            highlightthickness=0)
        self.inner_frame_scroll = ttk.Frame(self.canvas_scroll)
        self.scrollbar = ttk.Scrollbar(
            self.checklist_frame_scroll, orient='vertical', command=self.canvas_scroll.yview)
        self.canvas_scroll.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_scroll.create_window(
            (0, 0), window=self.inner_frame_scroll)
        self.inner_frame_scroll.bind(
            '<Configure>',
            lambda event: self.canvas_scroll.configure(
                scrollregion=self.canvas_scroll.bbox('all'),
                width=self.width - 25,
                height=self.height - 140))
        self.canvas_scroll.bind('<Enter>', lambda _: self.canvas_scroll.bind_all(
            '<MouseWheel>', lambda event: self.canvas_scroll.yview_scroll(int(-1 * (event.delta / 120)), 'units')))
        self.canvas_scroll.bind(
            '<Leave>', lambda _: self.canvas_scroll.unbind_all('<MouseWheel>'))
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.canvas_scroll.pack(side=tkinter.LEFT)

        self.reloadChecklist()
        self.checklist_frame_no_scroll.update()
        self.inner_frame_scroll.update()
        self.canvas_scroll.update()

        self.button_frame_top1.pack(side=tkinter.TOP)
        self.button_frame_top2.pack(side=tkinter.TOP)
        if self.pages > 1:
            self.button_frame_top3.pack(side=tkinter.TOP)
        if len(self.col_list_filtered) == 0:
            self.frame_state = 'empty'
            self.no_records_frame.pack(side=tkinter.TOP)
        elif self.page_size > self.height - 140:
            self.frame_state = 'scroll'
            self.checklist_frame_scroll.pack(side=tkinter.TOP)
        else:
            self.checklist_frame_no_scroll.pack(side=tkinter.TOP)
            self.frame_state = 'no_scroll'
        self.button_frame_bottom.pack(side=tkinter.TOP)

        self.hideLoadingCursor(self.root)

    def search(self):
        self.showLoadingCursor(self.checklist_window, 10000)
        if self.search_entry.state == 'empty':
            self.col_list_filtered = [(s, i) for s, i in zip(
                self.col_list, range(len(self.col_list)))]
        else:
            filter = self.search_var.get().lower()
            self.col_list_filtered = [(s, i) for s, i in zip(
                self.col_list, range(len(self.col_list))) if filter in s.lower()]

        if self.previous_search is None:
            self.previous_search = self.search_var.get().lower()
        elif self.previous_search != self.search_var.get().lower():
            self.previous_search = self.search_var.get().lower()
            self.page_nmb = 1
        self.pages = math.ceil(len(self.col_list_filtered) / self.page_len)
        self.height_adjusted = self.height if self.pages > 1 else self.height - 30

        self.reloadChecklist()
        self.checklist_frame_no_scroll.update()
        self.inner_frame_scroll.update()
        self.canvas_scroll.update()

        self.checklist_window.geometry(
            '%dx%d' %
            (self.width, self.height_adjusted))

        self.top_sep_1.place_forget()
        self.top_sep_2.place_forget()
        self.page_choice_menu.place_forget()
        self.total_selected_label_1.place_forget()
        self.total_selected_label_2.place_forget()

        if self.pages > 1:
            self.top_sep_2.place(relx=0, rely=0.98, relwidth=1)
            self.page_choice_menu.place(
                relx=0.555, rely=0.1, relwidth=0.43, relheight=0.78)
            self.total_selected_label_2.place(
                relx=0.555, rely=0.1, relwidth=0.42, relheight=0.78)
        else:
            self.top_sep_1.place(relx=0, rely=0.98, relwidth=1)
            self.total_selected_label_1.place(
                relx=0.555, rely=0.1, relwidth=0.42, relheight=0.78)

        self.button_frame_top1.pack_forget()
        self.button_frame_top2.pack_forget()
        self.button_frame_top3.pack_forget()
        self.checklist_frame_no_scroll.pack_forget()
        self.checklist_frame_scroll.pack_forget()
        self.no_records_frame.pack_forget()
        self.button_frame_bottom.pack_forget()

        self.button_frame_top1.pack(side=tkinter.TOP)
        self.button_frame_top2.pack(side=tkinter.TOP)
        if self.pages > 1:
            self.button_frame_top3.pack(side=tkinter.TOP)
        if len(self.col_list_filtered) == 0:
            self.frame_state = 'empty'
            self.no_records_frame.pack(side=tkinter.TOP)
        elif self.page_size > self.height - 140:
            self.frame_state = 'scroll'
            self.checklist_frame_scroll.pack(side=tkinter.TOP)
        else:
            self.frame_state = 'no_scroll'
            self.checklist_frame_no_scroll.pack(side=tkinter.TOP)
        self.button_frame_bottom.pack(side=tkinter.TOP)

        self.hideLoadingCursor(self.checklist_window)

    def reloadChecklist(self):
        for child in self.checklist_frame_no_scroll.winfo_children():
            child.destroy()
        for child in self.inner_frame_scroll.winfo_children():
            child.destroy()

        self.checkbutton_list_no_scroll = [None for _ in range(self.page_len)]
        self.checkbutton_list_scroll = [None for _ in range(self.page_len)]
        offset = (self.page_nmb - 1) * self.page_len
        counter = 0
        for i, j in zip(range(offset, self.page_len + offset),
                        range(min(len(self.col_list_filtered), self.page_len))):
            if i < len(self.col_list_filtered):
                counter += 1
                self.checkbutton_list_no_scroll[j] = ttk.Checkbutton(
                    self.checklist_frame_no_scroll,
                    text=self.col_list_filtered[i][0],
                    variable=self.vars[
                        self.col_list_filtered[i][1]],
                    command=self.handleSelectItem)
                self.checkbutton_list_scroll[j] = ttk.Checkbutton(
                    self.inner_frame_scroll, text=self.col_list_filtered[i][0], variable=self.vars[self.col_list_filtered[i][1]], command=self.handleSelectItem)
                self.checkbutton_list_no_scroll[j].pack(
                    side=tkinter.TOP, anchor='w', padx=(4, 0))
                self.checkbutton_list_scroll[j].pack(
                    side=tkinter.TOP, anchor='w', padx=(4, 0))

        self.handleSelectItem(show_loading_cursor=False)
        if self.page_nmb == self.pages and counter < self.page_len:
            self.canvas_scroll.yview_moveto(0.5)
        self.canvas_scroll.update_idletasks()
        self.canvas_scroll.yview_moveto(0)

        self.page_size = 0
        if not self.checkbutton_list_scroll[0] is None:
            self.page_size = self.checkbutton_list_scroll[0].winfo_height(
            ) * counter

    def handleSelectAll(self):
        self.showLoadingCursor(self.checklist_window, 10000)
        if self.select_all_var.get() == 0:
            self.setAllCurrentVars(0)
        else:
            self.setAllCurrentVars(1)
        self.handleSelectItem(show_loading_cursor=False)
        self.hideLoadingCursor(self.checklist_window)

    def handleSelectPage(self):
        self.showLoadingCursor(self.checklist_window, 10000)
        if self.select_page_var.get() == 0:
            self.setCurrentPageVars(0)
        else:
            self.setCurrentPageVars(1)
        self.handleSelectItem(show_loading_cursor=False)
        self.hideLoadingCursor(self.checklist_window)

    def handleSelectItem(self, show_loading_cursor=True):
        if show_loading_cursor:
            self.showLoadingCursor(self.checklist_window, 100000)
        self.selected_list = self.getVars()
        self.total_selected_label_1['text'] = str(
            self.getNumberOfSelected()) + '/' + str(len(self.col_list_filtered))
        self.total_selected_label_2['text'] = str(
            self.getNumberOfSelected()) + '/' + str(len(self.col_list_filtered))
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

            if len(self.col_list_filtered) == 0:
                state = 'empty'
            elif self.page_size > self.height - 140:
                state = 'scroll'
            else:
                state = 'no_scroll'

            if state != self.frame_state:
                self.frame_state = state

                self.button_frame_top1.pack_forget()
                self.button_frame_top2.pack_forget()
                self.button_frame_top3.pack_forget()
                self.checklist_frame_no_scroll.pack_forget()
                self.checklist_frame_scroll.pack_forget()
                self.no_records_frame.pack_forget()
                self.button_frame_bottom.pack_forget()

                self.button_frame_top1.pack(side=tkinter.TOP)
                self.button_frame_top2.pack(side=tkinter.TOP)
                if self.pages > 1:
                    self.button_frame_top3.pack(side=tkinter.TOP)
                if len(self.col_list_filtered) == 0:
                    self.no_records_frame.pack(side=tkinter.TOP)
                elif self.page_size > self.height - 140:
                    self.checklist_frame_scroll.pack(side=tkinter.TOP)
                else:
                    self.checklist_frame_no_scroll.pack(side=tkinter.TOP)
                self.button_frame_bottom.pack(side=tkinter.TOP)

            self.hideLoadingCursor(self.checklist_window)

    def getVars(self, i=None, j=None):
        vars = []
        i = i if not isinstance(i, type(None)) else 0
        j = j if not isinstance(j, type(None)) else len(self.vars)
        for n in range(i, j):
            if n < len(self.vars):
                vars.append(self.vars[n].get())
        return vars

    def setCurrentPageVars(self, val):
        offset = (self.page_nmb - 1) * self.page_len
        for i in range(offset, offset + self.page_len):
            if i < len(self.col_list_filtered):
                self.vars[self.col_list_filtered[i][1]].set(val)

    def setAllCurrentVars(self, val):
        for v in self.col_list_filtered:
            self.vars[v[1]].set(val)

    def getNumberOfSelected(self):
        selected_nmb = 0
        for v in self.col_list_filtered:
            if self.selected_list[v[1]] != 0:
                selected_nmb += 1
        return selected_nmb

    def isAnySelected(self):
        for v in self.col_list_filtered:
            if self.selected_list[v[1]] != 0:
                return True
        return False

    def areAllSelected(self):
        for v in self.col_list_filtered:
            if self.selected_list[v[1]] == 0:
                return False
        return True

    def isPageSelected(self, page_nmb=None):
        if isinstance(page_nmb, type(None)):
            page_nmb = self.page_nmb
        offset = (page_nmb - 1) * self.page_len
        for i in range(offset, self.page_len + offset):
            if i < len(
                    self.col_list_filtered) and self.selected_list[self.col_list_filtered[i][1]] == 0:
                return False
        return True

    def isPageNotSelected(self, page_nmb=None):
        if isinstance(page_nmb, type(None)):
            page_nmb = self.page_nmb
        offset = (page_nmb - 1) * self.page_len
        for i in range(offset, self.page_len + offset):
            if i < len(
                    self.col_list_filtered) and self.selected_list[self.col_list_filtered[i][1]] == 1:
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
