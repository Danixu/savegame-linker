# -*- coding: utf-8 -*-

# globals.py
import logging
from pathlib import Path
import sqlite3
import wx

def init():
    global BACKGROUNDCOLOR
    BACKGROUNDCOLOR = (240, 240, 240, 255)

    global dataFolder
    dataFolder = {
      "images": Path("images/"),
      "audio": Path("audio/"),
      "icons": Path("data/icons/"),
    }
    
    # Data from DB
    global options
    options = {
      "logLevel": logging.INFO,
      "logFile": "mainWindow.log"
    }
    
    # Formatos
    global labelFormat
    labelFormat = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_SLANT,
        wx.FONTWEIGHT_BOLD, underline=False, faceName="Segoe UI",
        encoding=wx.FONTENCODING_DEFAULT)
    global textBoxFormat
    textBoxFormat = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_SLANT,
        wx.FONTWEIGHT_NORMAL, underline=False, faceName="Segoe UI",
        encoding=wx.FONTENCODING_DEFAULT)
    
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
    
    # Options table
    c.execute(
        "CREATE TABLE IF NOT EXISTS Config (" +
        "var TEXT, " +
        "kind TEXT, " +
        "value TEXT);"
      )
    
    c.close()
    db_savedata.commit()
    
    # Replacing options from stored in database:
    c = db_savedata.cursor()
    for item in options:
      query = "SELECT * FROM Config WHERE var = '{}';".format(item)
      c.execute(query)
      data = c.fetchone()
      if data:
        options[item] = strToValue(data[2], data[1])
      
    c.close()
    
def strToValue(str, kind):
  if kind == "logLevel":
    if str == "CRITICAL":
      return logging.CRITICAL
    elif str == "ERROR":
      return logging.ERROR
    elif str == "WARNING":
      return logging.WARNING
    elif str == "INFO":
      return logging.INFO
    elif str == "DEBUG":
      return logging.DEBUG
    else:
      return logging.INFO
      
def valueToStr(value, kind):
  if kind == "logLevel":
    if value == logging.CRITICAL:
      return "CRITICAL"
    elif value == logging.ERROR:
      return "ERROR"
    elif value == logging.WARNING:
      return "WARNING"
    elif value == logging.INFO:
      return "INFO"
    elif value == logging.DEBUG:
      return "DEBUG"
    else:
      return "INFO"