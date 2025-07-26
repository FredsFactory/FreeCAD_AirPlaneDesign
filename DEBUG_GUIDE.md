# Guide de débogage FreeCAD avec VS Code

Ce guide vous explique comment configurer et utiliser le débogueur VS Code avec votre workbench FreeCAD AirPlaneDesign.

## 🛠️ Installation et Configuration

### 1. Installation de debugpy

Exécutez le script d'installation :
```bash
./install_debugpy.sh
```

Ou installez manuellement :
```bash
# Avec pip
pip install debugpy

# Ou avec pip3
pip3 install debugpy

# Ou dans l'environnement Python de FreeCAD
/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install debugpy
```

### 2. Configuration dans FreeCAD

Le code de débogage est déjà configuré dans `InitGui.py`. Quand vous chargez votre workbench, il démarre automatiquement un serveur de débogage sur le port 5678.

## 🚀 Utilisation

### Méthode 1 : Attach to FreeCAD (Recommandée)

1. **Lancez FreeCAD** et ouvrez votre workbench AirPlaneDesign
2. **Dans la console FreeCAD**, vous devriez voir :
   ```
   🔧 Serveur de débogage démarré sur le port 5678
   📋 Instructions pour se connecter :
   ⏳ En attente de la connexion du débogueur...
   ```
3. **Dans VS Code** :
   - Ouvrez votre workspace AirPlaneDesign
   - Appuyez sur `F5` ou allez dans `Run > Start Debugging`
   - Sélectionnez "Attach to FreeCAD"
4. **Placez des points d'arrêt** dans votre code Python
5. **Exécutez des commandes** dans FreeCAD pour déclencher le débogage

### Méthode 2 : Attach using Process ID

1. **Lancez FreeCAD**
2. **Dans VS Code** :
   - Appuyez sur `F5`
   - Sélectionnez "Python: Attach using Process ID"
   - Choisissez le processus FreeCAD dans la liste

## 🔧 Configuration avancée

### Points d'arrêt conditionnels

Vous pouvez créer des points d'arrêt conditionnels :
```python
# Exemple : s'arrêter seulement si une condition est vraie
if variable_name == "specific_value":
    debugpy.breakpoint()  # Point d'arrêt programmé
```

### Débogage avec attente de connexion

Si vous voulez que FreeCAD attende la connexion du débogueur, décommentez cette ligne dans `InitGui.py` :
```python
# debugpy.wait_for_client()
```

## 🐛 Résolution de problèmes

### debugpy non trouvé
```
⚠️ debugpy n'est pas installé. Installez-le avec : pip install debugpy
```
**Solution** : Exécutez `./install_debugpy.sh` ou installez debugpy manuellement.

### Port déjà utilisé
```
⚠️ Erreur lors de l'initialisation du débogueur : [Errno 48] Address already in use
```
**Solution** : Changez le port dans `InitGui.py` et `launch.json` (ex: 5679).

### VS Code ne se connecte pas
1. Vérifiez que FreeCAD affiche le message d'attente du débogueur
2. Vérifiez que le port est le même dans `InitGui.py` et `launch.json`
3. Redémarrez FreeCAD et VS Code

### Points d'arrêt ignorés
1. Assurez-vous que `justMyCode` est `false` dans `launch.json`
2. Vérifiez que le chemin dans `pathMappings` est correct
3. Les points d'arrêt ne fonctionnent que dans le code Python, pas dans les parties C++

## 📝 Exemple d'utilisation

1. Placez un point d'arrêt dans une fonction de votre workbench
2. Lancez FreeCAD et connectez le débogueur
3. Exécutez une commande qui déclenche cette fonction
4. Le débogueur s'arrêtera au point d'arrêt
5. Vous pouvez inspecter les variables, exécuter du code, etc.

## 🎯 Conseils

- **Performance** : Le débogage peut ralentir FreeCAD. Désactivez-le en production.
- **Logs** : Utilisez `print()` pour des logs simples, le débogueur pour l'inspection détaillée.
- **Redémarrage** : Parfois, redémarrer FreeCAD peut résoudre les problèmes de connexion.
- **Extensions VS Code** : Assurez-vous d'avoir l'extension Python installée dans VS Code.

## � Rechargement du Workbench (NOUVEAU)

### Rechargement manuel
Pour recharger le workbench sans redémarrer FreeCAD après une modification :

#### Méthodes disponibles :
1. **Console FreeCAD** : `reload_workbench.reload()` ou `reload_workbench.rl()`
2. **Raccourci clavier** : `Ctrl+R`
3. **Bouton dans la toolbar** : Cliquez sur l'icône de rechargement
4. **Menu** : Development > Recharger le Workbench

#### Rechargement automatique :
- **Console** : `reload_workbench.setup_auto_reload()`
- **Raccourci** : `Ctrl+Shift+R`
- **Bouton** : Icône auto-rechargement dans la toolbar

### Workflow de développement recommandé :
1. Activez l'auto-rechargement au début de votre session
2. Modifiez votre code dans VS Code
3. Le workbench se recharge automatiquement
4. Testez vos modifications dans FreeCAD
5. Placez des points d'arrêt si nécessaire
6. Connectez le débogueur VS Code

## �📂 Fichiers de configuration

- `InitGui.py` : Configuration du serveur de débogage
- `.vscode/launch.json` : Configuration VS Code
- `install_debugpy.sh` : Script d'installation
- `reload_workbench.py` : Module de rechargement
- `reload_commands.py` : Commandes FreeCAD pour le rechargement
- `keyboard_shortcuts.py` : Raccourcis clavier
- `DEBUG_GUIDE.md` : Ce guide
