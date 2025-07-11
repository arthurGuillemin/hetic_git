import os
import subprocess
import re
import shutil

MYGIT_DIR = ".mygit"

def setup_module(module):
    """Supprime .mygit avant chaque test si présent (réinitialisation propre)"""
    if os.path.exists(MYGIT_DIR):
        shutil.rmtree(MYGIT_DIR)

def test_commit_tree_creation():
    # Initialisation du dépôt s'il n'existe pas
    if not os.path.exists(MYGIT_DIR):
        subprocess.run(["python", "main.py", "init"], check=True)

    # Création d'un commit avec un tree SHA fictif
    result = subprocess.run(
        ["python", "main.py", "commit-tree", "d3adb33f", "-m", "Message de test"],
        capture_output=True,
        text=True,
        check=True
    )

    # Extraction du SHA généré depuis la sortie
    match = re.search(r"[a-f0-9]{40}", result.stdout)
    assert match, "Aucun SHA trouvé dans la sortie"
    sha = match.group(0)

    # Vérifie que l’objet Git a bien été écrit
    obj_path = os.path.join(MYGIT_DIR, "objects", sha[:2], sha[2:])
    assert os.path.exists(obj_path), f"Objet Git {sha} manquant dans {MYGIT_DIR}/objects/"
