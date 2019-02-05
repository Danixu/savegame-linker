# settings.py
from pathlib import Path
import sqlite3
import logging

log = logging.getLogger('SavegameLinker')

def init():
    log.debug("Global variables")
    global BACKGROUNDCOLOR
    BACKGROUNDCOLOR = (240, 240, 240, 255)

    global dataFolder
    dataFolder = {
      "images": Path("images/"),
      "audio": Path("audio/"),
      "icons": Path("icons/"),
    }
    
    log.info("Connecting to gamedata database")
    ## Save folder list database
    global db_gamedata
    db_gamedata = sqlite3.connect('gamedata.db')
    
    log.info("Connecting to savedata database")
    ## Savegames lists
    global db_savedata
    db_savedata = sqlite3.connect('savedata.db')
    
    log.info("Checking and creating tables")
    log.debug("Creating cursor")
    c = db_savedata.cursor()
    
    # Games table
    log.debug("Games table")
    c.execute(
        "CREATE TABLE IF NOT EXISTS Games (" +
        "id INTEGER AUTOINCREMENTAL UNIQE, " +
        "detected_id INTEGER, " +
        "name TEXT, " +
        "folder TEXT, " +
        "icon TEXT);"
      )
    
    # Saves table
    log.debug("Saves table")
    c.execute(
        "CREATE TABLE IF NOT EXISTS Saves (" +
        "id INTEGER AUTOINCREMENTAL UNIQE, " +
        "game_id INTEGER, " +
        "source TEXT, " +
        "destination TEXT);"
      )
      
    # Backups table
    log.debug("Backups table")
    c.execute(
        "CREATE TABLE IF NOT EXISTS Backups (" +
        "id INTEGER AUTOINCREMENTAL UNIQE, " +
        "game_id INTEGER, " +
        "filename TEXT);"
      )
    
    # Options table
    log.debug("Options table")
    c.execute(
        "CREATE TABLE IF NOT EXISTS Config (" +
        "var TEXT, " +
        "value TEXT);"
      )
    
    log.debug("Closing cursor")
    c.close()
    
    log.debug("Commiting DB changes")
    db_savedata.commit()
    
    log.info("Finished globals loading")