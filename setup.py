#setup.py
import sys, os
from cx_Freeze import setup, Executable

__version__ = "0.5.1"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

include_files = ['images', 'audio']
excludes = ["OpenGL", "email", "distutils", "html", "pydoc_data", "unittest", "http", "xml", "pkg_resources"]
packages = ["base64", "collections", "ctypes", "encodings", "importlib", "io", "json", "logging", "PIL", "platform", "pygame", "sqlite3", "subprocess", "sys", "urllib", "widgets", "windows", "wx"]

setup (
  name = "Savegame Linker",
  description='Program that allow you to keep all saves in one folder using symlinks.',
  version=__version__,
  options = {
    'build_exe': {
      'include_files': include_files,
      'excludes': excludes,
      'include_msvcr': True,
      'zip_include_packages': packages,
      'zip_exclude_packages': '',
      "optimize": 2,
    }
  },
  executables = [
    Executable(
      "mainWindow.pyw",
      base="Win32GUI",
      icon="images/icons.ico",
    )
  ]
)