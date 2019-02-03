# settings.py
from pathlib import Path

def init():
    global BACKGROUNDCOLOR
    BACKGROUNDCOLOR = (240, 240, 240, 255)

    global dataFolder
    dataFolder = {
      "images": Path("images/"),
      "audio": Path("audio/"),
    }