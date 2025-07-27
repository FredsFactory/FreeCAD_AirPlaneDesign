#!/usr/bin/env python3
"""
Script de test pour vérifier les imports Python dans le projet AirPlaneDesign
"""

import sys
import os


def test_import(module_name, description=""):
    """Teste l'import d'un module"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} {description}")
        return True
    except ImportError as e:
        print(f"❌ {module_name} {description} - Erreur: {e}")
        return False


def main():
    print("🐍 Test des Imports Python - AirPlaneDesign")
    print("=" * 50)

    # Informations système
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Répertoire de travail: {os.getcwd()}")
    print()

    # Test des modules standard
    print("📦 Modules Standard:")
    standard_modules = [
        ("os", "- Système d'exploitation"),
        ("sys", "- Système Python"),
        ("math", "- Mathématiques"),
        ("json", "- JSON"),
        ("re", "- Expressions régulières"),
        ("pathlib", "- Chemins de fichiers"),
    ]

    standard_ok = 0
    for module, desc in standard_modules:
        if test_import(module, desc):
            standard_ok += 1

    # Test des modules FreeCAD
    print(f"\n🏗️ Modules FreeCAD:")
    freecad_modules = [
        ("FreeCAD", "- Core FreeCAD"),
        ("FreeCADGui", "- Interface graphique"),
        ("Part", "- Géométrie"),
        ("Draft", "- Dessin 2D"),
        ("Mesh", "- Maillages"),
        ("Sketcher", "- Esquisse"),
    ]

    freecad_ok = 0
    for module, desc in freecad_modules:
        if test_import(module, desc):
            freecad_ok += 1

    # Test des modules tiers courants
    print(f"\n📊 Modules Tiers:")
    third_party_modules = [
        ("numpy", "- Calcul numérique"),
        ("matplotlib", "- Graphiques"),
        ("PySide", "- Interface graphique Qt"),
        ("QtCore", "- Qt Core (via PySide)"),
        ("QtGui", "- Qt GUI (via PySide)"),
    ]

    third_party_ok = 0
    for module, desc in third_party_modules:
        try:
            if module == "QtCore":
                from PySide import QtCore

                print(f"✅ {module} {desc}")
                third_party_ok += 1
            elif module == "QtGui":
                from PySide import QtGui

                print(f"✅ {module} {desc}")
                third_party_ok += 1
            else:
                if test_import(module, desc):
                    third_party_ok += 1
        except ImportError as e:
            print(f"❌ {module} {desc} - Erreur: {e}")

    # Test du système d'imports personnalisé
    print(f"\n🔧 Système Personnalisé:")
    custom_ok = 0

    if test_import("freecad_imports", "- Imports intelligents"):
        custom_ok += 1

        # Tester les imports via freecad_imports
        try:
            from freecad_imports import App, Vector, Console

            print("✅ freecad_imports.App - Module App via imports intelligents")
            print("✅ freecad_imports.Vector - Classe Vector via imports intelligents")
            print(
                "✅ freecad_imports.Console - Module Console via imports intelligents"
            )
            custom_ok += 3
        except ImportError as e:
            print(f"❌ Imports via freecad_imports - Erreur: {e}")

    # Test des modules du projet
    print(f"\n🛩️ Modules du Projet AirPlaneDesign:")
    project_modules = [
        ("airPlaneAirFoil", "- Génération de profils"),
        ("airPlaneAirFoilNaca", "- Profils NACA"),
        ("airPlaneRib", "- Nervures d'aile"),
        ("airPlaneWing", "- Ailes"),
        ("libAeroShapes", "- Formes aérodynamiques"),
    ]

    project_ok = 0
    for module, desc in project_modules:
        if test_import(module, desc):
            project_ok += 1

    # Affichage des chemins Python
    print(f"\n🎯 Chemins Python ({len(sys.path)} chemins):")
    for i, path in enumerate(sys.path[:10]):  # Afficher seulement les 10 premiers
        print(f"  {i+1}. {path}")
    if len(sys.path) > 10:
        print(f"  ... et {len(sys.path) - 10} autres chemins")

    # Résumé
    print(f"\n📊 Résumé des Tests:")
    print(f"  📦 Modules Standard: {standard_ok}/{len(standard_modules)}")
    print(f"  🏗️ Modules FreeCAD: {freecad_ok}/{len(freecad_modules)}")
    print(f"  📊 Modules Tiers: {third_party_ok}/{len(third_party_modules)}")
    print(f"  🔧 Système Personnalisé: {custom_ok}/4")
    print(f"  🛩️ Modules Projet: {project_ok}/{len(project_modules)}")

    total_ok = standard_ok + freecad_ok + third_party_ok + custom_ok + project_ok
    total_tests = (
        len(standard_modules)
        + len(freecad_modules)
        + len(third_party_modules)
        + 4
        + len(project_modules)
    )

    print(f"\n🎯 Total: {total_ok}/{total_tests} tests réussis")

    # Recommandations
    if freecad_ok == 0:
        print(f"\n⚠️ Recommandations:")
        print(f"   - Aucun module FreeCAD détecté")
        print(f"   - Vérifiez l'interpréteur Python dans VS Code")
        print(f"   - Utilisez: /Applications/FreeCAD.app/Contents/Resources/bin/python")
    elif freecad_ok < len(freecad_modules):
        print(f"\n💡 Conseils:")
        print(f"   - Certains modules FreeCAD manquent")
        print(f"   - Vérifiez l'installation FreeCAD")
        print(f"   - Le système freecad_imports devrait compenser")

    if total_ok == total_tests:
        print(f"\n🎉 Excellent ! Tous les imports fonctionnent parfaitement !")
    elif total_ok > total_tests * 0.8:
        print(f"\n👍 Bonne configuration ! Quelques modules optionnels manquent.")
    else:
        print(f"\n🔧 Configuration à améliorer. Consultez le guide de résolution.")

    return total_ok, total_tests


if __name__ == "__main__":
    success, total = main()
    exit(0 if success > total * 0.5 else 1)
