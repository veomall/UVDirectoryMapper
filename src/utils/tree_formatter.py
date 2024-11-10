def format_tree(tree, prefix="", is_last=True):
    output = ""
    for i, (name, subtree) in enumerate(tree.items()):
        is_last_item = i == len(tree) - 1
        output += f"{prefix}{'└── ' if is_last_item else '├── '}{name}\n"
        if subtree is not None:
            extension = "    " if is_last_item else "│   "
            output += format_tree(subtree, prefix + extension, is_last_item)
    return output
