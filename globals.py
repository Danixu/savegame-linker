# settings.py
from pathlib import Path
import sqlite3

def init():
    global BACKGROUNDCOLOR
    BACKGROUNDCOLOR = (240, 240, 240, 255)

    global dataFolder
    dataFolder = {
      "images": Path("images/"),
      "audio": Path("audio/"),
      "icons": Path("icons/"),
    }
    
    ## Save folder list database
    global db_gamedata
    db_gamedata = sqlite3.connect('gamedata.db')
    
    ## Savegames lists
    global db_savedata
    db_savedata = sqlite3.connect('savedata.db')
    
    c = db_savedata.cursor()
    # Games table
    c.execute(
        "CREATE TABLE IF NOT EXISTS Games (" +
        "id INTEGER AUTOINCREMENTAL UNIQE, " +
        "detected_id INTEGER, " +
        "name TEXT, " +
        "folder TEXT, " +
        "icon TEXT);"
      )
    
    # Saves table
    c.execute(
        "CREATE TABLE IF NOT EXISTS Saves (" +
        "id INTEGER AUTOINCREMENTAL UNIQE, " +
        "game_id INTEGER, " +
        "source TEXT, " +
        "destination TEXT);"
      )
      
    # Backups table
    c.execute(
        "CREATE TABLE IF NOT EXISTS Backups (" +
        "id INTEGER AUTOINCREMENTAL UNIQE, " +
        "game_id INTEGER, " +
        "filename TEXT);"
      )
      
    c.close()
    db_savedata.commit()