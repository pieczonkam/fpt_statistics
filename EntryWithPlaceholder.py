from imports import *

class EntryWithPlaceholder:
    def __init__(self, root, var, relx, rely, relwidth, relheight, placeholder="PLACEHOLDER", color='grey'):
        self.root = root
        self.var = var
        
        self.relx = relx
        self.rely = rely
        self.relwidth = relwidth
        self.relheight = relheight
        
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = 'black'
        self.state = 'normal'

        self.entry = ttk.Entry(self.root, textvariable=self.var, style='EWP.TEntry')
        self.entry.bind("<FocusIn>", self.foc_in)
        self.entry.bind("<FocusOut>", self.foc_out)

        self.entry.place(relx=self.relx, rely=self.rely, relwidth=self.relwidth, relheight=self.relheight)
        self.put_placeholder()

    def put_placeholder(self):
        self.state = 'empty'
        self.entry.insert(0, self.placeholder)
        ttk.Style().configure('EWP.TEntry', foreground=self.placeholder_color)
        

    def foc_in(self, *args):
        if self.state == 'empty':
            self.state = 'normal'
            self.entry.delete('0', 'end')
            ttk.Style().configure('EWP.TEntry', foreground=self.default_fg_color)
            

    def foc_out(self, *args):
        if not self.entry.get():
            self.put_placeholder()

if __name__ == "__main__": 
    pass