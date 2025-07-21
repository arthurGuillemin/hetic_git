import os
from index import read_index

def status():
    index_entries = {filename for _, filename, _ in read_index()}
    working_files = {f for f in os.listdir() if os.path.isfile(f) and not f.startswith('.')}
    
    print("[INFO] Fichiers ajoutés (staged):")
    for f in sorted(index_entries):
        print(f"  ➕ {f}")

    unstaged = working_files - index_entries
    if unstaged:
        print("[INFO] Fichiers non suivis :")
        for f in sorted(unstaged):
            print(f"  ❓ {f}")
