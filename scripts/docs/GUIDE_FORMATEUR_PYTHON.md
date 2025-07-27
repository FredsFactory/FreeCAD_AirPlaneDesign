# 🐍 Guide : Installer un Formateur Python dans VS Code

Guide complet pour installer et configurer un formateur Python (black, autopep8, yapf) dans VS Code.

## 🎯 Formateurs Python Recommandés

### 1. **Black** (Recommandé)

- ✅ **Le plus populaire** - Standard de facto
- ✅ **Configuration minimale** - "The uncompromising code formatter"
- ✅ **Consistant** - Style uniforme garanti
- ✅ **Rapide** - Performance excellente

### 2. **autopep8**

- ✅ **Conservateur** - Respecte votre style existant
- ✅ **Configurable** - Nombreuses options
- ✅ **Compatible PEP 8** - Suit les standards Python

### 3. **yapf** (Google)

- ✅ **Très configurable** - Style personnalisable
- ✅ **Esthétique** - Code très lisible
- ⚠️ **Plus complexe** - Configuration plus lourde

## 🚀 Installation et Configuration

### Option 1 : Black (Recommandé pour FreeCAD)

#### 1. Installation avec l'interpréteur FreeCAD

```bash
# Installer Black avec l'interpréteur Python de FreeCAD
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install black

# Ou avec pip3 standard si vous préférez
pip3 install black
```

#### 2. Installation de l'extension VS Code

```bash
# Installer l'extension Black Formatter
code --install-extension ms-python.black-formatter
```

#### 3. Configuration VS Code

Ajoutez dans `.vscode/settings.json` :

