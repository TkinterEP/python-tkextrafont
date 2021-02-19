"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2021 RedFantom
"""
import tkinter as tk
import tkextrafont
from unittest import TestCase


class TestTkExtraFont(TestCase):

    def setUp(self):
        self.window = tk.Tk()
        tkextrafont.load_extrafont(self.window)

    def test_font_load(self):
        # self.window.load_font()\
        pass
