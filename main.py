import os
import sys
import time
import hashlib
import zlib
import argparse

from gitfs.commands import add
from gitfs.commands import commit as commit_command
from gitfs.core import get_git_dir, write_object


GIT_DIR_NAME = '.mygit'


def get_git_dir_local():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), GIT_DIR_NAME))


def init_repo():
    git_dir = get_git_dir_local()
    if os.path.exists(git_dir):
        print("[ATT] Le dépôt .mygit existe déjà.")
        return

    os.makedirs(os.path.join(git_dir, 'objects'))
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'))

    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write('ref: refs/heads/master\n')

    print(f"[OK] Dépôt initialisé dans {git_dir}")


def write_object_local(sha1, data):
    git_dir = get_git_dir_local()
    obj_path = os.path.join(git_dir, 'objects', sha1[:2], sha1[2:])
    os.makedirs(os.path.dirname(obj_path), exist_ok=True)

    with open(obj_path, 'wb') as f:
        f.write(zlib.compress(data))

    print(f"[OK] Objet écrit dans : {GIT_DIR_NAME}/objects/{sha1[:2]}/{sha1[2:]}")


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


def main():
    parser = argparse.ArgumentParser(description="Mini Git from Scratch – Python")
    subparsers = parser.add_subparsers(dest='command')

    # Commande init
    subparsers.add_parser('init', help='Initialiser un dépôt Git minimal')

    # Commande add
    add_parser = subparsers.add_parser('add', help='Ajouter un fichier au staging area')
    add_parser.add_argument('file', help='Chemin du fichier à ajouter')

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

    elif args.command == 'add':
        add.add_file(args.file)

    elif args.command == 'commit-tree':
        git_dir = get_git_dir_local()
        if not os.path.isdir(git_dir):
            print("[ERR] Ce répertoire n'est pas un dépôt git. Lance d'abord `init`.")
            sys.exit(1)
        create_commit(args.tree_sha, args.message, args.parent)

    elif args.command == 'commit':
        git_dir = get_git_dir()
        if not os.path.isdir(git_dir):
            print("[ERR] Ce répertoire n'est pas un dépôt git. Lance d'abord `init`.")
            sys.exit(1)
        commit_command.create_commit(args.message)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
