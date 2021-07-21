from imports import *


class Loading:
    def __init__(self, window, frame, language):
        self.window = window
        self.giflist = []
        self.prepareGiflist(utils.resourcePath('loading_animation'))
        self.loading_text = ('Wczytywanie...', 'Loading...')
        self.label = ttk.Label(frame, text=utils.setLabel(
            language, self.loading_text[0], self.loading_text[1]), image=self.giflist[0], compound='left')

        self.timer_id = None

    def setText(self, language, text_pl=None, text_eng=None):
        if not text_pl is None and not text_eng is None:
            self.loading_text = (text_pl, text_eng)
        self.label['text'] = utils.setLabel(
            language, self.loading_text[0], self.loading_text[1])

    def prepareGiflist(self, imagespath):
        imagefiles = [f for f in os.listdir(
            imagespath) if os.path.isfile(os.path.join(imagespath, f))]
        for imagefile in imagefiles:
            image = tkinter.PhotoImage(
                file=os.path.join(imagespath, imagefile))
            self.giflist.append(image)

    def start(self, n=0):
        self.label.configure(image=self.giflist[n % len(self.giflist)])
        self.timer_id = self.window.after(50, self.start, n+1)

    def stop(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

    def show(self):
        self.label.pack(side=tkinter.LEFT, padx=10)
        self.window.update()
        self.start()

    def hide(self):
        self.stop()
        self.label.pack_forget()


if __name__ == '__main__':
    pass
