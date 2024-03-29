import wx
from .constants import APP_ICON, APP_NAME, project_type_to_icon
from .my_task_bar_icon import MyTaskBarIcon
from code_launcher.read_vscode_state import read_vscode_state
from code_launcher.parse_vscode_uri import parse_vscode_uri


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=APP_NAME, size=(384, 683))
        self.taskBarIcon = MyTaskBarIcon(self)
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.SetIcon(wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)

        self.render()
        self.Show()

    def render(self):
        self.sizer.AddSpacer(8)
        for project_uri in read_vscode_state():
            parsed_vscode_project = parse_vscode_uri(project_uri)
            project_sizer = wx.BoxSizer(wx.HORIZONTAL)
            project_sizer.AddSpacer(8)

            project_icon_image = wx.StaticBitmap(
                self.panel,
                bitmap=wx.Bitmap(
                    project_type_to_icon(parsed_vscode_project.project_type)))
            project_icon_image.SetSize((32, 32))
            project_sizer.Add(project_icon_image)
            project_sizer.AddSpacer(8)

            project_texts_sizer = wx.BoxSizer(wx.VERTICAL)

            project_name_text = wx.StaticText(self.panel, label=parsed_vscode_project.inferred_project_name)
            project_name_text.SetForegroundColour(wx.Colour(0, 0, 0))
            project_name_text.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            project_texts_sizer.Add(project_name_text)

            project_path_text = wx.StaticText(self.panel, label=parsed_vscode_project.url)
            project_path_text.SetForegroundColour(wx.Colour(128, 128, 128))
            project_path_text.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            project_texts_sizer.Add(project_path_text)

            project_sizer.Add(project_texts_sizer)

            self.sizer.Add(project_sizer)
            self.sizer.AddSpacer(16)

    def onClose(self, event):
        self.taskBarIcon.RemoveIcon()
        self.taskBarIcon.Destroy()
        self.Destroy()

    def onMinimize(self, event):
        if self.IsIconized():
            self.Hide()
