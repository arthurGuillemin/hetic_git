import os
import sys
import hashlib
import zlib
import time

def create_commit(tree_sha, message, parent_sha=None):
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

    sha1 = hashlib.sha1(store).hexdigest()
    obj_path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])

    os.makedirs(os.path.dirname(obj_path), exist_ok=True)

    with open(obj_path, 'wb') as f:
        f.write(zlib.compress(store))

    print(sha1)


if __name__ == "__main__":
    if not os.path.isdir('.git'):
        print("Error: Repository manquant (missing .git directory)")
        sys.exit(1)

    if len(sys.argv) < 4 or sys.argv[2] != "-m":
        print("Usage: python commit_tree.py <tree_sha> -m \"message\" [-p <parent_sha>]")
        sys.exit(1)

    tree_sha = sys.argv[1]
    message = sys.argv[3]
    parent_sha = None

    if len(sys.argv) > 5 and sys.argv[4] == "-p":
        parent_sha = sys.argv[5]

    create_commit(tree_sha, message, parent_sha)
