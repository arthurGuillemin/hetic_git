import os
import hashlib
import zlib
from gitfs.core import get_git_dir, write_object

def create_tree_from_index():
    git_dir = get_git_dir()
    index_path = os.path.join(git_dir, 'index')

    if not os.path.exists(index_path):
        print("[ERR] Aucun fichier index trouvé.")
        return None

    entries = []
    with open(index_path, 'r') as index_file:
        for line in index_file:
            sha1, filepath = line.strip().split(' ', 1)
            entries.append((filepath, sha1))

    tree_entries = []
    for filepath, sha1 in entries:
        mode = '100644'  # fichier classique (non-exécutable)
        tree_entries.append(f'{mode} {filepath}\0'.encode() + bytes.fromhex(sha1))

    # Encodage final
    content = b''.join(tree_entries)
    header = f'tree {len(content)}\0'.encode()
    store = header + content

    tree_sha1 = hashlib.sha1(store).hexdigest()
    write_object(tree_sha1, store)

    print(f"[OK] Arbre (tree) créé : {tree_sha1}")
    return tree_sha1
