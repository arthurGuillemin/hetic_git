import os
from gitfs.main import get_git_dir
def show_ref():
    refs_dir = os.path.join(get_git_dir(), 'refs', 'heads')
    for name in os.listdir(refs_dir):
        ref_path = os.path.join(refs_dir, name)
        with open(ref_path) as f:
            sha = f.read().strip()
        print(f"{sha} refs/heads/{name}")
