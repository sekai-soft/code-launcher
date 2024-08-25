from code_launcher.diff import diff
from code_launcher.reconcile import reconcile


def main():
    _diff = diff()
    if _diff.is_empty():
        print("No changes to make.")
        return
    if _diff.adding_shortcuts:
        print(f"Adding shortcuts: {', '.join([shortcut.project_name for shortcut in _diff.adding_shortcuts])}")
    if _diff.deleting_shortcuts:
        print(f"Deleting shortcuts: {', '.join([shortcut.project_name for shortcut in _diff.deleting_shortcuts])}")
    reconcile(_diff)


if __name__ == "__main__":
    main()
