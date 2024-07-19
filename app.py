# OS-specified Setting
# nuitka-project-if: {OS} is "Darwin":
#    nuitka-project: --standalone
#    nuitka-project: --macos-create-app-bundle
#    nuitka-project: --macos-target-arch=arm64
#    nuitka-project: --macos-app-mode=gui
#    nuitka-project: --macos-app-name=Code Launcher
#    nuitka-project: --macos-app-protected-resource="NSAppDataUsageDescription:Determine the statu of VSCode and Lists all the VSCode workspaces"
# nuitka-project-if: {OS} is "Windows":
#    nuitka-project: --onefile
# Building Setting
# nuitka-project: --assume-yes-for-downloads
# nuitka-project: --follow-imports
# nuitka-project: --onefile
# nuitka-project: --lto=yes
# Console Setting
# nuitka-project: --windows-console-mode=disable
# Data Dir Setting
# nuitka-project: --include-data-dir=assets=assets
# Icon Setting
# nuitka-project: --windows-icon-from-ico=assets/icon.ico
# nuitka-project: --macos-app-icon=assets/icon.ico


import wx
import multiprocessing
from code_launcher_ui.my_frame import MyFrame


def main():
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    multiprocessing.freeze_support()
    main()
