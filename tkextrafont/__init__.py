"""
Author: RedFantom
License: MIT License
Copyright (c) 2018 RedFantom

Python/Tkinter wrapper around extrafont library for Tk/Tcl. The original
project files can be found here:
<https://sourceforge.net/projects/irrational-numbers/>

Provides interface to load the extrafont library into a Tk instance by
loading it into the Tk interpreter.
"""
import tkinter as tk
import tkinter.font as tkfont
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


class Font(tkfont.Font):
    """
    tk.Font wrapper that allows loading fonts from a file

    Loads tkextrafont if the package has not yet been loaded.
    """

    def __init__(self, root=None, font=None, name=None, exists=False, file=None, **options):
        """
        :param file: Path to the file to load a font from
        """
        if file is None:  # May as well use normal tk.Font
            tkfont.Font.__init__(self, root, font, name, exists, **options)
            return
        self._file = file
        root = root or tk._default_root
        if root is None:
            raise tk.TclError("No Tk instance available to get interpreter from")
        if not getattr(root, "_tkextrafont_loaded", False):
            load(root)
        # Load the font file
        root.tk.call("extrafont::load", file)
        tkfont.Font.__init__(self, root, font, name, exists, **options)

    def unload(self):
        """Unload the current font"""
        self._tk.call("extrafont::unload", self.name)  # self._tk available after tk.font.Font.__init__

    def loaded_fonts(self) -> List[str]:
        """Return a list of fonts loaded with extrafont"""
        return self._tk.call("extrafont::query", "families")

    def font_info(self, fname: str) -> List[Dict[str, str]]:
        """Return info of a font file"""
        return list(map(_tk_dict_to_dict, self._tk.call("extrafont::nameinfo", fname)))

    def is_font_available(self, font_name) -> bool:
        """Return a boolean whether a font is available"""
        return self._tk.call("extrafont::isAvailable", font_name)


def load(window: tk.Tk):
    """Load extrafont into a Tk interpreter"""
    local = os.path.abspath(os.path.dirname(__file__))
    with chdir(local):
        window.tk.eval("source pkgIndex.tcl")
        try:
            window.tk.eval("package require extrafont")
        except tk.TclError as e:
            if "libfontconfig" in e.message:
                raise tk.TclError("Could not load extrafont due to missing fontconfig - See issue #1 on GitHub: <https://github.com/TkinterEP/python-tkextrafont/issues/1>")
        window._tkextrafont_loaded = True
