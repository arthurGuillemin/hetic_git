import os
from gitfs.utils.index import read_index, write_index
from gitfs.core import get_git_dir

def remove_file(file_path):
    file_path = os.path.normpath(file_path)

    entries = read_index()
    print("[DEBUG] Contenu de l'index :", entries)
    print("[DEBUG] Chemin à supprimer :", file_path)

    normalized_keys = {}
    for entry in entries:
        filename = os.path.normpath(entry[1])
        normalized_keys[filename] = entry

    if file_path not in normalized_keys:
        print(f"[WARN] Le fichier '{file_path}' n'est pas dans l'index.")
        return

    key_to_remove = normalized_keys[file_path]
    entries.remove(key_to_remove)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"[OK] '{file_path}' supprimé du répertoire de travail.")
    else:
        print(f"[INFO] '{file_path}' n'existe pas dans le répertoire de travail.")

    write_index(entries)
    print(f"[OK] '{file_path}' supprimé de l'index.")
