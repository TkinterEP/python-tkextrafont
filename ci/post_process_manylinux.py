"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2021 RedFantom

Modify generated wheels such that they load the sytem-version of the
libfontconfig binary rather than the manylinux provided one.
"""
import shutil
from typing import Any, List, Optional
import os
import zipfile  # Wheels are actually zip files

LIB = b"libfontconfig.so.1"


def get_whl_files() -> List[str]:
    return list(map(lambda s: os.path.join("dist", s), filter(lambda s: s.endswith(".whl"), os.listdir("dist"))))


def printf(string, **kwargs):
    kwargs.update({"end": "", "flush": True})
    print(string, **kwargs)


def first(lst: List[Any]) -> Optional[Any]:
    return lst[0] if len(lst) > 0 else None


for whl in get_whl_files():
    # Step one: Open the wheel as a zip file
    printf(f"Processing {whl}...")
    source = zipfile.ZipFile(whl)
    target = zipfile.ZipFile(os.path.basename(whl), "w")
    printf(".")

    # Step two: Find the fontconfig file
    members: List[str] = source.namelist()
    wo_fontconfig = [member for member in members if "libfontconfig" not in member]
    fontconfig = first(list(set(members) - set(wo_fontconfig)))
    if fontconfig is None:
        printf("notfound\n")
        continue
    fontconfig = os.path.basename(fontconfig)
    printf(fontconfig)
    printf(".")
    fontconfig = fontconfig.encode()

    # Step three: Copy the modified contents to the target wheel file
    for member in wo_fontconfig:
        buffer: bytes = source.read(member)
        if "extrafont.so" in member:  # We found our compiled binary!
            # Step four: Modify extrafont.so to no longer load the old fontconfig
            printf(buffer.index(fontconfig))
            buffer = buffer.replace(fontconfig, LIB + b"\x00" * (len(fontconfig) - len(LIB)))

        # Step five: Write the new zipfile
        target.writestr(member, buffer)
    source.close()
    target.close()

    # Step six: Replace the original wheel file with the new file
    os.remove(whl)
    shutil.copyfile(os.path.basename(whl), whl)
    os.remove(os.path.basename(whl))
    printf("  Done.\n")
