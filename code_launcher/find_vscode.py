import os
import platform
from .exception import CodeLauncherException, UnsupportedOSException


"""
Finds the default installation path for VSCode
"""
def find_vscode_installation_path() -> str:
    if platform.system() == 'Windows':
        if "USERPROFILE" not in os.environ:
            raise CodeLauncherException("USERPROFILE is not found in environment variables")
        p = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Programs", "Microsoft VS Code")
        if not os.path.exists(p):
            raise CodeLauncherException("VSCode installation path is not found")
        return p
    elif platform.system() == 'Darwin':
        p = os.path.join("/Applications", "Visual Studio Code.app", "Contents", "Resources", "app")
        if not os.path.exists(p):
            raise CodeLauncherException("VSCode installation path is not found")
        return p
    raise UnsupportedOSException()

"""
Finds the default bin path for VSCode (User) on Windows
"""
def find_vscode_bin_path() -> str:
    p = os.path.join(find_vscode_installation_path(), "bin")
    if not os.path.exists(p):
        raise CodeLauncherException("VSCode bin path is not found")
    return p


"""
Finds the default executable path for VSCode
"""
def find_vscode_exe_path() -> str:
    if platform.system() == 'Windows':
        p = os.path.join(find_vscode_installation_path(), "Code.exe")
        if not os.path.exists(p):
            raise CodeLauncherException("VSCode executable path is not found")
        return p
    elif platform.system() == 'Darwin':
        p = os.path.join(find_vscode_bin_path(), "code")
        if not os.path.exists(p):
            raise CodeLauncherException("VSCode executable path is not found")
        return p
    raise UnsupportedOSException()
