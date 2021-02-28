"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2021 RedFantom
"""
import tkinter as tk
import tkextrafont
from unittest import TestCase
import os


class TestTkExtraFont(TestCase):
    """Test the compiled extrafont binary with a public-domain font"""

    PATH = os.path.abspath(os.path.dirname(__file__))

    def setUp(self):
        self.window = tk.Tk()
        tkextrafont.load_extrafont(self.window)

    def test_font_load(self):
        assert not self.window.is_font_available("Overhaul")
        loaded = set(self.window.loaded_fonts())
        self.window.load_font(os.path.join(self.PATH, "overhaul.ttf"))
        assert len(list(set(self.window.loaded_fonts()) - loaded)) != 0
        assert self.window.is_font_available("Overhaul")
        assert "Overhaul" in self.window.loaded_fonts()

        label = tk.Label(self.window, text="Overhaul font", font=("Overhaul", 12, "bold"))
        label.pack()
        self.window.update()
