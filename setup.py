#setup.py
import sys, os
from cx_Freeze import setup, Executable

__version__ = "1.0.0"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

include_files = ['images', 'audio']
excludes = ["OpenGL", "email", "distutils", "html", "pydoc_data", "unittest", "http", "xml"]
packages = ["widgets", "windows", "ctypes"]

setup (
  name = "appname",
  description='App Description',
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