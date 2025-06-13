import os
import sys
import time
import hashlib
import zlib
import argparse


def get_git_dir():

    ##Retourne le chemin absolu vers le dossier .git à la racine du projet.
    git_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.git'))
    return git_dir


def init_repo():

    ##Initialise un dépôt git minimaliste : .git/ avec les sous-dossiers requis

    git_dir = get_git_dir()
    if os.path.exists(git_dir):
        print("[ATT] Le dépôt .git existe déjà.")
        return

    os.makedirs(os.path.join(git_dir, 'objects'))
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'))

    # HEAD par défaut pointant vers master
    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write('ref: refs/heads/master\n')

    print(f"[OK] Dépôt initialisé dans {git_dir}")


def write_object(sha1, data):
    ## Objet compressé dans le dossier .git/objects/xx/yyyyy...

    git_dir = get_git_dir()
    obj_path = os.path.join(git_dir, 'objects', sha1[:2], sha1[2:])
    os.makedirs(os.path.dirname(obj_path), exist_ok=True)

    with open(obj_path, 'wb') as f:
        f.write(zlib.compress(data))

    print(f"[OK] Objet écrit dans : .git/objects/{sha1[:2]}/{sha1[2:]}")


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
    write_object(sha1, store)

    print(f"[INFO] SHA-1 du commit : {sha1}")
    print(sha1)
    return sha1


def main():
    parser = argparse.ArgumentParser(description="Mini Git from Scratch – Python")
    subparsers = parser.add_subparsers(dest='command')

    ## Commande: init
    init_parser = subparsers.add_parser('init', help='Initialiser un dépôt Git minimal')

    ## Commande: commit-tree
    commit_parser = subparsers.add_parser('commit-tree', help='Créer un commit qui pointe vers un tree')
    commit_parser.add_argument('tree_sha', help='SHA-1 de l\'arbre (tree)')
    commit_parser.add_argument('-m', '--message', required=True, help='Message du commit')
    commit_parser.add_argument('-p', '--parent', help='SHA-1 du commit parent (facultatif)')

    args = parser.parse_args()

    if args.command == 'init':
        init_repo()

    elif args.command == 'commit-tree':
        git_dir = get_git_dir()
        if not os.path.isdir(git_dir):
            print("[ERR] Erreur : ce répertoire n'est pas un dépôt git. Lance d'abord `init`.")
            sys.exit(1)
        create_commit(args.tree_sha, args.message, args.parent)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
