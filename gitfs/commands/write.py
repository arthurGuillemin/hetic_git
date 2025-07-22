import os
import hashlib
from gitfs.main import get_git_dir, write_object

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
    entries = read_index()
    tree_content = b""
    for mode, filename, sha1 in sorted(entries, key=lambda x: x[1]):
        entry = f"{mode} {filename}".encode() + b"\0" + bytes.fromhex(sha1)
        tree_content += entry
    header = f"tree {len(tree_content)}\0".encode()
    full_data = header + tree_content
    sha1 = hashlib.sha1(full_data).hexdigest()
    write_object(sha1, full_data)
    print(f"[INFO] SHA-1 du tree : {sha1}")
    print(sha1)
    return sha1
