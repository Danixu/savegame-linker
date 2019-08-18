# -*- coding: utf-8 -*-

# globals.py
from modules import strToValue, pathTools
import logging
import os
import sqlite3
import sys
import wx
import gettext

### Log Configuration ###
log = logging.getLogger("MainWindow")


def init():
        global BACKGROUNDCOLOR
        BACKGROUNDCOLOR = (240, 240, 240, 255)

        global dataFolder
        dataFolder = {
            "images": "images/",
            "audio": "audio\\",
        }
        
        
        
        # Data from DB
        global options
        options = {
            "logLevel": logging.INFO,
            "logFile": "mainWindow.log",
            "savesFolder": "Saves",
            "lastDirIcon": "",
            "lastDirSaves": "",
            "moveOnAdd": False,
            "linkOnAdd": True,
            "generateJson": True
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
        
        try:
            ## Save folder list database
            global db_gamedata
            db_gamedata = sqlite3.connect('gamedata.db')
            
            ## Savegames lists
            global db_savedata
            db_savedata = sqlite3.connect('savedata.db')
            c = db_savedata.cursor()
        except Exception as e:
            log.error(
                "There was an error connecting to database:" +
                " {}".format(e)
            )
            dlg = wx.MessageDialog(
                None,
                _("There was an error. Please go to log for more info."),
                wx.OK | wx.ICON_ERROR
            )
            dlg.ShowModal()
            sys.exit(99)
        
        try:
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
        except Exception as e:
            log.error(
                "There was an error creating required databases in sqlite:" +
                " {}".format(e)
            )
            dlg = wx.MessageDialog(
                None,
                _("There was an error. Please go to log for more info."),
                wx.OK | wx.ICON_ERROR
            )
            dlg.ShowModal()
            sys.exit(99)
        
        try:
            # Replacing options from stored in database:
            c = db_savedata.cursor()
            for item in options:
                query = "SELECT * FROM Config WHERE var = ?;"
                c.execute(query, (item,))
                data = c.fetchone()
                if data:
                    options[item] = strToValue.strToValue(data[2], data[1])
            c.close()
        except Exception as e:
            log.error(
                "There was an error reading the config data from database:" +
                " {}".format(e)
            )
            dlg = wx.MessageDialog(
                None,
                _("There was an error. Please go to log for more info."),
                wx.OK | wx.ICON_ERROR
            )
            dlg.ShowModal()
            sys.exit(99)
        
        try:        
            ## Doing startup things ##
            if not os.path.isdir(pathTools.fullPath(options['savesFolder'])):
                os.makedirs(pathTools.fullPath(options['savesFolder']))
                
            if not os.path.isdir(pathTools.fullPath('gamedata')):
                os.makedirs(pathTools.fullPath('gamedata'))
        except Exception as e:
            log.error(
                "There was an error creating required folders:" +
                " {}".format(e)
            )
            dlg = wx.MessageDialog(
                None,
                _("There was an error. Please go to log for more info."),
                wx.OK | wx.ICON_ERROR
            )
            dlg.ShowModal()
            sys.exit(99)

        
def saveOption(key, value, keyType=None):
    try:
        c = db_savedata.cursor()
        options[key] = value
        query = "INSERT OR REPLACE INTO Config VALUES (?,?,?);"
        c.execute(query, (key, keyType or type(value).__name__, str(value).lower()))
        c.close()
        db_savedata.commit()
        return True
    except Exception as e:
        log.error(
            "There was an error inserting the config data to database:" +
            " {}".format(e)
        )
        dlg = wx.MessageDialog(
            None,
            _("There was an error. Please go to log for more info."),
            wx.OK | wx.ICON_ERROR
        )
        dlg.ShowModal()
        return False