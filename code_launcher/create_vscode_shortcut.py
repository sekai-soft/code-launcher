import os
import platform
from .find_vscode import find_vscode_bin_path, find_vscode_exe_path
from .ensure_shortcuts_folder import ensure_shortcuts_folder
from .create_macos_app import create_macos_app
from .list_vscode_shortcuts import ExistingShortcut
from .exception import UnsupportedOSException


def create_vscode_shortcut(shortcut: ExistingShortcut):
    if platform.system() == 'Windows':
        import pylnk3
        pylnk3.for_file(
            rf"{find_vscode_exe_path()}",
            rf"{os.path.join(ensure_shortcuts_folder(), shortcut.project_name + '.lnk')}",
            arguments=rf"--folder-uri {shortcut.folder_uri}",
            description=rf"Opens {shortcut.project_name} in VSCode",
            icon_file=rf"{find_vscode_exe_path()}",
            work_dir=rf"{find_vscode_bin_path()}",
            window_mode=r"Minimized"
        )
        return

    elif platform.system() == 'Darwin':
        create_macos_app(
            shortcut.project_name,
            # shebang is important here otherwise macOS won't be able to recognize the .app bundle as executable
            "#!/bin/bash\n" + find_vscode_exe_path().replace(" ", r"\ ") + " --folder-uri " + shortcut.folder_uri)
        return

    raise UnsupportedOSException()
