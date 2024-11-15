import os


def format_tree(tree, root_path, config, prefix="", is_last=True, is_root=True):
    output = ""
    if is_root:
        output += f"{os.path.basename(root_path)}/\n"
    
    for i, (name, subtree) in enumerate(tree.items()):
        is_last_item = i == len(tree) - 1
        is_directory = subtree is not None
        item_name = f"{name}/" if is_directory else name
        output += f"{prefix}{'└── ' if is_last_item else '├── '}{item_name}\n"
        if is_directory and not config.is_excluded(name):
            extension = "    " if is_last_item else "│   "
            output += format_tree(subtree, root_path, config, prefix + extension, is_last_item, is_root=False)
    return output
