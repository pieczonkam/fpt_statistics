from imports import *


class SettingsWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

    def show(self, language, fun):
        self.language = language
        self.show_error = False

        self.bars_nmb = Globals.bars_nmb
        self.bars_resolution = Globals.bars_resolution
        self._3d_bars_nmb = Globals.chartA_bars_nmb
        self.transition_expected_time = Globals.transition_expected_time
        self.operation_expected_time = Globals.operation_expected_time
        self.primary_color = Globals.primary_color
        self.secondary_color = Globals.secondary_color

        self.bars_nmb_var = tkinter.StringVar(value=self.bars_nmb)
        self.bars_resolution_var = tkinter.StringVar(
            value=self.bars_resolution)
        self._3d_bars_nmb_var = tkinter.StringVar(value=self._3d_bars_nmb)
        self.transition_expected_time_var = tkinter.StringVar(
            value=self.transition_expected_time)
        self.operation_expected_time_var = tkinter.StringVar(
            value=self.operation_expected_time)

        self.settings_window = tkinter.Toplevel(self.root)
        self.entries_frame = ttk.Frame(self.settings_window)
        self.others_frame = ttk.Frame(self.settings_window)
        self.error_frame = ttk.Frame(self.settings_window, style='AA.TFrame')
        self.button_frame = ttk.Frame(self.settings_window)

        self.button_frame_height = 40
        self.error_frame_height = 30
        self.others_frame_height = 95
        self.offset = 10
        self.entries_frame_height = self.height - self.button_frame_height - self.error_frame_height - self.others_frame_height - self.offset

        width = self.getWidth()
        height = self.getHeight()
        self.posx = self.root.winfo_x() + (self.root.winfo_width() - width) / 2
        self.posy = self.root.winfo_y() + (self.root.winfo_height() - height) / 2
        self.settings_window.geometry(
            '%dx%d+%d+%d' %
            (width, height, self.posx, self.posy))
        self.settings_window.resizable(0, 0)
        self.settings_window.title(
            utils.setLabel(
                language,
                'PMS Data Analysis - Ustawienia',
                'PMS Data Analysis - Settings'))
        self.settings_window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.settings_window.grab_set()

        self.placeFrames()

        # Button frame
        ttk.Separator(
            self.button_frame,
            orient='horizontal').place(
            relx=0,
            rely=0,
            relwidth=1)

        ttk.Button(
            self.button_frame,
            text='OK',
            command=lambda: self.overwriteVars(
                fun)).place(
            relx=0.05,
            rely=0.16,
            relwidth=0.27,
            relheight=0.7)
        ttk.Button(
            self.button_frame,
            text='Reset',
            command=self.resetVars).place(relx=0.365, rely=0.16, relwidth=0.27, relheight=0.7)
        ttk.Button(
            self.button_frame,
            text=utils.setLabel(
                language,
                'Anuluj',
                'Cancel'),
            command=self.settings_window.destroy).place(
            relx=0.68,
            rely=0.16,
            relwidth=0.27,
            relheight=0.7)

        # Others frame
        ttk.Separator(self.others_frame, orient='horizontal').place(relx=0, rely=0, relwidth=1)

        ttk.Label(self.others_frame, text=utils.setLabel(language, 'Inne', 'Others'), style='Header.TLabel', anchor='center').place(x=0, rely=0.1, relwidth=1)
        ttk.Label(self.others_frame, text=utils.setLabel(language, 'Kolor główny: ', 'Primary color: ')).place(x=10, rely=0.39, relwidth=0.49)
        ttk.Label(self.others_frame, text=utils.setLabel(language, 'Kolor pomocniczy: ', 'Secondary color: ')).place(x=10, rely=0.68, relwidth=0.49)

        self.canvas_size = 20
        self.primary_color_canvas = tkinter.Canvas(self.others_frame)
        self.secondary_color_canvas = tkinter.Canvas(self.others_frame)
        self.primary_color_canvas.place(x=9 + (width - 20) * 0.51, rely=0.39, width=self.canvas_size, height=self.canvas_size)
        self.secondary_color_canvas.place(x=9 + (width - 20) * 0.51, rely=0.68, width=self.canvas_size, height=self.canvas_size)

        self.primary_color_canvas.create_rectangle(2, 2, self.canvas_size - 2, self.canvas_size - 2, outline='#000', fill=self.primary_color, width=2)
        self.secondary_color_canvas.create_rectangle(2, 2, self.canvas_size - 2, self.canvas_size - 2, outline='#000', fill=self.secondary_color, width=2)

        ttk.Button(self.others_frame, text=utils.setLabel(language, 'Wybierz kolor', 'Choose color'), command=lambda: self.setColor('primary')).place(x=19 + (width - 20) * 0.51 + self.canvas_size, rely=0.37, width=(width - 20) * 0.35 - (10 + self.canvas_size), height=self.canvas_size + 0.04 * self.others_frame_height)
        ttk.Button(self.others_frame, text=utils.setLabel(language, 'Wybierz kolor', 'Choose color'), command=lambda: self.setColor('secondary')).place(x=19 + (width - 20) * 0.51 + self.canvas_size, rely=0.66, width=(width - 20) * 0.35 - (10 + self.canvas_size), height=self.canvas_size + 0.04 * self.others_frame_height)

        # Error frame
        self.error_label = ttk.Label(
            self.error_frame,
            text=utils.setLabel(
                language,
                'Błąd: Podano niepoprawne wartości',
                'Error: Inserted incorrect values'),
            style='Error.TLabel',
            anchor='center')
        self.error_label.place(
            relx=0.05,
            rely=0.1,
            relwidth=0.9,
            relheight=0.8)
        ttk.Style().configure('Error.TLabel', foreground='red')

        # Entries frame
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Histogram Czasu Przejścia',
                'Transition Time Histogram'),
            style='Header.TLabel',
            anchor='center').place(
            relx=0,
            rely=0,
            relwidth=1)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Ilość słupków na histogramie: ',
                'Number of bars on the histogram: ')).place(
            relx=0,
            rely=0.125,
            relwidth=0.49)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Rozdzielczość słupków: ',
                'Bars resolution: ')).place(
            relx=0,
            rely=0.25,
            relwidth=0.49)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Wykres 3D',
                '3D Chart'),
            style='Header.TLabel',
            anchor='center').place(
            relx=0,
            rely=0.375,
            relwidth=1)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Ilość słupków na wykresie:',
                'Number of bars on the chart:')).place(
            relx=0,
            rely=0.5,
            relwidth=0.49)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Wszystkie Wykresy',
                'All Charts'),
            style='Header.TLabel',
            anchor='center').place(
            relx=0,
            rely=0.625,
            relwidth=1)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Projektowy czas przejścia: ',
                'Expected transition time: ')).place(
            relx=0,
            rely=0.75,
            relwidth=0.49)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Projektowy czas operacji: ',
                'Expected operation time: ')).place(
            relx=0,
            rely=0.875,
            relwidth=0.49)

        self.bars_nmb_entry = ttk.Entry(
            self.entries_frame,
            textvariable=self.bars_nmb_var,
            justify='right')
        self.bars_resolution_entry = ttk.Entry(
            self.entries_frame,
            textvariable=self.bars_resolution_var,
            justify='right')
        self._3d_bars_nmb_entry = ttk.Entry(
            self.entries_frame,
            textvariable=self._3d_bars_nmb_var,
            justify='right')
        self.transition_expected_time_entry = ttk.Entry(
            self.entries_frame,
            textvariable=self.transition_expected_time_var,
            justify='right')
        self.operation_expected_time_entry = ttk.Entry(
            self.entries_frame,
            textvariable=self.operation_expected_time_var,
            justify='right')
        self.bars_nmb_entry.place(relx=0.51, rely=0.125, relwidth=0.35)
        self.bars_resolution_entry.place(relx=0.51, rely=0.25, relwidth=0.35)
        self._3d_bars_nmb_entry.place(relx=0.51, rely=0.5, relwidth=0.35)
        self.transition_expected_time_entry.place(
            relx=0.51, rely=0.75, relwidth=0.35)
        self.operation_expected_time_entry.place(
            relx=0.51, rely=0.875, relwidth=0.35)

        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'sekund',
                'seconds')).place(
            relx=0.87,
            rely=0.25,
            relwidth=0.13)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'sekund',
                'seconds')).place(
            relx=0.87,
            rely=0.75,
            relwidth=0.13)
        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'sekund',
                'seconds')).place(
            relx=0.87,
            rely=0.875,
            relwidth=0.13)

        ttk.Style().configure('Header.TLabel', font=(None, 9, 'bold'))

    def setColor(self, mode):
        if mode == 'primary':
            color = self.primary_color
            canvas = self.primary_color_canvas
        elif mode == 'secondary':
            color = self.secondary_color
            canvas = self.secondary_color_canvas
        else:
            return

        chosen_color = askcolor(color=color, title='PMS Data Analysis', parent=self.settings_window)[1]

        if not isinstance(chosen_color, type(None)):
            canvas.delete('all')
            canvas.create_rectangle(2, 2, self.canvas_size - 2, self.canvas_size - 2, outline='#000', fill=chosen_color, width=2)
            if mode == 'primary':
                self.primary_color = chosen_color
            else:
                self.secondary_color = chosen_color

    def resetVars(self):
        self.bars_nmb_var.set(Globals.bars_nmb_default)
        self.bars_resolution_var.set(Globals.bars_resolution_default)
        self._3d_bars_nmb_var.set(Globals.chartA_bars_nmb_default)
        self.transition_expected_time_var.set(Globals.transition_expected_time_default)
        self.operation_expected_time_var.set(Globals.operation_expected_time_default)
        self.primary_color = Globals.primary_color_default
        self.secondary_color = Globals.secondary_color_default

        self.primary_color_canvas.delete('all')
        self.secondary_color_canvas.delete('all')
        self.primary_color_canvas.create_rectangle(2, 2, self.canvas_size - 2, self.canvas_size - 2, outline='#000', fill=self.primary_color, width=2)
        self.secondary_color_canvas.create_rectangle(2, 2, self.canvas_size - 2, self.canvas_size - 2, outline='#000', fill=self.secondary_color, width=2)

        if self.show_error:
            self.show_error = False
            self.setGeometry()
            self.placeForgetFrames()
            self.placeFrames()

    def overwriteVars(self, fun):
        try:
            self.bars_nmb = int(self.bars_nmb_var.get())
            self.bars_resolution = int(self.bars_resolution_var.get())
            self._3d_bars_nmb = int(self._3d_bars_nmb_var.get())
            self.transition_expected_time = int(
                self.transition_expected_time_var.get())
            self.operation_expected_time = int(
                self.operation_expected_time_var.get())

            if self.bars_nmb <= 0 or self.bars_resolution <= 0 or self._3d_bars_nmb <= 0 or self.transition_expected_time <= 0 or self.operation_expected_time <= 0:
                raise Exception

            if self.bars_nmb != Globals.bars_nmb or self.bars_resolution != Globals.bars_resolution or self._3d_bars_nmb != Globals.chartA_bars_nmb or self.transition_expected_time != Globals.transition_expected_time or self.operation_expected_time != Globals.operation_expected_time or self.primary_color != Globals.primary_color or self.secondary_color != Globals.secondary_color:
                Globals.bars_nmb = self.bars_nmb
                Globals.bars_resolution = self.bars_resolution
                Globals.chartA_bars_nmb = self._3d_bars_nmb
                Globals.transition_expected_time = self.transition_expected_time
                Globals.operation_expected_time = self.operation_expected_time
                Globals.primary_color = self.primary_color
                Globals.secondary_color = self.secondary_color
                self.settings_window.destroy()
                fun()
            else:
                self.settings_window.destroy()
        except BaseException:
            if not self.show_error:
                self.show_error = True
                self.setGeometry()
                self.placeForgetFrames()
                self.placeFrames()

    def getWidth(self):
        if self.language == 'english':
            return self.width + 20
        return self.width

    def getHeight(self):
        if self.show_error:
            return self.height
        return self.height - self.error_frame_height

    def setGeometry(self):
        self.settings_window.geometry(
            '%dx%d' %
            (self.getWidth(), self.getHeight()))

    def placeFrames(self):
        width = self.getWidth()

        if self.show_error:
            self.entries_frame.place(x=10, y=self.offset, width=width - 20, height=self.entries_frame_height)
            self.others_frame.place(x=0, y=self.offset + self.entries_frame_height, width=width, height=self.others_frame_height)
            self.error_frame.place(x=0, y=self.offset + self.entries_frame_height + self.others_frame_height, width=width, height=self.error_frame_height)
            self.button_frame.place(x=0, y=self.offset + self.entries_frame_height + self.others_frame_height + self.error_frame_height, width=width, height=self.button_frame_height)
        else:
            self.entries_frame.place(x=10, y=self.offset, width=width - 20, height=self.entries_frame_height)
            self.others_frame.place(x=0, y=self.offset + self.entries_frame_height, width=width, height=self.others_frame_height)
            self.button_frame.place(x=0, y=self.offset + self.entries_frame_height + self.others_frame_height, width=width, height=self.button_frame_height)

    def placeForgetFrames(self):
        self.entries_frame.place_forget()
        self.others_frame.place_forget()
        self.error_frame.place_forget()
        self.button_frame.place_forget()
    

if __name__ == '__main__':
    pass
