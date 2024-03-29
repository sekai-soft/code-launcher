import wx
from wx.adv import TaskBarIcon, EVT_TASKBAR_LEFT_DOWN
from .constants import APP_ICON, APP_NAME


class MyTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        TaskBarIcon.__init__(self)
        self.frame = frame

        self.SetIcon(wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO), APP_NAME)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=1)
        self.Bind(EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(1, 'Exit')
        return menu

    def OnTaskBarClose(self, event):
        self.frame.Close()

    def OnTaskBarLeftClick(self, event):
        self.frame.Show()
        self.frame.Restore()
