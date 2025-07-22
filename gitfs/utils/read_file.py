import os
import zlib
from gitfs.core import get_git_dir

def read_file(sha1, git_dir=None):
    if git_dir is None:
        git_dir = get_git_dir()
    path = os.path.join(git_dir, "objects", sha1[:2], sha1[2:])

    if not os.path.exists(path):
        raise FileNotFoundError(f"L'objet '{sha1}' est introuvable.")
    with open(path, "rb") as f:
        compressed = f.read()

    decompressed = zlib.decompress(compressed)

    null_index = decompressed.find(b'\x00')
    content = decompressed[null_index + 1:]


    return content
