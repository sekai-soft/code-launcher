from dataclasses import dataclass
from .list_vscode_shortcuts import list_vscode_shortcuts, ExistingShortcut
from .read_vscode_state import read_vscode_state


@dataclass
class Diff:
    adding_shortcuts: list[ExistingShortcut]
    deleting_shortcuts: list[ExistingShortcut]

    def is_empty(self):
        return len(self.adding_shortcuts) == 0 and len(self.deleting_shortcuts) == 0
    
    def adding_and_deleting(self):
        return len(self.adding_shortcuts) != 0 and len(self.deleting_shortcuts) != 0
    
    def adding_only(self):
        return len(self.adding_shortcuts) != 0 and len(self.deleting_shortcuts) == 0


def diff():
    # read from VSCode state
    parsed_vscode_projects = read_vscode_state()
    
    # dedup: map inferred project name to potentially multiple projects
    inferred_project_name_to_projects = {}
    for project in parsed_vscode_projects:
        if project.inferred_project_name not in inferred_project_name_to_projects:
            inferred_project_name_to_projects[project.inferred_project_name] = []
        inferred_project_name_to_projects[project.inferred_project_name].append(project)

    # dedup: if there are multiple projects with the same inferred project name,
    # use unique_project_name() instead of inferred_project_name
    desired_shortcuts = []
    for _, projects in inferred_project_name_to_projects.items():
        if len(projects) == 1:
            desired_shortcuts.append(ExistingShortcut(
                projects[0].inferred_project_name,
                projects[0].folder_uri))
        else:
            for project in projects:
                desired_shortcuts.append(ExistingShortcut(
                    project.unique_project_name(),
                    project.folder_uri))

    # read list of existing shortcuts
    existing_shortcuts = list_vscode_shortcuts()

    # diff
    adding_shortcuts = []
    for desired_shortcut in desired_shortcuts:
        if desired_shortcut not in existing_shortcuts:
            adding_shortcuts.append(desired_shortcut)
    deleting_shortcuts = []
    for existing_shortcut in existing_shortcuts:
        if existing_shortcut not in desired_shortcuts:
            deleting_shortcuts.append(existing_shortcut)
    
    return Diff(adding_shortcuts, deleting_shortcuts)
