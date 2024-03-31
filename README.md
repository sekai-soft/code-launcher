# Code Launcher
Jetbrains Toolbox for VSCode!

## Development

### Package app on Windows
```
.\venv\Scripts\activate.bat
pyinstaller --name "Code Launcher" --windowed --icon assets\icon.ico --clean .\app.py
cp assets "dist\Code Launcher" -Recurse
```

Then find the built app in `dist` folder

### Package app on macOS
```
source ./venv/bin/activate
pyinstaller --name "Code Launcher" --windowed --icon assets/icon.ico --clean ./app.py
cp -r assets "dist/Code Launcher"
```

Then find the built app in `dist` folder