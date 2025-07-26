"""
Exemple d'utilisation de l'autocomplétion FreeCAD dans VS Code

Ce fichier démontre comment utiliser l'autocomplétion pour les fonctions FreeCAD.
Testez en tapant "App." ou "Vector." pour voir les suggestions d'autocomplétion.
"""

# Import pour l'autocomplétion
from freecad_imports import App, Gui, Vector, Placement, Part, Draft, Console

def test_autocompletion():
    """
    Fonction de test pour l'autocomplétion FreeCAD
    
    Instructions :
    1. Placez votre curseur après chaque point (.)
    2. Appuyez sur Ctrl+Space pour voir les suggestions
    3. VS Code devrait vous proposer les méthodes disponibles
    """
    
    # Test 1: Document
    # Tapez "App." et vous devriez voir : newDocument, ActiveDocument, etc.
    doc = App.newDocument("TestDoc")
    
    # Test 2: Objet
    # Tapez "doc." et vous devriez voir : addObject, recompute, save, etc.
    obj = doc.addObject("Part::Box", "MaBoite")
    
    # Test 3: Vector
    # Tapez "Vector(" et vous devriez voir les paramètres : x, y, z
    v1 = Vector(10, 20, 30)
    v2 = Vector(5, 10, 15)
    
    # Tapez "v1." et vous devriez voir : add, sub, cross, dot, Length, etc.
    v3 = v1.add(v2)
    length = v1.Length
    
    # Test 4: Placement
    # Tapez "Placement(" et vous devriez voir les paramètres
    placement = Placement(Vector(0, 0, 0))
    
    # Test 5: Part
    # Tapez "Part." et vous devriez voir : makeBox, makeCylinder, etc.
    box = Part.makeBox(10, 10, 10)
    cylinder = Part.makeCylinder(5, 10)
    
    # Test 6: Draft
    # Tapez "Draft." et vous devriez voir : makeLine, makeCircle, etc.
    line = Draft.makeLine(Vector(0, 0, 0), Vector(10, 10, 0))
    
    # Test 7: Console
    # Tapez "Console." et vous devriez voir : PrintMessage, PrintError, etc.
    Console.PrintMessage("Test d'autocomplétion réussi !")
    
    # Test 8: Récomputer le document
    doc.recompute()
    
    return doc

def test_avec_types():
    """
    Test avec annotations de type pour une meilleure autocomplétion
    """
    
    # Les annotations de type améliorent l'autocomplétion
    doc: App.Document = App.newDocument("TypedDoc")
    
    # VS Code connaît maintenant le type exact de 'obj'
    obj: App.DocumentObject = doc.addObject("Part::Box", "TypedBox")
    
    # L'autocomplétion sera plus précise
    obj_name: str = obj.Name
    obj_label: str = obj.Label
    
    return doc, obj

def exemple_workbench():
    """
    Exemple typique d'utilisation dans un workbench
    """
    
    # Vérifier qu'un document est actif
    if not App.ActiveDocument:
        doc = App.newDocument("MonWorkbench")
    else:
        doc = App.ActiveDocument
    
    # Créer une géométrie
    box = Part.makeBox(100, 50, 25)
    
    # Ajouter à FreeCAD
    box_obj = doc.addObject("Part::Feature", "MaBoite")
    box_obj.Shape = box
    
    # Positionnement
    box_obj.Placement = Placement(Vector(0, 0, 0))
    
    # Recompute et message
    doc.recompute()
    Console.PrintMessage("Objet créé avec succès !\n")
    
    # Si dans FreeCAD, mettre à jour la vue
    if hasattr(Gui, 'SendMsgToActiveView'):
        Gui.SendMsgToActiveView("ViewFit")

# Tests à exécuter seulement si dans FreeCAD
if __name__ == "__main__":
    print("🧪 Test de l'autocomplétion FreeCAD")
    print("Utilisez ce fichier pour tester l'autocomplétion dans VS Code")
    
    # Décommenter pour tester dans FreeCAD
    # test_autocompletion()
    # test_avec_types()
    # exemple_workbench()
