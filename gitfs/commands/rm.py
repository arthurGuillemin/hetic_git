import os
from gitfs.index import read_index, write_index  # Assure-toi d’avoir write_index
from gitfs.core import get_git_dir

def remove_file(file_path):
    # 1. Vérifie que le fichier est suivi
    entries = read_index()
    new_entries = [entry for entry in entries if entry[1] != file_path]

    if len(new_entries) == len(entries):
        print(f"[WARN] Le fichier '{file_path}' n'est pas dans l'index.")
        return

    # 2. Supprimer du répertoire de travail
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"[OK] '{file_path}' supprimé du répertoire de travail.")
    else:
        print(f"[INFO] '{file_path}' n'existe pas dans le répertoire de travail.")

    # 3. Écrire la nouvelle version de l'index
    write_index(new_entries)
    print(f"[OK] '{file_path}' supprimé de l'index.")
