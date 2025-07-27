#!/usr/bin/env python3
"""
Test des imports après les dernières corrections
"""
import sys
import os


def test_imports_final():
    print("🧪 Test final des imports après corrections...")

    # Test depuis le répertoire racine
    base_path = (
        "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign"
    )
    os.chdir(base_path)

    modules_to_test = [
        ("App.modules.airPlaneWing.airPlanePanel", "airPlanePanel"),
        ("App.modules.airPlaneRib.airPlaneRib", "airPlaneRib"),
        ("App.modules.airPlanePlane.airPlanePlane", "airPlanePlane"),
        ("App.modules.airPlaneWing.airPlaneWPanel", "airPlaneWPanel"),
        ("App.modules.airPlaneWing.airPlaneWing", "airPlaneWing"),
        ("App.modules.airPlaneWing.airPlaneWingWizard", "airPlaneWingWizard"),
        ("App.modules.airPlaneNacelle.airPlaneNacelle", "airPlaneNacelle"),
    ]

    all_success = True
    for module_path, module_name in modules_to_test:
        try:
            __import__(module_path)
            print(f"✅ {module_name}: Import réussi")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            all_success = False
        except Exception as e:
            print(f"⚠️ {module_name}: Autre erreur - {e}")

    if all_success:
        print("🎉 Tous les imports fonctionnent!")
    else:
        print("⚠️ Certains imports ont encore des problèmes.")

    return all_success


if __name__ == "__main__":
    test_imports_final()
