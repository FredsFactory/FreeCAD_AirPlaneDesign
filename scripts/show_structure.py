#!/usr/bin/env python3
"""
Affichage de la structure du répertoire scripts
"""

import os


def show_scripts_structure():
    """Affiche la structure du répertoire scripts avec descriptions"""
    print("📁 Structure du répertoire scripts/")
    print("=" * 50)

    base_path = os.path.dirname(__file__)

    # Development
    print("\n🔧 Development (scripts/development/)")
    dev_scripts = [
        ("reload_workbench.py", "Rechargement à chaud du workbench"),
        ("reload_commands.py", "Commandes UI pour rechargement"),
        ("keyboard_shortcuts.py", "Raccourcis clavier (F5, etc.)"),
        ("create_reload_icons.py", "Création icônes rechargement"),
        ("demo_imports_resolus.py", "Démo imports résolus"),
        ("demo_reload.py", "Démo système de reload"),
        ("setup_autocompletion.sh", "Configuration autocomplétion"),
        ("setup_freecad_paths.py", "Configuration chemins FreeCAD"),
        ("migrate_imports.sh", "Migration automatique imports"),
    ]

    for script, desc in dev_scripts:
        script_path = os.path.join(base_path, "development", script)
        status = "✅" if os.path.exists(script_path) else "❌"
        print(f"  {status} {script:<25} - {desc}")

    # Testing
    print("\n🔍 Testing (scripts/testing/)")
    test_scripts = [
        ("debug_icon_paths.py", "Vérification chemins d'icônes"),
        ("test_autocompletion.py", "Tests autocomplétion FreeCAD"),
    ]

    for script, desc in test_scripts:
        script_path = os.path.join(base_path, "testing", script)
        status = "✅" if os.path.exists(script_path) else "❌"
        print(f"  {status} {script:<25} - {desc}")

    # Utils
    print("\n⚡ Utilitaires (scripts/)")
    utils_scripts = [
        ("utils.py", "Interface unifiée pour tous les scripts"),
        ("README.md", "Documentation principale"),
    ]

    for script, desc in utils_scripts:
        script_path = os.path.join(base_path, script)
        status = "✅" if os.path.exists(script_path) else "❌"
        print(f"  {status} {script:<25} - {desc}")

    # Documentation
    print("\n📚 Documentation (scripts/docs/)")
    doc_files = [
        ("AUTOCOMPLETION_GUIDE.md", "Guide autocomplétion FreeCAD"),
        ("DEBUG_GUIDE.md", "Guide debug et dépannage"),
        ("MIGRATION_IMPORTS.md", "Guide migration imports"),
    ]

    for doc, desc in doc_files:
        doc_path = os.path.join(base_path, "docs", doc)
        status = "✅" if os.path.exists(doc_path) else "❌"
        print(f"  {status} {doc:<25} - {desc}")

    print("\n" + "=" * 50)
    print("💡 Utilisation rapide:")
    print("  import scripts.utils as utils")
    print("  utils.rl()         # Recharger workbench")
    print("  utils.debug_icons() # Debug icônes")
    print("  utils.help_scripts() # Aide complète")


if __name__ == "__main__":
    show_scripts_structure()
