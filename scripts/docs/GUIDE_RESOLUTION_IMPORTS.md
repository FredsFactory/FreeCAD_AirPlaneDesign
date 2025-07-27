# 🐍 Guide : Résoudre les Erreurs d'Importation Python dans VS Code

Guide complet pour résoudre les erreurs `Impossible de résoudre l'importation` avec Pylance dans VS Code.

## 🎯 Problème Courant

Erreur typique dans VS Code :

```
Impossible de résoudre l'importation « FreeCAD » à partir de la source
Pylance reportMissingModuleSource
```

## 🔧 Solutions par Type de Module

### 1. Modules FreeCAD (cas spécifique)

#### ✅ Solution Recommandée : Système d'Imports Intelligents

Utilisez notre système `freecad_imports.py` déjà en place :

```python
import freecad_imports

# Import des modules FreeCAD avec autocomplétion
try:
    # Import direct si dans FreeCAD
    import FreeCAD, Part, Draft
    from freecad_imports import App, Gui, Vector, Console
except ImportError:
    # Import des stubs si hors FreeCAD
    from freecad_imports import App, Gui, Vector, Console, Part, Draft, FreeCAD
```

#### 🛠️ Configuration Python Interpreter

1. **Configurer l'interpréteur Python de FreeCAD :**

   ```bash
   # Dans VS Code, appuyez sur Cmd+Shift+P
   # Tapez : "Python: Select Interpreter"
   # Choisissez : /Applications/FreeCAD.app/Contents/Resources/bin/python
   ```

2. **Ajouter les chemins FreeCAD :**
   Dans `.vscode/settings.json` :
   ```json
   {
     "python.analysis.extraPaths": [
       "/Applications/FreeCAD.app/Contents/Resources/lib",
       "/Applications/FreeCAD.app/Contents/lib"
     ]
   }
   ```

### 2. Modules Python Standards

#### ✅ Installation avec pip

```bash
# Utiliser l'interpréteur Python de FreeCAD
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install nom_module

# Ou utiliser l'outil VS Code
# Cmd+Shift+P → "Python: Install Package"
```

#### ✅ Vérification de l'installation

```python
import sys
print("Python executable:", sys.executable)
print("Python path:", sys.path)

# Tester l'import
try:
    import nom_module
    print("✅ Module importé avec succès")
except ImportError as e:
    print("❌ Erreur d'import:", e)
```

### 3. Modules Tiers (numpy, matplotlib, etc.)

#### ✅ Installation dans l'environnement FreeCAD

```bash
# Pour numpy
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install numpy

# Pour matplotlib
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install matplotlib

# Pour pandas
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install pandas
```

#### ✅ Gestion des environnements virtuels

Si vous utilisez un environnement virtuel :

```bash
# Créer un environnement virtuel
python -m venv freecad_env

# L'activer
source freecad_env/bin/activate

# Installer les modules
pip install numpy matplotlib pandas

# Configurer VS Code pour utiliser cet environnement
# Cmd+Shift+P → "Python: Select Interpreter" → freecad_env/bin/python
```

## 🔧 Configuration VS Code

### 1. Fichier settings.json du workspace

```json
{
  "python.defaultInterpreterPath": "/Applications/FreeCAD.app/Contents/Resources/bin/python",
  "python.analysis.extraPaths": [
    "/Applications/FreeCAD.app/Contents/Resources/lib",
    "/Applications/FreeCAD.app/Contents/lib"
  ],
  "python.analysis.autoImportCompletions": true,
  "python.analysis.typeCheckingMode": "off",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true
}
```

### 2. Fichier pyrightconfig.json (optionnel)

Créez un fichier `pyrightconfig.json` à la racine :

```json
{
  "include": ["."],
  "exclude": ["**/__pycache__", ".git"],
  "extraPaths": [
    "/Applications/FreeCAD.app/Contents/Resources/lib",
    "/Applications/FreeCAD.app/Contents/lib"
  ],
  "pythonPath": "/Applications/FreeCAD.app/Contents/Resources/bin/python",
  "typeCheckingMode": "off",
  "useLibraryCodeForTypes": true
}
```

### 3. Fichier .vscode/launch.json pour le debug

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "python": "/Applications/FreeCAD.app/Contents/Resources/bin/python",
      "env": {
        "PYTHONPATH": "/Applications/FreeCAD.app/Contents/Resources/lib:/Applications/FreeCAD.app/Contents/lib"
      }
    }
  ]
}
```

## 🛠️ Scripts de Diagnostic

### 1. Script de Test d'Imports

Créez un fichier `test_imports.py` :

```python
#!/usr/bin/env python3
"""
Script de test pour vérifier les imports Python
"""

import sys
import os

