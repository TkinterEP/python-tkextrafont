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
import os
from typing import Dict, List


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
        tk_result_list = self._tk.splitlist(
            self._tk.call("extrafont::nameinfo", fname)[0]
        )
        font_info_dict = {}

        for key, value in zip(tk_result_list[0::2], tk_result_list[1::2]):
            font_info_dict[key] = str(value)
        return font_info_dict

    def is_font_available(self, font_name) -> bool:
        """Return a boolean whether a font is available"""
        return self._tk.call("extrafont::isAvailable", font_name)


def load(window: tk.Tk):
    """Load extrafont into a Tk interpreter"""
    local = os.path.abspath(os.path.dirname(__file__))
    window.tk.setvar("dir", local)
    window.tk.eval("source [file join $dir pkgIndex.tcl]")
    try:
        window.tk.eval("package require extrafont")
    except tk.TclError as e:
        if "libfontconfig" in e.message:
            raise tk.TclError("Could not load extrafont due to missing fontconfig - See issue #1 on GitHub: <https://github.com/TkinterEP/python-tkextrafont/issues/1>")
    window.tk.unsetvar("dir")
    window._tkextrafont_loaded = True
