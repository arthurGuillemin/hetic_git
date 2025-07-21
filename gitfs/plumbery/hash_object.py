import hashlib
import os
import zlib

def hash_object(data: bytes, obj_type="blob", write=True) -> str:
    header = f"{obj_type} {len(data)}\0"
    full_data = (header.encode() + data)
    sha1 = hashlib.sha1(full_data).hexdigest()

    if write:
        obj_path = os.path.join(".git", "objects", sha1[:2], sha1[2:])
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
        with open(obj_path, "wb") as f:
            f.write(zlib.compress(full_data))
    return sha1
