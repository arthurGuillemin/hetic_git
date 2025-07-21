import os
import sys
import time
import hashlib
import zlib
import argparse
from gitfs.commands import add
from gitfs.commands import commit as commit_command
from gitfs.core import get_git_dir, write_object
from gitfs.index import read_index
from gitfs.commands import rm
from gitfs.commands import reset
from gitfs.commands import rev_parse


from gitfs.commands.cat_file import cat_file



GIT_DIR_NAME = '.mygit' 

def get_git_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), GIT_DIR_NAME))


def init_repo():
    git_dir = get_git_dir()
    if os.path.exists(git_dir):
        print("[ATT] Le dépôt .mygit existe déjà.")
        return

    os.makedirs(os.path.join(git_dir, 'objects'))
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'))

    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write('ref: refs/heads/master\n')

    print(f"[OK] Dépôt initialisé dans {git_dir}")




def write_object_local(sha1, data):
    git_dir = get_git_dir()
    obj_path = os.path.join(git_dir, 'objects', sha1[:2], sha1[2:])
    os.makedirs(os.path.dirname(obj_path), exist_ok=True)

    with open(obj_path, 'wb') as f:
        f.write(zlib.compress(data))

    print(f"[OK] Objet écrit dans : {GIT_DIR_NAME}/objects/{sha1[:2]}/{sha1[2:]}")


def write_tree():
    entries = read_index()
    tree_content = b""
    for mode, filename, sha1 in sorted(entries, key=lambda x: x[1]):
        entry = f"{mode} {filename}".encode() + b"\0" + bytes.fromhex(sha1)
        tree_content += entry
    header = f"tree {len(tree_content)}\0".encode()
    full_data = header + tree_content
    sha1 = hashlib.sha1(full_data).hexdigest()
    write_object(sha1, full_data)
    print(f"[INFO] SHA-1 du tree : {sha1}")
    print(sha1)
    return sha1


def create_commit(tree_sha, message, parent_sha=None):
    lines = [f'tree {tree_sha}']
    if parent_sha:
        lines.append(f'parent {parent_sha}')

    timestamp = int(time.time())
    timezone = '+0000'
    author = f'Test User <test@example.com> {timestamp} {timezone}'
    lines.append(f'author {author}')
    lines.append(f'committer {author}')
    lines.append('')
    lines.append(message)

    content = '\n'.join(lines).encode()
    header = f'commit {len(content)}\0'.encode()
    store = header + content

    sha1 = hashlib.sha1(store).hexdigest()

    write_object_local(sha1, store)

    print(f"[INFO] SHA-1 du commit : {sha1}")
    print(sha1)
    return sha1

def simple_commit(message):
    tree_sha = write_tree()
    head_path = os.path.join(get_git_dir(), 'HEAD')
    ref_path = os.path.join(get_git_dir(), 'refs', 'heads', 'master')
    parent_sha = None

    if os.path.exists(ref_path):
        with open(ref_path, "r") as f:
            parent_sha = f.read().strip()

    commit_sha = create_commit(tree_sha, message, parent_sha)

    with open(ref_path, "w") as f:
        f.write(commit_sha)

    print(f"[OK] Nouveau commit : {commit_sha}")

def status():
    index_entries = {filename for _, filename, _ in read_index()}
    working_files = {f for f in os.listdir() if os.path.isfile(f) and not f.startswith('.') and f != __file__}

    print("[INFO] Fichiers ajoutés (staged) :")
    for f in sorted(index_entries):
        print(f"  ➕ {f}")

    unstaged = working_files - index_entries
    if unstaged:
        print("[INFO] Fichiers non suivis :")
        for f in sorted(unstaged):
            print(f"  ❓ {f}")

def log():
    ref_path = os.path.join(get_git_dir(), 'refs', 'heads', 'master')
    if not os.path.exists(ref_path):
        print("[WARN] Aucun commit trouvé.")
        return

    current = open(ref_path).read().strip()
    objects_path = os.path.join(get_git_dir(), 'objects')

    while current:
        obj_path = os.path.join(objects_path, current[:2], current[2:])
        with open(obj_path, 'rb') as f:
            raw = zlib.decompress(f.read())
        _, body = raw.split(b'\x00', 1)
        lines = body.decode().split('\n')
        print(f"commit {current}")
        for line in lines:
            if line.startswith('author'):
                print(line)
            elif not line.startswith(('tree', 'parent', 'committer')) and line.strip():
                print(f"    {line}")
        parent = next((l.split()[1] for l in lines if l.startswith('parent')), None)
        print()
        current = parent

