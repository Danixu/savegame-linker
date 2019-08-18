# -*- coding: utf-8 -*-

'''
23 June 2018
@autor: Daniel Carrasco
'''

import wx
from widgets import ShapedButton
from modules import pathTools, winPathTools, imageResizeWX, imageRemoveTransparecyWX, getResourcePath
import sys
import shutil
import os
import gettext
import globals
import logging
import json
import base64
from sqlite3 import Binary

### Log Configuration ###
log = logging.getLogger("MainWindow")

#====================================================================
class addGame(wx.Dialog):
    ############# Funciones #############
    ## Función de salida ##
    def exitGUI(self, event):
        self.EndModal(0)
    
    def close(self):
        self.Destroy()

    def __init__(self, parent, genJson = False):
        wx.Dialog.__init__(
                self, 
                parent, 
                style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT, 
                title=_("Add Game"), 
                size=(485,550)
            )
            
        # Variables
        self.updated = False
        self.genJson = genJson
        
        # Binding close button to avoid memory leak
        # If not, when close button is pressed instead cancel, it keeps the memory
        # in use
        self.Bind(wx.EVT_CLOSE, self.exitGUI)
        
        # Cambiamos el icono
        icon = wx.Icon(getResourcePath.getResourcePath(globals.dataFolder["images"], 'icons.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        # Creamos el panel
        boxSizer = wx.BoxSizer()
        
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(globals.BACKGROUNDCOLOR)
        self.panel.SetSizerAndFit(boxSizer)
        
        # Creamos el Notebook con las páginas
        self.notebook = wx.Notebook(self.panel)
     
        #searchpage = self._searchPage(self.notebook, self)
        #self.notebook.AddPage(searchpage, "Buscar Juegos")

        addpage = self._addPage(self.notebook, self)
        self.notebook.AddPage(addpage, _("Add custom save"))

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
            self.btnAceptar = wx.Button(self, -1, _("Ok"),
                    pos=(150, 410), size=(80,30)
                )
                
            self.btnCancelar = wx.Button(self, -1, _("Cancel"),
                    pos=(236, 410), size=(80,30)
                )
            self.btnCancelar.Bind(wx.EVT_LEFT_UP, self.mainWindow.exitGUI)

    ### Página para añadir manualmente ###
    class _addPage(wx.Panel):
        def __init__(self, parent, mainWindow):
            wx.Panel.__init__(self, parent)
            self.mainWindow = mainWindow
            
            # Variables
            self._hasName = False
            self._hasFolders = False
            self._hasOutput = False
            self._gameIcon = None
    
            ### Title Group ###
            text1 = wx.StaticText(self, id=wx.ID_ANY, label=_("Title:"),
                    pos=(6, 5), size=wx.DefaultSize, style=0,
                    name=wx.StaticTextNameStr)
            text1.SetFont(globals.labelFormat)
            text1.SetForegroundColour(wx.Colour(0, 51, 153))
            # self.text1_warn = wx.StaticText(self, id=wx.ID_ANY, label="No",
                    # pos=(280, 5), size=wx.DefaultSize, style=0,
                    # name=wx.StaticTextNameStr)
            # self.text1_warn.SetFont(globals.labelFormat)
            # self.text1_warn.SetForegroundColour(wx.Colour(255, 0, 0))
            self.textBox1 = wx.TextCtrl(self, -1, "", (6, 23), (348, 20),
                    wx.BORDER_STATIC|wx.TE_LEFT)
            self.textBox1.SetFont(globals.textBoxFormat)
            self.textBox1.SetBackgroundColour(wx.Colour(255, 150, 150))
            
            ### Grupo nombre de Carpeta ###
            text4 = wx.StaticText(self, id=wx.ID_ANY, 
                    label=_("Data directory name:"),
                    pos=(6, 47), size=wx.DefaultSize, style=0,
                    name=wx.StaticTextNameStr)
            text4.SetFont(globals.labelFormat)
            text4.SetForegroundColour(wx.Colour(0, 51, 153))
            # self.text4_warn = wx.StaticText(self, id=wx.ID_ANY, label="No",
                    # pos=(280, 47), size=wx.DefaultSize, style=0,
                    # name=wx.StaticTextNameStr)
            # self.text4_warn.SetFont(globals.labelFormat)
            # self.text4_warn.SetForegroundColour(wx.Colour(255, 0, 0))
            self.textBox3 = wx.TextCtrl(self, -1, "", (6, 67), (348, 20),
                    wx.BORDER_STATIC|wx.TE_LEFT)
            self.textBox3.SetFont(globals.textBoxFormat)
            self.textBox3.SetBackgroundColour(wx.Colour(255, 150, 150))
            
            ### Icon ###
            image_icon = wx.Bitmap()
            image_icon.LoadFile(
                getResourcePath.getResourcePath(
                  globals.dataFolder["images"], 
                  'no_image_big.png'
                )
            )
            self.iconImage = wx.StaticBitmap(self, -1, image_icon, (361, 6), (95, 95), style=wx.BORDER_THEME)
            self.iconImage.Bind(wx.EVT_LEFT_UP, self.SelectIconButton)
            
            ### Grupo Folder List ###
            text3 = wx.StaticText(self, id=wx.ID_ANY, label=_("Folders to add:"),
                    pos=(6, 90), size=wx.DefaultSize, style=0,
                    name=wx.StaticTextNameStr)
            text3.SetFont(globals.labelFormat)
            text3.SetForegroundColour(wx.Colour(0, 51, 153))
            # self.text3_warn = wx.StaticText(self, id=wx.ID_ANY, label="No",
                    # pos=(280, 90), size=wx.DefaultSize, style=0,
                    # name=wx.StaticTextNameStr)
            # self.text3_warn.SetFont(globals.labelFormat)
            # self.text3_warn.SetForegroundColour(wx.Colour(255, 0, 0))
            self.folderList = wx.ListCtrl(self, id=wx.ID_ANY, pos=(6, 108), 
                    size=(450,200), style=wx.LC_REPORT | wx.BORDER_STATIC | wx.LC_NO_HEADER, 
                    validator=wx.DefaultValidator, name=wx.ListCtrlNameStr)
            self.folderList.InsertColumn(0, '', width=wx.LIST_AUTOSIZE_USEHEADER)
            self.folderList.SetBackgroundColour(wx.Colour(255, 150, 150))
             
            ### Add Button ###
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
            button_add = ShapedButton.ShapedButton(self, 
                    button_add_up, 
                    button_add_down, 
                    button_add_disabled,
                    audio_click=getResourcePath.getResourcePath(globals.dataFolder["audio"], 'Click1.wav'),
                    pos=(6, 312), size=(36,36)
                )
            button_add.Bind(wx.EVT_LEFT_UP, self.AddButtonClick)
            
            ### Remove Button ###
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
            button_rem = ShapedButton.ShapedButton(self, 
                    button_rem_up, 
                    button_rem_down, 
                    button_rem_disabled,
                    audio_click=getResourcePath.getResourcePath(globals.dataFolder["audio"], 'Click1.wav'),
                    pos=(48, 312), size=(36,36)
                )
            button_rem.Bind(wx.EVT_LEFT_UP, self.RemButtonClick)
             
            ### Grupo Checkbox ###
            self.check1 = wx.CheckBox(
                    self, id=wx.ID_ANY, 
                    label=_("Move folders/files to data folder"),
                    pos=(6, 360), size=(250,20)
                )
            self.check1.SetValue(globals.options['moveOnAdd'])
            self.check2 = wx.CheckBox(
                    self, id=wx.ID_ANY, 
                    label=_("Create symbolic link to data folder"),
                    pos=(6, 380), size=(250,20)
                )
            self.check2.SetValue(globals.options['linkOnAdd'])
            self.check3 = wx.CheckBox(
                    self, id=wx.ID_ANY, 
                    label=_("Generate JSON file with save info"),
                    pos=(6, 400), size=(250,20)
                )
            self.check3.SetValue(globals.options['generateJson'])
            #Set Check2 status depending of Check1
            self.checkBoxChange(None)
            if self.mainWindow.genJson:
                self.check1.Disable()
                self.check2.Disable()
                self.check3.Disable()

            self.btnAceptar = wx.Button(self, -1, _("Ok"),
                    pos=(150, 440), size=(80,30)
                )
            self.btnAceptar.Bind(wx.EVT_LEFT_UP, self.addGameToDB)
            if not self.mainWindow.genJson:
                self.btnAceptar.Disable()
            self.btnCancelar = wx.Button(self, -1, _("Cancel"),
                    pos=(236, 440), size=(80,30)
                )
            self.btnCancelar.Bind(wx.EVT_LEFT_UP, self.mainWindow.exitGUI)        

            # Binds
            self.Bind(wx.EVT_CHECKBOX, self.checkBoxChange)
            self.Bind(wx.EVT_TEXT, self.textBoxChange)
            
            
        ## Funcíón seleccionar icono ##
        def SelectIconButton(self, event):
            log.debug("Last icon directory: {}".format(globals.options.get('lastDirIcon', "")))
            with wx.FileDialog(self, _("Open image"),
                    globals.options.get('lastDirIcon', ""),
                    wildcard=_("Images|*.bmp;*.png;*.jpg;*.gif;*.ico"),
                    style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    event.Skip()
                    return

                self._gameIcon = fileDialog.GetPath()
                im = imageResizeWX.imageResizeWX(self._gameIcon, 95, 95, out_format = wx.Image)
                im = imageRemoveTransparecyWX.remove_transparency(im)

                self.iconImage.SetBitmap(im.ConvertToBitmap())
                self.iconImage.Refresh()
                globals.saveOption(
                    'lastDirIcon',
                    os.path.dirname(fileDialog.GetPath())
                )
                
            event.Skip()
        
        ## Función añadir carpeta ##
        def AddButtonClick(self, event):
            while True:
                with wx.DirDialog(None, _("Choose a directory:"),
                        defaultPath=globals.options.get('lastDirSaves', ""),
                        style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON) as folderDialog:
                    if folderDialog.ShowModal() == wx.ID_OK:
                        if folderDialog.GetPath() not in self.get_list_data():
                            self.folderList.InsertItem(920863821570964096, folderDialog.GetPath())
                            
                            if (self.textBox1.GetLineText(0) == "" 
                                    and self.textBox1.GetLineText(0) == ""):
                                fdname = os.path.basename(folderDialog.GetPath())
                                self.textBox1.SetValue(fdname)
                                self.textBox3.SetValue(fdname)
                                
                            globals.saveOption(
                                'lastDirSaves',
                                os.path.dirname(folderDialog.GetPath())
                            )
                            
                            break
                        else:
                            wx.MessageBox(
                                _("The selected directory is already on the list"),
                                _("Notice"), wx.OK | wx.ICON_WARNING
                            )
                    else:
                        break
                        
            if self.folderList.GetItemCount() > 0:
                # self.text3_warn.Hide()
                self.folderList.SetBackgroundColour(wx.Colour(255, 255, 255))
                self.folderList.Refresh()
                self._hasFolders = True
                if self._hasFolders and self._hasName and self._hasOutput:
                    self.btnAceptar.Enable()
            else:
                # self.text3_warn.Show()
                self.folderList.SetBackgroundColour(wx.Colour(255, 150, 150))
                self.folderList.Refresh()
                self._hasFolders = False
                self.btnAceptar.Disable()
            event.Skip()
        
        ## Función quitar carpeta ##
        def RemButtonClick(self, event):
            selected = self.folderList.GetSelectedItemCount()
            if selected == 0:
                wx.MessageBox(
                    _("You must select at least one item from the list"), 
                    _("Notice"), wx.OK | wx.ICON_WARNING
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
            if self.folderList.GetItemCount() > 0:
                # self.text3_warn.Hide()
                self.folderList.SetBackgroundColour(wx.Colour(255, 255, 255))
                self.folderList.Refresh()
                self._hasFolders = True
                if self._hasFolders and self._hasName and self._hasOutput:
                    self.btnAceptar.Enable()
            else:
                # self.text3_warn.Show()
                self.folderList.SetBackgroundColour(wx.Colour(255, 150, 150))
                self.folderList.Refresh()
                self._hasFolders = False
                self.btnAceptar.Disable()
            event.Skip()
            
        def addGameToDB(self, event):
            # Recuperamos los datos
            title = self.textBox1.GetValue()
            folders = []
            for i in range(0, self.folderList.GetItemCount()):
                folders.append(self.folderList.GetItemText(i))

            folderName = self.textBox3.GetValue()
            moveFiles = self.check1.GetValue()
            createSymbolic = self.check2.GetValue()
            generateJson = self.check3.GetValue()

            if (title.replace(" ", "") == "" or
                    folderName.replace(" ", "") == "" or
                    len(folders) == 0):
                wx.MessageBox(
                    _("All field less the icon are mandatory."),
                    _("Error"),
                    style=wx.ICON_ERROR | wx.OK | wx.STAY_ON_TOP
                )

            # Create saves folder
            if not os.path.isdir(
                    os.path.join(
                        pathTools.fullPath(globals.options['savesFolder']),
                        folderName
                    ) 
                ) and not self.mainWindow.genJson:
                os.makedirs(os.path.join(
                    pathTools.fullPath(globals.options['savesFolder']),
                    folderName
                ))
            
            # Create a dictionary with sources and destinations
            actual = 0
            foldersData = {}
            for folder in folders:
                dst = os.path.join(
                        pathTools.fullPath(globals.options['savesFolder']),
                        folderName,
                        "{0:03d}".format(actual)
                    )
                    
                foldersData.update({
                        folder: pathTools.relativePath(dst)
                    })
                
                actual+=1
            
            icon_data = imageResizeWX.imageResizeWX(self._gameIcon)
            
            # Generating Json
            if self.mainWindow.genJson or generateJson:
                jsonFile = "{}\\{}.json".format(
                    pathTools.fullPath('gamedata'),
                    title
                )
                iconBase64 = ""
                if icon_data:
                    iconBase64 = base64.b64encode(icon_data.getvalue()).decode("utf-8")
                    
                with open(jsonFile, "w") as fOut:
                    jsonData = {
                        "title": title,
                        "icon": iconBase64,
                        "folders": [key for key in foldersData]
                    }
                    fOut.write(json.dumps(jsonData, indent=4, sort_keys=True))
                 
                if self.mainWindow.genJson:
                    wx.MessageBox(
                        _("JSON file saved correctly."),
                        _("Saved!"),
                        style=wx.ICON_INFORMATION | wx.OK | wx.STAY_ON_TOP
                    )
            # if Window was not open exclusively to create a Json file
            # it saves the data to Database
            if not self.mainWindow.genJson:
                # Inserting all data on DB
                c = globals.db_savedata.cursor()
                log.debug("INSERT INTO Games (name, folder, icon) VALUES " +
                        "({}, {}, {});".format(title, folderName, icon_data)
                    )
                c.execute(
                    "INSERT INTO Games (name, folder, icon) VALUES " +
                    "(?, ?, ?);", (title, folderName, 
                    Binary(icon_data.getvalue()) if icon_data else None)
                )
                if icon_data:
                    icon_data.close()
                rowid = c.lastrowid
                c.execute(
                    "SELECT id FROM Games WHERE rowid = ?", (rowid,)
                )
                game_id = c.fetchone()[0]
                
                for src, dst in foldersData.items():
                    log.debug("INSERT INTO Saves (game_id, source, destination) VALUES " +
                        "({}, {}, {});".format(game_id, dst, winPathTools.folderToWindowsVariable(src))
                    )
                    c.execute(
                        "INSERT INTO Saves (game_id, source, destination) VALUES " +
                        "(?, ?, ?);", (game_id, dst, winPathTools.folderToWindowsVariable(src))
                    )
                c.close()
                
                # If move files and create symlink are checked, then do it
                for src, dst in foldersData.items():
                    if moveFiles:
                        shutil.move(src, dst)
                        #os.rename(src, dst) # Falla a veces
                        if createSymbolic:
                            winPathTools.makeSymbolicLink(src, dst)
                    else:
                        os.makedirs(dst)

                globals.saveOption('moveOnAdd', moveFiles)
                globals.saveOption('linkOnAdd', createSymbolic)
                globals.saveOption('generateJson', generateJson)
                # If everything was fine, we commit the data to DB
                globals.db_savedata.commit()
                
                # Set the game as added to update on close
                self.mainWindow.updated = True
                wx.MessageBox(
                    _("Save/s added correctly."),
                    _("Finished"),
                    style=wx.ICON_INFORMATION | wx.OK | wx.STAY_ON_TOP
                )
                self.mainWindow.exitGUI(0)
            
            event.Skip()
            
        def checkBoxChange(self, event):
            if self.check1.GetValue() == True:
                self.check2.Enable()
            else:
                self.check2.Disable()
        
        def textBoxChange(self, event):
            textBox = event.GetEventObject()
            textBoxText = textBox.GetValue()
            if textBox == self.textBox1:
                if len(textBoxText) > 0:
                    found = None
                    if not self.mainWindow.genJson:
                        temp = globals.db_savedata.cursor()
                        temp.execute(
                            "SELECT COUNT(name) FROM Games WHERE name = ?",
                            (textBoxText,)
                        )
                        found = temp.fetchone()
                        temp.close()
                    
                    if self.mainWindow.genJson or not found or found[0] == 0:
                        # self.text1_warn.Hide()
                        textBox.SetBackgroundColour(wx.Colour(255, 255, 255))
                        textBox.Refresh()
                        self._hasName = True
                        if self._hasFolders and self._hasName and self._hasOutput:
                            self.btnAceptar.Enable()
                    else:
                        # self.text1_warn.SetLabel("El título ya existe")
                        # self.text1_warn.Show()
                        textBox.SetBackgroundColour(wx.Colour(255, 150, 150))
                        textBox.Refresh()
                        self._hasName = False
                        self.btnAceptar.Disable()
                else:
                    # self.text1_warn.SetLabel("No puede estar vacío")
                    # self.text1_warn.Show()
                    textBox.SetBackgroundColour(wx.Colour(255, 150, 150))
                    textBox.Refresh()
                    self._hasName = False
                    self.btnAceptar.Disable()
            elif textBox == self.textBox3:
                # We verify if output folder exists
                if len(textBoxText) > 0:
                    fName = os.path.join(
                        pathTools.fullPath(globals.options['savesFolder']),
                        textBoxText
                    )
                    if self.mainWindow.genJson or not os.path.isdir(fName):
                        # self.text4_warn.Hide()
                        textBox.SetBackgroundColour(wx.Colour(255, 255, 255))
                        textBox.Refresh()
                        self._hasOutput = True
                        if self._hasFolders and self._hasName and self._hasOutput:
                            self.btnAceptar.Enable()
                    else:
                        # self.text4_warn.SetLabel("La carpeta ya existe")
                        # self.text4_warn.Show()
                        textBox.SetBackgroundColour(wx.Colour(255, 150, 150))
                        textBox.Refresh()
                        self._hasOutput = False
                        self.btnAceptar.Disable()
                else:
                    # self.text4_warn.SetLabel("No puede estar vacío")
                    # self.text4_warn.Show()
                    textBox.SetBackgroundColour(wx.Colour(255, 150, 150))
                    textBox.Refresh()
                    self._hasOutput = False
                    self.btnAceptar.Disable()
            else:
                print(textBox)
        
        
        def get_list_data(self):
            count = self.folderList.GetItemCount()
            itemlist = []
            for row in range(count):
                itemlist.append(self.folderList.GetItem(itemIdx=row, col=0).Text)
            return itemlist