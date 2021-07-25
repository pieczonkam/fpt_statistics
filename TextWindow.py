from imports import *


class TextWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

    def show(self, data_dict):
        self.showLoadingCursor(self.root)
        self.text_window = tkinter.Toplevel(self.root)
        self.posx = self.root.winfo_x() + (self.root.winfo_width() - self.width) / 2
        self.posy = self.root.winfo_y() + (self.root.winfo_height() - self.height) / 2
        self.text_window.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.posx, self.posy))
        self.text_window.resizable(0, 0)
        self.text_window.title('PMS DA')
        self.text_window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.text_window.grab_set()

        self.text_frame = ttk.Frame(self.text_window)
        self.button_frame = ttk.Frame(self.text_window)
        self.text_frame.place(x=0, y=0, width=self.width,
                              height=self.height - 40)
        self.button_frame.place(x=0, y=self.height - 40,
                                width=self.width, height=40)

        ttk.Separator(self.button_frame, orient='horizontal').place(
            relx=0, rely=0, relwidth=1)
        ttk.Button(self.button_frame, text='OK', command=self.text_window.destroy).place(
            relx=0.77, rely=0.16, relwidth=0.2, relheight=0.7)

        self.text = scrolledtext.ScrolledText(
            self.text_frame, font=('Courier', 12))
        self.text.place(relx=0, rely=0, relwidth=1, relheight=1)

        key_max_len = 0
        for key in data_dict.keys():
            if len(key) > key_max_len:
                key_max_len = len(key)
        for key, value in data_dict.items():
            delimiter = ':' if key.replace(' ', '') != '' else ''
            if isinstance(value, list):
                self.text.insert(tkinter.INSERT, key + delimiter + '\n')
                for v in value:
                    self.text.insert(tkinter.INSERT, self.addSpaces(
                        '', key_max_len + 2) + str(v) + '\n')
                self.text.insert(tkinter.INSERT, '\n')
            else:
                self.text.insert(tkinter.INSERT, self.addSpaces(
                    key + delimiter, key_max_len + 2) + str(value) + '\n')
        self.text.configure(state=tkinter.DISABLED)

        self.hideLoadingCursor(self.root)

    def addSpaces(self, text, expected_len):
        spaces = ''.join([' ' for _ in range(expected_len - len(text))])
        return text + spaces

    def showLoadingCursor(self, window, min=None):
        if isinstance(min, type(None)) or len(self.selected_list) > min:
            window.configure(cursor='wait')
            time.sleep(0.1)
            window.update()

    def hideLoadingCursor(self, window):
        window.configure(cursor='')


if __name__ == '__main__':
    pass
