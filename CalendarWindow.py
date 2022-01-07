from imports import *


class CalendarWindow:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height

    def show(self, language, item_list, already_selected_items, chart_name):
        self.showLoadingCursor(self.root)
        self.date_list = item_list.copy()
        self.date_list_str = [str(d) for d in item_list]
        self.already_selected_items = already_selected_items
        self.selected_items = already_selected_items.copy()

        self.chart_name = chart_name
        self.updateStartEndDates()
        self.setPrevDates()

        self.top_window = tkinter.Toplevel(self.root)
        self.posx = self.root.winfo_x() + (self.root.winfo_width() - self.width) / 2
        self.posy = self.root.winfo_y() + (self.root.winfo_height() - self.height) / 2
        self.top_window.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.posx, self.posy))
        self.top_window.resizable(0, 0)
        self.top_window.title('PMS DA')
        self.top_window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.top_window.grab_set()
        self.calendar_window = None

        self.calendar_frame = ttk.Frame(self.top_window)
        self.button_frame = ttk.Frame(self.top_window)
        self.calendar_frame.place(
            x=0, y=0, width=self.width, height=self.height - 40)
        self.button_frame.place(x=0, y=self.height - 40,
                                width=self.width, height=40)

        ttk.Separator(self.button_frame, orient='horizontal').place(
            relx=0, rely=0, relwidth=1)

        ttk.Button(self.button_frame, text='OK', command=self.overwriteRange).place(relx=0.05, rely=0.16,
                                                                                    relwidth=0.4, relheight=0.70)
        ttk.Button(self.button_frame, text=utils.setLabel(language, 'Anuluj', 'Cancel'), command=self.cancel).place(relx=0.55, rely=0.16,
                                                                                                                    relwidth=0.4, relheight=0.70)

        ttk.Label(self.calendar_frame, text=utils.setLabel(language, 'Od: ', 'From: ')).place(
            relx=0.03, rely=0.11, relwidth=0.19, relheight=0.34)
        ttk.Label(self.calendar_frame, text=utils.setLabel(language, 'Do: ', 'To:   ')).place(
            relx=0.03, rely=0.55, relwidth=0.19, relheight=0.34)

        self.start_date_btn = ttk.Button(
            self.calendar_frame,
            text=self.start_date,
            command=lambda: self.showCalendarWindow(
                self.root.winfo_x() +
                self.root.winfo_width() /
                2,
                self.root.winfo_y() +
                self.root.winfo_height() /
                2,
                310,
                390,
                dateutil.parser.parse(
                    self.start_date),
                language,
                mode='start'))
        self.end_date_btn = ttk.Button(
            self.calendar_frame,
            text=self.end_date,
            command=lambda: self.showCalendarWindow(
                self.root.winfo_x() +
                self.root.winfo_width() /
                2,
                self.root.winfo_y() +
                self.root.winfo_height() /
                2,
                310,
                390,
                dateutil.parser.parse(
                    self.end_date),
                language,
                mode='end'))
        self.start_date_btn.place(
            relx=0.22,
            rely=0.11,
            relwidth=0.75,
            relheight=0.34)
        self.end_date_btn.place(
            relx=0.22,
            rely=0.55,
            relwidth=0.75,
            relheight=0.34)

        self.hideLoadingCursor(self.root)

    def updateStartEndDates(self):
        if self.chart_name == 'A':
            self.start_date = str(Globals.chartA_start_date)
            self.end_date = str(Globals.chartA_end_date)
        if self.chart_name == 'B':
            self.start_date = str(Globals.chartB_start_date)
            self.end_date = str(Globals.chartB_end_date)
        if self.chart_name == 'C':
            self.start_date = str(Globals.chartC_start_date)
            self.end_date = str(Globals.chartC_end_date)
        if self.chart_name == 'D':
            self.start_date = str(Globals.chartD_start_date)
            self.end_date = str(Globals.chartD_end_date)
        if self.chart_name == 'E':
            self.start_date = str(Globals.chartE_start_date)
            self.end_date = str(Globals.chartE_end_date)

        if self.start_date == 'None':
            self.start_date = self.date_list_str[self.selected_items[0]]
        if self.end_date == 'None':
            self.end_date = self.date_list_str[self.selected_items[1]]

    def setPrevDates(self):
        if self.chart_name == 'A':
            self.prev_start_date = Globals.chartA_start_date
            self.prev_end_date = Globals.chartA_end_date
        if self.chart_name == 'B':
            self.prev_start_date = Globals.chartB_start_date
            self.prev_end_date = Globals.chartB_end_date
        if self.chart_name == 'C':
            self.prev_start_date = Globals.chartC_start_date
            self.prev_end_date = Globals.chartC_end_date
        if self.chart_name == 'D':
            self.prev_start_date = Globals.chartD_start_date
            self.prev_end_date = Globals.chartD_end_date
        if self.chart_name == 'E':
            self.prev_start_date = Globals.chartE_start_date
            self.prev_end_date = Globals.chartE_end_date

    def showCalendarWindow(self, x, y, width, height,
                           current_date, language, mode):
        self.showLoadingCursor(self.top_window)
        posx = x - width / 2
        posy = y - height / 2
        self.calendar_window = tkinter.Toplevel(self.top_window)
        self.calendar_window.geometry(
            '%dx%d+%d+%d' %
            (width, height, posx, posy))
        self.calendar_window.resizable(0, 0)
        self.calendar_window.title('PMS Data Analysis')
        self.calendar_window.iconbitmap(utils.resourcePath('applogo.ico'))
        self.calendar_window.grab_set()
        self.calendar_window.protocol(
            'WM_DELETE_WINDOW', self.exitCalendarWindow)

        date_frame = ttk.Frame(self.calendar_window)
        time_frame = ttk.Frame(self.calendar_window)
        button_frame = ttk.Frame(self.calendar_window)
        date_frame.place(x=0, y=0, width=width, height=height - 80)
        time_frame.place(x=0, y=height - 80, width=width, height=40)
        button_frame.place(x=0, y=height - 40, width=width, height=40)

        ttk.Separator(
            button_frame,
            orient='horizontal').place(
            relx=0,
            rely=0,
            relwidth=1)

        ttk.Button(
            button_frame,
            text='OK',
            command=lambda: self.overwriteDate(mode)).place(
            relx=0.05,
            rely=0.16,
            relwidth=0.4,
            relheight=0.7)
        ttk.Button(
            button_frame,
            text=utils.setLabel(
                language,
                'Anuluj',
                'Cancel'),
            command=self.exitCalendarWindow).place(
            relx=0.55,
            rely=0.16,
            relwidth=0.4,
            relheight=0.7)

        self.cal = tkcalendar.Calendar(
            date_frame,
            selectmode='day',
            year=current_date.year,
            month=current_date.month,
            day=current_date.day)
        self.cal.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        self.hour_var = tkinter.StringVar(
            value=utils.addZero(str(current_date.hour)))
        self.minute_var = tkinter.StringVar(
            value=utils.addZero(str(current_date.minute)))
        self.second_var = tkinter.StringVar(
            value=utils.addZero(str(current_date.second)))

        hour_combobox = ttk.Combobox(
            time_frame,
            textvariable=self.hour_var,
            values=[
                utils.addZero(
                    str(i)) for i in range(24)],
            state='readonly')
        minute_combobox = ttk.Combobox(
            time_frame,
            textvariable=self.minute_var,
            values=[
                utils.addZero(
                    str(i)) for i in range(60)],
            state='readonly')
        second_combobox = ttk.Combobox(
            time_frame,
            textvariable=self.second_var,
            values=[
                utils.addZero(
                    str(i)) for i in range(60)],
            state='readonly')
        Hovertip(hour_combobox, utils.setLabel(language, 'Godzina', 'Hour'))
        Hovertip(minute_combobox, utils.setLabel(language, 'Minuta', 'Minute'))
        Hovertip(
            second_combobox,
            utils.setLabel(
                language,
                'Sekunda',
                'Second'))
        hour_combobox.place(relx=0.16, rely=0.16, relwidth=0.2, relheight=0.7)
        ttk.Label(
            time_frame,
            text=':').place(
            relx=0.37,
            rely=0.16,
            relwidth=0.02,
            relheight=0.7)
        minute_combobox.place(relx=0.4, rely=0.16, relwidth=0.2, relheight=0.7)
        ttk.Label(
            time_frame,
            text=':').place(
            relx=0.61,
            rely=0.16,
            relwidth=0.02,
            relheight=0.7)
        second_combobox.place(
            relx=0.64,
            rely=0.16,
            relwidth=0.2,
            relheight=0.7)

        self.hideLoadingCursor(self.top_window)

    def overwriteDate(self, mode):
        self.showLoadingCursor(self.calendar_window)
        year = str(
            dateutil.parser.parse(
                self.cal.get_date()).year)
        month = str(
            dateutil.parser.parse(
                self.cal.get_date()).month)
        day = str(
            dateutil.parser.parse(
                self.cal.get_date()).day)
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        second = self.second_var.get()

        date_str = year + '-' + utils.addZero(month) + '-' + utils.addZero(
            day) + ' ' + utils.addZero(hour) + ':' + utils.addZero(minute) + ':' + utils.addZero(second)
        date = dateutil.parser.parse(date_str)

        if mode == 'start':
            if self.chart_name == 'A':
                Globals.chartA_start_date = date
            elif self.chart_name == 'B':
                Globals.chartB_start_date = date
            elif self.chart_name == 'C':
                Globals.chartC_start_date = date
            elif self.chart_name == 'D':
                Globals.chartD_start_date = date
            elif self.chart_name == 'E':
                Globals.chartE_start_date = date

            date_in_list = self.date_list_str[-1]
            for dl in self.date_list:
                if dl >= date:
                    date_in_list = str(dl)
                    break
            self.selected_items[0] = self.date_list_str.index(date_in_list)
        elif mode == 'end':
            if self.chart_name == 'A':
                Globals.chartA_end_date = date
            elif self.chart_name == 'B':
                Globals.chartB_end_date = date
            elif self.chart_name == 'C':
                Globals.chartC_end_date = date
            elif self.chart_name == 'D':
                Globals.chartD_end_date = date
            elif self.chart_name == 'E':
                Globals.chartE_end_date = date

            date_in_list = self.date_list_str[0]
            for dl in list(reversed(self.date_list)):
                if dl <= date:
                    date_in_list = str(dl)
                    break
            self.selected_items[1] = self.date_list_str.index(date_in_list)

        self.updateStartEndDates()
        self.start_date_btn['text'] = self.start_date
        self.end_date_btn['text'] = self.end_date
        self.hideLoadingCursor(self.calendar_window)
        self.exitCalendarWindow()

    def exitCalendarWindow(self):
        self.calendar_window.destroy()
        self.calendar_window = None
        self.top_window.grab_set()

    def overwriteRange(self):
        self.already_selected_items[0] = self.selected_items[0]
        self.already_selected_items[1] = self.selected_items[1]
        self.top_window.destroy()

    def cancel(self):
        if self.chart_name == 'A':
            Globals.chartA_start_date = self.prev_start_date
            Globals.chartA_end_date = self.prev_end_date
        elif self.chart_name == 'B':
            Globals.chartB_start_date = self.prev_start_date
            Globals.chartB_end_date = self.prev_end_date
        elif self.chart_name == 'C':
            Globals.chartC_start_date = self.prev_start_date
            Globals.chartC_end_date = self.prev_end_date
        elif self.chart_name == 'D':
            Globals.chartD_start_date = self.prev_start_date
            Globals.chartD_end_date = self.prev_end_date
        elif self.chart_name == 'E':
            Globals.chartE_start_date = self.prev_start_date
            Globals.chartE_end_date = self.prev_end_date

        self.top_window.destroy()

    def showLoadingCursor(self, window):
        window.configure(cursor='wait')
        time.sleep(0.1)
        window.update()

    def hideLoadingCursor(self, window):
        window.configure(cursor='')


if __name__ == '__main__':
    pass
