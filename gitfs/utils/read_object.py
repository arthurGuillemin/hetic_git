import os
import zlib
from gitfs.core import get_git_dir

def read_object(oid):
    path = os.path.join(get_git_dir(), 'objects', oid[:2], oid[2:])
    if not os.path.exists(path):
        raise Exception(f"Objet {oid} introuvable.")

    with open(path, 'rb') as f:
        compressed = f.read()

    decompressed = zlib.decompress(compressed)
    null_index = decompressed.index(b'\x00')
    header = decompressed[:null_index].decode()
    type_, _ = header.split(' ', 1)

    return type_

