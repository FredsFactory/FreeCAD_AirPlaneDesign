#!/usr/bin/env python3
"""
Utilitaires pour AirPlaneDesign - Accès rapide aux scripts de développement
"""

import sys
import os

# Ajouter le répertoire des scripts au path pour faciliter les imports
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)


def reload_workbench():
    """Raccourci pour recharger le workbench"""
    try:
        from development.reload_workbench import reload

        reload()
    except ImportError as e:
        print(f"❌ Impossible d'importer reload_workbench : {e}")


def rl():
    """Alias court pour reload_workbench()"""
    reload_workbench()


def clean_cache(mode="all"):
    """Nettoyer les caches Python"""
    try:
        from development.clean_cache import (
            clean_python_cache,
            clean_freecad_workbench,
            clean_specific_module,
        )

        if mode == "all":
            clean_python_cache()
        elif mode == "workbench":
            clean_freecad_workbench()
        elif mode.startswith("module:"):
            module_name = mode.split(":", 1)[1]
            clean_specific_module(module_name)
        else:
            print(f"❌ Mode inconnu: {mode}")
            print("Utilisez: 'all', 'workbench' ou 'module:nom_module'")
    except ImportError as e:
        print(f"❌ Impossible d'importer clean_cache : {e}")


def cc():
    """Alias court pour clean_cache()"""
    clean_cache()


def debug_icons():
    """Lancer le debug des icônes"""
    try:
        from testing.icons.debug_icon_paths import debug_module_icon_paths

        debug_module_icon_paths()
    except ImportError as e:
        print(f"❌ Impossible d'importer debug_icon_paths : {e}")


def run_tests(category="all"):
    """Lancer les tests par catégorie"""
    try:
        from testing.run_tests import TestRunner

        runner = TestRunner()

        if category == "all":
            runner.run_all_tests()
        elif category == "list":
            runner.list_tests()
        elif category in ["imports", "icons", "formatters", "xfoil"]:
            runner.run_category_tests(category)
        else:
            print(f"❌ Catégorie inconnue: {category}")
            print(
                "Utilisez: 'all', 'list', 'imports', 'icons', 'formatters' ou 'xfoil'"
            )
    except ImportError as e:
        print(f"❌ Impossible d'importer run_tests : {e}")


def test_imports():
    """Raccourci pour tester les imports"""
    run_tests("imports")


def test_icons():
    """Raccourci pour tester les icônes"""
    run_tests("icons")


def help_scripts():
    """Afficher l'aide pour les scripts disponibles"""
    print("🔧 Scripts disponibles dans AirPlaneDesign:")
    print("")
    print("📦 Développement:")
    print("  reload_workbench() ou rl() - Recharger le workbench")
    print("  clean_cache(mode) ou cc() - Nettoyer les caches Python")
    print("")
    print("🔍 Tests et Debug:")
    print("  debug_icons() - Vérifier les chemins d'icônes")
    print("  run_tests(category) - Lancer les tests ('all', 'imports', 'icons', etc.)")
    print("  test_imports() - Tester uniquement les imports")
    print("  test_icons() - Tester uniquement les icônes")
    print("")
    print("🧹 Nettoyage des caches:")
    print("  clean_cache('all') - Nettoyer tous les caches Python")
    print("  clean_cache('workbench') - Nettoyer le cache du workbench")
    print("  clean_cache('module:nom') - Nettoyer un module spécifique")
    print("")
    print("💡 Utilisation depuis la console FreeCAD:")
    print("  import scripts.utils as utils")
    print("  utils.rl()  # pour recharger")
    print("  utils.cc()  # pour nettoyer les caches")
    print("  utils.debug_icons()  # pour debug")
    print("  utils.run_tests('imports')  # pour tester les imports")
    print("  utils.run_tests('list')  # pour lister tous les tests")


# Afficher l'aide au chargement
if __name__ == "__main__":
    help_scripts()
