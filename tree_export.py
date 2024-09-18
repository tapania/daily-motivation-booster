import os
import sys
import win32clipboard
import win32con

# Configuration Section
CONFIG = {
    "source_dir": ".",  # Default to current directory; can be overridden via command-line argument
    "ignore_files": {"README.md", "LICENSE", "tree_export.py", "gunicorn_conf.py"},  # Files to ignore
    "ignore_dirs": {"venv", "__pycache__", ".git", "node_modules", "alembic"},  # Directories to ignore
    "file_patterns": ["*.py", "*.js", "*.jsx", "*.ts", "*.tsx"],  # File patterns to include
}

def matches_pattern(filename, patterns):
    """Check if the filename matches any of the given patterns."""
    from fnmatch import fnmatch
    return any(fnmatch(filename, pattern) for pattern in patterns)

def generate_tree(root_dir, file_patterns, ignore_dirs, ignore_files):
    tree_lines = []

    def _generate_tree(current_path, prefix=""):
        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError:
            tree_lines.append(f"{prefix}└── [Permission Denied]")
            return

        # Filter out ignored directories and files
        dirs = [e for e in entries if os.path.isdir(os.path.join(current_path, e)) and e not in ignore_dirs]
        files = [e for e in entries if os.path.isfile(os.path.join(current_path, e)) 
                 and matches_pattern(e, file_patterns) 
                 and e not in ignore_files]

        all_entries = dirs + files
        entry_count = len(all_entries)

        for index, entry in enumerate(all_entries):
            path = os.path.join(current_path, entry)
            is_last = index == (entry_count - 1)
            connector = "└── " if is_last else "├── "
            tree_lines.append(f"{prefix}{connector}{entry}")

            if os.path.isdir(path):
                extension = "    " if is_last else "│   "
                _generate_tree(path, prefix + extension)

    # Start the tree with the root directory name
    root_name = os.path.basename(os.path.abspath(root_dir))
    tree_lines.append(root_name)
    _generate_tree(root_dir)
    return "\n".join(tree_lines)

def read_files_markdown(root_dir, file_patterns, ignore_files, ignore_dirs):
    from fnmatch import fnmatch
    markdown_content = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip ignored directories
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        
        # Filter files based on patterns and ignore list
        relevant_files = [f for f in filenames 
                          if matches_pattern(f, file_patterns) 
                          and f not in ignore_files]
        for file in sorted(relevant_files):
            file_path = os.path.join(dirpath, file)
            relative_path = os.path.relpath(file_path, root_dir)
            ext = os.path.splitext(file)[1][1:]  # e.g., 'py' or 'js'
            markdown_content.append(f"### `{relative_path}`\n")
            markdown_content.append(f"```{ext}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                markdown_content.append(content)
            except Exception as e:
                markdown_content.append(f"Error reading file: {e}")
            markdown_content.append("```\n")
    return "\n".join(markdown_content)

def copy_to_clipboard(text):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(f"Failed to copy to clipboard: {e}")

def main():
    # Update configuration based on command-line argument
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
        if not os.path.isdir(source_dir):
            print(f"Error: The provided path '{source_dir}' is not a directory.")
            sys.exit(1)
    else:
        source_dir = CONFIG["source_dir"]

    # Retrieve configurations
    ignore_files = CONFIG["ignore_files"]
    ignore_dirs = CONFIG["ignore_dirs"]
    file_patterns = CONFIG["file_patterns"]

    # Generate the ASCII tree
    tree_str = generate_tree(source_dir, file_patterns, ignore_dirs, ignore_files)

    # Generate the Markdown code blocks
    markdown_str = read_files_markdown(source_dir, file_patterns, ignore_files, ignore_dirs)

    # Combine both parts
    final_output = f"```\n{tree_str}\n```\n\n{markdown_str}"

    # Print the output (optional)
    print(final_output)

    # Copy to clipboard
    copy_to_clipboard(final_output)
    print("Output has been copied to the clipboard.")

if __name__ == "__main__":
    main()
