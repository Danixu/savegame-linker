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
import globals
import logging
from PIL import Image
from io import BytesIO
from sqlite3 import Binary

### Log Configuration ###
log = logging.getLogger("SavegameLinker")

#====================================================================
class addGame(wx.Dialog):
    ############# Funciones #############
    ## Función de salida ##
    def exitGUI(self, event):
        self.EndModal(0)
    
    def close(self):
        self.Destroy()

    def __init__(self, parent):
        wx.Dialog.__init__(
                self, 
                parent, 
                style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT, 
                title="Añadir juego", 
                size=(485,520)
            )
            
        # Variables
        self.updated = False
        
        # Binding close button to avoid memory leak
        # If not, when close button is pressed instead cancel, it keeps the memory
        # in use
        self.Bind(wx.EVT_CLOSE, self.exitGUI)
        
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
            
            # Variables
            self._hasName = False
            self._hasFolders = False
            self._hasOutput = False
    
            ### Grupo Título ###
            text1 = wx.StaticText(self, id=wx.ID_ANY, label="Título:",
                    pos=(6, 5), size=wx.DefaultSize, style=0,
                    name=wx.StaticTextNameStr)
            text1.SetFont(globals.labelFormat)
            text1.SetForegroundColour(wx.Colour(0, 51, 153))
            self.text1_warn = wx.StaticText(self, id=wx.ID_ANY, label="No puede estar vacío",
                    pos=(280, 5), size=wx.DefaultSize, style=0,
                    name=wx.StaticTextNameStr)
            self.text1_warn.SetFont(globals.labelFormat)
            self.text1_warn.SetForegroundColour(wx.Colour(255, 0, 0))
            self.textBox1 = wx.TextCtrl(self, -1, "", (6, 23), (450, 20),
                    wx.BORDER_STATIC|wx.TE_LEFT)
            self.textBox1.SetFont(globals.textBoxFormat)
            self.textBox1.SetBackgroundColour(wx.Colour(255, 150, 150))
 
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
            text3 = wx.StaticText(self, id=wx.ID_ANY, label="Carpetas a añadir:",
                    pos=(6, 90), size=wx.DefaultSize, style=0,
                    name=wx.StaticTextNameStr)
            text3.SetFont(globals.labelFormat)
            text3.SetForegroundColour(wx.Colour(0, 51, 153))
            self.text3_warn = wx.StaticText(self, id=wx.ID_ANY, label="No puede estar vacío",
                    pos=(280, 90), size=wx.DefaultSize, style=0,
                    name=wx.StaticTextNameStr)
            self.text3_warn.SetFont(globals.labelFormat)
            self.text3_warn.SetForegroundColour(wx.Colour(255, 0, 0))
            self.folderList = wx.ListCtrl(self, id=wx.ID_ANY, pos=(6, 108), 
                    size=(410,200), style=wx.LC_REPORT | wx.BORDER_STATIC | wx.LC_NO_HEADER, 
                    validator=wx.DefaultValidator, name=wx.ListCtrlNameStr)
            self.folderList.InsertColumn(0, '', width=wx.LIST_AUTOSIZE_USEHEADER)
            self.folderList.SetBackgroundColour(wx.Colour(255, 150, 150))
             
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
                    audio_click=str(globals.dataFolder["audio"] / 'Click1.ogg'),
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
                    audio_click=str(globals.dataFolder["audio"] / 'Click1.ogg'),
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
            self.text4_warn = wx.StaticText(self, id=wx.ID_ANY, label="No puede estar vacío",
                    pos=(280, 315), size=wx.DefaultSize, style=0,
                    name=wx.StaticTextNameStr)
            self.text4_warn.SetFont(globals.labelFormat)
            self.text4_warn.SetForegroundColour(wx.Colour(255, 0, 0))
            self.textBox3 = wx.TextCtrl(self, -1, "", (6, 333), (450, 20),
                    wx.BORDER_STATIC|wx.TE_LEFT)
            self.textBox3.SetFont(globals.textBoxFormat)
            self.textBox3.SetBackgroundColour(wx.Colour(255, 150, 150))
            
            ### Grupo Checkbox ###
            self.check1 = wx.CheckBox(
                    self, id=wx.ID_ANY, 
                    label="Mover ficheros a la carpeta del programa",
                    pos=(6, 360), size=(250,20)
                )
            self.check1.SetValue(globals.options['moveOnAdd'])
            self.check2 = wx.CheckBox(
                    self, id=wx.ID_ANY, 
                    label="Generar enlace simbólico después de mover",
                    pos=(6, 380), size=(250,20)
                )
            self.check2.SetValue(globals.options['linkOnAdd'])
            #Set Check2 status depending of Check1
            self.checkBoxChange(None)

            self.btnAceptar = wx.Button(self, -1, "Aceptar",
                    pos=(150, 410), size=(80,30)
                )
            self.btnAceptar.Bind(wx.EVT_LEFT_UP, self.addGameToDB)
            self.btnAceptar.Disable()
                
            self.btnCancelar = wx.Button(self, -1, "Cancelar",
                    pos=(236, 410), size=(80,30)
                )
            self.btnCancelar.Bind(wx.EVT_LEFT_UP, self.mainWindow.exitGUI)        

            # Binds
            self.Bind(wx.EVT_CHECKBOX, self.checkBoxChange)
            self.Bind(wx.EVT_TEXT, self.textBoxChange)
            
            
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
                        
            if self.folderList.GetItemCount() > 0:
                self.text3_warn.Hide()
                self.folderList.SetBackgroundColour(wx.Colour(255, 255, 255))
                self.folderList.Refresh()
                self._hasFolders = True
                if self._hasFolders and self._hasName and self._hasOutput:
                    self.btnAceptar.Enable()
            else:
                self.text3_warn.Show()
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
            if self.folderList.GetItemCount() > 0:
                self.text3_warn.Hide()
                self.folderList.SetBackgroundColour(wx.Colour(255, 255, 255))
                self.folderList.Refresh()
                self._hasFolders = True
                if self._hasFolders and self._hasName and self._hasOutput:
                    self.btnAceptar.Enable()
            else:
                self.text3_warn.Show()
                self.folderList.SetBackgroundColour(wx.Colour(255, 150, 150))
                self.folderList.Refresh()
                self._hasFolders = False
                self.btnAceptar.Disable()
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

            # Create saves folder
            if not os.path.isdir(os.path.join(
                        globals.fullPath(globals.options['savesFolder']),
                        folderName)):
                os.makedirs(os.path.join(
                        globals.fullPath(globals.options['savesFolder']),
                        folderName
                    ))
            
            # Create a dictionary with sources and destinations
            actual = 0
            foldersData = {}
            for folder in folders:
                dst = os.path.join(
                        globals.fullPath(globals.options['savesFolder']),
                        folderName,
                        "{0:03d}".format(actual)
                    )
                    
                foldersData.update({
                        folder: globals.relativePath(dst)
                    })
                
                actual+=1
            
            icon_data = None
            if os.path.isfile(icon):
                # The file is saved to BytesIO and reopened because
                # if not, some ico files are not resized correctly
                tmp_data = BytesIO()
                tmp_image = Image.open(icon)
                tmp_image.save(tmp_data, "PNG", compress_level = 1)
                tmp_image.close()
                
                tmp_image = Image.open(tmp_data)
                
                if tmp_image.size[0] < 44 and tmp_image.size[1] < 44:
                    width, height = tmp_image.size
                
                    if width > height:
                        factor = 44 / width
                        width = 44
                        height = int(height * factor)
                        
                        if height%2 > 0:
                            height += 1
                        
                        tmp_image = tmp_image.resize((width, height), Image.LANCZOS)
                    else:
                        factor = 44 / height
                        width = int(width * factor)
                        height = 44
                        
                        if width%2 > 0:
                            height += 1
                        
                        tmp_image = tmp_image.resize((width, height), Image.LANCZOS)

                else:
                    tmp_image.thumbnail((44, 44), Image.LANCZOS)

                icon_data = BytesIO()
                tmp_image.save(icon_data, "PNG", optimize=True)
                tmp_image.close()
                tmp_data.close()

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
                        "({}, {}, {});".format(game_id, dst, globals.folderToWindowsVariable(src))
                    )
                c.execute(
                        "INSERT INTO Saves (game_id, source, destination) VALUES " +
                        "(?, ?, ?);", (game_id, dst, globals.folderToWindowsVariable(src))
                    )
            c.close()
            
            # If move files and create symlink are checked, then do it
            for src, dst in foldersData.items():
                if moveFiles:
                    os.rename(src, dst)
                
                if createSymbolic:
                    globals.makeSymbolicLink(src, dst)

            globals.saveOption('moveOnAdd', moveFiles)
            globals.saveOption('linkOnAdd', createSymbolic)
            # If everything was fine, we commit the data to DB
            globals.db_savedata.commit()
            
            # Set the game as added to update on close
            self.updated = True
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
                    temp = globals.db_savedata.cursor()
                    temp.execute(
                        "SELECT COUNT(name) FROM Games WHERE name = ?",
                        (textBoxText,)
                    )
                    found = temp.fetchone()
                    temp.close()
                    
                    if not found or found[0] == 0:
                        self.text1_warn.Hide()
                        textBox.SetBackgroundColour(wx.Colour(255, 255, 255))
                        textBox.Refresh()
                        self._hasName = True
                        if self._hasFolders and self._hasName and self._hasOutput:
                            self.btnAceptar.Enable()
                    else:
                        self.text1_warn.SetLabel("El título ya existe")
                        self.text1_warn.Show()
                        textBox.SetBackgroundColour(wx.Colour(255, 150, 150))
                        textBox.Refresh()
                        self._hasName = False
                        self.btnAceptar.Disable()
                else:
                    self.text1_warn.SetLabel("No puede estar vacío")
                    self.text1_warn.Show()
                    textBox.SetBackgroundColour(wx.Colour(255, 150, 150))
                    textBox.Refresh()
                    self._hasName = False
                    self.btnAceptar.Disable()
            elif textBox == self.textBox3:
                # We verify if output folder exists
                if len(textBoxText) > 0:
                    fName = os.path.join(
                        globals.fullPath(globals.options['savesFolder']),
                        textBoxText
                    )
                    if not os.path.isdir(fName):
                        self.text4_warn.Hide()
                        textBox.SetBackgroundColour(wx.Colour(255, 255, 255))
                        textBox.Refresh()
                        self._hasOutput = True
                        if self._hasFolders and self._hasName and self._hasOutput:
                            self.btnAceptar.Enable()
                    else:
                        self.text4_warn.SetLabel("La carpeta ya existe")
                        self.text4_warn.Show()
                        textBox.SetBackgroundColour(wx.Colour(255, 150, 150))
                        textBox.Refresh()
                        self._hasOutput = False
                        self.btnAceptar.Disable()
                else:
                    self.text4_warn.SetLabel("No puede estar vacío")
                    self.text4_warn.Show()
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