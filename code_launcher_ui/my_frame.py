import wx
import subprocess
import platform
from .constants import APP_ICON, APP_NAME, SYNC_BUTTON_LABEL, SYNC_EXPLAINATION, project_type_to_icon
from .my_task_bar_icon import MyTaskBarIcon
from code_launcher.exception import UnsupportedOSException
from code_launcher.read_vscode_state import read_vscode_state
from code_launcher.parse_vscode_uri import parse_vscode_uri
from code_launcher.find_vscode import find_vscode_exe_path
from code_launcher.reconcile import reconcile
from code_launcher.ensure_shortcuts_folder import ensure_shortcuts_folder


MENU_ITEM_OPEN_SHORTCUTS_FOLDER_ID = 1
MENU_ITEM_ABOUT_ID = 2
MENU_ITEM_EXIT_ID = 3


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=APP_NAME, size=(384, 683))
        self.taskBarIcon = MyTaskBarIcon(self)
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.SetIcon(wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)

        self.renderMainUI()
        self.Show()

        menuBar = wx.MenuBar() 
        helpMenu = wx.Menu() 
        helpMenu.Append(wx.MenuItem(
            helpMenu,
            MENU_ITEM_OPEN_SHORTCUTS_FOLDER_ID,
            text = "Open shortcuts folder",
            kind = wx.ITEM_NORMAL))
        helpMenu.AppendSeparator()
        helpMenu.Append(wx.MenuItem(
            helpMenu,
            MENU_ITEM_ABOUT_ID,
            text = "About",
            kind = wx.ITEM_NORMAL))
        helpMenu.Append(wx.MenuItem(
            helpMenu,
            MENU_ITEM_EXIT_ID,
            text = "Exit",
            kind = wx.ITEM_NORMAL))
        menuBar.Append(helpMenu, 'Help')
        self.Bind(wx.EVT_MENU, self.onHandleMenuBar) 
        self.SetMenuBar(menuBar) 

    def renderMainUI(self):
        vscode_projects = read_vscode_state()
        vscode_projects = sorted(vscode_projects, key=lambda p: (p.inferred_project_name, p.unique_project_identifier))
        self.sizer.AddSpacer(8)

        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        header_sizer.AddSpacer(8)
        header_project_count_text = wx.StaticText(self.panel, label=f'{len(vscode_projects)} projects')
        header_project_count_text.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        header_sizer.Add(header_project_count_text, flag=wx.ALIGN_CENTER_VERTICAL)
        header_sizer.AddSpacer(8)

        header_sync_button = wx.Button(self.panel, label=SYNC_BUTTON_LABEL)
        header_sync_button.Bind(wx.EVT_BUTTON, self.onSync)
        header_sizer.Add(header_sync_button, flag=wx.ALIGN_CENTER_VERTICAL)
        header_sizer.AddSpacer(4)

        header_sync_button_height = header_sync_button.GetSize().height
        header_explain_button = wx.Button(self.panel, label='?')
        header_explain_button.SetMinSize(wx.Size(header_sync_button_height, header_sync_button_height))
        header_explain_button.Bind(wx.EVT_BUTTON, self.onExplain)
        header_sizer.Add(header_explain_button, flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(header_sizer)

        self.sizer.AddSpacer(8)
        for vscode_project in vscode_projects:
            project_sizer = wx.BoxSizer(wx.HORIZONTAL)
            project_sizer.AddSpacer(8)

            project_icon_image = wx.StaticBitmap(
                self.panel,
                bitmap=wx.Bitmap(
                    project_type_to_icon(vscode_project.project_type)))
            project_icon_image.SetSize((32, 32))
            project_icon_image.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            # The issue you're experiencing is a common pitfall with Python's closures and late binding.
            # This causes the lambda function to capture the last value of vscode_project.folder_uri from the loop,
            # not the value at the time the lambda function was defined.
            # To fix this, you can use a default argument to capture the value of vscode_project.folder_uri at the time the lambda function is defined
            project_icon_image.Bind(wx.EVT_LEFT_DOWN, lambda event, uri=vscode_project.folder_uri: self.onLaunchVscodeProject(event, uri))
            project_sizer.Add(project_icon_image)
            project_sizer.AddSpacer(8)

            project_texts_sizer = wx.BoxSizer(wx.VERTICAL)

            project_name_text = wx.StaticText(self.panel, label=vscode_project.inferred_project_name)
            project_name_text.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            project_name_text.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            project_name_text.Bind(wx.EVT_LEFT_DOWN, lambda event, uri=vscode_project.folder_uri: self.onLaunchVscodeProject(event, uri))
            project_texts_sizer.Add(project_name_text)

            project_path_text = wx.StaticText(self.panel, label=vscode_project.url)
            project_path_text.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            project_path_text.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            project_path_text.Bind(wx.EVT_LEFT_DOWN, lambda event, uri=vscode_project.folder_uri: self.onLaunchVscodeProject(event, uri))
            project_texts_sizer.Add(project_path_text)

            project_sizer.Add(project_texts_sizer)

            self.sizer.Add(project_sizer)
            self.sizer.AddSpacer(16)
    
    def onLaunchVscodeProject(self, event, project_uri: str):
        subprocess.run([find_vscode_exe_path(), '--folder-uri', project_uri])

    def onSync(self, event):
        reconcile()

    def onExplain(self, event):
        wx.MessageBox(
            SYNC_EXPLAINATION,
            f'What is "{SYNC_BUTTON_LABEL}"?',
            wx.OK | wx.ICON_INFORMATION)

    def onHandleMenuBar(self, event):
        event_id = event.GetId()
        if platform.system() == 'Windows':
            opener = 'explorer.exe'
        elif platform.system() == 'Darwin':
            opener = 'open'
        else:
            raise UnsupportedOSException()

        if event_id == MENU_ITEM_OPEN_SHORTCUTS_FOLDER_ID: 
            subprocess.run([opener, ensure_shortcuts_folder()])
        elif event_id == MENU_ITEM_ABOUT_ID:
            subprocess.run([opener, "https://github.com/sekai-soft/code-launcher"])
        elif event_id == MENU_ITEM_EXIT_ID:
            self.onClose(event)

    def onClose(self, event):
        self.taskBarIcon.RemoveIcon()
        self.taskBarIcon.Destroy()
        self.Destroy()

    def onMinimize(self, event):
        if self.IsIconized():
            self.Hide()
