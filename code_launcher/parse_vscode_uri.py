import platform
import os
from enum import Enum
from dataclasses import dataclass
from urllib.parse import urlparse, unquote
from .exception import CodeLauncherException


class VscodeProjectType(Enum):
    Local = 1
    WSL = 2
    DevContainer = 3


@dataclass
class ParsedVscodeProject:
    project_type: VscodeProjectType
    inferred_project_name: str
    url: str


def get_url_for_file_project(path: str) -> str:
    if platform.system() == 'Windows':
        splits = path.split('/')
        windows_path_parts = [splits[1].capitalize()] + splits[2:]
        windows_path = '\\'.join(windows_path_parts)
        if 'USERPROFILE' not in os.environ:
            return windows_path
        windows_user_profile = os.environ['USERPROFILE']
        if windows_path.startswith(windows_user_profile):
            return windows_path.replace(os.environ['USERPROFILE'], '~')
        return windows_path
    return path


def parse_vscode_uri(uri: str) -> ParsedVscodeProject:
    parsed_uri = urlparse(uri)

    if parsed_uri.scheme == 'file':
        project_type = VscodeProjectType.Local
        decoded_path = unquote(parsed_uri.path)
        inferred_project_name = decoded_path.split('/')[-1]
        url = get_url_for_file_project(decoded_path)
    elif parsed_uri.scheme == 'vscode-remote':
        decoded_netloc = unquote(parsed_uri.netloc)
        inferred_project_name = parsed_uri.path.split('/')[-1]
        if decoded_netloc.startswith('wsl+'):
            decoded_path = unquote(parsed_uri.path)
            project_type = VscodeProjectType.WSL
            url = decoded_netloc[4:] + ":"  + decoded_path
        elif decoded_netloc.startswith('dev-container+'):
            project_type = VscodeProjectType.DevContainer
            url = 'dev-container'
        else:
            raise CodeLauncherException(f"Unknown vscode-remote netloc type: {decoded_netloc}")
    else:
        raise CodeLauncherException(f"Unknown vscode uri scheme: {parsed_uri.scheme}")

    return ParsedVscodeProject(project_type, inferred_project_name, url)
