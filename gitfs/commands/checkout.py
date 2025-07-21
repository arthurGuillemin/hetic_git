import os
from gitfs.core import get_git_dir

from gitfs.plumbery.restore_files_from_tree import restore_files_from_tree
def checkout_branch(branch_name):
    git_dir = get_git_dir()
    head_path = os.path.join(git_dir, 'HEAD')
    branch_path = os.path.join(git_dir, 'refs', 'heads', branch_name)

    # Vérifie si la branche existe, sinon la créer à partir du commit HEAD actuel
    if not os.path.exists(branch_path):
        print(f"[INFO] Création de la branche '{branch_name}'")
        # Lire le SHA actuel pointé par HEAD
        with open(head_path, 'r') as f:
            head_ref = f.read().strip()
        if head_ref.startswith('ref: '):
            current_branch = head_ref[5:]
            current_branch_path = os.path.join(git_dir, current_branch)
            if os.path.exists(current_branch_path):
                with open(current_branch_path, 'r') as f:
                    current_sha = f.read().strip()
                with open(branch_path, 'w') as f:
                    f.write(current_sha)
            else:
                # Aucun commit encore (init)
                with open(branch_path, 'w') as f:
                    f.write('')
    
    # Mise à jour de HEAD vers la nouvelle branche
    with open(head_path, 'w') as f:
        f.write(f'ref: refs/heads/{branch_name}')
    
    print(f"[OK] Passage à la branche '{branch_name}'")


from gitfs.utils.read_object import read_object

def restore_working_directory_from_branch(branch_path):
    if not os.path.exists(branch_path):
        print(f"[ERR] La branche n'existe pas : {branch_path}")
        return

    with open(branch_path, 'r') as f:
        commit_sha = f.read().strip()

    if not commit_sha:
        print("[WARN] Aucun commit pour cette branche.")
        return

    try:
        obj_type, commit_data = read_object(commit_sha, git_dir=".mygit")
    except Exception as e:
        print(f"[ERR] Impossible de lire le commit {commit_sha} : {e}")
        return

    if obj_type != "commit":
        print("[ERR] L'objet n'est pas un commit.")
        return

    lines = commit_data.decode().split('\n')
    tree_sha = None
    for line in lines:
        if line.startswith("tree "):
            tree_sha = line.split()[1]
            break

    if not tree_sha:
        print("[ERR] Aucun tree trouvé dans ce commit.")
        return

    print(f"[INFO] Restauration des fichiers depuis le tree {tree_sha}")
    restore_files_from_tree(tree_sha)
