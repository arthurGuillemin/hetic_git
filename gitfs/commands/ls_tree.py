from gitfs.utils.read_object import read_object

def ls_tree(args):
    if len(args) != 1:
        print("Usage: git ls-tree <tree-sha>")
        return

    oid = args[0]

    obj_type, content = read_object(oid)

    if obj_type != "tree":
        print(f"[ERR] {oid} n'est pas un objet tree.")
        return

    i = 0
    while i < len(content):
        space_index = content.find(b' ', i)
        mode = content[i:space_index].decode()

        null_index = content.find(b'\x00', space_index)
        filename = content[space_index+1:null_index].decode()

        sha1 = content[null_index+1:null_index+21].hex()

        print(f"{mode} {sha1} {filename}")

        i = null_index + 21
