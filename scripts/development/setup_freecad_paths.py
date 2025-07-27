# Configuration des chemins Python pour FreeCAD
# Ce fichier sera utilisé par Pylance/Pyright pour l'autocomplétion

import sys
import os

# Ajouter les chemins FreeCAD au sys.path
freecad_paths = [
    "/Applications/FreeCAD.app/Contents/lib",
    "/Applications/FreeCAD.app/Contents/Resources/lib/python3.11/site-packages",
    "/Applications/FreeCAD.app/Contents/Mod",
    "/Applications/FreeCAD.app/Contents/Resources/Mod",
]

# Ajouter tous les chemins valides
for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

print(f"Chemins Python configurés pour FreeCAD : {len([p for p in freecad_paths if os.path.exists(p)])} chemins trouvés")
