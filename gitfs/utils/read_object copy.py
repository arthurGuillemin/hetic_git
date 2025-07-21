import os
import zlib
from gitfs.core import get_git_dir

def read_object(oid):
    obj_path = os.path.join(get_git_dir(), 'objects', oid[:2], oid[2:])
    
    if not os.path.exists(obj_path):
        raise Exception(f"Objet {oid} introuvable à l'emplacement {obj_path}")

    with open(obj_path, 'rb') as f:
        compressed = f.read()

    decompressed = zlib.decompress(compressed)
    nul_index = decompressed.index(b'\x00')
    header = decompressed[:nul_index].decode()
    type_, size = header.split(" ")
    content = decompressed[nul_index + 1:]

    return type_, content
