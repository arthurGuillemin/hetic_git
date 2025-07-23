import sys
from gitfs.utils.read_object import read_object

def ls_tree(args):
    if len(args) != 1:
        print("Usage: git ls-tree <tree_sha>", file=sys.stderr)
        sys.exit(1)

    tree_sha = args[0]

    try:
        obj_type, content = read_object(tree_sha)
    except Exception as e:
        print(f"[ERR] Impossible de lire l'objet {tree_sha} : {e}")
        sys.exit(1)

    if obj_type != "tree":
        print(f"[ERR] {tree_sha} n'est pas un objet tree.")
        sys.exit(1)

    i = 0
    while i < len(content):
        try:
            space = content.index(b' ', i)
            mode = content[i:space].decode()

            null_byte = content.index(b'\x00', space)
            name = content[space + 1:null_byte].decode()

            sha_bin = content[null_byte + 1:null_byte + 21]
            sha = sha_bin.hex()

            pointed_type, _ = read_object(sha)

            print(f"{mode} {pointed_type} {sha}\t{name}")

            i = null_byte + 21
        except Exception as e:
            print(f"[ERR] Erreur de parsing dans le tree : {e}")
            break
