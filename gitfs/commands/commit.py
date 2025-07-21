import hashlib
import os
import time
from gitfs.plumbery.commit_tree import create_tree_from_index
from gitfs.core import write_object, get_git_dir

def create_commit(message, parent_sha=None):
    tree_sha = create_tree_from_index()
    if tree_sha is None:
        print("[ERR] Impossible de créer un commit : aucun arbre.")
        return

    lines = [f'tree {tree_sha}']
    if parent_sha:
        lines.append(f'parent {parent_sha}')

    timestamp = int(time.time())
    timezone = '+0000'
    author = f'Example User <example@example.com> {timestamp} {timezone}'

    lines.append(f'author {author}')
    lines.append(f'committer {author}')
    lines.append('')
    lines.append(message)

    content = '\n'.join(lines).encode()
    header = f'commit {len(content)}\0'.encode()
    store = header + content

    commit_sha = hashlib.sha1(store).hexdigest()
    write_object(commit_sha, store)

    # Enregistrer le commit HEAD
    git_dir = get_git_dir()
    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write(commit_sha)

    print(f"[OK] Commit créé : {commit_sha}")
