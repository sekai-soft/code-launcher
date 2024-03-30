import os
import pylnk3
from .ensure_shortcuts_folder import ensure_shortcuts_folder


def delete_vscode_shortcut(folder_uri: str):
    for _, _, files in os.walk(ensure_shortcuts_folder()):
        for f in files:
            if f.endswith(".lnk"):
                lnk_f = os.path.join(ensure_shortcuts_folder(), f)
                lnk = pylnk3.parse(lnk_f)
                # splits out the uri in arguments "--folder-uri <uri>"
                found_folder_uri = lnk.arguments.split(" ")[1]
                if found_folder_uri == folder_uri:
                    os.remove(lnk_f)
