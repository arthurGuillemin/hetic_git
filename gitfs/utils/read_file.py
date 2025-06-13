import os
import zlib

def read_file(sha1, git_dir=".git"):
    
    path = os.path.join(git_dir, "objects", sha1[:2], sha1[2:])

    if not os.path.exists(path):
        raise FileNotFoundError(f"L'objet '{sha1}' est introuvable.")
    
    with open(path, "rb") as f:
        compressed = f.read()

    decompressed = zlib.decompress(compressed)
    
    null_index = decompressed.find(b'\x00')
    content = decompressed[null_index + 1:]

    
    return content

#    


        # data = f.read()
        # si - t:
        #    return decode(data).split(" ")[0]
        # si -p:
           