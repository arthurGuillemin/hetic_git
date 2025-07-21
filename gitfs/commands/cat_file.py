import sys
from gitfs.utils.read_object import read_object
from gitfs.utils.read_file import read_file

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
            content = read_file(oid)
            try:
                print(content.decode(), end="")
            except UnicodeDecodeError:
                print(content)

        else:
            print("Erreur : option inconnue. Utilise -t ou -p", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)
