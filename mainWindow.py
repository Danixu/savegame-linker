#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
17 June 2018
@autor: Daniel Carrasco
'''

import ctypes
import gettext
import globals
import logging
from io import BytesIO
import platform
import sys
from widgets import CheckListCtrl, ShapedButton
from modules import imageRemoveTransparecyWX, getResourcePath
from windows import addGame, options
import wx


# Load main data
app = wx.App()
globals.init()

### Log Configuration ###
log = logging.getLogger("MainWindow")
log.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler(globals.options['logFile'])

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(funcName)s() - %(levelname)s: %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
log.addHandler(handler)

log.debug("Changing log level to {}".format(globals.options['logLevel']))
log.setLevel(globals.options['logLevel'])

es = gettext.translation('globals', localedir='lang', languages=['es'])
es.install()


class mainWindow(wx.Frame):
    ###=== Exit Function ===###
    def exitGUI(self, event):
        globals.db_gamedata.close()
        globals.db_savedata.close()
        self.Destroy()

    ###=== Main Function ===###
    def __init__(self):
        wx.Frame.__init__(
                self, 
                None, 
                style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX, 
                title="Savegame Linker", 
                size=(485,587)
            )
        
        log.info("Loading main windows...")
        self.Bind(wx.EVT_CLOSE, self.exitGUI)

        # Changing the icon
        icon = wx.Icon(
            getResourcePath.getResourcePath(globals.dataFolder["images"], 'icons.ico'), 
            wx.BITMAP_TYPE_ICO
        )
        self.SetIcon(icon)
        
        # Creating panel
        log.debug("Creating panel")
        boxSizer = wx.BoxSizer()
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(globals.BACKGROUNDCOLOR)
        self.panel.SetSizerAndFit(boxSizer)
 
        # Widget items list
        log.debug("Creating item list")
        self.itemList = CheckListCtrl.CheckListCtrl(self.panel)
        self.itemList.InsertColumn(0, '', width=32)
        self.itemList.InsertColumn(1, _('Icon'), width=52)
        self.itemList.InsertColumn(2, _('Title'), width=320)
        
        log.debug("Updating item list")
        self.itemListRefresh()

        #=== Buttons ===#
        # Add #
        log.debug("Adding 'Add' button")
        button_add_up = wx.Bitmap()
        button_add_up.LoadFile(
            getResourcePath.getResourcePath(
              globals.dataFolder["images"], 
              'add_up.png'
            )
        )
        button_add_down = wx.Bitmap()
        button_add_down.LoadFile(
            getResourcePath.getResourcePath(
              globals.dataFolder["images"], 
              'add_down.png'
            )
        )
        button_add_disabled = button_add_down.ConvertToDisabled()
        button_add = ShapedButton.ShapedButton(self.panel,
            button_add_up,
            button_add_down,
            button_add_disabled,
            audio_click=getResourcePath.getResourcePath(globals.dataFolder["audio"], 'Click1.wav'),
            pos=(427, 20), size=(36,36)
        )
        button_add.Bind(wx.EVT_LEFT_UP, self.AddButtonClick)
        
        # Remove #
        log.debug("Adding 'Remove' button")
        button_rem_up = wx.Bitmap()
        button_rem_up.LoadFile(
            getResourcePath.getResourcePath(
              globals.dataFolder["images"], 
              'remove_up.png'
            )
        )
        button_rem_down = wx.Bitmap()
        button_rem_down.LoadFile(
            getResourcePath.getResourcePath(
              globals.dataFolder["images"], 
              'remove_down.png'
            )
        )
        button_rem_disabled = button_rem_down.ConvertToDisabled()
        button_rem = ShapedButton.ShapedButton(self.panel,
            button_rem_up,
            button_rem_down,
            button_rem_disabled,
            audio_click=getResourcePath.getResourcePath(globals.dataFolder["audio"], 'Click1.wav').replace("\\", "\\\\"),
            pos=(427, 65), size=(36,36)
        )
        button_rem.Bind(wx.EVT_LEFT_UP, self.RemButtonClick)
        
        # Refresh #
        log.debug("Adding 'Refresh' button")
        button_ref_up = wx.Bitmap()
        button_ref_up.LoadFile(
            getResourcePath.getResourcePath(
              globals.dataFolder["images"], 
              'refresh_up.png'
            )
        )
        button_ref_down = wx.Bitmap()
        button_ref_down.LoadFile(
            getResourcePath.getResourcePath(
              globals.dataFolder["images"], 
              'refresh_down.png'
            )
        )
        button_ref_disabled = button_ref_down.ConvertToDisabled()
        button_ref = ShapedButton.ShapedButton(self.panel,
                button_ref_up,
                button_ref_down,
                button_ref_disabled,
                audio_click=getResourcePath.getResourcePath(globals.dataFolder["audio"], 'Click1.wav'),
                pos=(427, 110), size=(36,36)
            )
        button_ref.Bind(wx.EVT_LEFT_UP, self.RefreshButtonClick)
        
        # Run #
        log.debug("Adding 'Run' button")
        button_run_up = wx.Bitmap()
        button_run_up.LoadFile(
            getResourcePath.getResourcePath(
              globals.dataFolder["images"], 
              'run_up.png'
            )
        )
        button_run_down = wx.Bitmap()
        button_run_down.LoadFile(
            getResourcePath.getResourcePath(
              globals.dataFolder["images"], 
              'run_down.png'
            )
        )
        button_run_disabled = button_run_down.ConvertToDisabled()
        button_run = ShapedButton.ShapedButton(self.panel, 
                button_run_up, 
                button_run_down, 
                button_run_disabled,
                audio_click=getResourcePath.getResourcePath(globals.dataFolder["audio"], 'Click1.wav'),
                pos=(427, 450), size=(36,36)
            )
        button_run.Bind(wx.EVT_LEFT_UP, self.RunButtonClick)

        #=== Menu ===#
        log.debug("Creating main menu")
        self.CreateStatusBar()
        # Menu File
        mFile = wx.Menu()
        qmi = wx.MenuItem(mFile, 10, _("&Quit\tCtrl+Q"))
        image = wx.Image(getResourcePath.getResourcePath(globals.dataFolder["images"], 'exit.png'),wx.BITMAP_TYPE_PNG)
        image = image.Scale(16, 16, wx.IMAGE_QUALITY_HIGH)
        qmi.SetBitmap(image.ConvertToBitmap())
        mFile.Append(qmi)
        self.Bind(wx.EVT_MENU, self.exitGUI, id=10)
        
        # Menu Edit
        mEdit = wx.Menu()
        # qmi = wx.MenuItem(mEdit, 20, _("&Options\tAlt+F12"))
        # image = wx.Image(getResourcePath.getResourcePath(globals.dataFolder["images"], 'options.png'),wx.BITMAP_TYPE_PNG)
        # image = image.Scale(16, 16, wx.IMAGE_QUALITY_HIGH)
        # qmi.SetBitmap(image.ConvertToBitmap())
        # mEdit.Append(qmi)
        
        qmi = wx.MenuItem(mEdit, 21, _("Create JSON from &Save"))
        image = wx.Image(getResourcePath.getResourcePath(globals.dataFolder["images"], 'generate.png'),wx.BITMAP_TYPE_PNG)
        image = image.Scale(16, 16, wx.IMAGE_QUALITY_HIGH)
        qmi.SetBitmap(image.ConvertToBitmap())
        mEdit.Append(qmi)
        
        # self.Bind(wx.EVT_MENU, self.MenuOptions, id=20)
        self.Bind(wx.EVT_MENU, self.MenuGenerateJson, id=21)
        
        # Menu bar
        log.debug("Adding menu bar")
        menuBar = wx.MenuBar()
        menuBar.Append(mFile, _("&File"))
        menuBar.Append(mEdit, _("&Edit"))
        self.SetMenuBar(menuBar)
     
    
    ###=== Button "Add" click ===###
    def AddButtonClick(self, event):
        log.debug("Clicked 'Add' button")
        # Show add game page
        AddGame = addGame.addGame(self)
        AddGame.ShowModal()
        # Update if changed
        if AddGame.updated:
            self.itemListRefresh()

        AddGame.close()
        event.Skip()
        
    
    ###=== Button "Remove" click ===###
    def RemButtonClick(self, event):
        log.debug("Clicked 'Remove' button")
        
        toRemove = []
        
        for index in range(self.itemList.GetItemCount()): 
            if self.itemList.IsChecked(index):
                toRemove.append(index)
        
        if len(toRemove) == 0:
            wx.MessageBox(_("You must select at least one item from the list."), _("Notice"), wx.OK | wx.ICON_WARNING)
            return
        else:
            dlg = wx.MessageDialog(self, _("Are you sure that want to delete the selected items?"),
                    _("Delete?"), wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal()
             
            if result == wx.ID_YES:
                for item in reversed(toRemove):
                    GameID = self.itemList.GetItemData(item)
                    
                    try:
                        c = globals.db_savedata.cursor()
                        c.execute("DELETE FROM Games WHERE id = {};".format(GameID))
                        c.execute("DELETE FROM Saves WHERE game_id = {};".format(GameID))
                        c.close()
                    except Exception as e:
                        log.error("Error: there was an error removing data from database: {}".format(e))
                        dlg = wx.MessageDialog(self, _("There was an error removing data from database."),
                            _("Error"), wx.YES_NO | wx.ICON_ERROR)
                        globals.db_savedata.rollback()
                        break
                        
                    globals.db_savedata.commit()
                    self.itemList.DeleteItem(item)

                    
    ###=== Button "Refresh" click ===###
    def RefreshButtonClick(self, event):
        log.debug("Clicked 'Refresh' button")
        self.itemListRefresh()
        event.Skip()

    
    ###=== Button "Run" click ===###    
    def RunButtonClick(self, event):
        log.debug("Clicked 'Run' button")
        
        toSymlink = []
        
        for index in range(self.itemList.GetItemCount()): 
            if self.itemList.IsChecked(index):
                toSymlink.append(index)
        
        if len(toSymlink) == 0:
            wx.MessageBox(_("You must select at least one item from the list."), _("Notice"), wx.OK | wx.ICON_WARNING)
            return
        else:
            dlg = wx.MessageDialog(self, _("Do you want to create the symbolic links?"),
                    _("Continue"), wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal()
             
            if result == wx.ID_YES:
                for item in toSymlink:
                    GameID = self.itemList.GetItemData(item)
                    
                    c = globals.db_savedata.cursor()
                    c.execute(
                        "SELECT source, destination FROM Saves WHERE game_id = ?", (GameID,)
                    )
                    
                    for folder in c:
                        src = globals.windowsVariableToFolder(folder[1])
                        dst = folder[0]
                        
                        if not winPathTools.makeSymbolicLink(src, dst):
                            log.error(
                                "There was an error creating the symbolic link: " +
                                "{} -> {}".format(dst, src)
                            )
                            wx.MessageBox(
                                _("There was an error creating the symbolic link: ") +
                                    "{} -> {}".format(dst, src),
                                style=wx.OK | wx.ICON_WARNING | wx.STAY_ON_TOP
                            )
                            
                wx.MessageBox(
                    _("Symbolic links created successfully."),
                    _("Finished"),
                    style=wx.ICON_INFORMATION | wx.OK | wx.STAY_ON_TOP
                )
 
        event.Skip()
        
        
    ###=== Refresh List ===###
    def itemListRefresh(self):
        log.debug("Updating list")
        try:
            del self.il
            log.debug("ImageList deleted")
        except:
            pass
        
        log.debug("Creating image list")
        self.il = wx.ImageList(48, 48, wx.IMAGE_LIST_SMALL)
        self.itemList.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
        log.debug("Adding tick icons")
        image = wx.Image(getResourcePath.getResourcePath(globals.dataFolder["images"], "tick_1.png"), wx.BITMAP_TYPE_ANY)
        self.il.Add(wx.Bitmap(image))
        
        image = wx.Image(getResourcePath.getResourcePath(globals.dataFolder["images"], 'tick_2.png'), wx.BITMAP_TYPE_ANY)
        self.il.Add(wx.Bitmap(image))
        
        image = wx.Image(getResourcePath.getResourcePath(globals.dataFolder["images"], 'no_image_small.png'), wx.BITMAP_TYPE_ANY)
        self.il.Add(wx.Bitmap(image))

        log.info("Cleaning the list")
        self.itemList.DeleteAllItems()
        
        log.info("Getting database data")
        log.debug("Creating cursor")
        c = globals.db_savedata.cursor()
        
        query = "SELECT * FROM Games ORDER BY name;"
        log.debug("Executing query: {!r}".format(query))
        c.execute(query)
        
        log.info("Adding new items to list")
        for campo in c:
            icon_image = 2
            if type(campo[4]).__name__ == 'bytes':
                # Open the image
                sbuf = BytesIO(campo[4])
                im = wx.Image(sbuf)

                # Remove transparency (white background will be transparent on ImageList)
                im = imageRemoveTransparecyWX.remove_transparency(im)
                
                # Create an wx.Image from image
                im = im.Size(wx.Size(48,48), wx.Point(2,2), 255, 255, 255)

                # Convert it to Bitmap and add it to ImageList
                icon_image = self.il.Add(im.ConvertToBitmap())
                sbuf.close()

            index = self.itemList.InsertItem(920863821570964096, "")
            self.itemList.SetItemColumnImage(index, 1, icon_image)
            self.itemList.SetItem(index, 2, campo[2])
            self.itemList.SetItemData(index, campo[0])

    ###=== Button "Add" click ===###
    def MenuOptions(self, event):
        log.debug("Clicked 'Options' menu")

        Options = options.options(self)
        Options.ShowModal()

        event.Skip()
        
    def MenuGenerateJson(self, event):
        log.debug("Clicked 'Generate Json' menu")
        # Show add game page
        AddGame = addGame.addGame(self, genJson=True)
        AddGame.ShowModal()
        
 
 
#======================
# Start GUI
#======================
# Symlink needs admin rights on some Windows versions.
# On Windows 10 is not necessary, but Windows 8 is untested by now
# sys.getwindowsversion() fails when is compiled to exe and detects version 6
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

winVer = platform.platform(terse=True)
runAsAdmin = is_admin()
log.info("Windows version: {}".format(winVer))
log.info("Run as admin: {}".format(runAsAdmin))
if not winVer in ["Windows-10"] and not runAsAdmin:
    if getattr(sys, 'frozen', False):
        # The application is frozen
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.executable, None, 1)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
else:
    mainWindow().Show()
    app.MainLoop()