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

import os
from gitfs.core import get_git_dir

def write_index(entries):
    """
    Écrit les entrées dans .mygit/index au format :
    mode filename sha1
    """
    index_path = os.path.join(get_git_dir(), "index")
    with open(index_path, "w") as f:
        for mode, filename, sha1 in entries:
            f.write(f"{mode} {filename} {sha1}\n")

from gitfs.utils.indexs import read_index, write_index

def add_to_index(mode, filename, sha1):
    """
    Ajoute une entrée (mode, filename, sha1) à l'index.
    Remplace l'entrée existante si elle existe déjà.
    """
    entries = read_index()
    entries = [e for e in entries if e[1] != filename]
    entries.append((mode, filename, sha1))
    write_index(entries)

