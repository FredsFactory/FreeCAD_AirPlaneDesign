#!/usr/bin/env python3
"""
Script utilitaire pour lancer facilement les tâches du projet AirPlaneDesign
Usage: python3 task_runner.py [nom_de_la_tache]
"""

import os
import sys
import subprocess
from pathlib import Path


# Configuration des tâches disponibles
TASKS = {
    "clean": {
        "script": "scripts/development/clean_cache.py",
        "args": ["all"],
        "description": "🧹 Nettoie tous les caches Python",
    },
    "clean-workbench": {
        "script": "scripts/development/clean_cache.py",
        "args": ["workbench"],
        "description": "🧹 Nettoie uniquement le cache du workbench",
    },
    "test": {
        "script": "scripts/testing/run_tests.py",
        "args": [],
        "description": "🧪 Lance tous les tests",
    },
    "test-imports": {
        "script": "scripts/testing/imports/test_final_imports.py",
        "args": [],
        "description": "🔍 Teste les imports",
    },
    "test-icons": {
        "script": "scripts/testing/icons/test_icon_paths.py",
        "args": [],
        "description": "🎯 Teste les chemins d'icônes",
    },
    "test-xfoil": {
        "script": "scripts/testing/xfoil/test_xfoil.py",
        "args": [],
        "description": "🔧 Teste l'intégration XFoil",
    },
    "structure": {
        "script": "scripts/show_structure.py",
        "args": [],
        "description": "📋 Affiche la structure du projet",
    },
    "demo-reload": {
        "script": "scripts/development/demo_reload.py",
        "args": [],
        "description": "🔄 Démo du système de rechargement",
    },
    "test-autocompletion": {
        "script": "scripts/testing/test_autocompletion.py",
        "args": [],
        "description": "📝 Teste l'autocomplétion",
    },
    "test-formatter": {
        "script": "scripts/testing/formatters/test_formatter.py",
        "args": [],
        "description": "🎨 Teste le formateur",
    },
    "debug-icons": {
        "script": "scripts/testing/icons/debug_icon_paths.py",
        "args": [],
        "description": "🔍 Debug des chemins d'icônes",
    },
    "create-icons": {
        "script": "scripts/development/create_reload_icons.py",
        "args": [],
        "description": "🎯 Crée les icônes de rechargement",
    },
    "demo-imports": {
        "script": "scripts/development/demo_imports_resolus.py",
        "args": [],
        "description": "🔧 Démo des imports résolus",
    },
    "test-reload-commands": {
        "script": "scripts/testing/test_reload_commands.py",
        "args": [],
        "description": "🔧 Teste les commandes de rechargement",
    },
}


def show_help():
    """Affiche l'aide avec toutes les tâches disponibles"""
    print("🚀 Lanceur de tâches AirPlaneDesign")
    print("=" * 50)
    print("\nUsage: python3 task_runner.py [tache]")
    print("\nTâches disponibles:")
    print("-" * 30)

    for task_name, task_info in TASKS.items():
        print(f"  {task_name:<20} {task_info['description']}")

    print(f"\n  {'help':<20} 📖 Affiche cette aide")
    print(f"  {'list':<20} 📝 Liste toutes les tâches")

    print("\nExemples:")
    print("  python3 task_runner.py clean")
    print("  python3 task_runner.py test")
    print("  python3 task_runner.py help")


def list_tasks():
    """Liste toutes les tâches disponibles"""
    print("📝 Tâches disponibles:")
    for task_name in TASKS.keys():
        print(f"  - {task_name}")


def run_task(task_name):
    """Lance une tâche spécifique"""
    if task_name not in TASKS:
        print(f"❌ Tâche '{task_name}' inconnue.")
        print("📖 Utilisez 'help' pour voir les tâches disponibles.")
        return False

    task = TASKS[task_name]
    script_path = task["script"]
    args = task["args"]

    print(f"🚀 Lancement de la tâche: {task['description']}")
    print(f"📝 Script: {script_path}")
    if args:
        print(f"🔧 Arguments: {' '.join(args)}")
    print("-" * 50)

    # Construire la commande
    cmd = ["python3", script_path] + args

    try:
        # Lancer la commande
        result = subprocess.run(cmd, cwd=Path(__file__).parent, check=False)

        if result.returncode == 0:
            print(f"\n✅ Tâche '{task_name}' terminée avec succès!")
        else:
            print(
                f"\n❌ Tâche '{task_name}' terminée avec des erreurs (code: {result.returncode})"
            )

        return result.returncode == 0

    except FileNotFoundError:
        print(f"❌ Script non trouvé: {script_path}")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠️ Tâche '{task_name}' interrompue par l'utilisateur")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False


def main():
    """Fonction principale"""
    if len(sys.argv) < 2:
        show_help()
        return

    task_name = sys.argv[1].lower()

    if task_name in ["help", "--help", "-h"]:
        show_help()
    elif task_name in ["list", "--list", "-l"]:
        list_tasks()
    else:
        success = run_task(task_name)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
