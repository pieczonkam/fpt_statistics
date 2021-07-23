from imports import *


class TextWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

    def show(self, text_dict):
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
        self.text_frame.place(x=0, y=0, width=self.width, height=self.height - 40)
        self.button_frame.place(x=0, y=self.height - 40, width=self.width, height=40)

        ttk.Separator(self.button_frame, orient='horizontal').place(relx=0, rely=0, relwidth=1)
        ttk.Button(self.button_frame, text='OK', command=self.text_window.destroy).place(relx=0.55, rely=0.16, relwidth=0.4, relheight=0.7)

        self.text = scrolledtext.ScrolledText(self.text_frame, font=('Courier', 12))
        self.text.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        key_max_len = 0
        for key in text_dict.keys():
            if len(key) > key_max_len:
                key_max_len = len(key)
        for key, value in text_dict.items():
            if isinstance(value, list):
                self.text.insert(tkinter.INSERT, key + '\n')
                for v in value:
                    self.text.insert(tkinter.INSERT, self.addSpaces('', key_max_len + 1) + str(v) + '\n')
                self.text.insert(tkinter.INSERT, '\n')
            else:
                self.text.insert(tkinter.INSERT, self.addSpaces(key, key_max_len + 1) + str(value) + '\n')
        self.text.configure(state=tkinter.DISABLED)

    def addSpaces(self, text, expected_len):
        spaces = ''.join([' ' for _ in range(expected_len - len(text))])
        return text + spaces

if __name__ == '__main__':
    pass

