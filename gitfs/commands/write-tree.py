import os
import hashlib
from main import get_git_dir, write_object

def read_index():
    """
    Lit le fichier .mygit/index et retourne une liste d’entrées (mode, nom, sha1)
    """
    index_path = os.path.join(get_git_dir(), "index")
    if not os.path.exists(index_path):
        print("[WARN] Aucun fichier d’index trouvé.")
        return []

    entries = []
    with open(index_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                mode, filename, sha1 = parts
                entries.append((mode, filename, sha1))
    return entries

def write_tree():
    """
    Construit un objet tree à partir de l’index .mygit/index, l’écrit dans objects/, et retourne son SHA-1
    """
    entries = read_index()
    if not entries:
        print("[INFO] Aucun fichier dans l’index.")
        return None

    tree_content = b""
    for mode, filename, sha1 in sorted(entries, key=lambda x: x[1]):
        entry = f"{mode} {filename}".encode() + b"\0" + bytes.fromhex(sha1)
        tree_content += entry

    oid = write_object(tree_content, "tree")
    print(f"[OK] Objet écrit dans : .mygit/objects/{oid[:2]}/{oid[2:]}")
    print(f"[INFO] SHA-1 du tree : {oid}")
    return oid
