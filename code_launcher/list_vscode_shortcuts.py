import os
import pylnk3
from typing import List
from .ensure_shortcuts_folder import ensure_shortcuts_folder


def list_vscode_shortcuts() -> List[str]:
    folder_uris = []
    for _, _, files in os.walk(ensure_shortcuts_folder()):
        for f in files:
            if f.endswith(".lnk"):
                lnk_f = os.path.join(ensure_shortcuts_folder(), f)
                lnk = pylnk3.parse(lnk_f)
                # splits out the uri in arguments "--folder-uri <uri>"
                folder_uris.append(lnk.arguments.split(" ")[1])
    return folder_uris
