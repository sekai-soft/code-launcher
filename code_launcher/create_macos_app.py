import os
import hashlib
import base64
import stat
import shutil
from .ensure_shortcuts_folder import ensure_shortcuts_folder
from .find_vscode import find_vscode_installation_path
from .exception import CodeLauncherException


def hash_string(input_string):
    hash_object = hashlib.sha256(input_string.encode())
    hex_dig = hash_object.hexdigest()
    b64_string = base64.b64encode(bytes.fromhex(hex_dig)).decode()
    return b64_string.replace('+', '').replace('/', '')


print(hash_string("your string here"))


INFO_PLIST = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>en</string>
	<key>CFBundleExecutable</key>
	<string>script.sh</string>
	<key>CFBundleIconFile</key>
	<string>app.icns</string>
	<key>CFBundleIdentifier</key>
	<string>tech.sekaisoft.code-launcher.[CFBundleIdentifier_suffix]</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>[CFBundleName]</string>
	<key>CFBundlePackageType</key>
	<string>APPL</string>
	<key>CFBundleShortVersionString</key>
	<string></string>
	<key>CFBundleSignature</key>
	<string>????</string>
	<key>CFBundleVersion</key>
	<string>1.0.0</string>
	<key>NSHighResolutionCapable</key>
	<true/>
</dict>
</plist>'''


def create_macos_app(app_name: str, bash_script: str):
    shortcuts_folder = ensure_shortcuts_folder()

    # Create .app folder
    app_folder = os.path.join(shortcuts_folder, app_name + '.app')
    if os.path.exists(app_folder):
        raise CodeLauncherException(f'{app_folder} already exists')
    os.makedirs(app_folder)
    
    # Create .apps/Contents folder
    contents_folder = os.path.join(app_folder, 'Contents')
    os.makedirs(contents_folder)

    # Create .apps/Contents/Info.plist file
    info_plist = INFO_PLIST \
        .replace('[CFBundleName]', app_name) \
        .replace('[CFBundleIdentifier_suffix]', hash_string(app_name))
    with open(os.path.join(contents_folder, 'Info.plist'), 'w') as f:
        f.write(info_plist)

    # Create .apps/Contents/MacOS folder
    macos_folder = os.path.join(contents_folder, 'MacOS')
    os.makedirs(macos_folder)

    # Create .apps/Contents/MacOS/script.sh file
    script_sh_file = os.path.join(macos_folder, 'script.sh')
    with open(script_sh_file, 'w') as f:
        f.write(bash_script)
    st = os.stat(script_sh_file)
    os.chmod(script_sh_file, st.st_mode | stat.S_IEXEC)

    # Create .apps/Contents/PkgInfo file
    with open(os.path.join(contents_folder, 'PkgInfo'), 'w') as f:
        f.write('APPL????')

    # Create .apps/Contents/Resources folder
    resources_folder = os.path.join(contents_folder, 'Resources')
    os.makedirs(resources_folder)

    # Copy VSCode's icon over to .apps/Contents/Resources folder
    source_vscode_icon_file = os.path.join(
        find_vscode_installation_path(),
        os.pardir,
        "Code.icns")
    target_vscode_icon_file = os.path.join(resources_folder, 'app.icns')
    shutil.copyfile(source_vscode_icon_file, target_vscode_icon_file)
