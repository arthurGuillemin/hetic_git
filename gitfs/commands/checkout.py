import os
from gitfs.core import get_git_dir
from gitfs.plumbery.restore_files_from_tree import restore_files_from_tree
from gitfs.utils.read_object import read_object

def checkout_branch(branch_name):
    git_dir = get_git_dir()
    head_path = os.path.join(git_dir, 'HEAD')
    branch_path = os.path.join(git_dir, 'refs', 'heads', branch_name)

    # Vérifie si la branche existe, sinon la crée à partir du HEAD actuel
    if not os.path.exists(branch_path):
        print(f"[INFO] Création de la branche '{branch_name}'")
        current_sha = ''

        # Si HEAD existe, on essaie de récupérer le commit courant
    if os.path.exists(head_path):
        with open(head_path, 'r') as f:
            head_ref = f.read().strip()

        if head_ref.startswith('ref: '):
            current_branch = head_ref[5:]
            current_branch_path = os.path.join(git_dir, current_branch)
            if os.path.exists(current_branch_path):
                with open(current_branch_path, 'r') as f:
                    current_sha = f.read().strip()

    # ✅ Assure-toi que le dossier existe avant d'écrire dedans
    os.makedirs(os.path.dirname(branch_path), exist_ok=True)

    with open(branch_path, 'w') as f:
        f.write(current_sha)
    # Mise à jour de HEAD vers cette branche
    os.makedirs(os.path.dirname(branch_path), exist_ok=True)
    with open(head_path, 'w') as f:
        f.write(f'ref: refs/heads/{branch_name}')

    print(f"[OK] Passage à la branche '{branch_name}'")

    # Restauration des fichiers à partir du commit de cette branche
    restore_working_directory_from_branch(branch_path)


def restore_working_directory_from_branch(branch_path):
    git_dir = get_git_dir()

    if not os.path.exists(branch_path):
        print(f"[ERR] La branche n'existe pas : {branch_path}")
        return

    with open(branch_path, 'r') as f:
        commit_sha = f.read().strip()

    if not commit_sha:
        print("[WARN] Aucun commit dans cette branche.")
        return

    try:
        obj_type, commit_data = read_object(commit_sha, git_dir=git_dir)
    except Exception as e:
        print(f"[ERR] Erreur lecture commit {commit_sha} : {e}")
        return

    if obj_type != "commit":
        print("[ERR] L'objet lu n'est pas un commit.")
        return

    lines = commit_data.decode().split('\n')
    tree_sha = None
    for line in lines:
        if line.startswith("tree "):
            tree_sha = line.split()[1]
            break

    if not tree_sha:
        print("[ERR] Aucun tree trouvé dans le commit.")
        return

    print(f"[INFO] Restauration des fichiers depuis le tree {tree_sha}")
    restore_files_from_tree(tree_sha)
