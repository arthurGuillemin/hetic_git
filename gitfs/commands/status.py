import os
import hashlib
from index import read_index

def file_sha1(path):
    with open(path, "rb") as f:
        content = f.read()
    header = f"blob {len(content)}\0".encode()
    store = header + content
    return hashlib.sha1(store).hexdigest()

def status():
    index_entries = {filename: sha1 for _, filename, sha1 in read_index()}
    working_files = {f for f in os.listdir() if os.path.isfile(f) and not f.startswith('.')}

    print("[INFO] Fichiers ajoutés (staged) :")
    for f in sorted(index_entries):
        # Vérifie si le fichier existe et s'il est modifié
        if f in working_files:
            current_sha = file_sha1(f)
            if current_sha == index_entries[f]:
                print(f"  ➕ {f}")  # staged et non modifié
            else:
                print(f"  ✏️ {f} (modifié depuis staging)")  # staged mais modifié
        else:
            print(f"  ❌ {f} (supprimé depuis staging)")

    # Fichiers non suivis : dans le dossier mais pas dans l'index
    unstaged = working_files - set(index_entries.keys())
    if unstaged:
        print("[INFO] Fichiers non suivis :")
        for f in sorted(unstaged):
            print(f"  ❓ {f}")
