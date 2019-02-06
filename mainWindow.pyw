#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
17 June 2018
@autor: Daniel Carrasco
'''

from pathlib import Path
import globals
import logging
import sys
from widgets.CheckListCtrl import CheckListCtrl
from widgets.ShapedButton import ShapedButton
from windows.addGame import addGame
from windows.options import options
import wx


# Load main data
app = wx.App()
globals.init()

### Log Configuration ###
log = logging.getLogger("SavegameLinker")
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
    icon = wx.Icon(str(globals.dataFolder["images"] / 'icons.ico'), wx.BITMAP_TYPE_ICO)
    self.SetIcon(icon)
    
    # Creating panel
    log.debug("Creating panel")
    boxSizer = wx.BoxSizer()
    self.panel = wx.Panel(self)
    self.panel.SetBackgroundColour(globals.BACKGROUNDCOLOR)
    self.panel.SetSizerAndFit(boxSizer)
 
    # Widget items list
    log.debug("Creating item list")
    self.itemList = CheckListCtrl(self.panel)
    self.itemList.InsertColumn(0, '', width=32)
    self.itemList.InsertColumn(1, 'Icono', width=52)
    self.itemList.InsertColumn(2, 'Título', width=140)
    
    log.debug("Updating item list")
    self.itemListRefresh()

    #=== Buttons ===#
    # Add #
    log.debug("Adding 'Add' button")
    image_addup = wx.Image(str(globals.dataFolder["images"] / 'add_up.png'),
        wx.BITMAP_TYPE_ANY )
    image_adddown = wx.Image(str(globals.dataFolder["images"] / 'add_down.png'),
        wx.BITMAP_TYPE_ANY )
    image_adddisabled = image_addup.ConvertToDisabled(70)
    button_add = ShapedButton(self.panel,
        image_addup.ConvertToBitmap(),
        image_adddown.ConvertToBitmap(),
        image_adddisabled.ConvertToBitmap(),
        pos=(427, 20), size=(36,36)
      )
    button_add.Bind(wx.EVT_LEFT_DOWN, self.AddButtonClick)
    
    # Remove #
    log.debug("Adding 'Remove' button")
    image_remup = wx.Image(str(globals.dataFolder["images"] / 'remove_up.png'),
        wx.BITMAP_TYPE_ANY )
    image_remdown = wx.Image(str(globals.dataFolder["images"] / 'remove_down.png'),
        wx.BITMAP_TYPE_ANY )
    image_remdisabled = image_remup.ConvertToDisabled(70)
    button_rem = ShapedButton(self.panel,
        image_remup.ConvertToBitmap(),
        image_remdown.ConvertToBitmap(),
        image_remdisabled.ConvertToBitmap(),
        pos=(427, 65), size=(36,36)
      )
    button_rem.Bind(wx.EVT_LEFT_DOWN, self.RemButtonClick)
    
    # Refresh #
    log.debug("Adding 'Refresh' button")
    image_refup = wx.Image(str(globals.dataFolder["images"] / 'refresh_up.png'),
        wx.BITMAP_TYPE_ANY )
    image_refdown = wx.Image(str(globals.dataFolder["images"] / 'refresh_down.png'),
        wx.BITMAP_TYPE_ANY )
    image_refdisabled = image_refup.ConvertToDisabled(70)
    button_ref = ShapedButton(self.panel,
        image_refup.ConvertToBitmap(),
        image_refdown.ConvertToBitmap(),
        image_refdisabled.ConvertToBitmap(),
        pos=(427, 110), size=(36,36)
      )
    button_ref.Bind(wx.EVT_LEFT_DOWN, self.RefreshButtonClick)
    
    # Run #
    log.debug("Adding 'Run' button")
    image_runup = wx.Image(str(globals.dataFolder["images"] / 'run_up.png'),
        wx.BITMAP_TYPE_ANY )
    image_rundown = wx.Image(str(globals.dataFolder["images"] / 'run_down.png'),
        wx.BITMAP_TYPE_ANY )
    image_rundisabled = image_runup.ConvertToDisabled(70)
    button_run = ShapedButton(self.panel, 
        image_runup.ConvertToBitmap(), 
        image_rundown.ConvertToBitmap(), 
        image_rundisabled.ConvertToBitmap(),
        pos=(427, 450), size=(36,36)
      )
    button_run.Bind(wx.EVT_LEFT_DOWN, self.RunButtonClick)  

    #=== Menu ===#
    log.debug("Creating main menu")
    self.CreateStatusBar()
    # Menu File
    mFile = wx.Menu()
    qmi = wx.MenuItem(mFile, 10, '&Salir\tCtrl+Q')
    image = wx.Image(str(globals.dataFolder["images"] / 'exit.png'),wx.BITMAP_TYPE_PNG)
    image = image.Scale(16, 16, wx.IMAGE_QUALITY_HIGH)
    qmi.SetBitmap(image.ConvertToBitmap())
    mFile.Append(qmi)
    self.Bind(wx.EVT_MENU, self.exitGUI, id=10)
    
    # Menu Edit
    mEdit = wx.Menu()
    qmi = wx.MenuItem(mEdit, 20, '&Opciones\tAlt+F12')
    image = wx.Image(str(globals.dataFolder["images"] / 'options.png'),wx.BITMAP_TYPE_PNG)
    image = image.Scale(16, 16, wx.IMAGE_QUALITY_HIGH)
    qmi.SetBitmap(image.ConvertToBitmap())
    mEdit.Append(qmi)
    self.Bind(wx.EVT_MENU, self.MenuOptions, id=20)
    
    # Menu bar
    log.debug("Adding menu bar")
    menuBar = wx.MenuBar()
    menuBar.Append(mFile, "&Archivo")
    menuBar.Append(mEdit, "&Edición")
    self.SetMenuBar(menuBar)
   
  
  ###=== Button "Add" click ===###
  def AddButtonClick(self, event):
    log.debug("Clicked 'Add' button")

    AddGame = addGame(self)
    AddGame.ShowModal()

    print("despues de spawn")
    event.Skip()
    
  
  ###=== Button "Remove" click ===###
  def RemButtonClick(self, event):
    log.debug("Clicked 'Remove' button")
    
    toRemove = []
    
    for index in range(self.itemList.GetItemCount()): 
      if self.itemList.IsChecked(index):
        toRemove.append(index)
    
    if len(toRemove) == 0:
      wx.MessageBox('Tienes que seleccionar al menos un item de la lista.', 'Aviso', wx.OK | wx.ICON_WARNING)
      return
    else:
      dlg = wx.MessageDialog(self, "¿Seguro que deseas borrar los items seleccionados?",
          'Borrar', wx.YES_NO | wx.ICON_QUESTION)
      result = dlg.ShowModal()
       
      if result == wx.ID_YES:
        for item in reversed(toRemove):
          GameID = self.itemList.GetItemData(item)
          print(GameID)
          
          try:
            c = globals.db_savedata.cursor()
            c.execute("DELETE FROM Games WHERE id = {};".format(GameID))
            c.execute("DELETE FROM Saves WHERE game_id = {};".format(GameID))
            globals.db_savedata.commit()
          except Exception as e:
            print("Error: error borrando los datos de la BBDD: {}".format(e))
          self.itemList.DeleteItem(item)

          
  ###=== Button "Refresh" click ===###
  def RefreshButtonClick(self, event):
    log.debug("Clicked 'Refresh' button")
    self.itemListRefresh()
    event.Skip()

  
  ###=== Button "Run" click ===###  
  def RunButtonClick(self, event):
    log.debug("Clicked 'Run' button")
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
    image = wx.Image(str(globals.dataFolder["images"] / "tick_1.png"), wx.BITMAP_TYPE_ANY)
    self.il.Add(wx.Bitmap(image))
    
    image = wx.Image(str(globals.dataFolder["images"] / 'tick_2.png'), wx.BITMAP_TYPE_ANY)
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
      image = wx.Image( str(globals.dataFolder["icons"] / campo[4]), wx.BITMAP_TYPE_ANY )
      #image = image.Blur(1)
      image = image.Scale(44, 44, wx.IMAGE_QUALITY_HIGH)
      image.ConvertAlphaToMask(threshold=1)
      image = image.Size(wx.Size(48,48), wx.Point(2,2), 255, 255, 255)
      
      self.il.Add(image.ConvertToBitmap())
    
      index = self.itemList.InsertItem(sys.maxsize, "")
      self.itemList.SetItemColumnImage(index, 1, self.il.GetImageCount()-1)
      self.itemList.SetItem(index, 2, campo[2])
      self.itemList.SetItemData(index, campo[0])

   ###=== Button "Add" click ===###
  def MenuOptions(self, event):
    log.debug("Clicked 'Options' menu")

    Options = options(self)
    Options.ShowModal()

    print("despues de spawn")
    event.Skip()
 
 
#======================
# Start GUI
#======================

mainWindow().Show()
app.MainLoop()