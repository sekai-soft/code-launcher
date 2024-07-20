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
        * Should work as low as macOS Big Sur

## Download
* Windows
    * Download [here](https://nightly.link/sekai-soft/code-launcher/workflows/build/master/windows.zip)
    * The program might be erroneously identified by Windows Security/Defender as Trojan. Because malware authors also use Nuitka to build their trojans and please exempt `Code Launcher.exe` file.
    * Unzip the downloaded file and run `Code Launcher.exe`
* macOS (Apple Silicon)
    * Download [here](https://nightly.link/sekai-soft/code-launcher/workflows/build/master/mac-arm.zip)
    * Unzip the downloaded file and copy `Code Launcher.app` to your `Applications` folder

## Development

**Python 3.12 or newer is needed on both Windows or MacOS.**

<details>
<summary><h3>On Windows</h3></summary>

### Set Up Development Environment
```
python -m venv .
.\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements_win.txt
```

### Package App
```
.\Scripts\activate.bat
python -m nuitka app.py
```

Then find the built app in `app.dist` folder
</details>

<details>
<summary><h3>On MacOS</h3></summary>

### Set Up Development Environment
```
python -m venv .
./Scripts/activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements_win.txt
```

### Package App
```
./Scripts/activate
python -m nuitka app.py
```

Then find the built app in `app.dist` folder
</details>