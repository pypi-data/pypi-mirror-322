import tkinter as tk

class GkBaseClass(tk.Frame):
    def __init__(self, master, width=0, height=0):
        super().__init__(master, width=width, height=height)

    def destroy(self):
        tk.Frame.destroy(self)
    
    def pack(self):
        super().pack()

__all__ = ['GkBaseClass']