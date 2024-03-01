"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2018 RedFantom
"""
import tkinter as tk
from tkinter import ttk
from tkextrafont import Font

window = tk.Tk()
font = Font(file="Roboto-Medium.ttf")
assert font.is_font_available("Roboto")
assert "Roboto Medium" in font.loaded_fonts()
assert font.font_info("Roboto-Medium.ttf")["copyright"]
ttk.Label(window, text="Roboto Font", font=("Roboto", 12)).grid()
ttk.Label(window, text="Normal Font", font=("default", 12)).grid()
window.mainloop()
