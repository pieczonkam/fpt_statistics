from imports import *

class ChartPreview:
    def __init__(self, root):
        self.root = root

    def show(self, language, chart_name, data):
        self.showLoadingCursor(self.root)
        
        self.language = language
        self.chart_preview = tkinter.Toplevel(self.root)
        self.chart_preview.iconbitmap(utils.resourcePath('applogo.ico'))
        self.chart_preview.grab_set()

        self.frame = ttk.Frame(self.chart_preview)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        if chart_name == 'A':
            self.showChartA(data)

        self.hideLoadingCursor(self.root)

    def showChartA(self, data):
        self.chart_preview.title(utils.setLabel(self.language, 'PMS Data Analysis - Wykres 3D - Podgląd', 'PMS Data Analysis - 3D Chart - Preview'))
        self.chart_preview.state('zoomed')
        self.chart_preview.minsize(800, 600)

        X = data['X']
        Y= data['Y']
        Z = data['Z']
        X_labels = data['X_labels']
        Y_labels = data['Y_labels']
        Y_labels_nmb = data['Y_labels_nmb']

        ax = self.figure.add_subplot(111, projection='3d')

        if len(X) > 0 and len(Y) > 0 and len(Z) > 0:
            self.A_poly3d = ax.bar3d(X, Y, np.zeros_like(Z), 0.9, 1, Z, shade=True)
            self.A_poly3d._facecolors2d = self.A_poly3d._facecolor3d
            self.A_poly3d._edgecolors2d = self.A_poly3d._edgecolor3d

            ax.set_xticks(np.arange(0.5, len(X_labels), 1))
            ax.set_xticklabels(X_labels, rotation=90)

            ax.set_yticks(Y_labels_nmb)
            ax.set_yticklabels(Y_labels, rotation=90)

        ax.set_box_aspect((2, 2, 1), zoom=1.2)
        ax.set_title(utils.setLabel(self.language, 'Wykres 3D', '3D Chart'), pad=15, weight='bold')

        ax.set_xlabel(data['xlabel'])
        ax.set_ylabel(data['ylabel'])
        ax.set_zlabel(data['zlabel'])

        self.canvas.draw()
        
    def showLoadingCursor(self, window):
        window.configure(cursor='wait')
        time.sleep(0.1)
        window.update()

    def hideLoadingCursor(self, window):
        window.configure(cursor='')

if __name__ == '__main__':
    pass