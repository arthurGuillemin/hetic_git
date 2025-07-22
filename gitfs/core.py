import os
import hashlib
import zlib

GIT_DIR_NAME = '.mygit'

def get_git_dir():
    return os.path.abspath(os.path.join(os.getcwd(), GIT_DIR_NAME))  # <- nouvelle version propre

def write_object(sha1, data):
    git_dir = get_git_dir()
    obj_path = os.path.join(git_dir, 'objects', sha1[:2], sha1[2:])
    os.makedirs(os.path.dirname(obj_path), exist_ok=True)

    with open(obj_path, 'wb') as f:
        f.write(zlib.compress(data))

    print(f"[OK] Objet écrit dans : {GIT_DIR_NAME}/objects/{sha1[:2]}/{sha1[2:]}")
