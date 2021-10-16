from imports import *


class MenuBar:
    def __init__(self, window):
        self.window = window
        self.menubar = tkinter.Menu(self.window)
        self.window.config(menu=self.menubar)

    def clear(self):
        self.menubar.destroy()

    def addMenu(self, main_label, main_command=None,
                labels=None, commands=None):
        menu = tkinter.Menu(self.menubar, tearoff=0)
        if not isinstance(labels, type(None)) and not isinstance(
                commands, type(None)):
            for label, command in zip(labels, commands):
                menu.add_command(label=label, command=command)

        if isinstance(main_command, type(None)):
            self.menubar.add_cascade(label=main_label, menu=menu)
        else:
            self.menubar.add_cascade(label=main_label, command=main_command)


if __name__ == '__main__':
    pass
