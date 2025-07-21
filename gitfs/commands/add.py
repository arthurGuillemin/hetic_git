import os
import hashlib

from ..core import get_git_dir, write_object
from gitfs.utils.indexs import add_to_index

def add_file(file_path):
    if not os.path.isfile(file_path):
        print(f"[ERR] Le fichier '{file_path}' n'existe pas.")
        return

    with open(file_path, 'rb') as f:
        content = f.read()

    header = f'blob {len(content)}\0'.encode()
    store = header + content

    sha1 = hashlib.sha1(store).hexdigest()
    write_object(sha1, store)

    mode = "100644"

    filename = os.path.basename(file_path)

    add_to_index(mode, filename, sha1)

    print(f"[OK] Objet écrit dans : .mygit/objects/{sha1[:2]}/{sha1[2:]}")
    print(f"[OK] Fichier ajouté au staging : {filename}")
