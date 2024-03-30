from typing import Callable
from dataclasses import dataclass
from .create_vscode_shortcut import create_vscode_shortcut
from .list_vscode_shortcuts import list_vscode_shortcuts
from .delete_vscode_shortcut import delete_vscode_shortcut    
from .read_vscode_state import read_vscode_state
from .parse_vscode_uri import parse_vscode_uri


def reconcile():
    # read from VSCode state
    vscode_folder_uris = read_vscode_state()

    # read list of existing shortcuts
    existing_shortcuts = list_vscode_shortcuts()

    # reconcile: create and delete
    added_folder_uris = []
    for vscode_folder_uri in vscode_folder_uris:
        if vscode_folder_uri not in existing_shortcuts:
            added_folder_uris.append(vscode_folder_uri)
    deleted_folder_uris = []
    for existing_shortcut in existing_shortcuts:
        if existing_shortcut not in vscode_folder_uris:
            deleted_folder_uris.append(existing_shortcut)
    for added_folder_uri in added_folder_uris:
        # TODO: duplicate workspace names?
        create_vscode_shortcut(
            added_folder_uri,
            parse_vscode_uri(added_folder_uri).inferred_project_name,
        )
    for deleted_folder_uri in deleted_folder_uris:
        delete_vscode_shortcut(deleted_folder_uri)
