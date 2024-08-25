import platform
import subprocess
from .create_vscode_shortcut import create_vscode_shortcut
from .delete_vscode_shortcut import delete_vscode_shortcut    
from .diff import Diff
from .ensure_shortcuts_folder import ensure_shortcuts_folder


def reconcile(diff: Diff):
    for adding_shortcut in diff.adding_shortcuts:
        create_vscode_shortcut(adding_shortcut)
    for deleting_shortcut in diff.deleting_shortcuts:
        delete_vscode_shortcut(deleting_shortcut.folder_uri)
    
    if platform.system() == 'Linux':
        # refresh desktop entries
        subprocess.run(["update-desktop-database", ensure_shortcuts_folder()])
