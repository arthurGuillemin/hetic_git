import os
from gitfs.core import get_git_dir

def rev_parse(ref):
    git_dir = get_git_dir()

    if ref == "HEAD":
        head_path = os.path.join(git_dir, 'HEAD')
        with open(head_path, 'r') as f:
            content = f.read().strip()
        if content.startswith('ref:'):
            ref_path = os.path.join(git_dir, content[5:])
        else:
            # SHA-1 direct (cas rare)
            print(content)
            return

    elif ref.startswith("refs/heads/"):
        ref_path = os.path.join(git_dir, ref)
    else:
        # Alias master → refs/heads/master
        ref_path = os.path.join(git_dir, 'refs', 'heads', ref)

    if not os.path.exists(ref_path):
        print(f"[ERR] Référence introuvable : {ref}")
        return

    with open(ref_path) as f:
        sha = f.read().strip()
        print(sha)
