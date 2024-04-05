# -*- mode: python ; coding: utf-8 -*-
import os
import platform


if platform.system() == 'Windows':
    icon_file = os.path.join('assets', 'icon.ico')
elif platform.system() == 'Darwin':
    icon_file = os.path.join('assets', 'icon_macos.ico')


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Code Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[icon_file],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Code Launcher',
)

if platform.system() == 'Darwin':
    app = BUNDLE(
        coll,
        name='Code Launcher.app',
        icon=icon_file,
        bundle_identifier=None,
        info_plist={
            'LSUIElement': True
        }
    )
