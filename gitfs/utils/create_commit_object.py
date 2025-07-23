import os
import hashlib
import zlib
import time
from gitfs.core import get_git_dir, write_object # Importations depuis core

def create_commit_object(tree_sha, message, parent_sha=None):
    """
    Crée un objet commit avec le tree, le message et un parent optionnel, et l'écrit dans le dépôt.
    """
    lines = [f'tree {tree_sha}']
    if parent_sha:
        lines.append(f'parent {parent_sha}')

    timestamp = int(time.time())
    timezone = '+0000'
    author = f'Test User <test@example.com> {timestamp} {timezone}'
    lines.append(f'author {author}')
    lines.append(f'committer {author}')
    lines.append('')
    lines.append(message)

    content = '\n'.join(lines).encode()
    header = f'commit {len(content)}\0'.encode()
    store = header + content

    sha1 = hashlib.sha1(store).hexdigest()

    write_object(sha1, store) # Utilise write_object de gitfs.core

    print(f"[INFO] SHA-1 du commit : {sha1}")
    print(sha1)
    return sha1

