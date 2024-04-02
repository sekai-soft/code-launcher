import platform
import os
import re
from enum import Enum
from dataclasses import dataclass
from urllib.parse import urlparse, unquote
from .exception import CodeLauncherException, UnsupportedOSException


class VscodeProjectType(Enum):
    Local = 1
    WSL = 2
    DevContainer = 3
    SshRemote = 4


@dataclass
class ParsedVscodeProject:
    project_type: VscodeProjectType
    inferred_project_name: str
    # in case there is a conflict in inferred_project_name
    unique_project_identifier: str
    url: str
    folder_uri: str

    def unique_project_name(self):
        return f"{self.inferred_project_name}-{self.project_type.name}-{self.unique_project_identifier}"


def _compute_url_for_file_project(path: str) -> str:
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
    elif platform.system() == 'Darwin':
        if 'HOME' not in os.environ:
            return path
        home = os.environ['HOME']
        if path.startswith(home):
            return path.replace(home, '~')
        return path
    raise UnsupportedOSException()


def _compute_url_for_remote_project(path: str) -> str:
    if path.startswith('/home'):
        username = path.split('/')[2]
        return f"~/{path[len(f'/home/{username}'):].lstrip('/')}"
    if path.startswith('/root'):
        return f"~/{path[len('/root'):].lstrip('/')}"
    if path.startswith('/mnt/c/Users'):
        username = path.split('/')[3]
        return f"~/{path[len(f'/mnt/c/Users/{username}'):].lstrip('/')}"
    if path.startswith('/c/Users'):
        username = path.split('/')[2]
        return f"~/{path[len(f'/c/Users/{username}'):].lstrip('/')}"
    return path


def _decoded_path_as_safe_filename(decoded_path: str) -> str:
        # For Windows (& macOS because it replaces forward slashes already)
        res = re.sub(r'[\\/*?:"<>|]', '_', decoded_path)  # replace reserved characters with underscore
        res = re.sub(r'\.$', '', res)  # remove trailing period
        res = re.sub(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$', '_', res, flags=re.I)  # replace reserved names
        return res


def parse_vscode_uri(uri: str) -> ParsedVscodeProject:
    parsed_uri = urlparse(uri)

    if parsed_uri.scheme == 'file':
        project_type = VscodeProjectType.Local
        decoded_path = unquote(parsed_uri.path)
        # if the project can be created on the local OS in the first place,
        # there is no worry that the project name (which is only a part of the original project path)
        # could ever exceed local OS limit
        inferred_project_name = decoded_path.split('/')[-1]
        unique_project_identifier = _decoded_path_as_safe_filename(decoded_path)
        url = _compute_url_for_file_project(decoded_path)

    elif parsed_uri.scheme == 'vscode-remote':
        decoded_netloc = unquote(parsed_uri.netloc)
        inferred_project_name = parsed_uri.path.split('/')[-1]
        if decoded_netloc.startswith('wsl+'):
            decoded_path = unquote(parsed_uri.path)
            project_type = VscodeProjectType.WSL
            wsl_name = decoded_netloc[len('wsl+'):]
            url = wsl_name + ":"  + _compute_url_for_remote_project(decoded_path)
            unique_project_identifier = _decoded_path_as_safe_filename(url)
        elif decoded_netloc.startswith('dev-container+'):
            project_type = VscodeProjectType.DevContainer
            dev_container_hash = decoded_netloc[len('dev-container+'):]
            unique_project_identifier = dev_container_hash[:8]
            url = 'dev-container'
        elif decoded_netloc.startswith('ssh-remote+'):
            decoded_path = unquote(parsed_uri.path)
            project_type = VscodeProjectType.SshRemote
            ssh_ip = decoded_netloc[len('ssh-remote+'):]
            url = ssh_ip + ":" + _compute_url_for_remote_project(decoded_path)
            unique_project_identifier = _decoded_path_as_safe_filename(url)
            
        else:
            raise CodeLauncherException(f"Unknown vscode-remote netloc type: {decoded_netloc}")

    else:
        raise CodeLauncherException(f"Unknown vscode uri scheme: {parsed_uri.scheme}")

    return ParsedVscodeProject(project_type, inferred_project_name, unique_project_identifier, url, uri)
