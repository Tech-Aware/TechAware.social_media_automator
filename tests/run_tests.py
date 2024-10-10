# tests/run_tests.py

"""
Ce module fournit un script pour exécuter tous les tests unitaires du projet Automator
en utilisant pytest.

Il découvre automatiquement tous les fichiers de test dans le répertoire 'tests'
et ses sous-répertoires, puis exécute chaque fichier de test individuellement
en utilisant pytest. Le script affiche les résultats détaillés de chaque test
et retourne un code de sortie global.

Usage:
    python tests/run_tests.py

Note:
    Ce script doit être exécuté depuis la racine du projet pour assurer
    la découverte correcte des fichiers de test.
    Assurez-vous que pytest est installé : pip install pytest
"""

import os
import sys
import subprocess


def find_test_files(directory):
    """
  Trouve tous les fichiers de test dans le répertoire donné et ses sous-répertoires.

  Args:
      directory (str): Le répertoire de départ pour la recherche.

  Returns:
      list: Une liste des chemins des fichiers de test trouvés.
  """
    test_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(root, file))
    return test_files


def run_test(test_file):
    """
  Exécute un fichier de test spécifique en utilisant pytest.

  Args:
      test_file (str): Le chemin du fichier de test à exécuter.

  Returns:
      int: Le code de retour du processus d'exécution du test.
  """
    print(f"\nExécution du test : {test_file}")

    result = subprocess.run([sys.executable, "-m", "pytest", "-v", test_file], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Erreurs :", result.stderr)
    return result.returncode


def run_all_tests():
    """
  Découvre et exécute tous les tests unitaires du projet.

  Cette fonction trouve tous les fichiers de test dans le répertoire 'tests',
  les exécute un par un avec pytest, et retourne un code de sortie global
  basé sur le succès ou l'échec de l'ensemble des tests.

  Returns:
      int: 0 si tous les tests ont réussi, 1 si au moins un test a échoué ou n'a pas été exécuté.
  """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = find_test_files(current_dir)

    if not test_files:
        print("Aucun fichier de test trouvé.")
        return 1

    failed_tests = []
    for test_file in test_files:
        if run_test(test_file) != 0:
            failed_tests.append(test_file)

    if failed_tests:
        print(f"\n{len(failed_tests)} test(s) ont échoué ou n'ont pas été exécutés:")
        for test in failed_tests:
            print(f"  - {test}")
        return 1
    else:
        print(f"\nTous les tests ({len(test_files)}) ont réussi!")
        return 0


if __name__ == '__main__':
    sys.exit(run_all_tests())