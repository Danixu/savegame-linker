# -*- coding: utf-8 -*-

'''
23 June 2018
@autor: Daniel Carrasco
'''

import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from widgets.ShapedButton import ShapedButton
import sys
import os
from pathlib import Path
import subprocess
import globals
import logging

#====================================================================
class addGame(wx.Dialog):
  ############# Funciones #############
  ## Función de salida ##
  def exitGUI(self, event):
    self.Destroy()
  
  def __del__(self):
    print("addGame deleted")

  def __init__(self, parent):
    wx.Dialog.__init__(
        self, 
        parent, 
        style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT, 
        title="Añadir juego", 
        size=(485,520)
      )
    
    # Binding close button to avoid memory leak
    # If not, when close button is pressed instead cancel, it keeps the memory
    # in use
    self.Bind(wx.EVT_CLOSE, self.exitGUI)
    
    # Varaibles del objeto
    self.exit_code = 0
    
    # Cambiamos el icono
    icon = wx.Icon(str(globals.dataFolder["images"] / 'icons.ico'), wx.BITMAP_TYPE_ICO)
    self.SetIcon(icon)
    
    # Creamos el panel
    boxSizer = wx.BoxSizer()
    
    self.panel = wx.Panel(self)
    self.panel.SetBackgroundColour(globals.BACKGROUNDCOLOR)
    self.panel.SetSizerAndFit(boxSizer)
    
    # Creamos el Notebook con las páginas
    self.notebook = wx.Notebook(self.panel)
   
    searchpage = self._searchPage(self.notebook, self)
    self.notebook.AddPage(searchpage, "Buscar Juegos")

    addpage = self._addPage(self.notebook, self)
    self.notebook.AddPage(addpage, "Añadir manualmente")

    # layout
    boxSizer = wx.BoxSizer()
    boxSizer.Add(self.notebook, 1, wx.EXPAND)
    self.panel.SetSizerAndFit(boxSizer)


  ### Página de Búsqueda ###
  class _searchPage(wx.Panel):
    def __init__(self, parent, mainWindow):
      wx.Panel.__init__(self, parent)
      t = wx.StaticText(self, -1, "This is a PageTwo object", (20,20))
      
      self.mainWindow = mainWindow

      # Accept/Cancel buttons
      self.btnAceptar = wx.Button(self, -1, "Aceptar",
          pos=(150, 410), size=(80,30)
        )
        
      self.btnCancelar = wx.Button(self, -1, "Cancelar",
          pos=(236, 410), size=(80,30)
        )
      self.btnCancelar.Bind(wx.EVT_LEFT_UP, self.mainWindow.exitGUI)

  ### Página para añadir manualmente ###
  class _addPage(wx.Panel):
    def __init__(self, parent, mainWindow):
      wx.Panel.__init__(self, parent)
      
      self.mainWindow = mainWindow
  
      ### Grupo Título ###
      text1 = wx.StaticText(self, id=wx.ID_ANY, label="Título:",
          pos=(6, 5), size=wx.DefaultSize, style=0,
          name=wx.StaticTextNameStr)
      text1.SetFont(globals.labelFormat)
      text1.SetForegroundColour(wx.Colour(0, 51, 153))
      
      self.textBox1 = wx.TextCtrl(self, -1, "", (6, 23), (450, 20),
          wx.BORDER_STATIC|wx.TE_LEFT)
      self.textBox1.SetFont(globals.textBoxFormat)
 
 
      ### Grupo Icono ###
      text2 = wx.StaticText(self, id=wx.ID_ANY, label="Icono:",
          pos=(6, 47), size=wx.DefaultSize, style=0,
          name=wx.StaticTextNameStr)
      text2.SetFont(globals.labelFormat)
      text2.SetForegroundColour(wx.Colour(0, 51, 153))
      
      self.textBox2 = wx.TextCtrl(self, -1, "", (6, 67), (410, 20),
          wx.BORDER_STATIC | wx.TE_LEFT | wx.TE_READONLY)
      self.textBox2.SetFont(globals.textBoxFormat)
      self.textBox2.SetBackgroundColour(wx.WHITE)

      
      ## Add Button ###
      image_iconup = wx.Image(str(globals.dataFolder["images"] / 'folder_close.png'),
          wx.BITMAP_TYPE_ANY )
      image_iconover = wx.Image(str(globals.dataFolder["images"] / 'folder_open.png'),
          wx.BITMAP_TYPE_ANY )
      image_icondown = wx.Image(str(globals.dataFolder["images"] / 'folder_click.png'),
          wx.BITMAP_TYPE_ANY )
      image_icondisabled = image_iconup.ConvertToDisabled(70)
      button_icon = ShapedButton(self, 
          image_iconup.ConvertToBitmap(), 
          image_icondown.ConvertToBitmap(), 
          image_icondisabled.ConvertToBitmap(),
          image_iconover.ConvertToBitmap(),
          pos=(423, 55), size=(36,36)
        )
      button_icon.Bind(wx.EVT_LEFT_UP, self.SelectIconButton)

      
      ### Grupo Folder List ###
      text2 = wx.StaticText(self, id=wx.ID_ANY, label="Carpetas a añadir:",
          pos=(6, 90), size=wx.DefaultSize, style=0,
          name=wx.StaticTextNameStr)
      text2.SetFont(globals.labelFormat)
      text2.SetForegroundColour(wx.Colour(0, 51, 153))
      self.folderList = wx.ListCtrl(self, id=wx.ID_ANY, pos=(6, 108), 
          size=(410,200), style=wx.LC_REPORT | wx.BORDER_STATIC | wx.LC_NO_HEADER, 
          validator=wx.DefaultValidator, name=wx.ListCtrlNameStr)
      self.folderList.InsertColumn(0, '', width=wx.LIST_AUTOSIZE_USEHEADER)
       
       
      ### Add Button ###
      image_addup = wx.Image(str(globals.dataFolder["images"] / 'add_up.png'),
          wx.BITMAP_TYPE_ANY )
      image_adddown = wx.Image(str(globals.dataFolder["images"] / 'add_down.png'),
          wx.BITMAP_TYPE_ANY )
      image_adddisabled = image_addup.ConvertToDisabled(70)
      button_add = ShapedButton(self, 
          image_addup.ConvertToBitmap(), 
          image_adddown.ConvertToBitmap(), 
          image_adddisabled.ConvertToBitmap(),
          pos=(422, 108), size=(36,36)
        )
      button_add.Bind(wx.EVT_LEFT_UP, self.AddButtonClick)

      
      ### Remove Button ###
      image_remup = wx.Image(str(globals.dataFolder["images"] / 'remove_up.png'),
          wx.BITMAP_TYPE_ANY )
      image_remdown = wx.Image(str(globals.dataFolder["images"] / 'remove_down.png'),
          wx.BITMAP_TYPE_ANY )
      image_remdisabled = image_remup.ConvertToDisabled(70)
      button_rem = ShapedButton(self, 
          image_remup.ConvertToBitmap(), 
          image_remdown.ConvertToBitmap(), 
          image_remdisabled.ConvertToBitmap(),
          pos=(422, 150), size=(36,36)
        )
      button_rem.Bind(wx.EVT_LEFT_UP, self.RemButtonClick)
      
      
      ### Grupo nombre de Carpeta ###
      text4 = wx.StaticText(self, id=wx.ID_ANY, 
          label="Nombre de carpeta donde guardar:",
          pos=(6, 315), size=wx.DefaultSize, style=0,
          name=wx.StaticTextNameStr)
      text4.SetFont(globals.labelFormat)
      text4.SetForegroundColour(wx.Colour(0, 51, 153))
      
      self.textBox3 = wx.TextCtrl(self, -1, "", (6, 333), (450, 20),
          wx.BORDER_STATIC|wx.TE_LEFT)
      self.textBox3.SetFont(globals.textBoxFormat)
      
      
      ### Grupo Checkbox ###
      self.check1 = wx.CheckBox(
          self, id=wx.ID_ANY, 
          label="Mover ficheros a la carpeta del programa",
          pos=(6, 360), size=(250,20)
        )
          
      self.check2 = wx.CheckBox(
          self, id=wx.ID_ANY, 
          label="Generar enlace simbólico después de mover",
          pos=(6, 380), size=(250,20)
        )

      self.btnAceptar = wx.Button(self, -1, "Aceptar",
          pos=(150, 410), size=(80,30)
        )
      self.btnAceptar.Bind(wx.EVT_LEFT_UP, self.addGameToDB)
        
      self.btnCancelar = wx.Button(self, -1, "Cancelar",
          pos=(236, 410), size=(80,30)
        )
      self.btnCancelar.Bind(wx.EVT_LEFT_UP, self.mainWindow.exitGUI)    
    
    ## Funcíón seleccionar icono ##
    def SelectIconButton(self, event):
      with wx.FileDialog(self, "Abrir Imagen", 
          wildcard="Imágenes|*.bmp;*.png;*.jpg;*.gif;*.ico",
          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        if fileDialog.ShowModal() == wx.ID_CANCEL:
          event.Skip()
          return

        self.textBox2.SetValue(fileDialog.GetPath())
      event.Skip()
    
    ## Función añadir carpeta ##
    def AddButtonClick(self, event):
      while True:
        with wx.DirDialog(None, "Choose a directory:",
            style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON) as folderDialog:
          if folderDialog.ShowModal() == wx.ID_OK:
            if folderDialog.GetPath() not in self.get_list_data():
              self.folderList.InsertItem(sys.maxsize, folderDialog.GetPath())
              
              if (self.textBox1.GetLineText(0) == "" 
                  and self.textBox1.GetLineText(0) == ""):
                fdname = os.path.basename(folderDialog.GetPath())
                self.textBox1.SetValue(fdname)
                self.textBox3.SetValue(fdname)
              break
            else:
              wx.MessageBox(
                  'La carpeta seleccionada ya está en la lista', 
                  'Aviso', wx.OK | wx.ICON_WARNING
                )
          else:
            break
      event.Skip()
    
    ## Función quitar carpeta ##
    def RemButtonClick(self, event):
      selected = self.folderList.GetSelectedItemCount()
      if selected == 0:
        wx.MessageBox(
            'Tienes que seleccionar al menos un item de la lista.', 
            'Aviso', wx.OK | wx.ICON_WARNING
          )
        return
      else:
        item_list = []
        current = -1
        while True:
          next = self.folderList.GetNextSelected(current)
          if next == -1:
              break

          item_list.append(next)
          current = next
        
        for item in reversed(item_list):
          self.folderList.DeleteItem(item)
      event.Skip()
      
    def addGameToDB(self, event):
      # Recuperamos los datos
      title = self.textBox1.GetValue()
      icon = self.textBox2.GetValue()
      folders = []
      for i in range(0, self.folderList.GetItemCount()):
        folders.append(self.folderList.GetItemText(i))

      folderName = self.textBox3.GetValue()
      moveFiles = self.check1.GetValue()
      createSymbolic = self.check2.GetValue()

      if (title.replace(" ", "") == "" or
          folderName.replace(" ", "") == "" or
          len(folders) == 0):
        wx.MessageBox(
            "Todos los campos salvo el icono, son necesarios",
            "Error",
            style=wx.ICON_ERROR | wx.OK | wx.STAY_ON_TOP
          )
      

      if not os.path.isdir(os.path.join(
            globals.fullPath(globals.options['savesFolder']),
            folderName)):
        os.makedirs(os.path.join(
            globals.fullPath(globals.options['savesFolder']),
            folderName
          ))
      
      actual = 0
      foldersData = {}
      for folder in folders:
        dst = os.path.join(
            globals.fullPath(globals.options['savesFolder']),
            folderName,
            "{0:03d}".format(actual)
          )
          
        foldersData.update({
            globals.folderToWindowsVariable(folder): globals.relativePath(dst)
          })

        if moveFiles:
          os.rename(folder, dst)
        
        if createSymbolic:
          #os.symlink(dst, folder) # Fails, so I've used subprocess
          subprocess.check_call(
              'mklink /J "{}" "{}"'.format(folder, dst), shell=True
            )
        
        actual+=1

      print(foldersData)
      
      # Adding data to database
      
      event.Skip()
      
    def get_list_data(self):
      count = self.folderList.GetItemCount()
      itemlist = []
      for row in range(count):
        itemlist.append(self.folderList.GetItem(itemIdx=row, col=0).Text)
      return itemlist