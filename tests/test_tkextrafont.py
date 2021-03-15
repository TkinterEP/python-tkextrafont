"""
Author: RedFantom
License: MIT License
Copyright (c) 2021 RedFantom
"""
import sys
sys.path = sys.path[2:]
import tkinter as tk
import tkextrafont
from unittest import TestCase
import os


class TestTkExtraFont(TestCase):
    """Test the compiled extrafont binary with a public-domain font"""

    PATH = os.path.abspath(os.path.dirname(__file__))

    def setUp(self):
        self.window = tk.Tk()
        tkextrafont.load(self.window)

    def test_font_load(self):
        font = tkextrafont.Font()
        assert not font.is_font_available("Overhaul")
        loaded = set(font.loaded_fonts())
        loaded_font = tkextrafont.Font(file=os.path.join(self.PATH, "overhaul.ttf"), family="Overhaul")
        assert len(list(set(font.loaded_fonts()) - loaded)) != 0
        assert font.is_font_available("Overhaul")
        assert "Overhaul" in font.loaded_fonts()
        label = tk.Label(self.window, text="Overhaul font", font=loaded_font)
        label.pack()
        self.window.update()
        label.destroy()

        label = tk.Label(self.window, text="Overhaul font", font=("Overhaul", 12, "bold"))
        label.pack()
        self.window.update()
