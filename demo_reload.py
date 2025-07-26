"""
Script de démonstration pour tester le rechargement du workbench

Modifiez ce fichier pour tester le rechargement automatique !
"""

# Import des modules FreeCAD avec autocomplétion (plus d'erreur d'import !)
from freecad_imports import App, Console

def demo_function():
    """Fonction de démonstration - modifiez ce message pour tester le rechargement"""
    message = "🎉 Version 1.0 - Workbench chargé avec succès !"
    print(message)
    
    # Utilisation sécurisée de Console pour compatibilité VS Code/FreeCAD
    try:
        Console.PrintMessage(f"{message}\n")
    except (AttributeError, NameError):
        # Fallback si Console n'est pas disponible
        print(f"[Console] {message}")
    
    return message

def demo_calculation(x, y):
    """Fonction de calcul pour tester le débogage"""
    print(f"📊 Calcul : {x} + {y}")
    result = x + y
    print(f"📊 Résultat : {result}")
    
    # Point d'arrêt potentiel ici
    if result > 10:
        print("🔥 Résultat élevé détecté !")
    
    return result

class DemoClass:
    """Classe de démonstration pour tester le rechargement des classes"""
    
    def __init__(self, name="Demo"):
        self.name = name
        self.version = "1.0"  # Changez cette version pour tester
        print(f"🏗️ Création de {self.name} v{self.version}")
    
    def get_info(self):
        """Retourne les informations de l'objet"""
        info = f"Objet {self.name} version {self.version}"
        print(f"ℹ️ {info}")
        return info

# Test automatique lors du chargement
if __name__ == "__main__":
    print("🧪 Test du module de démonstration")
    demo_function()
    demo_calculation(5, 7)
    
    demo_obj = DemoClass("TestObject")
    demo_obj.get_info()

# Appel automatique lors de l'import
demo_function()

print("📝 Instructions pour tester le rechargement :")
print("1. Modifiez le message dans demo_function()")
print("2. Sauvegardez le fichier")  
print("3. Rechargez avec Ctrl+R ou reload_workbench.reload()")
print("4. Observez le nouveau message !")
