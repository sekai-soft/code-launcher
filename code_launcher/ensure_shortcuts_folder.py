import os
import platform
from .exception import CodeLauncherException, UnsupportedOSException


def ensure_shortcuts_folder() -> str:
    if platform.system() == 'Windows':
        if 'APPDATA' not in os.environ:
            raise CodeLauncherException('APPDATA environment variable is not found')
        p = os.path.join(
            os.environ['APPDATA'],
            'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Code Launcher Shortcuts')
        if not os.path.exists(p):
            os.makedirs(p)
        return p

    elif platform.system() == 'Darwin':
        if 'HOME' not in os.environ:
            raise CodeLauncherException('HOME environment variable is not found')
        p = os.path.join(
            os.environ['HOME'],
            'Applications', 'Code Launcher Shortcuts')
        if not os.path.exists(p):
            os.makedirs(p)
        return p

    elif platform.system() == 'Linux':
        if 'HOME' not in os.environ:
            raise CodeLauncherException('HOME environment variable is not found')
        p = os.path.join(
            os.environ['HOME'],
            '.local', 'share', 'applications', 'Code Launcher Shortcuts')
        if not os.path.exists(p):
            os.makedirs(p)
        return p

    raise UnsupportedOSException()
