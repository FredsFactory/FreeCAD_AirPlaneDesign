"""
Configuration des raccourcis clavier pour le rechargement du workbench
"""

import FreeCADGui as Gui
from PySide import QtCore, QtGui


def setup_keyboard_shortcuts():
    """Configure les raccourcis clavier pour le rechargement"""
    try:
        # Obtenir l'application principale
        main_window = Gui.getMainWindow()

        if main_window:
            # Raccourci Ctrl+R pour recharger le workbench
            reload_action = QtGui.QAction("Recharger Workbench", main_window)
            reload_action.setShortcut(QtGui.QKeySequence("Ctrl+R"))
            reload_action.setToolTip("Recharge le workbench AirPlaneDesign (Ctrl+R)")

            def reload_shortcut():
                try:
                    import scripts.development.reload_workbench as reload_workbench

                    reload_workbench.reload_workbench()
                except Exception as e:
                    print(f"❌ Erreur raccourci : {e}")

            reload_action.triggered.connect(reload_shortcut)
            main_window.addAction(reload_action)

            # Raccourci Ctrl+Shift+R pour activer l'auto-rechargement
            auto_reload_action = QtGui.QAction("Auto-rechargement", main_window)
            auto_reload_action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+R"))
            auto_reload_action.setToolTip("Active l'auto-rechargement (Ctrl+Shift+R)")

            def auto_reload_shortcut():
                try:
                    import scripts.development.reload_workbench as reload_workbench

                    reload_workbench.setup_auto_reload()
                except Exception as e:
                    print(f"❌ Erreur auto-rechargement : {e}")

            auto_reload_action.triggered.connect(auto_reload_shortcut)
            main_window.addAction(auto_reload_action)

            # Raccourci Ctrl+Shift+C pour nettoyer les caches
            clean_cache_action = QtGui.QAction("Nettoyer Cache", main_window)
            clean_cache_action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+C"))
            clean_cache_action.setToolTip("Nettoie les caches Python (Ctrl+Shift+C)")

            def clean_cache_shortcut():
                try:
                    import scripts.development.clean_cache as clean_cache

                    clean_cache.clean_freecad_workbench()
                    print("🧹 Caches nettoyés avec succès!")
                except Exception as e:
                    print(f"❌ Erreur nettoyage cache : {e}")

            clean_cache_action.triggered.connect(clean_cache_shortcut)
            main_window.addAction(clean_cache_action)

            print("⌨️ Raccourcis clavier configurés :")
            print("   Ctrl+R : Recharger le workbench")
            print("   Ctrl+Shift+R : Activer l'auto-rechargement")
            print("   Ctrl+Shift+C : Nettoyer les caches Python")

        else:
            print("⚠️ Impossible d'obtenir la fenêtre principale pour les raccourcis")

    except Exception as e:
        print(f"⚠️ Erreur lors de la configuration des raccourcis : {e}")


# Configuration automatique lors de l'import
setup_keyboard_shortcuts()
