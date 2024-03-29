import os
import json
import sqlite3
import platform
from typing import List
from .exception import CodeLauncherException, UnsupportedOSException


def parse_vscode_state(value: str) -> List[str]:
    try:
        folder_uris = []
        value = json.loads(value)
        if 'entries' not in value:
            raise CodeLauncherException("VSCode state does not contain 'entries'")
        entries = value['entries']
        for entry in entries:
            if 'folderUri' in entry:
                folder_uris.append(entry['folderUri'])
        return folder_uris
    except json.JSONDecodeError:
        raise CodeLauncherException("VSCode state is not a valid JSON")


def get_vscode_state_path() -> str:
    if platform.system() == 'Windows':
        if 'APPDATA' not in os.environ:
            raise CodeLauncherException("APPDATA is not found in environment variables")
        return os.path.join(os.environ['APPDATA'], "Code", "User", "globalStorage", "state.vscdb")
    elif platform.system() == 'Darwin':
        if 'HOME' not in os.environ:
            raise CodeLauncherException("HOME is not found in environment variables")
        return os.path.join(os.environ['HOME'], "Library", "Application Support", "Code", "User", "globalStorage", "state.vscdb")
    raise UnsupportedOSException()


def read_vscode_state() -> List[str]:
    p = get_vscode_state_path()
    if not os.path.exists(p):
        raise CodeLauncherException("VSCode state file is not found")
    conn = sqlite3.connect(p)
    c = conn.cursor()
    c.execute("SELECT * FROM ItemTable")
    state = c.fetchall()
    conn.close()
    for (key, value) in state:
        if key == "history.recentlyOpenedPathsList":
            return parse_vscode_state(value)
    raise CodeLauncherException("VSCode state file does not contain history.recentlyOpenedPathsList")
