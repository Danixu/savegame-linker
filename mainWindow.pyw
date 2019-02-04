'''
17 June 2018
@autor: Daniel Carrasco
'''

import globals
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from ShapedButton import ShapedButton
from addGame import addGame
import sys
from pathlib import Path


globals.init()


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
  def __init__(self, parent):
    wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER,
              size=wx.Size(410, 485), pos=wx.Point(10, 10))
    CheckListCtrlMixin.__init__(self)
    ListCtrlAutoWidthMixin.__init__(self)


class mainWindow(wx.Frame):
  ###=== Exit Function ===###
  def exitGUI(self, event):
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

    # Changing the icon
    icon = wx.Icon("icons.ico", wx.BITMAP_TYPE_ICO)
    self.SetIcon(icon)
    
    # Creating panel
    boxSizer = wx.BoxSizer()  
    self.panel = wx.Panel(self)
    self.panel.SetBackgroundColour(globals.BACKGROUNDCOLOR)
    self.panel.SetSizerAndFit(boxSizer)
 
 
    # Widget items list
    self.itemList = CheckListCtrl(self.panel)
    self.itemList.InsertColumn(0, '', width=32)
    self.itemList.InsertColumn(1, 'Icono', width=52)
    self.itemList.InsertColumn(2, 'Título', width=140)
       
    self.il = wx.ImageList(48, 48, wx.IMAGE_LIST_SMALL)
    self.itemList.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
    
    image = wx.Image(str(globals.dataFolder["images"] / "tick_1.png"), wx.BITMAP_TYPE_ANY)
    self.il.Add(wx.Bitmap(image))
    
    image = wx.Image(str(globals.dataFolder["images"] / 'tick_2.png'), wx.BITMAP_TYPE_ANY)
    self.il.Add(wx.Bitmap(image))
    
    image = wx.Image(str(globals.dataFolder["images"] / 'exit.png'), wx.BITMAP_TYPE_ANY )
    image = image.Scale(40, 40, wx.IMAGE_QUALITY_HIGH)
    image = image.Size(wx.Size(48,48), wx.Point(4,4), 255, 255, 255)
    self.il.Add(wx.Bitmap(image))
    
    image = wx.Image(str(globals.dataFolder["images"] / 'test.png'), wx.BITMAP_TYPE_ANY )
    image = image.Scale(40, 40, wx.IMAGE_QUALITY_HIGH)
    image.ConvertAlphaToMask(threshold=50)
    image = image.Size(wx.Size(48,48), wx.Point(4,4), 255, 255, 255)
    self.il.Add(image.ConvertToBitmap())
    
    for item in range(0, 200):
      index = self.itemList.InsertItem(sys.maxsize, "")
      self.itemList.SetItemColumnImage(item, 1, 3)

      
    #=== Buttons ===#  
    # Add #
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
    self.CreateStatusBar()
    # Menu File
    APP_EXIT = 1
    mArchivo = wx.Menu()
    qmi = wx.MenuItem(mArchivo, APP_EXIT, '&Salir\tCtrl+Q')
    image = wx.Image(str(globals.dataFolder["images"] / 'exit.png'),wx.BITMAP_TYPE_PNG)
    image = image.Scale(16, 16, wx.IMAGE_QUALITY_HIGH)
    qmi.SetBitmap(image.ConvertToBitmap())
    mArchivo.Append(qmi)
    self.Bind(wx.EVT_MENU, self.exitGUI, id=APP_EXIT)
    
    # Menu bar
    menuBar = wx.MenuBar()
    menuBar.Append(mArchivo, "&Archivo")
    self.SetMenuBar(menuBar)
   
  
  ###=== Button "Add" click ===###
  def AddButtonClick(self, event):
    print("AddButtonClick OnLeftDown")

    AddGame = addGame(self)
    AddGame.ShowModal()

    print("despues de spawn")
    event.Skip()
    
  
  ###=== Button "Remove" click ===###
  def RemButtonClick(self, event):
    print("RemButtonClick OnLeftDown")
    
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
          self.itemList.DeleteItem(item)

          
  ###=== Button "Refresh" click ===###
  def RefreshButtonClick(self, event):
    print("RemButtonClick OnLeftDown")
    event.Skip()

  
  ###=== Button "Run" click ===###  
  def RunButtonClick(self, event):
    print("RunButtonClick OnLeftDown")
    event.Skip()

 
#======================
# Start GUI
#======================
app = wx.App()
mainWindow().Show()
app.MainLoop()
