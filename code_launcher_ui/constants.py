import platform
import os
from .exception import CodeLauncherUiException
from code_launcher.parse_vscode_uri import VscodeProjectType

ASSETS_FOLDER = 'assets' + os.sep

APP_ICON = ASSETS_FOLDER + 'icon.ico'
if platform.system() == 'Darwin':
    MENU_BAR_ICON = ASSETS_FOLDER + 'icon_mac_menu_bar.ico'
else:
    MENU_BAR_ICON = ASSETS_FOLDER + 'icon.ico'
APP_NAME = 'Code Launcher'

LOCAL_PROJECT_ICON = ASSETS_FOLDER + 'local.ico'
WSL_PROJECT_ICON = ASSETS_FOLDER + 'wsl.ico'
DEV_CONTAINER_PROJECT_ICON = ASSETS_FOLDER + 'dev-container.ico'

if platform.system() == 'Windows':
    SYNC_TO_OS_BUTTON_LABEL = "Sync to Start menu"
elif platform.system() == 'Darwin':
    SYNC_TO_OS_BUTTON_LABEL = "Sync to ~/Applications"

if platform.system() == 'Windows':
    SYNC_EXPLAINATION = """Synchronizes your VSCode projects as shortcuts to the Start menu so that you can launch them quickly in Start menu or PowerToys Run."""
elif platform.system() == 'Darwin':
    SYNC_EXPLAINATION = """Synchronizes your VSCode projects as apps to the ~/Applications folder so that you can launch them quickly in Spotlight."""

def project_type_to_icon(project_type) -> str:
    if project_type == VscodeProjectType.Local:
        return LOCAL_PROJECT_ICON
    elif project_type == VscodeProjectType.WSL:
        return WSL_PROJECT_ICON
    elif project_type == VscodeProjectType.DevContainer:
        return DEV_CONTAINER_PROJECT_ICON
    else:
        raise CodeLauncherUiException(f"Unknown project type: {project_type}")
