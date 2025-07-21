import os
from gitfs.utils.read_object import read_object

def restore_files_from_tree(tree_sha, base_path=""):
    obj_type, content = read_object(tree_sha, git_dir=".mygit")
    if obj_type != "tree":
        print(f"[ERR] Objet {tree_sha} n'est pas un tree")
        return

    i = 0
    while i < len(content):
        # format: mode SP name NULL sha
        space_index = content.find(b" ", i)
        mode = content[i:space_index].decode()

        null_index = content.find(b"\x00", space_index)
        name = content[space_index + 1:null_index].decode()

        sha = content[null_index + 1:null_index + 21]
        sha_hex = sha.hex()

        i = null_index + 21

        full_path = os.path.join(base_path, name)

        obj_type, obj_content = read_object(sha_hex, git_dir=".mygit")
        if obj_type == "blob":
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "wb") as f:
                f.write(obj_content)
        elif obj_type == "tree":
            os.makedirs(full_path, exist_ok=True)
            restore_files_from_tree(sha_hex, full_path)
