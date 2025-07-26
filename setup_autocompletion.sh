#!/bin/bash

# Script d'installation des packages pour l'autocomplétion FreeCAD dans VS Code

echo "🔧 Configuration de l'autocomplétion FreeCAD pour VS Code"
echo "======================================================="

# Vérifier si Python est disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

echo "📦 Installation des packages Python recommandés..."

# Installer les packages utiles pour l'autocomplétion
packages=(
    "pylsp-mypy"        # Support MyPy pour le type checking
    "python-lsp-server" # Language Server Protocol
    "pylint"            # Linter
    "flake8"           # Linter alternatif
    "autopep8"         # Formateur de code
    "black"            # Formateur de code moderne
)

for package in "${packages[@]}"; do
    echo "📥 Installation de $package..."
    pip3 install "$package" --user --quiet
    
    if [ $? -eq 0 ]; then
        echo "✅ $package installé"
    else
        echo "⚠️ Erreur lors de l'installation de $package"
    fi
done

echo ""
echo "🔧 Vérification de l'installation de FreeCAD..."

# Vérifier l'installation de FreeCAD
if [ -d "/Applications/FreeCAD.app" ]; then
    echo "✅ FreeCAD trouvé dans /Applications/"
    
    # Vérifier les modules Python de FreeCAD
    freecad_python="/Applications/FreeCAD.app/Contents/Resources/bin/python"
    if [ -f "$freecad_python" ]; then
        echo "✅ Python FreeCAD trouvé"
        
        # Tester l'import des modules FreeCAD
        $freecad_python -c "import FreeCAD; print('FreeCAD version:', FreeCAD.Version())" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Modules FreeCAD fonctionnels"
        else
            echo "⚠️ Problème avec les modules FreeCAD"
        fi
    else
        echo "⚠️ Python FreeCAD non trouvé"
    fi
else
    echo "❌ FreeCAD non trouvé dans /Applications/"
    echo "💡 Veuillez installer FreeCAD depuis https://www.freecadweb.org/"
fi

echo ""
echo "📋 Configuration VS Code..."

# Créer le dossier .vscode s'il n'existe pas
mkdir -p .vscode

echo "✅ Configuration terminée !"
echo ""
echo "📝 Prochaines étapes :"
echo "1. Redémarrez VS Code"
echo "2. Ouvrez un fichier Python de votre workbench"
echo "3. Ajoutez cette ligne en haut : from freecad_imports import *"
echo "4. Profitez de l'autocomplétion ! 🎉"
echo ""
echo "💡 Conseils :"
echo "- Utilisez Ctrl+Space pour forcer l'autocomplétion"
echo "- Utilisez Cmd+Click pour aller à la définition"
echo "- Activez 'Python › Analysis: Type Checking Mode' à 'basic' dans les paramètres"
