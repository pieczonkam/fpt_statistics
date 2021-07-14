from imports import *


class Chart:
    def __init__(self, frame, excel_table):
        self.frame = frame
        self.excel_table = excel_table
        self.cols = len(excel_table.columns)
        self.rows = len(excel_table)

        self.vars = []

    def getColumn(self, column_name):
        return self.excel_table[column_name].tolist()

    def clearFrame(self):
        for child in self.frame.winfo_children():
            child.destroy()

    def drawChart(self, chart='A'):
        def chartChoice(chart):
            return {
                'A': self.drawChartA,
                'B': self.drawChartB,
                'C': self.drawChartC,
                'D': self.drawChartD,
                'E': self.drawChartE
            }.get(chart, self.drawChartA)

        chartChoice(chart)()

    def drawChartA(self):
        self.clearFrame()
        options_frame = ttk.Frame(self.frame)
        chart_frame = ttk.Frame(self.frame)
        options_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        chart_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)


        station = self.getColumn('Stacja')
        operator = self.getColumn('Operator Name')
        current_time = self.getColumn('Aktualny czas trwania [s]')
        expected_time = self.getColumn('Czas trwania cyklu [s]')

        print(station)
        print(operator)
        print(current_time)
        print(expected_time)

        check1_var = tkinter.IntVar()
        check2_var = tkinter.IntVar()
        print(check1_var.get())
        print(check2_var.get())
        check1_var.set(1)
        check2_var.set(1)
        print(check1_var.get())
        print(check2_var.get())
        check1 = ttk.Checkbutton(options_frame, text='a', variable=check1_var)
        check2 = ttk.Checkbutton(options_frame, text='b', variable=check2_var)
        check1.pack(side=tkinter.LEFT, padx=10)
        check2.pack(side=tkinter.LEFT, padx=10)

        print('Chart A')

    def drawChartB(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        data = {'Year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
                'Unemployment_Rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
                }
        df = pd.DataFrame(data, columns=['Year', 'Unemployment_Rate'])

        figure = plt.Figure()
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, chart_frame)
        line.get_tk_widget().place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        df = df[['Year', 'Unemployment_Rate']].groupby('Year').sum()
        df.plot(kind='line', legend=True, ax=ax,
                color='r', marker='o', fontsize=10)
        ax.set_title('Year Vs. Unemployment Rate')

    def drawChartC(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        data = {'Interest_Rate': [5, 5.5, 6, 5.5, 5.25, 6.5, 7, 8, 7.5, 8.5],
                'Stock_Index_Price': [1500, 1520, 1525, 1523, 1515, 1540, 1545, 1560, 1555, 1565]
                }
        df = pd.DataFrame(data, columns=['Interest_Rate', 'Stock_Index_Price'])

        figure = plt.Figure()
        ax = figure.add_subplot(111)
        ax.scatter(df['Interest_Rate'], df['Stock_Index_Price'], color='g')
        scatter = FigureCanvasTkAgg(figure, chart_frame)
        scatter.get_tk_widget().place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        ax.legend(['Stock_Index_Price'])
        ax.set_xlabel('Interest Rate')
        ax.set_title('Interest Rate Vs. Stock Index Price')

    def drawChartD(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        data = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
                'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]
                }
        df = pd.DataFrame(data, columns=['Country', 'GDP_Per_Capita'])

        figure = plt.Figure()
        ax = figure.add_subplot(111)
        bar = FigureCanvasTkAgg(figure, chart_frame)
        bar.get_tk_widget().place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        df = df[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
        df.plot(kind='bar', legend=True, ax=ax)
        ax.set_title('Country Vs. GDP Per Capita')

    def drawChartE(self):
        self.clearFrame()
        chart_frame = ttk.Frame(self.frame)
        chart_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        print('Chart E')


if __name__ == '__main__':
    pass
