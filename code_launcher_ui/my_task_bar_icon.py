import wx
import platform
from wx.adv import TaskBarIcon, EVT_TASKBAR_LEFT_DOWN
from .constants import MENU_BAR_ICON, APP_NAME


MENU_ITEM_SHOW_ID = 1
MENU_ITEM_QUIT_ID = 2


class MyTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        TaskBarIcon.__init__(self)
        self.frame = frame

        self.SetIcon(wx.Icon(MENU_BAR_ICON, wx.BITMAP_TYPE_ICO), APP_NAME)
        self.Bind(wx.EVT_MENU, self.onHandleTaskBarMenu)
        self.Bind(EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        if platform.system() == 'Darwin':
            menu.Append(MENU_ITEM_SHOW_ID, 'Show')
            menu.AppendSeparator()
        menu.Append(MENU_ITEM_QUIT_ID, 'Quit')
        return menu

    def onHandleTaskBarMenu(self, event):
        event_id = event.GetId()
        if event_id == MENU_ITEM_SHOW_ID:
            self._show()
        elif event_id == MENU_ITEM_QUIT_ID:
            self.frame.Close()

    def OnTaskBarLeftClick(self, event):
        # this is no-op under macOS because the left click triggers the task bar menu
        self._show()

    def _show(self):
        self.frame.Show()
        self.frame.Restore()
