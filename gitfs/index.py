import json
import os

INDEX_PATH = os.path.join(".git", "index.json")

def read_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r") as f:
            return json.load(f)
    return {}

def write_index(index):
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)

def add_to_index(file_path, sha):
    index = read_index()
    index[file_path] = sha
    write_index(index)