def show_ref():
    refs_dir = os.path.join(get_git_dir(), 'refs', 'heads')
    for name in os.listdir(refs_dir):
        ref_path = os.path.join(refs_dir, name)
        with open(ref_path) as f:
            sha = f.read().strip()
        print(f"{sha} refs/heads/{name}")


def main():
    parser = argparse.ArgumentParser(description="Mini Git from Scratch – Python")
    subparsers = parser.add_subparsers(dest='command')


   
    # Commande init
    subparsers.add_parser('init', help='Initialiser un dépôt Git minimal')

    # Commande add
    add_parser = subparsers.add_parser('add', help='Ajouter un fichier au staging area')
    add_parser.add_argument('file', help='Chemin du fichier à ajouter')

    # Commande rm
    rm_parser = subparsers.add_parser('rm', help='Supprimer un fichier du working directory et de l\'index')
    rm_parser.add_argument('file', help='Chemin du fichier à supprimer')
    #reset
    reset_parser = subparsers.add_parser('reset', help='Réinitialiser HEAD (et potentiellement index et working dir)')
    reset_parser.add_argument('sha', help='SHA-1 du commit cible')
    reset_parser.add_argument('--soft', action='store_true', help='Déplace HEAD seulement')
    reset_parser.add_argument('--mixed', action='store_true', help='HEAD + index (défaut)')
    reset_parser.add_argument('--hard', action='store_true', help='HEAD + index + fichiers')



    # Commande commit-tree (bas niveau)
    commit_tree_parser = subparsers.add_parser('commit-tree', help='Créer un commit qui pointe vers un tree')
    commit_tree_parser.add_argument('tree_sha', help='SHA-1 de l\'arbre (tree)')
    commit_tree_parser.add_argument('-m', '--message', required=True, help='Message du commit')
    commit_tree_parser.add_argument('-p', '--parent', help='SHA-1 du commit parent (facultatif)')

    # Commande commit (haut niveau)
    commit_parser = subparsers.add_parser('commit', help='Créer un commit depuis l\'index')
    commit_parser.add_argument('-m', '--message', required=True, help='Message du commit')

    args = parser.parse_args()

    if args.command == 'init':
        init_repo()
    elif args.command == 'commit-tree':
        if not os.path.isdir(get_git_dir()):
            print("[ERR] Ce répertoire n'est pas un dépôt. Lance `init` d'abord.")
            sys.exit(1)
        create_commit(args.tree_sha, args.message, args.parent)
    elif args.command == 'write-tree':
        write_tree()
    elif args.command == 'commit':
        simple_commit(args.message)
    elif args.command == 'status':
        status()
    elif args.command == 'log':
        log()
    elif args.command == 'show-ref':
        show_ref()
    elif args.command == 'rm':
        git_dir = get_git_dir()
        if not os.path.isdir(git_dir):
            print("[ERR] Ce répertoire n'est pas un dépôt git. Lance d'abord `init`.")
            sys.exit(1)
        rm.remove_file(args.file)
    elif args.command == 'reset':
        if args.soft:
            mode = 'soft'
        elif args.hard:
            mode = 'hard'
        else:
            mode = 'mixed'
        reset.reset(args.sha, mode)

    elif args.command == 'rev-parse':
        rev_parse.rev_parse(args.ref)


    elif args.command == 'add':
        add.add_file(args.file)

    elif args.command == 'commit-tree':
        git_dir = get_git_dir()
        if not os.path.isdir(git_dir):
            print("[ERR] Ce répertoire n'est pas un dépôt git. Lance d'abord `init`.")
            sys.exit(1)
        create_commit(args.tree_sha, args.message, args.parent)
        
   elif args.command == 'cat-file':
        git_dir = get_git_dir()
        if not os.path.isdir(git_dir):
            print("[ERR] Ce répertoire n'est pas un dépôt git. Lance d'abord `init`.")
            sys.exit(1)
        cat_file([args.option, args.oid])



    else:
        parser.print_help()


if __name__ == '__main__':
    main()
