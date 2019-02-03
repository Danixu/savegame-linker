#setup.py
import sys, os
from cx_Freeze import setup, Executable

__version__ = "1.0.0"

include_files = ['images/tick_1.png', 'images/tick_2.png', 'images/exit.png', 'images/test.png', 'icons.ico']
excludes = [""]
packages = ["wx", "pathlib", "sys"]

setup(
    name = "appname",
    description='App Description',
    version=__version__,
    options = {"build_exe": {
    'packages': packages,
    'include_files': include_files,
    'excludes': excludes,
    'include_msvcr': True,
}},
executables = [Executable("mainWindows.py",base="Win32GUI",icon="icons.ico")]
)