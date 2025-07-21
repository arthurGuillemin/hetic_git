import os
from gitfs.core import get_git_dir

def get_index_path():
    return os.path.join(get_git_dir(), 'index')

def read_index():
    """
    Lit le fichier .mygit/index et retourne un dictionnaire {filename: sha1}
    """
    index_path = get_index_path()
    entries = {}
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            for line in f:
                sha1, path = line.strip().split(' ', 1)
                entries[path] = sha1
    return entries

def write_index(entries):
    """
    Écrit le dictionnaire {filename: sha1} dans .mygit/index
    """
    index_path = get_index_path()
    with open(index_path, 'w') as f:
        for path, sha1 in entries.items():
            f.write(f"{sha1} {path}\n")

def add_to_index(sha1, path):
    entries = read_index()
    entries[path] = sha1
    write_index(entries)
