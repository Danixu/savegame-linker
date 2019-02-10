# -*- coding: utf-8 -*-

# globals.py
from PIL import Image
import logging
import os
import subprocess
from pathlib import Path
import sqlite3
import sys
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
        
        global rootPath
        if getattr(sys, 'frozen', False):
                # The application is frozen
                rootPath = os.path.dirname(os.path.realpath(sys.executable))
        else:
                # The application is not frozen
                # Change this bit to match where you store your data files:
                rootPath = os.path.dirname(os.path.realpath(__file__))
        
        # Data from DB
        global options
        options = {
            "logLevel": logging.INFO,
            "logFile": "mainWindow.log",
            "savesFolder": "Saves"
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
                "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "detected_id INTEGER DEFAULT NULL, " +
                "name TEXT UNIQE NOT NULL, " +
                "folder TEXT NOT NULL, " +
                "icon BLOB DEFAULT NULL);"
            )
        c.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS games_name " +
                "ON Games(name);"
            )

        # Saves table
        c.execute(
                "CREATE TABLE IF NOT EXISTS Saves (" +
                "game_id INTEGER NOT NULL, " +
                "source TEXT NOT NULL, " +
                "destination TEXT NOT NULL);"
            )
        c.execute(
                "CREATE INDEX IF NOT EXISTS saves_game_id " +
                "ON Saves(game_id);"
            )
            
        # Backups table
        c.execute(
                "CREATE TABLE IF NOT EXISTS Backups (" +
                "game_id INTEGER NOT NULL, " +
                "filename TEXT NOT NULL);"
            )
        
        # Options table
        c.execute(
                "CREATE TABLE IF NOT EXISTS Config (" +
                "var TEXT UNIQUE NOT NULL, " +
                "kind TEXT DEFAULT 'str', " +
                "value TEXT NOT NULL);"
            )
        c.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS config_var " +
                "ON Config(var);"
            )
        c.close()
        db_savedata.commit()
        
        # Replacing options from stored in database:
        c = db_savedata.cursor()
        for item in options:
            query = "SELECT * FROM Config WHERE var = ?;"
            c.execute(query, (item,))
            data = c.fetchone()
            if data:
                options[item] = strToValue(data[2], data[1])
        c.close()
         
        ## Doing startup things ##
        if not os.path.isdir(fullPath(options['savesFolder'])):
            os.makedirs(fullPath(options['savesFolder']))

        
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
            
def fullPath(path):
    if ":" in path or path[0] == "/":
        return path
    else:
        return os.path.join(rootPath, path)
        
def relativePath(path):
    if ":" in path or path[0] == "/":
        return path.replace("{}\\".format(rootPath.rstrip("\\")), "")
    else:
        return path
        
def folderToWindowsVariable(folder):
    for variable in ['USERPROFILE', 'LOCALAPPDATA', 'APPDATA', 'Public', 'ALLUSERSPROFILE']:
        folder = folder.replace(os.environ[variable], "%{}%".format(variable))
    return folder


def windowsVariableToFolder(folder):
    for variable in ['USERPROFILE', 'LOCALAPPDATA', 'APPDATA', 'Public', 'ALLUSERSPROFILE']:
        folder = folder.replace("%{}%".format(variable), os.environ[variable])
        
    return folder
    
def remove_transparency(im, bg_colour=(255, 255, 255)):
        # Only process if image has transparency (http://stackoverflow.com/a/1963146)
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
                # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
                alpha = im.convert('RGBA').split()[-1]
                # Create a new background image of our matt color.
                # Must be RGBA because paste requires both images have the same format
                # (http://stackoverflow.com/a/8720632    and    http://stackoverflow.com/a/9459208)
                bg = Image.new("RGBA", im.size, bg_colour + (255,))
                bg.paste(im, mask=alpha)
                return bg

        else:
                return im
                
def makeSymbolicLink(src, dst):
    try:
        #os.symlink(src=folder, dst=dst, target_is_directory=True) # Fails, so I've used subprocess
        subprocess.check_call(
                'mklink /J "{}" "{}"'.format(src, dst), shell=True
            )
        return True
            
    except Exception as e:
        return False
        