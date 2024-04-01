import platform
import os
import sys
import subprocess
from .exception import CodeLauncherUiException
from code_launcher.parse_vscode_uri import VscodeProjectType


DEV_ASSETS_FOLDER = 'assets'


# https://www.reddit.com/r/learnpython/comments/4kjie3/how_to_include_gui_images_with_pyinstaller/
def asset_file(relative_file):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_file)
     return os.path.join(os.path.abspath("."), DEV_ASSETS_FOLDER, relative_file)


# https://stackoverflow.com/questions/65294987/detect-os-dark-mode-in-python
def is_macos_dark_mode():
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return bool(p.communicate()[0])


if platform.system() == 'Windows':
    DEFAULT_FONT_SIZE = 10
elif platform.system() == 'Darwin':
    DEFAULT_FONT_SIZE = 12

if platform.system() == 'Windows':
    DEFAULT_FONT_FAMILY = 'Consolas'
elif platform.system() == 'Darwin':
    DEFAULT_FONT_FAMILY = 'Menlo'

APP_ICON = asset_file('icon.ico')
MENU_BAR_ICON = asset_file('icon.ico')
if platform.system() == 'Darwin':
    MENU_BAR_ICON = asset_file('icon_macos_menubar.ico')
APP_NAME = 'Code Launcher'

LOCAL_PROJECT_ICON = asset_file('local.ico')
if platform.system() == 'Darwin' and is_macos_dark_mode():
    LOCAL_PROJECT_ICON = asset_file('local_macos_dark.ico')

WSL_PROJECT_ICON = asset_file('wsl.ico')
if platform.system() == 'Darwin' and is_macos_dark_mode():
    WSL_PROJECT_ICON = asset_file('wsl_macos_dark.ico')

DEV_CONTAINER_PROJECT_ICON = asset_file('dev-container.ico')
if platform.system() == 'Darwin' and is_macos_dark_mode():
    DEV_CONTAINER_PROJECT_ICON = asset_file('dev-container_macos_dark.ico')

SSH_REMOTE_PROJECT_ICON = asset_file('ssh-remote.ico')
if platform.system() == 'Darwin' and is_macos_dark_mode():
    SSH_REMOTE_PROJECT_ICON = asset_file('ssh-remote_macos_dark.ico')

if platform.system() == 'Windows':
    SYNC_TO_OS_BUTTON_LABEL = "Sync to Start menu"
elif platform.system() == 'Darwin':
    SYNC_TO_OS_BUTTON_LABEL = "Sync to ~/Applications"

if platform.system() == 'Windows':
    SYNC_EXPLANATION = """Synchronizes your VSCode projects as shortcuts to the Start menu so that you can launch them quickly in Start menu or PowerToys Run."""
elif platform.system() == 'Darwin':
    SYNC_EXPLANATION = """Synchronizes your VSCode projects as apps to the ~/Applications folder so that you can launch them quickly in Spotlight."""

def project_type_to_icon(project_type) -> str:
    if project_type == VscodeProjectType.Local:
        return LOCAL_PROJECT_ICON
    elif project_type == VscodeProjectType.WSL:
        return WSL_PROJECT_ICON
    elif project_type == VscodeProjectType.DevContainer:
        return DEV_CONTAINER_PROJECT_ICON
    elif project_type == VscodeProjectType.SshRemote:
        return SSH_REMOTE_PROJECT_ICON
    raise CodeLauncherUiException(f"Unknown project type: {project_type}")
