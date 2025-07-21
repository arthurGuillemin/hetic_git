import os
import struct
from ..core import get_git_dir

def ls_files():
    git_dir = get_git_dir()
    if not git_dir:
        print("[ERR] Pas un dépôt git.")
        return
    
    index_path = os.path.join(git_dir, 'index')
    
    if not os.path.exists(index_path):
        return
    
    try:
        with open(index_path, 'rb') as f:
            f.read(4)
            f.read(4)
            num_entries = struct.unpack('>I', f.read(4))[0]
            
            files = []
            
            for _ in range(num_entries):
                f.read(60)
                
                flags = struct.unpack('>H', f.read(2))[0]
                name_length = flags & 0xfff
                
                filename = f.read(name_length).decode('utf-8')
                files.append(filename)
                
                entry_size = 62 + name_length
                padding = (8 - (entry_size % 8)) % 8
                f.read(padding)
            
            for filename in sorted(files):
                print(filename)