# 🔧 Résolution du problème "Unknown command"

## 🎯 Problème identifié

```
Unknown command 'ReloadWorkbench'
Unknown command 'ToggleAutoReload'
```

## ✅ Solution mise en place

### 1. **Imports conditionnels**

Les modules `reload_commands.py` et `reload_workbench.py` utilisent maintenant des imports conditionnels pour éviter les erreurs si FreeCAD n'est pas disponible.

### 2. **Enregistrement explicite**

Dans `InitGui.py`, les commandes sont maintenant enregistrées explicitement :

```python
# Importer les commandes de rechargement pour le développement
try:
    from scripts.development import reload_commands

    # S'assurer que les commandes sont enregistrées
    if hasattr(reload_commands, 'register_commands'):
        reload_commands.register_commands()

    print("🔧 Commandes de rechargement chargées")
except Exception as e:
    print(f"⚠️ Commandes de rechargement non disponibles : {e}")
```

### 3. **Fonction d'enregistrement robuste**

```python
def register_commands():
    """Enregistre les commandes dans FreeCAD"""
    if not FREECAD_AVAILABLE:
        print("⚠️ FreeCAD non disponible - impossible d'enregistrer les commandes")
        return False

    try:
        # Vérifier que Gui est disponible
        if 'Gui' not in globals():
            import FreeCADGui as Gui
        else:
            Gui = globals()['Gui']

        # Enregistrer les commandes
        Gui.addCommand("ReloadWorkbench", ReloadWorkbenchCommand())
        Gui.addCommand("ToggleAutoReload", ToggleAutoReloadCommand())

        print("🔧 Commandes ReloadWorkbench et ToggleAutoReload enregistrées")
        return True

    except Exception as e:
        print(f"⚠️ Erreur lors de l'enregistrement des commandes : {e}")
        return False
```

## 🧪 Tests disponibles

### Test complet des commandes :

```bash
python3 task_runner.py test-reload-commands
```

### Via VS Code :

- `Cmd+Shift+P` → `Tasks: Run Task` → `🔧 Test Reload Commands`

## 🔄 Prochaines étapes

1. **Redémarrer FreeCAD** complètement
2. **Activer le workbench AirPlaneDesign**
3. **Vérifier dans la console** que les messages suivants apparaissent :
   ```
   🔧 Commandes de rechargement chargées
   🔧 Commandes ReloadWorkbench et ToggleAutoReload enregistrées
   ```

## 🎛️ Interface utilisateur

Une fois les commandes enregistrées, vous devriez voir :

### Barre d'outils "Development"

- 🔄 Bouton "Recharger le Workbench"
- 🔄 Bouton "Basculer le rechargement automatique"

### Menu "Development"

- Recharger le Workbench
- Basculer le rechargement automatique

### Raccourcis clavier (si configurés)

- `F5` : Rechargement rapide
- `Ctrl+F5` : Basculer rechargement automatique

## 🔍 Diagnostic

Si le problème persiste :

1. **Vérifier les messages dans la console FreeCAD**
2. **Tester en mode debug** :
   ```python
   from scripts.development import reload_commands
   reload_commands.register_commands()
   ```
3. **Nettoyer les caches** :
   ```bash
   python3 task_runner.py clean
   ```

## 📋 Checklist de résolution

- ✅ Imports conditionnels implémentés
- ✅ Enregistrement explicite des commandes
- ✅ Fonction robuste d'enregistrement
- ✅ Tests de validation créés
- ✅ Gestion d'erreurs améliorée
- ✅ Documentation mise à jour

---

💡 **Note :** Ces modifications garantissent que les commandes sont correctement enregistrées même si FreeCAD charge les modules dans un ordre différent ou si certaines dépendances ne sont pas immédiatement disponibles.
