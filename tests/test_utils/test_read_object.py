import subprocess
import os
from gitfs.utils.read_object import read_object

def test_read_object_blob(tmp_path):
    os.chdir(tmp_path)

    subprocess.run(["git", "init"], check=True)

    file_path = tmp_path / "hello.txt"
    file_content = "Coucou Git !"
    file_path.write_text(file_content)

    result = subprocess.run(
        ["git", "hash-object", "-w", str(file_path)],
        stdout=subprocess.PIPE,
        check=True
    )
    oid = result.stdout.decode().strip()

    obj_type, content = read_object(oid)
    print(f"Type retourné : {obj_type}")

    assert obj_type == "blob"
    assert content == file_content.encode()