from .exception import CodeLauncherUiException
from code_launcher.parse_vscode_uri import VscodeProjectType


APP_ICON = 'icon.ico'
APP_NAME = 'Code Launcher'

LOCAL_PROJECT_ICON = 'local.ico'
WSL_PROJECT_ICON = 'wsl.ico'
DEV_CONTAINER_PROJECT_ICON = 'dev-container.ico'


def project_type_to_icon(project_type) -> str:
    if project_type == VscodeProjectType.Local:
        return LOCAL_PROJECT_ICON
    elif project_type == VscodeProjectType.WSL:
        return WSL_PROJECT_ICON
    elif project_type == VscodeProjectType.DevContainer:
        return DEV_CONTAINER_PROJECT_ICON
    else:
        raise CodeLauncherUiException(f"Unknown project type: {project_type}")
