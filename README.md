# tkextrafont
[![Build status](https://ci.appveyor.com/api/projects/status/s64648offncdbmbk/branch/master?svg=true)](https://ci.appveyor.com/project/RedFantom/python-tkextrafont/branch/master)
[![Build status](https://api.travis-ci.com/TkinterEP/python-tkextrafont.svg?branch=master)](https://travis-ci.com/github/TkinterEP/python-tkextrafont/)
[![PyPI version](https://badge.fury.io/py/tkextrafont.svg)](https://pypi.python.org/pypi/tkextrafont)

From the basic concept of [the old version](https://github.com/TkinterEP/python-tkextrafont.old)
of this repository and the [build system](https://github.com/TkinterEP/python-gttk/blob/master/CMakeLists.txt)
created for [`python-gttk`](https://github.com/TkinterEP/python-gttk)
now comes a version of the `extrafont` package that is packaged for
Python on both Windows and Linux platforms and run on CI platforms.

## Building & Installation
The package is built with `CMake` and [`scikit-build`](https://scikit-build.readthedocs.io/en/latest/),
and on Windows an installation of [`MYS2`](https://www.msys2.org/) is 
required. The original build system for the `extrafont` package with
a build system that depends on Visual Studio is not available in this 
repository, though you might be able to build the `extrafont` binary
separately and then copy it as you require.

### Linux
This example is given for Ubuntu 20.04, change the names of packages and
commands as required for your distribution of choice.
```bash
sudo apt install python3-dev tcl-dev tk-dev \
    fontconfig libfontconfig1 libfontconfig1-dev \
    cmake cmake-data extra-cmake-modules build-essential
python -m pip install scikit-build
python setup.py install 
```

### Windows
See the `setup.py` and `.appveyor.yml` for more detailed installation 
instructions. After installing the dependencies (`tk`, `cmake`, 
`toolchain`, `fontconfig`), run in the MSYS shell:
```
python setup..py build
python setup.py install
```

## Usage
```python
import tkinter as tk
from tkextrafont import Font

window = tk.Tk()
font = Font(file="tests/overhaul.ttf", family="Overhaul")
tk.Label(window, text="Hello", font=font).pack()
window.mainloop()
```

## License & Copyright
This library is available under the MIT License, as described in 
`LICENSE.md`. `extrafont` is originally available under a different 
license, which is also found in `LICENSE.md`. The build system
(`setup.py`, `.appveyor.yml` and `.travis.yml`) are available under
GNU GPLv3 only.
