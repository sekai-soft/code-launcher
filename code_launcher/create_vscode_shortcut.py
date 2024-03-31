import os
import platform
from .find_vscode import find_vscode_bin_path, find_vscode_exe_path
from .ensure_shortcuts_folder import ensure_shortcuts_folder
from .create_macos_app import create_macos_app
from .exception import UnsupportedOSException
from .parse_vscode_uri import parse_vscode_uri


def create_vscode_shortcut(folder_uri: str):
    inferred_project_name = parse_vscode_uri(folder_uri).inferred_project_name
    if platform.system() == 'Windows':
        import pylnk3
        pylnk3.for_file(
            rf"{find_vscode_exe_path()}",
            rf"{os.path.join(ensure_shortcuts_folder(), inferred_project_name + '.lnk')}",
            arguments=rf"--folder-uri {folder_uri}",
            description=rf"Opens {inferred_project_name} in VSCode",
            icon_file=rf"{find_vscode_exe_path()}",
            work_dir=rf"{find_vscode_bin_path()}",
            window_mode=r"Minimized"
        )
        return

    elif platform.system() == 'Darwin':
        create_macos_app(
            inferred_project_name,
            find_vscode_exe_path().replace(" ", "\ ") + " --folder-uri " + folder_uri)
        return

    raise UnsupportedOSException()
