# -*- coding: utf-8 -*-

'''
6 Feb 2019
@autor: Daniel Carrasco
'''

import wx
from widgets.ShapedButton import ShapedButton
import sys
import os
from pathlib import Path
import globals
import logging

#====================================================================
class options(wx.Dialog):
  ############# Funciones #############
  ## Función de salida ##
  def exitGUI(self, event):
    self.Destroy()

  def __init__(self, parent):
    wx.Dialog.__init__(
        self, 
        parent, 
        style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT, 
        title="Opciones", 
        size=(485,520)
      )
    
    # Binding close button to avoid memory leak
    # If not, when close button is pressed instead cancel, it keeps the memory
    # in use
    self.Bind(wx.EVT_CLOSE, self.exitGUI)
    
    # Varaibles del objeto
    self.exit_code = 0
    
    # Cambiamos el icono
    icon = wx.Icon(str(globals.dataFolder["images"] / 'options.ico'), wx.BITMAP_TYPE_ICO)
    self.SetIcon(icon)
    
    # Creamos el panel
    boxSizer = wx.BoxSizer()
    
    self.panel = wx.Panel(self)
    self.panel.SetBackgroundColour(globals.BACKGROUNDCOLOR)
    self.panel.SetSizerAndFit(boxSizer)
    
    # Creamos el Notebook con las páginas
    self.notebook = wx.Notebook(self.panel)
   
    searchpage = self._global(self.notebook, self)
    self.notebook.AddPage(searchpage, "Globales")

    addpage = self._logging(self.notebook, self)
    self.notebook.AddPage(addpage, "Logging")

    # layout
    boxSizer = wx.BoxSizer()
    boxSizer.Add(self.notebook, 1, wx.EXPAND)
    self.panel.SetSizerAndFit(boxSizer)


  ### Página de Búsqueda ###
  class _global(wx.Panel):
    def __init__(self, parent, mainWindow):
      wx.Panel.__init__(self, parent)
      t = wx.StaticText(self, -1, "There are no global options for now", (20,20))
      
      self.mainWindow = mainWindow

      # Accept/Cancel buttons
      self.btnAceptar = wx.Button(self, -1, "Aceptar",
          pos=(150, 410), size=(80,30)
        )
        
      self.btnCancelar = wx.Button(self, -1, "Cancelar",
          pos=(236, 410), size=(80,30)
        )
      self.btnCancelar.Bind(wx.EVT_LEFT_DOWN, self.mainWindow.exitGUI)

  ### Página para añadir manualmente ###
  class _logging(wx.Panel):
    def __init__(self, parent, mainWindow):
      wx.Panel.__init__(self, parent)

      self.mainWindow = mainWindow

      ## Log search Button ###
      text2 = wx.StaticText(self, id=wx.ID_ANY, label="Archivo log:",
          pos=(6, 5), size=wx.DefaultSize, style=0,
          name=wx.StaticTextNameStr)
      text2.SetFont(globals.labelFormat)
      text2.SetForegroundColour(wx.Colour(0, 51, 153))
      
      self.textBox2 = wx.TextCtrl(self, -1, "", (6, 23), (410, 20),
          wx.BORDER_STATIC | wx.TE_LEFT | wx.TE_READONLY)
      self.textBox2.SetFont(globals.textBoxFormat)
      self.textBox2.SetBackgroundColour(wx.WHITE)

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
          pos=(423, 14), size=(36,36)
        )
      button_icon.Bind(wx.EVT_LEFT_DOWN, self.SelectLogButton)

      
      ## Log Level selector ##
      text1 = wx.StaticText(self, id=wx.ID_ANY, label="Nivel de log:",
          pos=(6, 47), size=wx.DefaultSize, style=0,
          name=wx.StaticTextNameStr)
      text1.SetFont(globals.labelFormat)
      text1.SetForegroundColour(wx.Colour(0, 51, 153))
      
      logLevel = wx.ComboBox(
          self, id=wx.ID_ANY, value="",
          pos=(6, 67), size=(450, 30), style=wx.CB_DROPDOWN | wx.CB_READONLY,
          choices=[
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
            ],
          validator=wx.DefaultValidator, name="LogLevel"
        )
      
      
      # Set values on widgets
      self.textBox2.SetValue(globals.options['logFile'])
      
      found = logLevel.FindString(
          globals.valueToStr(
              globals.options['logLevel'],
              "logLevel"
          )
        )
        
      logLevel.SetSelection(found)
      
      
      # Accept/Cancel buttons
      self.btnAceptar = wx.Button(self, -1, "Aceptar",
          pos=(150, 410), size=(80,30)
        )
        
      self.btnCancelar = wx.Button(self, -1, "Cancelar",
          pos=(236, 410), size=(80,30)
        )
      self.btnCancelar.Bind(wx.EVT_LEFT_DOWN, self.mainWindow.exitGUI)    
    
    ## Funcíón seleccionar icono ##
    def SelectLogButton(self, event):
      with wx.FileDialog(self, "Abrir Imagen", wildcard="Ficheros de log|*.log",
          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        if fileDialog.ShowModal() == wx.ID_CANCEL:
          event.Skip()
          return

        self.textBox2.SetValue(fileDialog.GetPath())
    
      event.Skip()
    
    ## Función añadir carpeta ##
    def AddButtonClick(self, event):
      while True:
        with wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON) as folderDialog:
          if folderDialog.ShowModal() == wx.ID_OK:
            if folderDialog.GetPath() not in self.get_list_data():
              self.folderList.InsertItem(sys.maxsize, folderDialog.GetPath())
              
              if self.textBox1.GetLineText(0) == "" and self.textBox1.GetLineText(0) == "":
                fdname = os.path.basename(folderDialog.GetPath())
                self.textBox1.SetValue(fdname)
                self.textBox3.SetValue(fdname)
              break
            else:
              wx.MessageBox('La carpeta seleccionada ya está en la lista', 'Aviso', wx.OK | wx.ICON_WARNING)
          else:
            break
            
      event.Skip()
    
    ## Función quitar carpeta ##
    def RemButtonClick(self, event):
      selected = self.folderList.GetSelectedItemCount()
      if selected == 0:
        wx.MessageBox('Tienes que seleccionar al menos un item de la lista.', 'Aviso', wx.OK | wx.ICON_WARNING)
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
      
    def get_list_data(self):
      count = self.folderList.GetItemCount()
      itemlist = []
      for row in range(count):
        itemlist.append(self.folderList.GetItem(itemIdx=row, col=0).Text)
      return itemlist