# Code Launcher
Jetbrains Toolbox for VSCode!

## How to use
The application is tested on

* Windows 11
    * Windows 10 should work as well
* macOS Sonoma on Apple Silicon
    * Should work as low as macOS Catalina
* VSCode stable version

Find the latest workflow run in [GitHub Actions tab](https://github.com/sekai-soft/code-launcher/actions)

Under the "Artifacts" section
* Windows
    * Download `windows`
    * The program might be erroneously identified by Windows Security/Defender as Trojan. This is a [known issue by PyInstaller](https://github.com/pyinstaller/pyinstaller/issues/5854) and please exempt the exe.
    * Unzip the downloaded file and run `Code Launcher.exe`
* macOS (Apple Silicon)
    * Download `mac-arm`
    * Unzip the downloaded file and copy `Code Launcher.app` to your `Applications` folder

## Development

### Package app on Windows
```
.\venv\Scripts\activate.bat
pyinstaller --name "Code Launcher" --windowed --icon assets\icon.ico --add-data "assets:." --clean --noconfirm .\app.py
```

Then find the built app in `dist` folder

### Package app on macOS
```
source ./venv/bin/activate
pyinstaller --name "Code Launcher" --windowed --icon assets/icon.ico --add-data "assets:." --clean --noconfirm ./app.py
```

Then find the built app in `dist` folder