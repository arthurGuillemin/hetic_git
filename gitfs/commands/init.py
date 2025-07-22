import os

GIT_DIR_NAME = '.mygit'

def get_git_dir():
    # Remonte d'un niveau, puis ajoute .mygit
    root = os.path.dirname(os.getcwd())  # Parent du cwd
    return os.path.join(root, GIT_DIR_NAME)

def init_repo():
    git_dir = get_git_dir()
    if os.path.exists(git_dir):
        print("[ATT] Le dépôt .mygit existe déjà.")
        return

    os.makedirs(os.path.join(git_dir, 'objects'))
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'))

    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write('ref: refs/heads/master\n')

    print(f"[OK] Dépôt initialisé dans {git_dir}")
