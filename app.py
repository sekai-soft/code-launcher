import wx
from code_launcher_ui.my_frame import MyFrame


def main():
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
