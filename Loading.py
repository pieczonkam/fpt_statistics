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
        self.n = 0
        self.is_shown = False

    def setText(self, language, text_pl=None, text_eng=None):
        if not isinstance(text_pl, type(None)) and not isinstance(text_eng, type(None)):
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

    def start(self):
        self.label.configure(image=self.giflist[self.n])
        self.n = (self.n + 1) % len(self.giflist)
        self.timer_id = self.window.after(50, self.start)

    def stop(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

    def show(self):
        if not self.is_shown:
            self.is_shown = True
            self.label.pack(side=tkinter.LEFT, padx=10)
            self.window.update()
            self.start()

    def hide(self):
        if self.is_shown:
            self.is_shown = False
            self.stop()
            self.label.pack_forget()


if __name__ == '__main__':
    pass
