import os
import sys
import time
import hashlib
import zlib
import argparse
from gitfs.commands import add
from gitfs.commands import commit as commit_command
from gitfs.core import get_git_dir, write_object
from gitfs.utils.index import read_index
from gitfs.commands import checkout
from gitfs.commands import status
from gitfs.commands.ls_tree import ls_tree
from gitfs.commands import rm
from gitfs.commands import reset
from gitfs.commands import rev_parse
from gitfs.commands import ls_file
from gitfs.commands.write import write_tree
from gitfs.commands.cat_file import cat_file
from gitfs.commands import log
from gitfs.commands import show
from gitfs.commands import init
GIT_DIR_NAME = '.mygit' 




def write_object_local(sha1, data):
    git_dir = get_git_dir()
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

def simple_commit(message):
    tree_sha = write_tree()
    head_path = os.path.join(get_git_dir(), 'HEAD')
    ref_path = os.path.join(get_git_dir(), 'refs', 'heads', 'master')
    parent_sha = None

    if os.path.exists(ref_path):
        with open(ref_path, "r") as f:
            parent_sha = f.read().strip()

    commit_sha = create_commit(tree_sha, message, parent_sha)

    os.makedirs(os.path.dirname(ref_path), exist_ok=True)

    with open(ref_path, "w") as f:
        f.write(commit_sha)

    print(f"[OK] Nouveau commit : {commit_sha}")



def main():
    parser = argparse.ArgumentParser(description="Mini Git from Scratch – Python")
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('write-tree', help='Créer un objet tree à partir de l\'index')

   
    # Commande init
    subparsers.add_parser('init', help='Initialiser un dépôt Git minimal')

    # Commande add
    add_parser = subparsers.add_parser('add', help='Ajouter un fichier au staging area')
    add_parser.add_argument('file', help='Chemin du fichier à ajouter')

    # Commande Checkout
    checkout_parser = subparsers.add_parser('checkout', help='Changer ou créer une branche')
    checkout_parser.add_argument('branch', help='Nom de la branche')
    # Commande rm
    rm_parser = subparsers.add_parser('rm', help='Supprimer un fichier du working directory et de l\'index')
    rm_parser.add_argument('file', help='Chemin du fichier à supprimer')
    #reset
    reset_parser = subparsers.add_parser('reset', help='Réinitialiser HEAD (et potentiellement index et working dir)')
    reset_parser.add_argument('sha', help='SHA-1 du commit cible')
    reset_parser.add_argument('--soft', action='store_true', help='Déplace HEAD seulement')
    reset_parser.add_argument('--mixed', action='store_true', help='HEAD + index (défaut)')
    reset_parser.add_argument('--hard', action='store_true', help='HEAD + index + fichiers')

    subparsers.add_parser('status', help='Afficher le statut du dépôt')

    # Commande commit-tree (bas niveau)
    commit_tree_parser = subparsers.add_parser('commit-tree', help='Créer un commit qui pointe vers un tree')
    commit_tree_parser.add_argument('tree_sha', help='SHA-1 de l\'arbre (tree)')
    commit_tree_parser.add_argument('-m', '--message', required=True, help='Message du commit')
    commit_tree_parser.add_argument('-p', '--parent', help='SHA-1 du commit parent (facultatif)')

    # Commande commit (haut niveau)
    commit_parser = subparsers.add_parser('commit', help='Créer un commit depuis l\'index')
    commit_parser.add_argument('-m', '--message', required=True, help='Message du commit')
    # Commande: cat-file
    catfile_parser = subparsers.add_parser('cat-file', help='Afficher le type ou le contenu d\'un objet Git')
    group = catfile_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', action='store_true', help='Afficher le type de l’objet')
    group.add_argument('-p', action='store_true', help='Afficher le contenu de l’objet')
    catfile_parser.add_argument('oid', help='OID de l’objet Git')

    # Commande: ls-tree
    lstree_parser = subparsers.add_parser('ls-tree', help='Lister les entrées d’un objet tree')
    lstree_parser.add_argument('tree_sha', help='SHA-1 de l’objet tree à inspecter')

    # Commande ls-files
    subparsers.add_parser('ls_files', help='Lister les fichiers dans l\'index')

    # Commande log
    subparsers.add_parser('log', help='Afficher l\'historique des commits')
    
    # Commande show-ref
    subparsers.add_parser('show-ref', help='Afficher les références et leurs SHA-1')
    
    # Commande rev-parse
    revparse_parser = subparsers.add_parser('rev-parse', help='Résoudre une référence en SHA-1')
    revparse_parser.add_argument('ref', help='Référence à résoudre (HEAD, master, refs/heads/master, etc.)')


    args = parser.parse_args()

    if args.command == 'init':
        init.init_repo()
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
        status.status()
    elif args.command == 'log':
        log.log()
    elif args.command == 'show-ref':
        show.show_ref()
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

    elif args.command == 'checkout':
        checkout.checkout_branch(args.branch)

    elif args.command == 'commit-tree':
        git_dir = get_git_dir()
        if not os.path.isdir(git_dir):
            print("[ERR] Ce répertoire n'est pas un dépôt git. Lance d'abord `init`.")
            sys.exit(1)
        create_commit(args.tree_sha, args.message, args.parent)
        
    elif args.command == 'cat-file':
        if args.t:
            cat_file(['-t', args.oid])
        elif args.p:
            cat_file(['-p', args.oid])
    
    elif args.command == 'ls_files':
        git_dir = get_git_dir()
        if not os.path.isdir(git_dir):
            print("[ERR] Ce répertoire n'est pas un dépôt git. Lance d'abord `init`.")
            sys.exit(1)
        ls_file.ls_files()

    elif args.command == 'ls-tree':
        ls_tree([args.tree_sha])
    else:
        parser.print_help()


if __name__ == '__main__':
    main()