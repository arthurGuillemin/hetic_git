import os
from gitfs.core import get_git_dir

def ls_files():
    index_path = os.path.join(get_git_dir(), 'index')
    if not os.path.exists(index_path):
        print("[ERR] Fichier index introuvable.")
        return

    try:
        with open(index_path, 'r') as f:
            files = []
            for line in f:
                parts = line.strip().split(' ', 2)
                if len(parts) == 3:
                    _, filename, _ = parts
                    files.append(filename)
        for filename in sorted(files):
            print(filename)
    except Exception as e:
        print(f"[ERR] Une erreur est survenue : {e}")