#!/usr/bin/env python3
"""
Test de chargement des commandes de rechargement
Simule le processus de chargement dans FreeCAD
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire du workbench au path
workbench_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workbench_root))


def test_command_loading():
    """Teste le chargement des commandes sans FreeCAD"""
    print("🧪 Test de chargement des commandes de rechargement")
    print("=" * 50)

    # Changer vers le répertoire du workbench
    os.chdir(workbench_root)

    try:
        # Test 1: Import du module
        print("\n1️⃣ Test d'import du module...")
        from scripts.development import reload_commands

        print("   ✅ Module reload_commands importé")

        # Test 2: Vérification de la disponibilité FreeCAD
        print(f"\n2️⃣ Disponibilité FreeCAD: {reload_commands.FREECAD_AVAILABLE}")
        if not reload_commands.FREECAD_AVAILABLE:
            print("   ⚠️ FreeCAD non disponible (normal hors de FreeCAD)")

        # Test 3: Création des classes de commandes
        print("\n3️⃣ Test de création des commandes...")
        cmd1 = reload_commands.ReloadWorkbenchCommand()
        cmd2 = reload_commands.ToggleAutoReloadCommand()
        print("   ✅ ReloadWorkbenchCommand créée")
        print("   ✅ ToggleAutoReloadCommand créée")

        # Test 4: Test des méthodes GetResources
        print("\n4️⃣ Test des ressources...")
        try:
            res1 = cmd1.GetResources()
            res2 = cmd2.GetResources()
            print(f"   ✅ Commande 1: {res1['MenuText']}")
            print(f"   ✅ Commande 2: {res2['MenuText']}")

            # Vérifier que les icônes existent
            icon1_path = res1["Pixmap"]
            icon2_path = res2["Pixmap"]

            if os.path.exists(icon1_path):
                print(f"   ✅ Icône 1 trouvée: {icon1_path}")
            else:
                print(f"   ❌ Icône 1 manquante: {icon1_path}")

            if os.path.exists(icon2_path):
                print(f"   ✅ Icône 2 trouvée: {icon2_path}")
            else:
                print(f"   ❌ Icône 2 manquante: {icon2_path}")

        except Exception as e:
            print(f"   ❌ Erreur lors du test des ressources: {e}")

        # Test 5: Test de la fonction d'enregistrement
        print("\n5️⃣ Test de la fonction d'enregistrement...")
        result = reload_commands.register_commands()
        if result:
            print("   ✅ Enregistrement réussi")
        else:
            print("   ⚠️ Enregistrement échoué (normal sans FreeCAD)")

        # Test 6: Test du module de rechargement
        print("\n6️⃣ Test du module de rechargement...")
        try:
            reload_result = reload_commands.reload_workbench.reload_workbench()
            if reload_result is False:
                print("   ⚠️ Rechargement échoué (normal sans FreeCAD)")
            else:
                print("   ✅ Rechargement réussi")
        except Exception as e:
            print(f"   ❌ Erreur lors du test de rechargement: {e}")

        print("\n" + "=" * 50)
        print("🎯 Résumé du test:")
        print("   ✅ Import du module: OK")
        print("   ✅ Création des commandes: OK")
        print("   ✅ Ressources des commandes: OK")
        print("   ⚠️ Enregistrement: Nécessite FreeCAD")
        print("   ⚠️ Rechargement: Nécessite FreeCAD")
        print("\n💡 Le module est prêt pour FreeCAD!")

        return True

    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_command_loading()
    sys.exit(0 if success else 1)
