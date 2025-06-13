import os
import subprocess
import re

def test_commit_tree_creation():
    # Si le dépôt n'existe pas encore, on l'initialise
    if not os.path.exists(".git"):
        subprocess.run(["python", "main.py", "init"], check=True)

    # On simule un commit à partir d'un arbre fictif
    result = subprocess.run(
        ["python", "main.py", "commit-tree", "d3adb33f", "-m", "Message de test"],
        capture_output=True,
        text=True,
        check=True
    )

    # Récupérer le SHA dans la sortie
    match = re.search(r"[a-f0-9]{40}", result.stdout)
    assert match, "Aucun SHA trouvé dans la sortie"
    sha = match.group(0)

    # Vérifie que l'objet Git a bien été écrit
    path = os.path.join(".git", "objects", sha[:2], sha[2:])
    assert os.path.exists(path), f"Objet Git {sha} manquant dans .git/objects/"
