import sys
from gitfs.utils.read_object import read_object
from gitfs.utils.read_file import read_file

def ls_tree(args):
    if len(args) != 1:
        print("Usage: git ls-tree <tree_sha>", file=sys.stderr)
        sys.exit(1)

    tree_sha = args[0]

    obj_type = read_object(tree_sha)
    if obj_type != "tree":
        print(f"[ERR] {tree_sha} n'est pas un objet tree.")
        sys.exit(1)

    content = read_file(tree_sha)

    i = 0
    while i < len(content):
        space = content.index(b' ', i)
        mode = content[i:space].decode()

        null_byte = content.index(b'\x00', space)
        name = content[space + 1:null_byte].decode()

        sha_bin = content[null_byte + 1:null_byte + 21]
        sha = sha_bin.hex()

        pointed_type = read_object(sha)

        print(f"{mode} {pointed_type} {sha}\t{name}")

        i = null_byte + 21