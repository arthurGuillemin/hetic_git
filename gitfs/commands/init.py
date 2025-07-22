import os

GIT_DIR_NAME = '.mygit' 


def get_git_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), GIT_DIR_NAME))

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

