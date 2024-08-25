import os
import platform
import shutil
from .ensure_shortcuts_folder import ensure_shortcuts_folder
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
        for app_folder in os.listdir(ensure_shortcuts_folder()):
            if app_folder.endswith('.app'):
                with open(os.path.join(ensure_shortcuts_folder(), app_folder, 'Contents', 'MacOS', 'script.sh'), 'r') as f:
                    if f.read().endswith(f"--folder-uri {folder_uri}"):
                        shutil.rmtree(os.path.join(ensure_shortcuts_folder(), app_folder))
        return

    elif platform.system() == 'Linux':
        for _, _, files in os.walk(ensure_shortcuts_folder()):
            for f in files:
                if f.endswith(".desktop"):
                    desktop_f = os.path.join(ensure_shortcuts_folder(), f)
                    with open(desktop_f, 'r') as _f:
                        for line in _f:
                            if line.startswith("Exec="):
                                found_folder_uri = line.split(" ")[2].replace("%%", "%").strip()
                                if found_folder_uri == folder_uri:
                                    os.remove(desktop_f)
        return

    raise UnsupportedOSException()
