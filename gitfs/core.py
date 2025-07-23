import os
import hashlib
import zlib

GIT_DIR_NAME = '.mygit'

def get_git_dir():
    current_dir = os.getcwd()

    while True:
        potential_git_dir = os.path.join(current_dir, GIT_DIR_NAME)
        if os.path.isdir(potential_git_dir):
            return os.path.abspath(potential_git_dir)

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise FileNotFoundError(f"Le dossier {GIT_DIR_NAME} n'a pas été trouvé dans les dossiers parents.")
        
        current_dir = parent_dir
def write_object(sha1, data):
    git_dir = get_git_dir()
    obj_path = os.path.join(git_dir, 'objects', sha1[:2], sha1[2:])
    os.makedirs(os.path.dirname(obj_path), exist_ok=True)

    with open(obj_path, 'wb') as f:
        f.write(zlib.compress(data))

    print(f"[OK] Objet écrit dans : {GIT_DIR_NAME}/objects/{sha1[:2]}/{sha1[2:]}")
