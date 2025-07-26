#!/bin/bash

# Script d'installation de debugpy pour FreeCAD
# Ce script installe debugpy dans l'environnement Python de FreeCAD

echo "🔧 Installation de debugpy pour le débogage FreeCAD avec VS Code"
echo "=================================================="

# Détecter l'installation de FreeCAD sur macOS
FREECAD_PYTHON=""

# Chemins possibles pour FreeCAD sur macOS
POSSIBLE_PATHS=(
    "/Applications/FreeCAD.app/Contents/Resources/bin/python"
    "/Applications/FreeCAD.app/Contents/bin/python"
    "/usr/local/bin/python3"
    "/opt/homebrew/bin/python3"
    "python3"
)

echo "🔍 Recherche de l'exécutable Python de FreeCAD..."

for path in "${POSSIBLE_PATHS[@]}"; do
    if command -v "$path" &> /dev/null; then
        echo "✅ Python trouvé : $path"
        FREECAD_PYTHON="$path"
        break
    fi
done

if [ -z "$FREECAD_PYTHON" ]; then
    echo "❌ Impossible de trouver l'exécutable Python de FreeCAD"
    echo "💡 Veuillez installer debugpy manuellement :"
    echo "   pip install debugpy"
    exit 1
fi

echo "📦 Installation de debugpy..."
$FREECAD_PYTHON -m pip install debugpy

if [ $? -eq 0 ]; then
    echo "✅ debugpy installé avec succès !"
    echo ""
    echo "📋 Instructions pour utiliser le débogueur :"
    echo "1. Lancez FreeCAD"
    echo "2. Chargez votre workbench AirPlaneDesign"
    echo "3. Dans VS Code, appuyez sur F5 ou allez dans Run > Start Debugging"
    echo "4. Sélectionnez 'Attach to FreeCAD'"
    echo "5. Placez des points d'arrêt dans votre code Python"
    echo ""
    echo "🎯 Le serveur de débogage sera sur le port 5678"
else
    echo "❌ Erreur lors de l'installation de debugpy"
    echo "💡 Essayez d'installer manuellement :"
    echo "   pip install debugpy"
    echo "   ou"
    echo "   pip3 install debugpy"
fi
