#!/usr/bin/env python3
"""
Test des imports après la réorganisation des modules
"""
import sys
import os


def test_imports():
    print("🧪 Test des imports après réorganisation...")

    try:
        # Test de l'import principal qui posait problème
        from App.modules.airPlaneWing.airPlaneWPanel import WingPanel

        print("✅ airPlaneWPanel importé avec succès")

        # Test des autres imports
        from App.modules.airPlaneWing.airPlaneWingUI import WingEditorPanel

        print("✅ airPlaneWingUI importé avec succès")

        from App.modules.airPlaneWing.airPlaneWing import Wing

        print("✅ airPlaneWing importé avec succès")

        print("🎉 Tous les imports fonctionnent correctement!")
        return True

    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False


if __name__ == "__main__":
    test_imports()
