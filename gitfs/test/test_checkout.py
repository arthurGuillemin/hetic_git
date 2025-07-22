import os
import subprocess
import shutil

def run_cmd(cmd):
    print(f">> [CMD] {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def assert_file_content(filename, expected_content):
    with open(filename, "r") as f:
        content = f.read()
    assert content == expected_content, f"[ERR] Contenu inattendu dans {filename}.\nAttendu : {expected_content}\nTrouvé : {content}"

def cleanup():
    # Supprime les fichiers et dossiers sauf le script de test
    for f in os.listdir("."):
        if f == "test_checkout.py":
            continue
        if os.path.isfile(f):
            os.remove(f)
        elif os.path.isdir(f):
            shutil.rmtree(f)

def test_checkout_branch_switch():
    print("=== TEST : switch entre deux branches et restauration des fichiers ===")
    cleanup()

    # Étape 1 : Initialiser le dépôt
    run_cmd("python ../main.py init")

    # Étape 2 : Créer un fichier sur master
    write_file("fichier.txt", "contenu master")
    run_cmd("python ../main.py add fichier.txt")
    run_cmd('python ../main.py commit -m "commit master"')

    # Étape 3 : Créer une nouvelle branche et modifier le fichier
    run_cmd("python ../main.py checkout branche2")
    write_file("fichier.txt", "contenu branche2")
    run_cmd("python ../main.py add fichier.txt")
    run_cmd('python ../main.py commit -m "commit branche2"')

    # Étape 4 : Revenir sur master et vérifier le contenu restauré
    run_cmd("python ../main.py checkout master")
    assert_file_content("fichier.txt", "contenu master")

    print("[OK] Le switch de branche restaure correctement les fichiers.\n")

if __name__ == "__main__":
    test_checkout_branch_switch()
