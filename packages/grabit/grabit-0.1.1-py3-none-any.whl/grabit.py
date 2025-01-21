import os
import platform
import argparse
import dataclasses
import subprocess
from pathlib import Path
import re
from typing import List, Set

def copy_to_clipboard(text: str):
    """Copies text to clipboard based on OS."""
    system = platform.system()
    if system == 'Windows':
        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
    elif system == 'Darwin':  # macOS
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))

@dataclasses.dataclass
class File:
    path: str
    contents: str

def read_gitignore(directory: str) -> Set[str]:
    """
    Reads a .grabit file (if present) and returns a set of patterns as
    re.compile objects to ignore.
    """
    gitignore_path = Path(directory) / ".grabit"
    ignore_patterns = set()

    if gitignore_path.exists():
        print("--- Found .grabit ---")
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore comments and empty lines
                    ignore_patterns.add(re.compile(line))

    print("--- ignore patterns ---")
    print(ignore_patterns)
    return ignore_patterns

def is_ignored(file_path: str, ignore_patterns: Set[str], base_path: str) -> bool:
    """Checks if a file matches a regex pattern from the .grabit config."""
    for pattern in ignore_patterns:
        found = pattern.match(file_path)
        if found is not None:
            return True

    return False

def recursive_files(path: str, ignore_patterns: Set[str], data: List[File] = []) -> List[File]:
    """Recursively gets all file paths and contents in a directory, respecting .gitignore."""
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for file in files:
        file_path = os.path.join(path, file)

        if is_ignored(file_path, ignore_patterns, path):
            print(f"Skipping ignored file: {file_path}")
            continue

        print(f"Found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
                contents = f.read()
            data.append(File(file_path, contents))
        except Exception as e:
            print(f"Skipping {file_path}: {e}")

    for directory in directories:
        recursive_files(os.path.join(path, directory), ignore_patterns, data)
    
    return data

def prepare_context(path: str, output: str = None, to_clipboard: bool = False):
    """Prepares a context string for AI to read, optionally saves or copies it."""
    ignore_patterns = read_gitignore(path)
    files = recursive_files(path, ignore_patterns)

    context = "Below is a list of all the files in this project and their contents.\n\n"

    for file in files:
        unix_style_path = file.path.replace("\\", "/")
        context += f"## `{unix_style_path}`:\n```\n{file.contents}\n```\n\n"

    if output:
        with open(output, 'w', encoding="utf-8") as f:
            f.write(context)
        print(f"Context saved to {output}")

    if to_clipboard:
        print("Context copied to clipboard.")
        copy_to_clipboard(context)

    return context

def main():
    """Command-line interface for the script."""
    parser = argparse.ArgumentParser(
        description="Recursively scan a directory, extract file contents, and save/copy them, respecting .gitignore."
    )
    parser.add_argument("directory", type=str, help="The directory to scan")
    parser.add_argument("-o", "--output", type=str, help="File to save extracted content")
    parser.add_argument("-c", "--clipboard", action="store_true", help="Copy output to clipboard")

    args = parser.parse_args()

    prepare_context(args.directory, output=args.output, to_clipboard=args.clipboard)

if __name__ == "__main__":
    main()
