from imports import *


class SettingsWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

    def show(self, language, fun):
        self.bars_nmb = Globals.bars_nmb
        self.bars_resolution = Globals.bars_resolution
        self._3d_bars_nmb = Globals.chartA_bars_nmb
        self.transition_expected_time = Globals.transition_expected_time
        self.operation_expected_time = Globals.operation_expected_time

        if language == 'english':
            width = self.width + 20
        else:
            width = self.width
        self.settings_window = tkinter.Toplevel(self.root)
        self.posx = self.root.winfo_x() + (self.root.winfo_width() - width) / 2
        self.posy = self.root.winfo_y() + (self.root.winfo_height() - self.height) / 2
        self.settings_window.geometry(
            '%dx%d+%d+%d' %
            (width, self.height, self.posx, self.posy))
        self.settings_window.resizable(0, 0)
        self.settings_window.title(
            utils.setLabel(
                language,
                'PMS Data Analysis - Ustawienia',
                'PMS Data Analysis - Settings'))
        self.settings_window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.settings_window.grab_set()

        self.entries_frame = ttk.Frame(self.settings_window)
        self.error_frame = ttk.Frame(self.settings_window, style='AA.TFrame')
        self.button_frame = ttk.Frame(self.settings_window)
        self.entries_frame.place(
            x=10,
            y=10,
            width=width - 20,
            height=self.height - 80)
        self.error_frame.place(x=0, y=self.height - 70, width=width, height=30)
        self.button_frame.place(
            x=0,
            y=self.height - 40,
            width=width,
            height=40)

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
                fun,
                language)).place(
            relx=0.05,
            rely=0.16,
            relwidth=0.4,
            relheight=0.7)
        ttk.Button(
            self.button_frame,
            text=utils.setLabel(
                language,
                'Anuluj',
                'Cancel'),
            command=self.settings_window.destroy).place(
            relx=0.55,
            rely=0.16,
            relwidth=0.4,
            relheight=0.7)

        self.error_label = ttk.Label(
            self.error_frame,
            text='',
            style='Error.TLabel',
            anchor='center')
        self.error_label.place(
            relx=0.05,
            rely=0.1,
            relwidth=0.9,
            relheight=0.8)
        ttk.Style().configure('Error.TLabel', foreground='red')

        ttk.Label(
            self.entries_frame,
            text=utils.setLabel(
                language,
                'Histogram Czasu Przejścia:',
                'Transition Time Histogram:'),
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
                'Wszystkie Wykresy:',
                'All Charts:'),
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
        ttk.Style().configure('Header.TLabel', font=(None, 9, 'bold'))

        self.bars_nmb_var = tkinter.StringVar(value=self.bars_nmb)
        self.bars_resolution_var = tkinter.StringVar(
            value=self.bars_resolution)
        self._3d_bars_nmb_var = tkinter.StringVar(value=self._3d_bars_nmb)
        self.transition_expected_time_var = tkinter.StringVar(
            value=self.transition_expected_time)
        self.operation_expected_time_var = tkinter.StringVar(
            value=self.operation_expected_time)

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

    def overwriteVars(self, fun, language):
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

            self.error_label['text'] = ''

            if self.bars_nmb != Globals.bars_nmb or self.bars_resolution != Globals.bars_resolution or self._3d_bars_nmb != Globals.chartA_bars_nmb or self.transition_expected_time != Globals.transition_expected_time or self.operation_expected_time != Globals.operation_expected_time:
                Globals.bars_nmb = self.bars_nmb
                Globals.bars_resolution = self.bars_resolution
                Globals.chartA_bars_nmb = self._3d_bars_nmb
                Globals.transition_expected_time = self.transition_expected_time
                Globals.operation_expected_time = self.operation_expected_time
                self.settings_window.destroy()
                fun()
            else:
                self.settings_window.destroy()
        except BaseException:
            self.error_label['text'] = utils.setLabel(
                language,
                'Błąd: Podano niepoprawne wartości',
                'Error: Inserted incorrect values')


if __name__ == '__main__':
    pass
