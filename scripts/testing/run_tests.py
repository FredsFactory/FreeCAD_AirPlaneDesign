#!/usr/bin/env python3
"""
Runner de tests principal pour AirPlaneDesign
Permet de lancer tous les tests ou par catégorie
"""

import os
import sys
import subprocess
from pathlib import Path


class TestRunner:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.python_cmd = sys.executable

    def run_test_file(self, test_file):
        """Exécute un fichier de test spécifique"""
        print(f"🧪 Exécution de {test_file.name}...")
        try:
            result = subprocess.run(
                [self.python_cmd, str(test_file)],
                cwd=str(test_file.parent),
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                print(f"✅ {test_file.name} - Succès")
                if result.stdout:
                    print(f"   📋 {result.stdout.strip()}")
            else:
                print(f"❌ {test_file.name} - Échec")
                if result.stderr:
                    print(f"   🚨 {result.stderr.strip()}")

        except subprocess.TimeoutExpired:
            print(f"⏱️ {test_file.name} - Timeout (30s)")
        except Exception as e:
            print(f"💥 {test_file.name} - Erreur: {e}")

    def run_category_tests(self, category):
        """Exécute tous les tests d'une catégorie"""
        category_path = self.base_path / category

        if not category_path.exists():
            print(f"❌ Catégorie {category} introuvable")
            return

        print(f"\n📂 === Tests {category.upper()} ===")

        test_files = list(category_path.glob("test_*.py"))

        if not test_files:
            print(f"   ℹ️ Aucun test trouvé dans {category}")
            return

        for test_file in sorted(test_files):
            self.run_test_file(test_file)

    def run_all_tests(self):
        """Exécute tous les tests de toutes les catégories"""
        print("🚀 Lancement de tous les tests AirPlaneDesign")
        print("=" * 50)

        categories = ["imports", "icons", "formatters", "xfoil"]

        for category in categories:
            self.run_category_tests(category)

        # Tests à la racine de testing/
        print(f"\n📂 === Tests GÉNÉRAUX ===")
        general_tests = list(self.base_path.glob("test_*.py"))
        for test_file in sorted(general_tests):
            self.run_test_file(test_file)

        print("\n" + "=" * 50)
        print("🏁 Tests terminés")

    def list_tests(self):
        """Liste tous les tests disponibles"""
        print("📋 Tests disponibles dans AirPlaneDesign:")
        print("=" * 40)

        categories = ["imports", "icons", "formatters", "xfoil"]

        for category in categories:
            category_path = self.base_path / category
            if category_path.exists():
                test_files = list(category_path.glob("test_*.py"))
                print(f"\n🔧 {category.upper()}:")
                if test_files:
                    for test_file in sorted(test_files):
                        print(f"   - {test_file.name}")
                else:
                    print(f"   (aucun test)")

        # Tests généraux
        general_tests = list(self.base_path.glob("test_*.py"))
        if general_tests:
            print(f"\n🔧 GÉNÉRAUX:")
            for test_file in sorted(general_tests):
                print(f"   - {test_file.name}")


def main():
    runner = TestRunner()

    if len(sys.argv) == 1:
        print("🧪 Test Runner AirPlaneDesign")
        print("\nUsage:")
        print("  python run_tests.py all              # Tous les tests")
        print("  python run_tests.py imports          # Tests d'imports")
        print("  python run_tests.py icons            # Tests d'icônes")
        print("  python run_tests.py formatters       # Tests formatters")
        print("  python run_tests.py xfoil            # Tests xfoil")
        print("  python run_tests.py list             # Lister les tests")
        return

    command = sys.argv[1].lower()

    if command == "all":
        runner.run_all_tests()
    elif command == "list":
        runner.list_tests()
    elif command in ["imports", "icons", "formatters", "xfoil"]:
        runner.run_category_tests(command)
    else:
        print(f"❌ Commande inconnue: {command}")
        print("Utilisez 'all', 'list', 'imports', 'icons', 'formatters' ou 'xfoil'")


if __name__ == "__main__":
    main()
