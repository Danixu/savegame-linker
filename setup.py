#setup.py
import sys, os
from cx_Freeze import setup, Executable

__version__ = "0.5.3"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

include_files = [
    'images',
    'audio',
    ('lang\es\LC_MESSAGES\globals.mo', 'lang\es\LC_MESSAGES\globals.mo'),
    ('lang\en\LC_MESSAGES\globals.mo', 'lang\en\LC_MESSAGES\globals.mo'),
]

# packages to include/exclude
includes = {
    "external": [],
    "zip": ["base64", "collections", "ctypes", "encodings", "importlib", "io", "json", "logging", "platform", "playsound", "sqlite3", "subprocess", "sys", "urllib", "widgets", "windows", "win32com", "wx"]
}
excludes = {
    "external": ["OpenGL", "email", "distutils", "html", "pydoc_data", "unittest", "http", "xml", "pkg_resources"],
    "zip": []
}

# find translations and add files
for root, folders, files in os.walk('lang'):
    for fName in files:
        if ".mo" in fName:
            include_files.append(
                (
                    os.path.join(root, fName),
                    os.path.join(root, fName)
                )
            )

setup (
  name = "Savegame Linker",
  description='Program that allow you to keep all saves in one folder using symlinks.',
  version=__version__,
  options = {
    'build_exe': {
      'include_files': include_files,
      'includes': includes['external'],
      'excludes': excludes['external'],
      'include_msvcr': True,
      'zip_include_packages': includes['zip'],
      'zip_exclude_packages': excludes['zip'],
      "optimize": 2,
    }
  },
  executables = [
    Executable(
      "mainWindow.py",
      base="Win32GUI",
      icon="images/icons.ico",
    )
  ]
)