# 🎯 Guide Complet : Autocomplétion FreeCAD dans VS Code

## ✅ Configuration Terminée

Votre workspace est maintenant configuré pour l'autocomplétion FreeCAD ! Voici ce qui a été mis en place :

### 📁 Fichiers créés :

1. **`freecad_stubs.py`** - Définitions des types FreeCAD
2. **`freecad_imports.py`** - Module d'import intelligent  
3. **`.vscode/settings.json`** - Configuration VS Code
4. **`test_autocompletion.py`** - Fichier de test
5. **`setup_freecad_paths.py`** - Configuration des chemins

## 🚀 Comment utiliser l'autocomplétion

### Méthode 1 : Import direct (Recommandée)

Dans vos fichiers Python, ajoutez en haut :

```python
# Pour l'autocomplétion FreeCAD
from freecad_imports import App, Gui, Vector, Part, Draft, Console

# Votre code ici
def ma_fonction():
    doc = App.newDocument()  # ← VS Code vous proposera les méthodes !
    obj = doc.addObject("Part::Box", "MaBoite")
    # etc...
```

### Méthode 2 : Import conditionnel (pour compatibilité)

```python
try:
    import FreeCAD as App
    import FreeCADGui as Gui
except ImportError:
    # Import des stubs pour l'autocomplétion VS Code
    from freecad_imports import App, Gui
```

## 🧪 Test de l'autocomplétion

1. **Ouvrez** `test_autocompletion.py`
2. **Placez votre curseur** après `App.` (ligne 23)
3. **Appuyez sur `Ctrl+Space`** (ou `Cmd+Space` sur Mac)
4. **Vous devriez voir** : `newDocument`, `ActiveDocument`, etc.

### Test complet :

```python
from freecad_imports import App, Vector, Part

# Testez ces lignes :
App.  # ← Ctrl+Space ici
Vector(  # ← Vous verrez les paramètres x, y, z
Part.make  # ← Vous verrez makeBox, makeCylinder, etc.
```

## ⚙️ Configuration VS Code

### Extensions recommandées :

1. **Python** (Microsoft) - Obligatoire
2. **Pylance** (Microsoft) - Pour l'autocomplétion avancée  
3. **Python Docstring Generator** - Pour la documentation

### Paramètres VS Code optimaux :

Ajoutez dans vos paramètres VS Code (`Cmd+,`) :

```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.autoSearchPaths": true,
    "editor.suggestSelection": "first",
    "editor.acceptSuggestionOnCommitCharacter": false,
    "python.analysis.completeFunctionParens": true
}
```

## 🔧 Raccourcis Utiles

| Raccourci | Action |
|-----------|--------|
| `Ctrl+Space` | Forcer l'autocomplétion |
| `Cmd+Click` | Aller à la définition |
| `Ctrl+Shift+Space` | Aide sur les paramètres |
| `F12` | Aller à la définition |
| `Shift+F12` | Voir toutes les références |

## 🎯 Exemples d'Usage

### 1. Création d'objets
```python
from freecad_imports import App, Part, Vector

doc = App.newDocument("MonProjet")
box = Part.makeBox(10, 20, 30)  # ← Autocomplétion sur makeBox
obj = doc.addObject("Part::Feature", "MaBoite")
obj.Shape = box
```

### 2. Manipulation de vecteurs
```python
from freecad_imports import Vector

v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)
v3 = v1.add(v2)  # ← Autocomplétion sur .add, .sub, .cross, etc.
length = v1.Length  # ← Propriété Length
```

### 3. Interface utilisateur
```python
from freecad_imports import Gui, Console

# Messages
Console.PrintMessage("Hello!")  # ← Autocomplétion sur Print*
Console.PrintError("Erreur!")

# GUI
main_window = Gui.getMainWindow()  # ← Autocomplétion sur get*
```

## 🔄 Intégration avec le rechargement

Combinez avec votre système de rechargement :

```python
from freecad_imports import App, Console
import reload_workbench

def ma_commande():
    # Votre code avec autocomplétion
    doc = App.ActiveDocument
    if not doc:
        Console.PrintError("Aucun document actif!\n")
        return
    
    # Votre logique métier
    # ...
    
    # Recharger si nécessaire
    # reload_workbench.rl()
```

## 🐛 Résolution de Problèmes

### L'autocomplétion ne fonctionne pas

1. **Vérifiez l'extension Python** : Extension > Python installée et activée
2. **Redémarrez VS Code** : Parfois nécessaire après la configuration
3. **Vérifiez l'import** : `from freecad_imports import App` en haut du fichier
4. **Mode TypeChecking** : Activez `"python.analysis.typeCheckingMode": "basic"`

### Erreurs d'import

Si vous voyez des erreurs rouges :
- C'est normal quand vous n'êtes pas dans FreeCAD
- Les stubs permettent l'autocomplétion même avec ces erreurs
- Dans FreeCAD, les vrais modules seront importés

### Autocomplétion partielle

1. **Ajoutez des annotations de type** :
   ```python
   doc: App.Document = App.newDocument()
   obj: App.DocumentObject = doc.addObject(...)
   ```

2. **Utilisez les imports spécifiques** :
   ```python
   from freecad_imports import Vector, Placement, Part
   ```

## 📈 Workflow Optimal

1. **Développement** :
   - Ouvrez VS Code
   - Ajoutez `from freecad_imports import *` 
   - Codez avec autocomplétion complète
   - Sauvegardez → rechargement automatique

2. **Test** :
   - Basculez vers FreeCAD
   - Testez vos modifications
   - Retour à VS Code si besoin

3. **Débogage** :
   - Placez des points d'arrêt dans VS Code
   - Connectez le débogueur (`F5`)
   - Déboguez pas à pas

## 🎊 Félicitations !

Vous avez maintenant :
- ✅ **Autocomplétion complète** pour FreeCAD
- ✅ **Rechargement automatique** du workbench  
- ✅ **Débogage intégré** VS Code ↔ FreeCAD
- ✅ **Workflow de développement** optimal

**Bon développement ! 🚀**

---

## 📚 Références

- [Documentation FreeCAD](https://www.freecadweb.org/wiki/)
- [API Python FreeCAD](https://www.freecadweb.org/api/)
- [VS Code Python](https://code.visualstudio.com/docs/python/python-tutorial)
