"""
Commande FreeCAD pour recharger le workbench AirPlaneDesign
"""

import os
import sys

# Import du module de rechargement
from . import reload_workbench

# Imports conditionnels de FreeCAD et PySide
try:
    import FreeCAD as App
    import FreeCADGui as Gui

    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False

try:
    from PySide import QtCore, QtGui
except ImportError:
    try:
        from PySide2 import QtCore, QtWidgets as QtGui
    except ImportError:
        QtGui = None


class ReloadWorkbenchCommand:
    """Commande pour recharger le workbench"""

    def GetResources(self):
        """Retourne les ressources de la commande"""
        # Chemin vers les icônes - utiliser un chemin absolu
        current_dir = os.path.dirname(__file__)
        workbench_root = os.path.dirname(os.path.dirname(current_dir))
        icons_path = os.path.join(workbench_root, "resources", "icons")

        return {
            "Pixmap": os.path.join(icons_path, "reload.svg"),
            "MenuText": "Recharger le Workbench",
            "ToolTip": "Recharge le workbench AirPlaneDesign sans redémarrer FreeCAD",
        }

    def Activated(self):
        """Exécute la commande"""
        try:
            reload_workbench.reload_workbench()
            if "App" in globals() and hasattr(App, "Console"):
                App.Console.PrintMessage("Workbench rechargé avec succès !\n")
            else:
                print("Workbench rechargé avec succès !")
        except Exception as e:
            error_msg = f"Erreur lors du rechargement : {str(e)}"
            if "App" in globals() and hasattr(App, "Console"):
                App.Console.PrintError(error_msg + "\n")
            else:
                print(error_msg)

            # Afficher une boîte de dialogue d'erreur si possible
            try:
                from PySide import QtGui

                QtGui.QMessageBox.critical(
                    None,
                    "Erreur de rechargement",
                    f"Impossible de recharger le workbench :\n{str(e)}",
                )
            except:
                pass

    def IsActive(self):
        """Retourne True si la commande est active"""
        return True


class ToggleAutoReloadCommand:
    """Commande pour activer/désactiver le rechargement automatique"""

    def GetResources(self):
        """Retourne les ressources de la commande"""
        # Chemin vers les icônes - utiliser un chemin absolu
        current_dir = os.path.dirname(__file__)
        workbench_root = os.path.dirname(os.path.dirname(current_dir))
        icons_path = os.path.join(workbench_root, "resources", "icons")

        return {
            "Pixmap": os.path.join(icons_path, "auto_reload.svg"),
            "MenuText": "Basculer le rechargement automatique",
            "ToolTip": "Active/désactive le rechargement automatique du workbench",
        }

    def Activated(self):
        """Exécute la commande"""
        try:
            # Vérifier l'état actuel du rechargement automatique
            current_state = getattr(reload_workbench, "_auto_reload_enabled", False)
            new_state = not current_state

            # Basculer l'état
            reload_workbench._auto_reload_enabled = new_state

            # Message de confirmation
            status = "activé" if new_state else "désactivé"
            message = f"Rechargement automatique {status}"

            if "App" in globals() and hasattr(App, "Console"):
                App.Console.PrintMessage(message + "\n")
            else:
                print(message)

            # Afficher une notification si possible
            try:
                from PySide import QtGui

                QtGui.QMessageBox.information(None, "Rechargement automatique", message)
            except:
                pass

        except Exception as e:
            error_msg = f"Erreur lors du basculement : {str(e)}"
            if "App" in globals() and hasattr(App, "Console"):
                App.Console.PrintError(error_msg + "\n")
            else:
                print(error_msg)

    def IsActive(self):
        """Retourne True si la commande est active"""
        return True


def register_commands():
    """Enregistre les commandes dans FreeCAD"""
    if not FREECAD_AVAILABLE:
        print("⚠️ FreeCAD non disponible - impossible d'enregistrer les commandes")
        return False

    try:
        # Vérifier que Gui est disponible
        if "Gui" not in globals():
            import FreeCADGui as Gui
        else:
            Gui = globals()["Gui"]

        # Enregistrer les commandes
        Gui.addCommand("ReloadWorkbench", ReloadWorkbenchCommand())
        Gui.addCommand("ToggleAutoReload", ToggleAutoReloadCommand())

        print("🔧 Commandes ReloadWorkbench et ToggleAutoReload enregistrées")
        return True

    except Exception as e:
        print(f"⚠️ Erreur lors de l'enregistrement des commandes : {e}")
        return False


# Note: L'enregistrement est fait explicitement depuis InitGui.py
