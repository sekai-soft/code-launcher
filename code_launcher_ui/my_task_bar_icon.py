import wx
import platform
import subprocess
from wx.adv import TaskBarIcon, EVT_TASKBAR_LEFT_DOWN
from code_launcher.exception import UnsupportedOSException
from code_launcher.ensure_shortcuts_folder import ensure_shortcuts_folder
from .constants import MENU_BAR_ICON, APP_NAME


MENU_ITEM_SHOW_ID = 1
MENU_ITEM_OPEN_SHORTCUTS_FOLDER_ID = 2
MENU_ITEM_ABOUT_ID = 3
MENU_ITEM_QUIT_ID = 4


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
        menu.Append(MENU_ITEM_OPEN_SHORTCUTS_FOLDER_ID, 'Open shortcuts folder')
        menu.AppendSeparator()
        menu.Append(MENU_ITEM_ABOUT_ID, 'About')
        menu.Append(MENU_ITEM_QUIT_ID, 'Quit')
        return menu

    def onHandleTaskBarMenu(self, event):
        event_id = event.GetId()
        if platform.system() == 'Windows':
            opener = 'explorer.exe'
        elif platform.system() == 'Darwin':
            opener = 'open'
        else:
            raise UnsupportedOSException()

        if event_id == MENU_ITEM_SHOW_ID:
            self._show()
        elif event_id == MENU_ITEM_OPEN_SHORTCUTS_FOLDER_ID:
            subprocess.run([opener, ensure_shortcuts_folder()], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif event_id == MENU_ITEM_ABOUT_ID:
            subprocess.run([opener, "https://github.com/sekai-soft/code-launcher"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif event_id == MENU_ITEM_QUIT_ID:
            self.frame.quit()

    def OnTaskBarLeftClick(self, event):
        # this is no-op under macOS because the left click triggers the task bar menu
        self._show()

    def _show(self):
        self.frame.Show()
        self.frame.Restore()
