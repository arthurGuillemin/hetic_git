import os
import zlib

def read_object(oid, git_dir=".git"):
    """Retourne uniquement le type de l’objet Git (blob, tree, commit...)"""
    path = os.path.join(git_dir, "objects", oid[:2], oid[2:])
    if not os.path.exists(path):
        raise Exception(f"Objet {oid} introuvable.")

    with open(path, "rb") as f:
        compressed = f.read()

    decompressed = zlib.decompress(compressed)
    header_end = decompressed.index(b'\x00')
    header = decompressed[:header_end].decode()
    obj_type = header.split()[0]

    return obj_type
