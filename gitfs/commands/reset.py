import os
import zlib
import hashlib
from gitfs.index import write_index
from gitfs.core import get_git_dir
from gitfs.utils import read_object  

def read_commit(sha):
    """Retourne (tree_sha, parent_sha, message)"""
    obj_type, data = read_object(sha)
    assert obj_type == 'commit', f"{sha} n'est pas un commit"
    lines = data.decode().split('\n')
    tree_sha = None
    for line in lines:
        if line.startswith('tree'):
            tree_sha = line.split()[1]
            break
    return tree_sha

def read_tree(sha):
    """Retourne une liste de (mode, filename, sha) depuis un tree"""
    obj_type, data = read_object(sha)
    assert obj_type == 'tree', f"{sha} n'est pas un tree"
    entries = []
    i = 0
    while i < len(data):
        space = data.find(b' ', i)
        mode = data[i:space].decode()
        null = data.find(b'\x00', space)
        filename = data[space+1:null].decode()
        sha = data[null+1:null+21].hex()
        entries.append((mode, filename, sha))
        i = null + 21
    return entries

def reset(sha, mode='mixed'):
    git_dir = get_git_dir()
    ref_path = os.path.join(git_dir, 'HEAD')

    # 1. Met à jour HEAD
    with open(ref_path, 'w') as f:
        f.write(sha)
    print(f"[OK] HEAD déplacé vers {sha}")

    if mode in ('mixed', 'hard'):
        # 2. Recharger l’index depuis le tree
        tree_sha = read_commit(sha)
        tree_entries = read_tree(tree_sha)
        write_index(tree_entries)
        print(f"[OK] Index mis à jour depuis {tree_sha}")

    if mode == 'hard':
        # 3. Remettre à jour les fichiers du répertoire de travail
        for _, filename, blob_sha in tree_entries:
            _, blob_data = read_object(blob_sha)
            with open(filename, 'wb') as f:
                f.write(blob_data)
        print("[OK] Répertoire de travail synchronisé (hard reset)")
