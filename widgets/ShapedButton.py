import wx
from pygame import mixer
from time import sleep

#====================================================================
class ShapedButton(wx.Control):
  #----------------------------------------------------------
  def __init__(self, parent, image_normal, image_pressed=None, image_disabled=None, image_hover=None,
               audio_click=None, audio_enter=None, audio_leave=None,
               pos=wx.DefaultPosition, size=wx.DefaultSize):
    # Only load the pygame library if necessary
    if audio_click or audio_enter or audio_leave:
      from pygame import mixer
      mixer.pre_init(44100, -16, 2, 350)
      mixer.init();
    super(ShapedButton, self).__init__(parent, -1, style=wx.BORDER_NONE)
    self.image_normal = image_normal
    self.image_pressed = image_pressed
    self.image_disabled = image_disabled
    self.image_hover = image_hover
    self.audio_click = mixer.Sound(audio_click) if audio_click else None
    self.audio_enter = mixer.Sound(audio_enter) if audio_enter else None
    self.audio_leave = mixer.Sound(audio_leave) if audio_leave else None
    self.region = wx.Region(image_normal, wx.Colour(0, 0, 0, 0))
    self._clicked = False
    self._inside = False
    self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
    self.Bind(wx.EVT_SIZE, self.on_size)
    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
    self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)
    self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
    self.Bind(wx.EVT_MOTION, self.on_motion)
    self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter_window)
    self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)
    self.SetPosition(pos);
    self.SetInitialSize(size);
    
    

  #----------------------------------------------------------
  def DoGetBestSize(self):
    return self.image_normal.GetSize()

  #----------------------------------------------------------
  def Enable(self, *args, **kwargs):
    super(ShapedButton, self).Enable(*args, **kwargs)
    self.Refresh()

  #----------------------------------------------------------
  def Disable(self, *args, **kwargs):
    super(ShapedButton, self).Disable(*args, **kwargs)
    self.Refresh()

  #----------------------------------------------------------
  def post_event(self):
    event = wx.CommandEvent()
    event.SetEventObject(self)
    event.SetEventType(wx.EVT_BUTTON.typeId)
    wx.PostEvent(self, event)

  #----------------------------------------------------------
  def on_size(self, event):
    self.Refresh()
    event.Skip()

  #----------------------------------------------------------
  def on_paint(self, event):
    dc = wx.AutoBufferedPaintDC(self)
    dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
    dc.Clear()
    bitmap = self.image_normal
    if self._inside:
      bitmap = self.image_hover or bitmap
    if self.clicked:
      bitmap = self.image_pressed or bitmap
    if not self.IsEnabled():
      bitmap = self.image_disabled or bitmap
    dc.DrawBitmap(bitmap, 0, 0)

  #----------------------------------------------------------
  def set_clicked(self, clicked):
    if clicked != self._clicked:
      self._clicked = clicked
      self.Refresh()

  #----------------------------------------------------------
  def get_clicked(self):
    return self._clicked
    
  #----------------------------------------------------------
  def set_inside(self, inside):
    if inside != self._inside:
      self._inside = inside
      self.Refresh()

  #----------------------------------------------------------
  def get_inside(self):
    return self._inside

  clicked = property(get_clicked, set_clicked)
  inside = property(get_inside, set_inside)

  #----------------------------------------------------------
  def on_left_down(self, event):
    x, y = event.GetPosition();
    if self.region.Contains(x, y):
      self.clicked = True
      if self.audio_click:
        self.audio_click.play();
      event.Skip()

  #----------------------------------------------------------
  def on_left_dclick(self, event):
    self.on_left_down(event)

  #----------------------------------------------------------
  def on_left_up(self, event):
    if self.clicked:
      x, y = event.GetPosition()
      if self.region.Contains(x, y):
        self.clicked = False
        self.post_event()
        event.Skip()

  #----------------------------------------------------------
  def on_motion(self, event):
    if self.clicked:
      x, y = event.GetPosition()
      if not self.region.Contains(x, y):
        self.clicked = False
    event.Skip()

  #----------------------------------------------------------
  def on_enter_window(self, event):
    if self.audio_enter:
      self.audio_enter.play();
    self.clicked = False
    self.inside = True
    event.Skip()

  #----------------------------------------------------------
  def on_leave_window(self, event):
    self.clicked = False
    self.inside = False
    if self.audio_leave:
      self.audio_leave.play();
    event.Skip()