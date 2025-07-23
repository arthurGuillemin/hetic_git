import os

GIT_DIR_NAME = '.mygit'

def init_repo():
    current_dir = os.getcwd()
    git_dir = os.path.join(current_dir, GIT_DIR_NAME)

    if os.path.exists(git_dir):
        print("[ATT] Le dépôt .mygit existe déjà.")
        return

    os.makedirs(os.path.join(git_dir, 'objects'))
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'))

    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write('ref: refs/heads/master\n')

    print(f"[OK] Dépôt initialisé dans {git_dir}")
