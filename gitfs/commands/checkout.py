import os
from gitfs.core import get_git_dir

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
