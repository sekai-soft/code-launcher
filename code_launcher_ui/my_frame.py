import wx
import subprocess
import multiprocessing
import platform
from .constants import APP_ICON, APP_NAME, SYNC_TO_OS_BUTTON_LABEL, SYNC_EXPLANATION, project_type_to_icon, DEFAULT_FONT_SIZE, DEFAULT_FONT_FAMILY
from .my_task_bar_icon import MyTaskBarIcon
from code_launcher.read_vscode_state import read_vscode_state
from code_launcher.find_vscode import find_vscode_exe_path
from code_launcher.reconcile import reconcile
from code_launcher.diff import diff


WINDOW_WIDTH = 408
TEXT_CUTOFF_THRESHOLD_WIDTH = 336
TEXT_CUTOFF_LENGTH = 39


def scale_bitmap(bitmap, width, height):
    image = wx.Bitmap.ConvertToImage(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    return wx.Bitmap(image)


def launch_vscode_project(folder_uri: str):
    subprocess.run([find_vscode_exe_path(), '--folder-uri', folder_uri], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class MyFrame(wx.Frame):
    def __init__(self):
        self.defaultFont = wx.Font(DEFAULT_FONT_SIZE, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, DEFAULT_FONT_FAMILY)
        self.defaultFontBold = wx.Font(DEFAULT_FONT_SIZE, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, DEFAULT_FONT_FAMILY)

        wx.Frame.__init__(self, None, title=APP_NAME, size=(WINDOW_WIDTH, 683), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        self.taskBarIcon = MyTaskBarIcon(self)
        self.SetIcon(wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)

        self.panel = wx.ScrolledWindow(self)
        self.panel.SetScrollRate(0, 5)
        self.panel.SetFont(self.defaultFont)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)
        self.renderMainUI()

    def renderMainUI(self):
        vscode_projects = read_vscode_state()
        vscode_projects = sorted(vscode_projects, key=lambda p: (p.inferred_project_name, p.unique_project_identifier))
        self.sizer.AddSpacer(8)

        header_controls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        header_controls_sizer.AddSpacer(8)

        header_sync_from_vscode_button = wx.Button(self.panel, label="Sync from VSCode")
        header_sync_from_vscode_button.Bind(wx.EVT_BUTTON, self.onSyncFromVSCode)
        header_controls_sizer.Add(header_sync_from_vscode_button, flag=wx.ALIGN_CENTER_VERTICAL)
        header_controls_sizer.AddSpacer(4)
        header_button_height = header_sync_from_vscode_button.GetSize().height

        _diff = diff()
        if _diff.is_empty():
            header_sync_to_os_label = SYNC_TO_OS_BUTTON_LABEL
        elif _diff.adding_and_deleting():
            header_sync_to_os_label = SYNC_TO_OS_BUTTON_LABEL + f' (+{len(_diff.adding_shortcuts)}, -{len(_diff.deleting_shortcuts)})'
        elif _diff.adding_only():
            header_sync_to_os_label = SYNC_TO_OS_BUTTON_LABEL + f' (+{len(_diff.adding_shortcuts)})'
        else:
            header_sync_to_os_label = SYNC_TO_OS_BUTTON_LABEL + f' (-{len(_diff.deleting_shortcuts)})'
        header_sync_to_os_button = wx.Button(self.panel, label=header_sync_to_os_label)
        if _diff.is_empty():
            header_sync_to_os_button.Disable()
        header_sync_to_os_button.Bind(wx.EVT_BUTTON, self.onSyncToOS)
        header_controls_sizer.Add(header_sync_to_os_button, flag=wx.ALIGN_CENTER_VERTICAL)
        header_controls_sizer.AddSpacer(4)

        header_explain_button = wx.Button(self.panel, label='?')
        header_explain_button.SetMinSize(wx.Size(header_button_height, header_button_height))
        header_explain_button.Bind(wx.EVT_BUTTON, self.onExplain)
        header_controls_sizer.Add(header_explain_button, flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(header_controls_sizer)
        self.sizer.AddSpacer(8)

        header_text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        header_text_sizer.AddSpacer(8)

        header_project_count_text = wx.StaticText(self.panel, label=f'{len(vscode_projects)} projects')
        header_text_sizer.Add(header_project_count_text, flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(header_text_sizer)
        self.sizer.AddSpacer(8)

        for vscode_project in vscode_projects:
            project_sizer = wx.BoxSizer(wx.HORIZONTAL)
            project_sizer.AddSpacer(8)

            project_icon_bitmap = scale_bitmap(
                wx.Bitmap(project_type_to_icon(vscode_project.project_type)),
                32,
                32)
            project_icon_image = wx.StaticBitmap(self.panel, -1, project_icon_bitmap)
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
            if project_name_text.GetSize().width > TEXT_CUTOFF_THRESHOLD_WIDTH:
                project_name_text.SetLabel(vscode_project.inferred_project_name[:TEXT_CUTOFF_LENGTH] + '...')
            project_name_text.SetToolTip(vscode_project.inferred_project_name)
            project_name_text.SetFont(self.defaultFontBold)
            project_name_text.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            project_name_text.Bind(wx.EVT_LEFT_DOWN, lambda event, uri=vscode_project.folder_uri: self.onLaunchVscodeProject(event, uri))
            project_texts_sizer.Add(project_name_text)

            project_path_text = wx.StaticText(self.panel, label=vscode_project.url)
            if project_path_text.GetSize().width > TEXT_CUTOFF_THRESHOLD_WIDTH:
                project_path_text.SetLabel(vscode_project.url[:TEXT_CUTOFF_LENGTH] + '...')
            project_path_text.SetToolTip(vscode_project.url)
            project_path_text.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            project_path_text.Bind(wx.EVT_LEFT_DOWN, lambda event, uri=vscode_project.folder_uri: self.onLaunchVscodeProject(event, uri))
            project_texts_sizer.Add(project_path_text)

            project_sizer.Add(project_texts_sizer)

            self.sizer.Add(project_sizer)
            self.sizer.AddSpacer(16)
            # added to prevent refreshing UI causing texts overlapping, don't know why though :(
            self.sizer.Layout()

    def onLaunchVscodeProject(self, event, project_uri: str):
        multiprocessing.Process(target=launch_vscode_project, args=(project_uri,)).start()

    def onSyncFromVSCode(self, event):
        self.sizer.Clear(True)
        self.renderMainUI()

    def onSyncToOS(self, event):
        reconcile(diff())
        self.onSyncFromVSCode(event)

    def onExplain(self, event):
        wx.MessageBox(
            SYNC_EXPLANATION,
            f'What is "{SYNC_TO_OS_BUTTON_LABEL}"?',
            wx.OK | wx.ICON_INFORMATION)

    def onClose(self, event):
        if platform.system() == 'Darwin':
            self.Hide()
        else:
            self.quit()

    def quit(self):
        self.taskBarIcon.RemoveIcon()
        self.taskBarIcon.Destroy()
        self.Destroy()

    def onMinimize(self, event):
        self.Hide()
