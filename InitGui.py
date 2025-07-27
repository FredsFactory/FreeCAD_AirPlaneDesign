#################################################
#
# Airfoil creation - Aircraft
#
# Copyright (c) F. Nivoix - 2018 - V0.1
#
# For FreeCAD Versions = or > 0.17 Revision xxxx
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (LGPL)
# as published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
# for detail see the LICENCE text file.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
################################################
# ------------------------------------------------------
# AirPlaneDesign
# ------------------------------------------------------

import path_locator

import freecad_imports

# Import des modules FreeCAD avec autocomplétion
try:
    import FreeCAD as App, FreeCADGui as Gui
    from freecad_imports import Vector, Console, Workbench
except ImportError:
    from freecad_imports import (
        App,
        Gui,
        Vector,
        Console,
        FreeCAD,
        FreeCADGui,
        Workbench,
    )

from PySide import QtCore
import os


def setup_debug():
    """Configuration du débogueur VS Code pour FreeCAD"""
    try:
        import debugpy

        # Port pour le débogage
        debug_port = 5678

        # Vérifier si debugpy est déjà en écoute
        if not debugpy.is_client_connected():
            # Configurer debugpy
            debugpy.configure(python="python")

            # Démarrer le serveur de débogage
            debugpy.listen(("localhost", debug_port))
            print(f"🔧 Serveur de débogage démarré sur le port {debug_port}")
            print("📋 Instructions pour se connecter :")
            print("   1. Dans VS Code, ouvrez Command Palette (Cmd+Shift+P)")
            print(
                "   2. Tapez 'Python: Attach using Process ID' ou utilisez la configuration launch.json"
            )
            print(
                "   3. Ou utilisez 'Python: Attach to Local Process' et sélectionnez FreeCAD"
            )
            print("⏳ En attente de la connexion du débogueur...")

            print(f"🔧 Debug server started on port {debug_port}")
            print("📋 Instructions to connect:")
            print("   1. In VS Code, open the Command Palette (Cmd+Shift+P)")
            print(
                "   2. Type 'Python: Attach using Process ID' or use the launch.json configuration"
            )
            print("   3. Or use 'Python: Attach to Local Process' and select FreeCAD")
            print("⏳ Waiting for debugger to connect...")

            # Optionnel : attendre la connexion (décommentez si nécessaire)
            # debugpy.wait_for_client()
            # print("✅ Débogueur VS Code connecté à FreeCAD")
        else:
            print("✅ Débogueur déjà connecté")

    except ImportError:
        print("⚠️ debugpy n'est pas installé. Installez-le avec : pip install debugpy")
        print("⚠️ debugpy is not installed. Install it with: pip install debugpy")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation du débogueur : {e}")


# Démarrer le débogage
setup_debug()

# Importer le module de rechargement pour le développement
try:
    import scripts.development.reload_workbench as reload_workbench

    print("🔄 Module de rechargement disponible")
    print(
        "💡 Tapez 'reload_workbench.reload()' ou 'reload_workbench.rl()' dans la console pour recharger"
    )

    # Configurer les raccourcis clavier
    import scripts.development.keyboard_shortcuts

except Exception as e:
    print(f"⚠️ Module de rechargement non disponible : {e}")

# Qt translation handling
# from DraftGui import translate
# from DraftGui import utf8_decode
FreeCADGui.addLanguagePath(":/translations")


smWBpath = os.path.dirname(path_locator.__file__)
smWB_icons_path = os.path.join(smWBpath, "resources", "icons")
global main_smWB_Icon  # lgtm[py/redundant-global-declaration]
main_smWB_Icon = os.path.join(smWB_icons_path, "appicon.svg")

# def QT_TRANSLATE_NOOP(scope, text):
#    return text


# Qt translation handling
def translate(context, text, disambig=None):
    return QtCore.QCoreApplication.translate(context, text, disambig)


class AirPlaneDesignWorkbench(Workbench):
    def __init__(self):
        self.__class__.Icon = main_smWB_Icon
        self.__class__.MenuText = "AirPlaneDesign"
        self.__class__.ToolTip = "A description of my workbench"

    def Initialize(self):
        def QT_TRANSLATE_NOOP(scope, text):
            return text

        print("Initialisation workbench")
        # "This function is executed when FreeCAD starts"
        import App.modules.airPlaneWing.airPlanePanel as airPlanePanel
        import App.modules.airPlaneRib.airPlaneRib as airPlaneRib
        import App.modules.airPlanePlane.airPlanePlane as airPlanePlane
        import App.modules.airPlaneWing.airPlaneWPanel as airPlaneWPanel
        import App.modules.airPlaneWing.airPlaneWing as airPlaneWing
        import App.modules.airPlaneWing.airPlaneWingWizard as airPlaneWingWizard
        import App.modules.airPlaneNacelle.airPlaneNacelle as airPlaneNacelle

        # Importer les commandes de rechargement pour le développement
        try:
            from scripts.development import reload_commands

            # S'assurer que les commandes sont enregistrées
            if hasattr(reload_commands, "register_commands"):
                reload_commands.register_commands()

            print("🔧 Commandes de rechargement chargées")
        except Exception as e:
            print(f"⚠️ Commandes de rechargement non disponibles : {e}")

        # Liste des commandes principales
        self.comList = [
            "airPlaneDesignPlane",
            "airPlaneDesignWing",
            "airPlaneDesignWingPanel",
            "airPlaneDesignWRib",
            "airPlaneDesignWingWizard",
            "airPlaneDesignWPanel",
            "airPlaneDesignNacelle",
        ]

        # Liste des commandes de développement
        self.devComList = ["ReloadWorkbench", "ToggleAutoReload"]

        # creates a new toolbar with your commands
        self.appendToolbar(
            QT_TRANSLATE_NOOP("AirPlaneDesign", "Air Plane Design"), self.comList
        )

        # Toolbar de développement (optionnel)
        self.appendToolbar(
            QT_TRANSLATE_NOOP("AirPlaneDesign", "Development"), self.devComList
        )

        # creates a new menu
        self.appendMenu(
            [QT_TRANSLATE_NOOP("AirPlaneDesign", "Air Plane Design")], self.comList
        )

        # Menu de développement
        self.appendMenu(
            [QT_TRANSLATE_NOOP("AirPlaneDesign", "Development")], self.devComList
        )

    def Activated(self):
        # This function is executed when the workbench is activated
        return

    def Deactivated(self):
        # This function is executed when the workbench is deactivated
        return

    def ContextMenu(self, recipient):
        # This is executed whenever the user right-clicks on screen
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu(
            "AirPlaneDesignInitPlane", self.comList
        )  # add commands to the context menu

    def GetClassName(self):
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"


Gui.addWorkbench(AirPlaneDesignWorkbench())