```json
{
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=88", "--target-version=py311"],
  "editor.formatOnSave": true,
  "editor.formatOnType": false,
  "editor.formatOnPaste": false,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

#### 4. Configuration Black (optionnel)

Créez un fichier `pyproject.toml` :

```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # Exclure certains dossiers
  __pycache__
  | \.git
  | \.venv
  | examples
)/
'''
```

### Option 2 : autopep8

#### 1. Installation

```bash
# Avec l'interpréteur FreeCAD
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install autopep8

# Extension VS Code (déjà incluse dans Python extension)
```

#### 2. Configuration VS Code

```json
{
  "python.formatting.provider": "autopep8",
  "python.formatting.autopep8Args": [
    "--max-line-length=88",
    "--aggressive",
    "--aggressive"
  ],
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  }
}
```

#### 3. Configuration autopep8

Créez un fichier `setup.cfg` :

```ini
[pycodestyle]
max-line-length = 88
ignore = E203, W503
```

### Option 3 : yapf

#### 1. Installation

```bash
# Avec l'interpréteur FreeCAD
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install yapf
```

#### 2. Configuration VS Code

```json
{
  "python.formatting.provider": "yapf",
  "python.formatting.yapfArgs": [
    "--style={based_on_style: pep8, column_limit: 88}"
  ],
  "editor.formatOnSave": true
}
```

## 🛠️ Configuration Spécifique FreeCAD

### Pour le Projet AirPlaneDesign

Ajoutez dans votre workspace `.vscode/settings.json` :

```json
{
  // Configuration Python FreeCAD
  "python.defaultInterpreterPath": "/Applications/FreeCAD.app/Contents/Resources/bin/python",

  // Configuration Formatage
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=88", "--target-version=py311"],

  // Formatage automatique
  "editor.formatOnSave": true,
  "editor.insertSpaces": true,
  "editor.tabSize": 4,

  // Configuration spécifique Python
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },

  // Linting
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Args": ["--max-line-length=88", "--ignore=E203,W503"]
}
```

### Configuration pyproject.toml pour FreeCAD

```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  __pycache__
  | \.git
  | examples
  | wingribprofil
  | resources
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

## 🧪 Test du Formateur

### 1. Test Manuel

Créez un fichier `test_formatter.py` :

```python
# Code mal formaté intentionnellement
def   test_function(  x,y,z  ):
    if x>0:
        result=x*y+z
        return result
    else:
        return None

class   TestClass:
    def __init__(self,value):
        self.value=value
    def   get_value(  self):
        return self.value
```

### 2. Formatter le Code

**Méthode 1 : VS Code**

- Sauvegardez le fichier (Cmd+S) - formatage automatique
- Ou clic droit → "Format Document"
- Ou Cmd+Shift+P → "Format Document"

**Méthode 2 : Terminal**

```bash
# Avec Black
black test_formatter.py

# Avec autopep8
autopep8 --in-place --aggressive test_formatter.py

# Avec yapf
yapf --in-place test_formatter.py
```

### 3. Résultat Attendu (Black)

```python
# Code formaté par Black
def test_function(x, y, z):
    if x > 0:
        result = x * y + z
        return result
    else:
        return None


class TestClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
```

## 🔧 Scripts d'Automatisation

### Script de Formatage Global

Créez `format_project.py` :

```python
#!/usr/bin/env python3
"""
Script pour formater tout le projet AirPlaneDesign
"""

import os
import subprocess
import glob

def format_with_black():
    """Formate tous les fichiers Python avec Black"""
    print("🎨 Formatage avec Black...")

    # Trouver tous les fichiers Python
    python_files = glob.glob("*.py")

    for file in python_files:
        if file.startswith(('test_', 'setup_', 'fix_')):
            continue  # Ignorer les scripts utilitaires

        try:
            subprocess.run(['black', file], check=True)
            print(f"✅ {file} formaté")
        except subprocess.CalledProcessError:
            print(f"❌ Erreur avec {file}")

def organize_imports():
    """Organise les imports avec isort"""
    print("📦 Organisation des imports...")

    try:
        subprocess.run(['python3', '-m', 'pip', 'install', 'isort'], check=True)
        subprocess.run(['isort', '.'], check=True)
        print("✅ Imports organisés")
    except subprocess.CalledProcessError:
        print("⚠️ isort non disponible")

if __name__ == "__main__":
    print("🚀 Formatage du Projet AirPlaneDesign")
    print("=" * 40)

    format_with_black()
    organize_imports()

    print("\n🎉 Formatage terminé !")
```

### Hook Git Pre-commit

Créez `.git/hooks/pre-commit` :

```bash
#!/bin/bash
# Hook Git pour formater automatiquement avant commit

echo "🎨 Formatage automatique du code..."

# Formater les fichiers modifiés
git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | while read file; do
    black "$file"
    git add "$file"
    echo "✅ $file formaté et ajouté"
done

echo "✅ Code formaté avant commit"
```

Rendre le hook exécutable :

```bash
chmod +x .git/hooks/pre-commit
```

## 📋 Raccourcis Clavier Utiles

Ajoutez dans `keybindings.json` :

```json
[
  {
    "key": "cmd+shift+f",
    "command": "editor.action.formatDocument",
    "when": "editorHasDocumentFormattingProvider && !editorReadonly"
  },
  {
    "key": "cmd+k cmd+f",
    "command": "editor.action.formatSelection",
    "when": "editorHasDocumentSelectionFormattingProvider && !editorReadonly"
  },
  {
    "key": "cmd+shift+o",
    "command": "python.sortImports",
    "when": "editorLangId == python"
  }
]
```

## 🔍 Dépannage

### Problème : Formateur non trouvé

```bash
# Vérifier l'installation
/Applications/FreeCAD.app/Contents/Resources/bin/python -c "import black; print('Black installé')"

# Réinstaller si nécessaire
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install --upgrade black
```

### Problème : Conflit de formatage

1. Désactivez les autres formatters
2. Rechargez VS Code
3. Vérifiez les paramètres du workspace

### Problème : Formatage trop agressif

```json
{
  "python.formatting.blackArgs": [
    "--line-length=100",
    "--skip-string-normalization"
  ]
}
```

## 🎯 Recommandation Finale

**Pour le projet AirPlaneDesign, utilisez Black :**

1. ✅ **Installation simple**
2. ✅ **Intégration parfaite VS Code**
3. ✅ **Compatible FreeCAD**
4. ✅ **Style consistant**
5. ✅ **Configuration minimale**

```bash
# Installation en une commande
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install black
code --install-extension ms-python.black-formatter
```

Avec Black configuré, votre code sera automatiquement formaté à chaque sauvegarde ! 🎉
