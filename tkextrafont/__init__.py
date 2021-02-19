"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2018 RedFantom

Python/Tkinter wrapper around extrafont library for Tk/Tcl. The original
project files can be found here:
<https://sourceforge.net/projects/irrational-numbers/>

Provides interface to load the extrafont library into a Tk instance by
loading it into the Tk interpreter. After loading additional functions
are available on the Tk instance:

load_font: Load a font file into the Tk interpreter
unload_font: Unload a font family from the Tk interpreter
loaded_fonts: Return a List of font families loaded with extrafont
font_info: Return information on the font contained in a font file
is_font_available: Return whether a font is available for usage
"""
import tkinter as tk
# Standard Library
from contextlib import contextmanager
import os
from typing import Dict, List


_FILE_DIR = os.path.abspath(__file__)


def _tk_dict_to_dict(d):
    """Build a dictionary from a Tcl dictionary by parsing its str repr"""
    # type: (tk._tkinter.Tcl_Obj) -> Dict[str, str]
    string = str(d)  # Every Tcl_Obj supports conversion to string
    elements = string.split(" ")
    results, key, brackets, total = dict(), None, False, str()
    for e in elements:
        if key is None:  # New dictionary key
            key = e
        elif brackets is True:  # Brackets were opened
            if e.endswith("}"):  # Closing brackets
                brackets = False
                results[key] = total + " " + e[:-1]
                key, total = None, str()
            else:  # Still within brackets
                total += " " + e
        elif e.startswith("{"):  # Open Brackets
            brackets = True
            total = e[1:]
        else:  # No brackets, just a simple value
            results[key] = e
            key = None
    return results


@contextmanager
def chdir(target):
    # type: (str) -> None
    """
    Temporarily change the working directory

    Based on @Akuli's contribution to ttkthemes
    Copyright (c) Akuli 2018
    """
    current = os.getcwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(current)


def get_file_directory():
    """Return an absolute path to the directory that contains this file"""
    return os.path.dirname(_FILE_DIR)


def load_extrafont(window):
    # type: (tk.Tk) -> None
    """Load extrafont into a tk interpreter and provide functions"""

    def load_font(file_name):
        # type: (str) -> None
        window.tk.call("extrafont::load", file_name)

    def unload_font(font_name):
        # type: (str) -> None
        window.tk.call("extrafont::unload", font_name)

    def loaded_fonts():
        # type: () -> list
        return window.tk.call("extrafont::query", "families")

    def font_info(file_name):
        # type: (str) -> List[Dict[str, str]]
        return list(map(_tk_dict_to_dict, window.tk.call("extrafont::nameinfo", file_name)))

    def is_font_available(font_name):
        # type: (str) -> bool
        return window.tk.call("extrafont::isAvailable", font_name)

    window.tk.eval("set dir {}".format(get_file_directory()))
    with chdir(get_file_directory()):
        window.tk.eval("source pkgIndex.tcl")
    window.tk.call("package", "require", "extrafont")
    window.load_font = load_font
    window.is_font_available = is_font_available
    window.unload_font = unload_font
    window.loaded_fonts = loaded_fonts
    window.font_info = font_info
