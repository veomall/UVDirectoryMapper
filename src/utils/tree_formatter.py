import os


def format_tree(tree, root_path, prefix="", is_last=True, is_root=True):
    output = ""
    if is_root:
        output += f"{os.path.basename(root_path)}\n"
    
    for i, (name, subtree) in enumerate(tree.items()):
        is_last_item = i == len(tree) - 1
        output += f"{prefix}{'└── ' if is_last_item else '├── '}{name}\n"
        if subtree is not None:
            extension = "    " if is_last_item else "│   "
            output += format_tree(subtree, root_path, prefix + extension, is_last_item, is_root=False)
    return output
