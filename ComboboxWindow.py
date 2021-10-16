from imports import *


class ComboboxWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

    def show(self, language, item_list, already_selected_items):
        self.showLoadingCursor(self.root)
        self.item_list = [str(item_list[i]) for i in range(len(item_list))]
        self.already_selected_items = already_selected_items
        self.selected_items = already_selected_items.copy()

        self.combobox_window = tkinter.Toplevel(self.root)
        self.posx = self.root.winfo_x() + (self.root.winfo_width() - self.width) / 2
        self.posy = self.root.winfo_y() + (self.root.winfo_height() - self.height) / 2
        self.combobox_window.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.posx, self.posy))
        self.combobox_window.resizable(0, 0)
        self.combobox_window.title('PMS DA')
        self.combobox_window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.combobox_window.grab_set()

        self.combobox_frame = ttk.Frame(self.combobox_window)
        self.button_frame = ttk.Frame(self.combobox_window)
        self.combobox_frame.place(
            x=0, y=0, width=self.width, height=self.height - 40)
        self.button_frame.place(x=0, y=self.height - 40,
                                width=self.width, height=40)

        ttk.Separator(self.button_frame, orient='horizontal').place(
            relx=0, rely=0, relwidth=1)

        ttk.Button(self.button_frame, text='OK', command=self.overwriteRange).place(relx=0.05, rely=0.16,
                                                                                    relwidth=0.4, relheight=0.70)
        ttk.Button(self.button_frame, text=utils.setLabel(language, 'Anuluj', 'Cancel'), command=self.combobox_window.destroy).place(relx=0.55, rely=0.16,
                                                                                                                                     relwidth=0.4, relheight=0.70)

        ttk.Label(self.combobox_frame, text=utils.setLabel(language, 'Od: ', 'From: ')).place(
            relx=0.03, rely=0.11, relwidth=0.19, relheight=0.34)
        ttk.Label(self.combobox_frame, text=utils.setLabel(language, 'Do: ', 'To:   ')).place(
            relx=0.03, rely=0.55, relwidth=0.19, relheight=0.34)
        self.var1 = tkinter.StringVar(
            value=self.item_list[self.selected_items[0]])
        self.var2 = tkinter.StringVar(
            value=self.item_list[self.selected_items[1]])
        self.combobox1 = ttk.Combobox(
            self.combobox_frame, textvariable=self.var1, values=self.item_list, state='readonly')
        self.combobox2 = ttk.Combobox(
            self.combobox_frame, textvariable=self.var2, values=self.item_list, state='readonly')
        self.combobox1.bind('<<ComboboxSelected>>',
                            lambda event: self.selectItem1(language))
        self.combobox2.bind('<<ComboboxSelected>>',
                            lambda event: self.selectItem2(language))
        self.combobox1.place(relx=0.22, rely=0.11,
                             relwidth=0.75, relheight=0.34)
        self.combobox2.place(relx=0.22, rely=0.55,
                             relwidth=0.75, relheight=0.34)

        self.hideLoadingCursor(self.root)

    def selectItem1(self, language):
        selected_item = self.var1.get()
        selected_item_idx = self.item_list.index(selected_item)
        if self.selected_items[0] != selected_item_idx:
            self.selected_items[0] = selected_item_idx
            if self.selected_items[1] < selected_item_idx:
                self.selected_items[1] = selected_item_idx
                self.var2.set(self.item_list[self.selected_items[1]])

    def selectItem2(self, language):
        selected_item = self.var2.get()
        selected_item_idx = self.item_list.index(selected_item)
        if self.selected_items[1] != selected_item_idx:
            self.selected_items[1] = selected_item_idx
            if self.selected_items[0] > selected_item_idx:
                self.selected_items[0] = selected_item_idx
                self.var1.set(self.item_list[self.selected_items[0]])

    def overwriteRange(self):
        self.already_selected_items[0] = self.selected_items[0]
        self.already_selected_items[1] = self.selected_items[1]
        self.combobox_window.destroy()

    def showLoadingCursor(self, window):
        window.configure(cursor='wait')
        time.sleep(0.1)
        window.update()

    def hideLoadingCursor(self, window):
        window.configure(cursor='')


if __name__ == '__main__':
    pass
