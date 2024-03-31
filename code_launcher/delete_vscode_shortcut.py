import os
import platform
import shutil
from .ensure_shortcuts_folder import ensure_shortcuts_folder
from .parse_vscode_uri import parse_vscode_uri
from .exception import UnsupportedOSException


def delete_vscode_shortcut(folder_uri: str):
    if platform.system() == 'Windows':
        import pylnk3
        for _, _, files in os.walk(ensure_shortcuts_folder()):
            for f in files:
                if f.endswith(".lnk"):
                    lnk_f = os.path.join(ensure_shortcuts_folder(), f)
                    lnk = pylnk3.parse(lnk_f)
                    # splits out the uri in arguments "--folder-uri <uri>"
                    found_folder_uri = lnk.arguments.split(" ")[1]
                    if found_folder_uri == folder_uri:
                        os.remove(lnk_f)
        return

    elif platform.system() == 'Darwin':
        inferred_project_name = parse_vscode_uri(folder_uri).inferred_project_name
        app_folder = os.path.join(ensure_shortcuts_folder(), inferred_project_name + '.app')
        if os.path.exists(app_folder):
            shutil.rmtree(app_folder)
        return

    raise UnsupportedOSException()
