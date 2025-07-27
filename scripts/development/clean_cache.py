#!/usr/bin/env python3
"""
Nettoyage des caches Python pour AirPlaneDesign
Supprime tous les fichiers .pyc et répertoires __pycache__
"""

import os
import shutil
import sys
from pathlib import Path


def clean_python_cache(directory=None):
    """
    Nettoie tous les caches Python dans un répertoire

    Args:
        directory: Répertoire à nettoyer (par défaut: répertoire du workbench)
    """

    if directory is None:
        # Répertoire racine du workbench
        directory = Path(__file__).parent.parent.parent
    else:
        directory = Path(directory)

    print(f"🧹 Nettoyage des caches Python dans: {directory}")
    print("=" * 60)

    cleaned_files = 0
    cleaned_dirs = 0

    # 1. Supprimer tous les fichiers .pyc
    print("\n📁 Suppression des fichiers .pyc...")
    for pyc_file in directory.rglob("*.pyc"):
        try:
            pyc_file.unlink()
            print(f"   ✅ Supprimé: {pyc_file.relative_to(directory)}")
            cleaned_files += 1
        except Exception as e:
            print(f"   ❌ Erreur: {pyc_file.relative_to(directory)} - {e}")

    # 2. Supprimer tous les répertoires __pycache__
    print("\n📂 Suppression des répertoires __pycache__...")
    for pycache_dir in directory.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            print(f"   ✅ Supprimé: {pycache_dir.relative_to(directory)}")
            cleaned_dirs += 1
        except Exception as e:
            print(f"   ❌ Erreur: {pycache_dir.relative_to(directory)} - {e}")

    # 3. Supprimer les fichiers .pyo (Python optimisé)
    print("\n📄 Suppression des fichiers .pyo...")
    pyo_count = 0
    for pyo_file in directory.rglob("*.pyo"):
        try:
            pyo_file.unlink()
            print(f"   ✅ Supprimé: {pyo_file.relative_to(directory)}")
            pyo_count += 1
        except Exception as e:
            print(f"   ❌ Erreur: {pyo_file.relative_to(directory)} - {e}")

    print("\n" + "=" * 60)
    print(f"🎯 Résultats du nettoyage:")
    print(f"   📁 Fichiers .pyc supprimés: {cleaned_files}")
    print(f"   📂 Répertoires __pycache__ supprimés: {cleaned_dirs}")
    print(f"   📄 Fichiers .pyo supprimés: {pyo_count}")

    if cleaned_files + cleaned_dirs + pyo_count == 0:
        print("   ✨ Aucun cache trouvé - déjà propre!")
    else:
        print("   ✨ Nettoyage terminé avec succès!")


def clean_specific_module(module_name):
    """
    Nettoie le cache d'un module spécifique et le recharge

    Args:
        module_name: Nom du module à nettoyer
    """
    print(f"🔄 Nettoyage du cache pour le module: {module_name}")

    # Supprimer le module du cache sys.modules s'il existe
    modules_to_remove = []
    for name in sys.modules:
        if name == module_name or name.startswith(module_name + "."):
            modules_to_remove.append(name)

    for name in modules_to_remove:
        print(f"   🗑️ Suppression de sys.modules: {name}")
        del sys.modules[name]

    print(f"   ✅ Module {module_name} nettoyé du cache")


def clean_freecad_workbench():
    """Nettoie spécifiquement le cache du workbench AirPlaneDesign"""
    print("🎯 Nettoyage spécifique du workbench AirPlaneDesign")

    # Modules à nettoyer
    modules_to_clean = [
        "InitGui",
        "airPlanePanel",
        "airPlaneRib",
        "airPlanePlane",
        "airPlaneWPanel",
        "airPlaneWing",
        "airPlaneWingWizard",
        "airPlaneNacelle",
        "reload_workbench",
        "freecad_imports",
    ]

    for module in modules_to_clean:
        try:
            clean_specific_module(module)
        except Exception as e:
            print(f"   ⚠️ Erreur pour {module}: {e}")


def main():
    """Fonction principale avec options"""

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "all":
            clean_python_cache()
        elif command == "workbench":
            clean_freecad_workbench()
        elif command == "module" and len(sys.argv) > 2:
            module_name = sys.argv[2]
            clean_specific_module(module_name)
        elif command == "help":
            print("🧹 Nettoyeur de cache Python - AirPlaneDesign")
            print("\nUsage:")
            print("  python clean_cache.py all              # Nettoie tous les caches")
            print(
                "  python clean_cache.py workbench        # Nettoie le cache workbench"
            )
            print(
                "  python clean_cache.py module <nom>     # Nettoie un module spécifique"
            )
            print("  python clean_cache.py help             # Affiche cette aide")
        else:
            print("❌ Commande inconnue. Utilisez 'help' pour voir les options.")
    else:
        # Par défaut, nettoie tous les caches
        clean_python_cache()


if __name__ == "__main__":
    main()
