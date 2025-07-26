"""
Commande FreeCAD pour recharger le workbench AirPlaneDesign
"""

import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtCore, QtGui
import os

class ReloadWorkbenchCommand:
    """Commande pour recharger le workbench"""
    
    def GetResources(self):
        """Retourne les ressources de la commande"""
        return {
            'Pixmap': os.path.join(os.path.dirname(__file__), 'resources', 'icons', 'reload.png'),
            'MenuText': 'Recharger le Workbench',
            'ToolTip': 'Recharge le workbench AirPlaneDesign sans redémarrer FreeCAD'
        }
    
    def Activated(self):
        """Exécute la commande"""
        try:
            import reload_workbench
            result = reload_workbench.reload_workbench()
            
            if result:
                # Afficher une notification de succès
                from PySide import QtGui
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Information)
                msg.setWindowTitle("Workbench rechargé")
                msg.setText("Le workbench AirPlaneDesign a été rechargé avec succès !")
                msg.setInformativeText("Toutes les modifications de code ont été prises en compte.")
                msg.exec_()
            else:
                # Afficher une erreur
                from PySide import QtGui
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setWindowTitle("Erreur de rechargement")
                msg.setText("Erreur lors du rechargement du workbench.")
                msg.setInformativeText("Consultez la console pour plus de détails.")
                msg.exec_()
                
        except Exception as e:
            App.Console.PrintError(f"Erreur lors du rechargement : {e}\n")
    
    def IsActive(self):
        """Détermine si la commande est active"""
        return True

class ToggleAutoReloadCommand:
    """Commande pour activer/désactiver le rechargement automatique"""
    
    def __init__(self):
        self.auto_reload_active = False
    
    def GetResources(self):
        """Retourne les ressources de la commande"""
        return {
            'Pixmap': os.path.join(os.path.dirname(__file__), 'resources', 'icons', 'auto_reload.png'),
            'MenuText': 'Auto-rechargement',
            'ToolTip': 'Active/désactive le rechargement automatique lors des modifications'
        }
    
    def Activated(self):
        """Exécute la commande"""
        try:
            import reload_workbench
            
            if not self.auto_reload_active:
                reload_workbench.setup_auto_reload()
                self.auto_reload_active = True
                App.Console.PrintMessage("🔄 Auto-rechargement activé\n")
                
                # Notification
                from PySide import QtGui
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Information)
                msg.setWindowTitle("Auto-rechargement activé")
                msg.setText("Le rechargement automatique est maintenant activé.")
                msg.setInformativeText("Le workbench sera rechargé automatiquement lors des modifications de fichiers.")
                msg.exec_()
            else:
                App.Console.PrintMessage("⚠️ Auto-rechargement déjà activé\n")
                
        except Exception as e:
            App.Console.PrintError(f"Erreur lors de l'activation de l'auto-rechargement : {e}\n")
    
    def IsActive(self):
        """Détermine si la commande est active"""
        return True

# Enregistrer les commandes
Gui.addCommand('ReloadWorkbench', ReloadWorkbenchCommand())
Gui.addCommand('ToggleAutoReload', ToggleAutoReloadCommand())

# Message d'information
print("🔧 Commandes de rechargement ajoutées :")
print("   - ReloadWorkbench : Recharge le workbench manuellement")
print("   - ToggleAutoReload : Active le rechargement automatique")
