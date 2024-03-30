import os
from .exception import CodeLauncherException

def ensure_shortcuts_folder() -> str:
    if 'APPDATA' not in os.environ:
        raise CodeLauncherException('APPDATA environment variable is not found')
    p = os.path.join(
        os.environ['APPDATA'],
        'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Code Launcher Shortcuts')
    if not os.path.exists(p):
        os.makedirs(p)
    return p
