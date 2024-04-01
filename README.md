# Code Launcher
Jetbrains Toolbox for VSCode!

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