import platform


class CodeLauncherException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UnsupportedOSException(CodeLauncherException):
    def __init__(self):
        super().__init__("Unsupported OS: " + platform.system())
