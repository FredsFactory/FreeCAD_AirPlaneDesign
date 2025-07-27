# 🚀 Guide d'utilisation des tâches VS Code

Ce guide explique comment utiliser les différentes méthodes pour lancer les scripts du projet AirPlaneDesign dans VS Code.

## 📋 Méthodes disponibles

### 1. 🎯 Via la palette de commandes VS Code

**Raccourci : `Cmd+Shift+P` (macOS)**

1. Ouvrez la palette de commandes
2. Tapez `Tasks: Run Task`
3. Sélectionnez la tâche désirée dans la liste

**Tâches disponibles :**

- 🧹 Clean Python Cache - All
- 🧹 Clean Python Cache - Workbench Only
- 🧪 Run All Tests
- 🔍 Test Imports
- 🎯 Test Icon Paths
- 🔧 Test XFoil Integration
- 📋 Show Project Structure
- 🔄 Demo Reload System
- 📝 Test Autocompletion
- 🎨 Test Formatter
- 🚀 Launch FreeCAD with Debug
- 🔍 Debug Icon Paths
- 🎯 Create Reload Icons
- 🔧 Demo Resolved Imports
- 🧹 Clean Python Cache (Custom Module)

### 2. ⌨️ Via les raccourcis clavier

**Raccourcis prédéfinis :**

- `Cmd+Shift+C` : Clean Python Cache - All
- `Cmd+Shift+T` : Run All Tests
- `Cmd+Shift+I` : Test Imports
- `Cmd+Shift+F` : Launch FreeCAD with Debug
- `Cmd+Shift+S` : Show Project Structure

### 3. 🖱️ Via l'interface VS Code

**Dans l'explorateur :**

1. Cliquez avec le bouton droit dans l'explorateur de fichiers
2. Sélectionnez `Tasks: Run Task`
3. Choisissez votre tâche

**Via la barre de statut :**

- Certaines tâches peuvent apparaître dans la barre de statut de VS Code

### 4. 🔧 Via le terminal intégré

**Lanceur de tâches personnalisé :**

```bash
# Voir toutes les tâches disponibles
python3 task_runner.py help

# Lancer une tâche spécifique
python3 task_runner.py clean
python3 task_runner.py test
python3 task_runner.py structure

# Lister uniquement les noms des tâches
python3 task_runner.py list
```

**Lancement direct :**

```bash
# Nettoyer les caches
python3 scripts/development/clean_cache.py all

# Lancer tous les tests
python3 scripts/testing/run_tests.py

# Tester les imports
python3 scripts/testing/imports/test_final_imports.py
```

## 🎛️ Configuration personnalisée

### Ajouter une nouvelle tâche

1. **Dans `.vscode/tasks.json` :**

```json
{
  "label": "🆕 Ma Nouvelle Tâche",
  "type": "shell",
  "command": "python3",
  "args": ["scripts/mon_script.py"],
  "group": "build",
  "presentation": {
    "echo": true,
    "reveal": "always",
    "focus": false,
    "panel": "shared"
  },
  "problemMatcher": []
}
```

2. **Dans `task_runner.py` :**

```python
"ma-tache": {
    "script": "scripts/mon_script.py",
    "args": [],
    "description": "🆕 Description de ma tâche"
}
```

### Ajouter un raccourci clavier

**Dans `.vscode/keybindings.json` :**

```json
{
  "key": "cmd+shift+m",
  "command": "workbench.action.tasks.runTask",
  "args": "🆕 Ma Nouvelle Tâche",
  "when": "inTasksView || editorTextFocus"
}
```

## 🔍 Détails des tâches principales

### 🧹 Nettoyage des caches

**Clean Python Cache - All :**

- Supprime tous les fichiers `.pyc` et `.pyo`
- Supprime tous les répertoires `__pycache__`
- Nettoie le workspace complet

**Clean Python Cache - Workbench Only :**

- Nettoie uniquement les modules du workbench
- Plus rapide pour le développement

**Clean Python Cache (Custom Module) :**

- Permet de nettoyer un module spécifique
- VS Code demande le nom du module

### 🧪 Tests

**Run All Tests :**

- Lance tous les tests du projet
- Affiche un rapport complet

**Test Imports :**

- Vérifie que tous les imports fonctionnent
- Teste la résolution des dépendances

**Test Icon Paths :**

- Vérifie que toutes les icônes sont accessibles
- Debug les chemins d'icônes

### 🔧 Développement

**Demo Reload System :**

- Démontre le système de rechargement
- Utile pour tester les modifications

**Launch FreeCAD with Debug :**

- Lance FreeCAD en mode debug
- Prêt pour la connexion du debugger VS Code

## 🎯 Bonnes pratiques

### Pour le développement quotidien :

1. **Avant de commencer :**

   ```bash
   python3 task_runner.py clean
   ```

2. **Après des modifications :**

   ```bash
   python3 task_runner.py test-imports
   ```

3. **Avant de commiter :**
   ```bash
   python3 task_runner.py test
   ```

### Pour le debugging :

1. **Problème d'icônes :**

   ```bash
   python3 task_runner.py debug-icons
   ```

2. **Problème d'imports :**

   ```bash
   python3 task_runner.py demo-imports
   ```

3. **Problème de rechargement :**
   ```bash
   python3 task_runner.py demo-reload
   ```

## 🔄 Integration avec FreeCAD

Toutes les tâches sont conçues pour fonctionner avec le système de rechargement du workbench. Vous pouvez :

1. Modifier le code Python
2. Lancer `Clean Python Cache`
3. Recharger le workbench dans FreeCAD (F5 ou bouton reload)
4. Voir immédiatement les changements

## 📚 Ressources supplémentaires

- **Documentation complète :** `scripts/docs/`
- **Utils unifiés :** `import scripts.utils as utils`
- **Structure du projet :** `python3 task_runner.py structure`

---

💡 **Astuce :** Utilisez `Cmd+Shift+P` → `Tasks: Run Task` pour un accès rapide à toutes les fonctionnalités !
