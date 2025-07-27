# Scripts Directory

Ce répertoire contient tous les scripts utilitaires, de développement et de test pour le workbench AirPlaneDesign.

## Structure

```
scripts/
├── __init__.py                 # Package principal
├── utils.py                    # Utilitaires d'accès rapide
├── README.md                   # Cette documentation
├── development/                # Scripts de développement
│   ├── __init__.py
│   ├── reload_workbench.py     # Rechargement à chaud du workbench
│   ├── reload_commands.py      # Commandes UI pour rechargement
│   ├── keyboard_shortcuts.py   # Configuration raccourcis clavier
│   ├── create_reload_icons.py  # Création icônes pour rechargement
│   ├── demo_*.py               # Scripts de démonstration
│   ├── setup_*.py/sh           # Scripts de configuration
│   └── migrate_imports.sh      # Migration des imports
├── testing/                    # Scripts de test et debug
│   ├── __init__.py
│   ├── debug_icon_paths.py     # Vérification chemins d'icônes
│   └── test_autocompletion.py  # Test de l'autocomplétion
└── docs/                       # Documentation détaillée
    ├── AUTOCOMPLETION_GUIDE.md # Guide autocomplétion
    ├── DEBUG_GUIDE.md          # Guide de debug
    └── MIGRATION_IMPORTS.md    # Guide migration imports
```

## Utilisation

### Depuis la console FreeCAD

```python
# Accès rapide via utils.py
import scripts.utils as utils
utils.rl()                     # Recharger le workbench
utils.debug_icons()            # Debug des icônes
utils.help_scripts()           # Afficher l'aide

# Accès direct aux modules
from scripts.development import reload_workbench
reload_workbench.reload()

from scripts.testing import debug_icon_paths
debug_icon_paths.debug_module_icon_paths()
```

### Depuis VS Code

Les scripts sont automatiquement chargés par `InitGui.py` et les commandes de rechargement sont disponibles dans l'interface FreeCAD.

## Scripts disponibles

### Développement

- **reload_workbench.py** : Système de rechargement à chaud complet
- **reload_commands.py** : Commandes FreeCAD pour rechargement via interface
- **keyboard_shortcuts.py** : Configuration des raccourcis clavier (F5, etc.)
- **create_reload_icons.py** : Création d'icônes pour les commandes de rechargement
- **demo\_\*.py** : Scripts de démonstration des fonctionnalités
- **setup\_\*.py/sh** : Scripts de configuration et installation
- **migrate_imports.sh** : Script de migration automatique des imports

### Testing

- **debug_icon_paths.py** : Vérification et debug des chemins d'icônes
- **test_autocompletion.py** : Tests de l'autocomplétion FreeCAD
- **utils.py** : Interface unifiée pour accéder facilement à tous les scripts

### Documentation

- **docs/AUTOCOMPLETION_GUIDE.md** : Guide complet pour l'autocomplétion
- **docs/DEBUG_GUIDE.md** : Guide de debug et dépannage
- **docs/MIGRATION_IMPORTS.md** : Guide de migration des imports

## Ajout de nouveaux scripts

1. Placer le script dans le sous-répertoire approprié (`development/` ou `testing/`)
2. Documenter dans le `__init__.py` du sous-répertoire
3. Optionnellement ajouter un raccourci dans `utils.py`
4. Mettre à jour ce README
