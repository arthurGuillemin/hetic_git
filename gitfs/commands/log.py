import os
import zlib
from main import get_git_dir

def log():
    head_path = os.path.join(get_git_dir(), 'refs', 'heads', 'master')
    if not os.path.exists(head_path):
        print("[WARN] Aucun commit")
        return

    current = open(head_path).read().strip()
    objects_path = os.path.join(get_git_dir(), 'objects')

    while current:
        obj_path = os.path.join(objects_path, current[:2], current[2:])
        with open(obj_path, 'rb') as f:
            raw = zlib.decompress(f.read())
        _, body = raw.split(b'\x00', 1)
        lines = body.decode().split('\n')
        print(f"commit {current}")
        for line in lines:
            if line.startswith('author'):
                print(line)
            elif not line.startswith(('tree', 'parent', 'committer')) and line.strip():
                print(f"    {line}")
        parent = next((l.split()[1] for l in lines if l.startswith('parent')), None)
        print()
        current = parent
