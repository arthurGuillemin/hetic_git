import sys
from gitfs.utils.read_object import read_object
from gitfs.utils.read_file import read_file

def parse_tree(data):
    i = 0
    entries = []
    while i < len(data):
        space_index = data.index(b' ', i)
        mode = data[i:space_index].decode()

        null_index = data.index(b'\x00', space_index)
        name = data[space_index + 1:null_index].decode()
        sha = data[null_index + 1:null_index + 21].hex()

        entries.append((mode, sha, name))
        i = null_index + 21

    return entries


def cat_file(args):
    if len(args) != 2:
        print("Usage: git cat-file -t|-p <oid>", file=sys.stderr)
        sys.exit(1)

    flag, oid = args

    try:
        if flag == "-t":
            obj_type = read_object(oid)
            print(obj_type)

        elif flag == "-p":
            type_ = read_object(oid)
            content = read_file(oid)

            if type_ == "blob":
                try:
                    sys.stdout.write(content.decode())
                except UnicodeDecodeError:
                    sys.stdout.buffer.write(content)

            elif type_ == "tree":
                entries = parse_tree(content)
                for mode, sha, name in entries:
                    print(f"{mode} {sha}\t{name}")

            else:
                print(f"(Non implémenté pour les objets de type : {type_})")

        else:
            print("Erreur : option inconnue. Utilise -t ou -p", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)
