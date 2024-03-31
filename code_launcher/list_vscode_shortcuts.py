import os
import platform
from typing import List
from .ensure_shortcuts_folder import ensure_shortcuts_folder
from .exception import UnsupportedOSException


def list_vscode_shortcuts() -> List[str]:
    if platform.system() == 'Windows':
        import pylnk3
        folder_uris = []
        for _, _, files in os.walk(ensure_shortcuts_folder()):
            for f in files:
                if f.endswith(".lnk"):
                    lnk_f = os.path.join(ensure_shortcuts_folder(), f)
                    lnk = pylnk3.parse(lnk_f)
                    # splits out the uri in arguments "--folder-uri <uri>"
                    folder_uris.append(lnk.arguments.split(" ")[1])
        return folder_uris

    elif platform.system() == 'Darwin':
        folder_uris = []
        for app_folder in os.listdir(ensure_shortcuts_folder()):
            if app_folder.endswith('.app'):
                with open(os.path.join(ensure_shortcuts_folder(), app_folder, 'Contents', 'MacOS', 'script.sh'), 'r') as f:
                    folder_uris.append(f.read().split(" --folder-uri ")[1])
        return folder_uris

    raise UnsupportedOSException()
