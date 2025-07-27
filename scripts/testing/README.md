# Tests - AirPlaneDesign

Cette section contient tous les scripts de test organisés par catégorie.

## Structure

```
testing/
├── run_tests.py            # Runner principal pour tous les tests
├── test_autocompletion.py  # Tests d'autocomplétion générale
├── imports/                # Tests des imports et du système d'importation
│   ├── test_imports.py
│   ├── test_final_imports.py
│   └── test_reorganized_imports.py
├── icons/                  # Tests et debug des icônes
│   ├── debug_icon_paths.py
│   └── test_icon_paths.py
├── formatters/             # Tests des formatters de code
│   └── test_formatter.py
└── xfoil/                  # Tests des fonctionnalités xfoil
    └── test_xfoil.py
```

## Utilisation

### Lancer tous les tests

```bash
cd scripts/testing
python run_tests.py all
```

### Lancer les tests par catégorie

```bash
python run_tests.py imports     # Tests d'imports
python run_tests.py icons       # Tests d'icônes
python run_tests.py formatters  # Tests formatters
python run_tests.py xfoil       # Tests xfoil
```

### Lister les tests disponibles

```bash
python run_tests.py list
```

### Depuis utils.py

```python
import scripts.utils as utils
utils.run_tests('all')        # Tous les tests
utils.run_tests('imports')    # Tests d'imports seulement
utils.test_imports()          # Raccourci pour les imports
utils.test_icons()            # Raccourci pour les icônes
```

## Types de tests

### Tests d'imports (`imports/`)

- Validation du système d'importation FreeCAD
- Tests de résolution des imports après réorganisation
- Vérification des imports finaux

### Tests d'icônes (`icons/`)

- Vérification des chemins d'icônes
- Debug des ressources graphiques
- Validation de l'affichage des icônes

### Tests de formatters (`formatters/`)

- Validation du formatter Black
- Tests de formatage de code
- Vérification des règles de style

### Tests xfoil (`xfoil/`)

- Tests des fonctionnalités du module xfoil
- Validation des calculs aérodynamiques

## Ajouter de nouveaux tests

1. Créer un fichier `test_*.py` dans la catégorie appropriée
2. Le test sera automatiquement détecté par `run_tests.py`
3. Suivre la convention de nommage `test_*.py`
4. Documenter dans ce README si nécessaire
