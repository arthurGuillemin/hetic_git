import pytest
import os
import hashlib
import zlib


from gitfs.utils.read_file import read_file

def test_read_file_reads_binary_content(tmp_path):

    git_dir = tmp_path / ".git"
    objects_dir = git_dir / "objects"
    objects_dir.mkdir(parents=True)

    content = b"hello world"
    header = f"blob {len(content)}\0".encode()
    full_data = header + content
    sha1 = hashlib.sha1(full_data).hexdigest()

    sha1_dir = objects_dir / sha1[:2]
    sha1_dir.mkdir(parents=True)

    object_path = sha1_dir / sha1[2:]
    object_path.write_bytes(zlib.compress(full_data))

    result = read_file(sha1, git_dir=str(git_dir))
    print(content)

    assert result == content