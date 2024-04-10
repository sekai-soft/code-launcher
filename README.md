# Code Launcher
Jetbrains Toolbox for VSCode! 

## Screenshots
Windows                    |  macOS
:-------------------------:|:-------------------------:
![Screenshot of Code Launcher on Windows](./docs/win-screenshot.png) | ![Screenshot of Code Launcher on macOS](./docs/mac-screenshot.webp)

## Features
* Lists all your VSCode workspaces
* Opens workspaces with one-click
    * Supports local, WSL, DevContainer and remote SSH workspaces
* Syncs workspaces as shortcuts to various places on the OS so that you can search for and open them conveniently
    * Start menu (Windows)
    * PowerToys Run (Windows)
    * Spotlight (macOS)
    * Alfred (macOS)
    * Raycast (macOS)
* Supports Windows and macOS
    * Tested on Windows 11
        * Windows 10 should work as well
    * Tested on macOS Sonoma on Apple Silicon
        * Should work as low as macOS Catalina

## Download
* Windows
    * Download [here](https://nightly.link/sekai-soft/code-launcher/workflows/build/master/windows.zip)
    * The program might be erroneously identified by Windows Security/Defender as Trojan. This is a [known issue by PyInstaller](https://github.com/pyinstaller/pyinstaller/issues/5854) and please exempt `Code Launcher.exe` file.
    * Unzip the downloaded file and run `Code Launcher.exe`
* macOS (Apple Silicon)
    * Download [here](https://nightly.link/sekai-soft/code-launcher/workflows/build/master/mac-arm.zip)
    * Unzip the downloaded file and copy `Code Launcher.app` to your `Applications` folder*

## Development

### Package app on Windows
```
.\venv\Scripts\activate.bat
pyinstaller --clean --noconfirm "Code Launcher.spec"
```

Then find the built app in `dist` folder

### Package app on macOS
```
source ./venv/bin/activate
pyinstaller --clean --noconfirm "Code Launcher.spec"
```

Then find the built app in `dist` folder