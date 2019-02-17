# -*- coding: utf-8 -*-

# globals.py
from io import BytesIO
from PIL import Image
import datetime
import logging
import os
import shutil
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
            "savesFolder": "Saves",
            "moveOnAdd": False,
            "linkOnAdd": True
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
    if kind == "bool":
        if str.lower() == "true":
            return True
        else:
            return False
            
    if kind == "int":
        return int(str)
        
    return str

        
def saveOption(key, value):
    c = db_savedata.cursor()
    options[key] = value
    query = "INSERT OR REPLACE INTO Config VALUES (?,?,?);"
    c.execute(query, key, type(value).__name__, str(value).lower())
    c.close()
    db_savedata.commit()

            
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
    log = logging.getLogger("SavegameLinker")
    log.info("Creating symlink...")
    try:
        # Check if is a synlink
        child = subprocess.Popen(
            "fsutil reparsepoint query \"{}\"".format(src),
            stdout=subprocess.PIPE
        )
        streamdata = child.communicate()[0]
        rc = child.returncode
        if rc == 0:
            # If is a symlink, just remove it
            #shutil.rmtree(src)
            os.rmdir(src)
        else:
            # If not, rename the folder
            now = datetime.date.today().strftime("%Y%m%d_%H%M%S")
            newName = "{}-{}".format(src, now)
            os.rename(src, newName)
            
            
        #os.symlink(src=folder, dst=dst, target_is_directory=True) # Fails, so I've used subprocess
        subprocess.check_call(
                'mklink /J "{}" "{}"'.format(src, dst), shell=True
            )
        return True
            
    except Exception as e:
        log.error("Error creating symlink: {}".format(e))
        return False

def imageResize(fName, nWidth=44, nHeight=44):
    if not fName == None and os.path.isfile(fName):
        # The file is saved to BytesIO and reopened because
        # if not, some ico files are not resized correctly
        tmp_data = BytesIO()
        tmp_image = Image.open(fName)
        tmp_image.save(tmp_data, "PNG", compress_level = 1)
        tmp_image.close()
        
        tmp_image = Image.open(tmp_data)
        
        if tmp_image.size[0] < nWidth and tmp_image.size[1] < nHeight:
            width, height = tmp_image.size
        
            if width > height:
                factor = nWidth / width
                width = nWidth
                height = int(height * factor)
                
                if height%2 > 0:
                    height += 1
                
                tmp_image = tmp_image.resize((width, height), Image.LANCZOS)
            else:
                factor = nHeight / height
                width = int(width * factor)
                height = nHeight
                
                if width%2 > 0:
                    height += 1
                
                tmp_image = tmp_image.resize((width, height), Image.LANCZOS)

        else:
            tmp_image.thumbnail((nWidth, nHeight), Image.LANCZOS)

        icon_data = BytesIO()
        tmp_image.save(icon_data, "PNG", optimize=True)
        tmp_image.close()
        tmp_data.close()
        return icon_data
    else:
        return None