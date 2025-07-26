"""
Module d'imports FreeCAD pour l'autocomplétion VS Code
Importez ce module dans vos fichiers pour avoir l'autocomplétion
"""

# Essayer d'importer les vrais modules FreeCAD
try:
    import FreeCAD as App
    import FreeCADGui as Gui
    import Part
    import Draft
    import Mesh
    import Sketcher
    from FreeCAD import Vector, Placement, Rotation, Matrix, Console
    
    # Vérifier si nous sommes dans FreeCAD
    FREECAD_AVAILABLE = True
    print("✅ Modules FreeCAD importés avec succès")
    
except ImportError:
    # Si FreeCAD n'est pas disponible, utiliser les stubs
    print("⚠️ FreeCAD non disponible, utilisation des stubs pour l'autocomplétion")
    FREECAD_AVAILABLE = False
    
    # Importer les stubs
    from freecad_stubs import (
        App, Vector, Placement, Rotation, Matrix, Console,
        Part, Mesh, Draft, Sketcher, DocumentObject, Document
    )
    
    # Créer un faux module Gui
    class FreeCADGui:
        @staticmethod
        def addCommand(name: str, command_class) -> None:
            """Enregistre une commande FreeCAD"""
            pass
        
        @staticmethod
        def getMainWindow():
            """Retourne la fenêtre principale"""
            return None
        
        @staticmethod
        def activateWorkbench(name: str) -> None:
            """Active un workbench"""
            pass
        
        @staticmethod
        def activeWorkbench():
            """Retourne le workbench actif"""
            return None
        
        class Control:
            @staticmethod
            def showDialog(dialog) -> None:
                """Affiche un dialogue"""
                pass
            
            @staticmethod
            def closeDialog() -> None:
                """Ferme le dialogue"""
                pass
        
        class ActiveDocument:
            @staticmethod
            def resetEdit() -> None:
                """Reset l'édition"""
                pass
    
    Gui = FreeCADGui()

# Fonction utilitaire pour vérifier la disponibilité
def is_freecad_available() -> bool:
    """Retourne True si FreeCAD est disponible"""
    return FREECAD_AVAILABLE

# Exemples d'utilisation pour l'autocomplétion
def exemple_autocompletion():
    """
    Exemples d'utilisation pour tester l'autocomplétion
    Ces fonctions ne sont jamais appelées, elles servent juste d'exemples
    """
    
    # Document
    doc = App.newDocument("MonDocument")
    doc.recompute()
    
    # Objets
    obj = doc.addObject("Part::Box", "MaBoite")
    obj.Length = 10
    obj.Width = 10 
    obj.Height = 10
    
    # Géométrie
    box = Part.makeBox(10, 10, 10)
    cylinder = Part.makeCylinder(5, 10)
    
    # Vecteurs
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    v3 = v1.add(v2)
    
    # Placement
    p = Placement(Vector(0, 0, 0), Rotation(Vector(0, 0, 1), 0))
    
    # Console
    Console.PrintMessage("Hello FreeCAD!")
    Console.PrintError("Erreur!")
    
    # Draft
    line = Draft.makeLine(Vector(0, 0, 0), Vector(10, 10, 0))
    
    # Gui (si disponible)
    if FREECAD_AVAILABLE:
        Gui.activeWorkbench()

# Exports pour faciliter l'import
__all__ = [
    'App', 'Gui', 'Part', 'Draft', 'Mesh', 'Sketcher',
    'Vector', 'Placement', 'Rotation', 'Matrix', 'Console',
    'FREECAD_AVAILABLE', 'is_freecad_available'
]
