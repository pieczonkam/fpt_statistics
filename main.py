from App import *

if __name__ == '__main__':
    try:
        app = App()
        app.reloadMenuBar()
        app.reloadWidgets()
        app.window.mainloop()
    except Exception as e:
        print(e)
        input()
