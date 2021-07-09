from imports import *


class Loading:
    def __init__(self, window, frame, language):
        self.window = window
        self.giflist = []
        self.prepareGiflist()
        self.label = ttk.Label(frame, text=utils.setLabel(
            language, 'Ładowanie...', 'Loading...'), image=self.giflist[0], compound='left')
        self.label.pack(side=tkinter.LEFT, padx=15)
        threading.Thread(target=self.run).start()
      
    def setLanguage(self, language):
        self.label['text'] = utils.setLabel(
            language, 'Ładowanie...', 'Loading...')

    def prepareGiflist(self):
        imagespath = os.path.join('.', 'loading_animation')
        imagefiles = [f for f in os.listdir(imagespath) if os.path.isfile(os.path.join(imagespath, f))]
        for imagefile in imagefiles:
            image = tkinter.PhotoImage(file=os.path.join(imagespath, imagefile))
            self.giflist.append(image)
    
    def run(self):
        self.thread_running = True
        n=0
        while self.thread_running == True:
            self.label.configure(image=self.giflist[n % len(self.giflist)])
            self.window.update()
            n += 1
            time.sleep(0.05)
            print(threading.active_count())

    def stop(self):
        self.thread_running = False

    def show(self):
        self.label.pack(side=tkinter.LEFT, padx=15)
        threading.Thread(target=self.run).start()
        self.window.update()
        

    def hide(self):
        self.stop()
        self.label.pack_forget()


if __name__ == '__main__':
    pass
