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
