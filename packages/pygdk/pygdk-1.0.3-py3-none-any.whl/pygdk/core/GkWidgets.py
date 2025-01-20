import sys
import os
import tkinter as tk
from .Gk import GkBaseClass

class Gk(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self._current_width = 600
        self._current_height = 500
        
        self.title("pygdk")
        self.geometry(f"{self._current_width}x{self._current_height}")

        if sys.platform.startswith("win"):
            self.after(200, self._set_titlebar_icon)

    def _set_titlebar_icon(self):
        try:
            pygdk_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.iconbitmap(os.path.join(pygdk_dir, "assets", "icons", "pygdk.ico"))
        except Exception:
            pass


class GkLabel(GkBaseClass):
    def __init__(self, master, width=0, height=0, text=""):
        super().__init__(master=master, width=width, height=height)
        
        self._text = text
        self._label = tk.Label(master=self, padx=0, pady=0, text=self._text)
    
    def configure(self, **kwargs):
        if "text" in kwargs:
            self._text = kwargs.pop("text")
            self._label.configure(text=self._text)
            
    def pack(self):
        super().pack()
        self._label.pack()

__all__ = [
    'Gk', 'GkLabel'
]