def test_import(module_name, description=""):
    """Teste l'import d'un module"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} {description}")
        return True
    except ImportError as e:
        print(f"❌ {module_name} {description} - Erreur: {e}")
        return False

def main():
    print("🐍 Test des Imports Python")
    print("=" * 40)

    # Informations système
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print()

    # Test des modules standard
    print("📦 Modules Standard:")
    test_import("os", "- Système d'exploitation")
    test_import("sys", "- Système Python")
    test_import("math", "- Mathématiques")
    test_import("json", "- JSON")

    # Test des modules FreeCAD
    print("\n🏗️ Modules FreeCAD:")
    test_import("FreeCAD", "- Core FreeCAD")
    test_import("FreeCADGui", "- Interface graphique")
    test_import("Part", "- Géométrie")
    test_import("Draft", "- Dessin 2D")

    # Test des modules tiers courants
    print("\n📊 Modules Tiers:")
    test_import("numpy", "- Calcul numérique")
    test_import("matplotlib", "- Graphiques")
    test_import("pandas", "- Analyse de données")

    # Test du système d'imports personnalisé
    print("\n🔧 Système Personnalisé:")
    test_import("freecad_imports", "- Imports intelligents")

    print("\n🎯 Chemins Python:")
    for i, path in enumerate(sys.path):
        print(f"  {i+1}. {path}")

if __name__ == "__main__":
    main()
```

### 2. Script de Réparation Automatique

Créez un fichier `fix_imports.py` :

```python
#!/usr/bin/env python3
"""
Script de réparation automatique des imports
"""

import os
import re
import glob

def fix_freecad_imports(file_path):
    """Corrige les imports FreeCAD dans un fichier"""

    print(f"🔧 Traitement de {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Pattern pour détecter les imports FreeCAD directs
    freecad_import_pattern = r'^import FreeCAD.*$'
    freecadgui_import_pattern = r'^import FreeCADGui.*$'
    part_import_pattern = r'^import Part.*$'

    # Vérifier si freecad_imports est déjà importé
    if 'import freecad_imports' not in content:
        # Trouver la ligne après les commentaires d'en-tête
        lines = content.split('\n')
        insert_line = 0

        for i, line in enumerate(lines):
            if line.startswith('__'):  # __title__, __author__, etc.
                insert_line = i + 3  # Insérer après les métadonnées
                break

        # Insérer le système d'imports
        import_block = """
import freecad_imports

# Import des modules FreeCAD avec autocomplétion
try:
    # Import direct si dans FreeCAD
    import FreeCAD, Part, Draft
    from freecad_imports import App, Gui, Vector, Console
except ImportError:
    # Import des stubs si hors FreeCAD
    from freecad_imports import App, Gui, Vector, Console, Part, Draft, FreeCAD
"""

        lines.insert(insert_line, import_block)
        content = '\n'.join(lines)

        # Supprimer les anciens imports directs
        content = re.sub(freecad_import_pattern, '', content, flags=re.MULTILINE)
        content = re.sub(freecadgui_import_pattern, '', content, flags=re.MULTILINE)
        content = re.sub(part_import_pattern, '', content, flags=re.MULTILINE)

        # Nettoyer les lignes vides multiples
        content = re.sub(r'\n\n\n+', '\n\n', content)

        if content != original_content:
            # Sauvegarder l'original
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)

            # Écrire le nouveau contenu
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ {file_path} mis à jour (sauvegarde: {backup_path})")
            return True
        else:
            print(f"ℹ️ {file_path} déjà à jour")
            return False

def main():
    """Fonction principale"""
    print("🔧 Réparation Automatique des Imports FreeCAD")
    print("=" * 50)

    # Chercher tous les fichiers Python
    python_files = glob.glob("*.py")

    if not python_files:
        print("❌ Aucun fichier Python trouvé")
        return

    updated_files = 0

    for file_path in python_files:
        # Ignorer certains fichiers
        if file_path in ['freecad_imports.py', 'test_imports.py', 'fix_imports.py']:
            continue

        try:
            if fix_freecad_imports(file_path):
                updated_files += 1
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")

    print(f"\n📊 Résumé: {updated_files} fichiers mis à jour sur {len(python_files)} traités")

if __name__ == "__main__":
    main()
```

## 🚀 Utilisation Pratique

### 1. Diagnostic Rapide

```bash
# Exécuter le test d'imports
python test_imports.py

# Ou avec l'interpréteur FreeCAD
/Applications/FreeCAD.app/Contents/Resources/bin/python test_imports.py
```

### 2. Réparation Automatique

```bash
# Corriger tous les fichiers Python du projet
python fix_imports.py
```

### 3. Vérification dans VS Code

1. Ouvrez un fichier Python
2. Vérifiez la barre de statut (en bas à droite)
3. L'interpréteur doit être celui de FreeCAD
4. Les erreurs Pylance doivent avoir disparu

## 🔍 Troubleshooting

### Problème : Extension Pylance trop stricte

```json
// Dans settings.json
{
  "python.analysis.typeCheckingMode": "off",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.diagnosticMode": "workspace"
}
```

### Problème : Modules non trouvés malgré l'installation

```bash
# Vérifier l'installation
/Applications/FreeCAD.app/Contents/Resources/bin/python -c "import sys; print(sys.path)"

# Réinstaller si nécessaire
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip uninstall module_name
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install module_name
```

### Problème : Cache Pylance corrompu

```bash
# Dans VS Code, Cmd+Shift+P
# Tapez : "Python: Refresh Language Server"
# Ou redémarrez VS Code
```

## 📋 Checklist de Validation

- [ ] Interpréteur Python FreeCAD configuré
- [ ] Chemins extraPaths ajoutés dans settings.json
- [ ] Système freecad_imports.py en place
- [ ] Tests d'imports passent
- [ ] Aucune erreur Pylance rouge
- [ ] Autocomplétion FreeCAD fonctionne

Avec cette configuration, vous ne devriez plus avoir d'erreurs d'importation dans VS Code ! 🎉
