#!/bin/bash

# Script de migration automatique des imports FreeCAD
# Corrige tous les problèmes d'import "Module non trouvable" dans VS Code

echo "🔧 Migration automatique des imports FreeCAD"
echo "============================================="

# Compteurs
total_files=0
modified_files=0
backup_dir="./backup_$(date +%Y%m%d_%H%M%S)"

# Créer le dossier de sauvegarde
mkdir -p "$backup_dir"
echo "📁 Sauvegardes dans : $backup_dir"

# Traiter tous les fichiers .py
for file in *.py; do
    if [[ -f "$file" ]]; then
        total_files=$((total_files + 1))
        
        # Vérifier si le fichier contient des imports FreeCAD problématiques
        if grep -q "import FreeCAD\|import FreeCADGui\|from FreeCAD import" "$file"; then
            echo ""
            echo "🔄 Traitement de $file..."
            
            # Créer une sauvegarde
            cp "$file" "$backup_dir/$file"
            echo "   💾 Sauvegarde créée"
            
            # Créer un fichier temporaire pour les modifications
            temp_file=$(mktemp)
            
            # Traitement ligne par ligne avec préservation du contexte
            while IFS= read -r line; do
                # Remplacements spécifiques
                case "$line" in
                    "import FreeCAD as App")
                        echo "from freecad_imports import App"
                        ;;
                    "import FreeCAD")
                        echo "from freecad_imports import App as FreeCAD"
                        ;;
                    "import FreeCADGui as Gui")
                        echo "from freecad_imports import Gui"
                        ;;
                    "import FreeCADGui")
                        echo "from freecad_imports import Gui as FreeCADGui"
                        ;;
                    "from FreeCAD import Vector")
                        echo "from freecad_imports import Vector"
                        ;;
                    "from FreeCAD import Vector, Placement, Rotation"*)
                        echo "from freecad_imports import Vector, Placement, Rotation"
                        ;;
                    *"import FreeCAD"*|*"import FreeCADGui"*|*"from FreeCAD import"*)
                        # Pour les lignes plus complexes, essayer des remplacements simples
                        modified_line="$line"
                        modified_line=$(echo "$modified_line" | sed 's/import FreeCAD as App/from freecad_imports import App/g')
                        modified_line=$(echo "$modified_line" | sed 's/import FreeCAD,/from freecad_imports import App as FreeCAD,/g')
                        modified_line=$(echo "$modified_line" | sed 's/import FreeCADGui,/from freecad_imports import Gui as FreeCADGui,/g')
                        echo "$modified_line"
                        ;;
                    *)
                        # Ligne normale, garder telle quelle
                        echo "$line"
                        ;;
                esac
            done < "$file" > "$temp_file"
            
            # Remplacer le fichier original
            mv "$temp_file" "$file"
            
            modified_files=$((modified_files + 1))
            echo "   ✅ $file migré avec succès"
            
            # Afficher un aperçu des changements
            echo "   📋 Changements appliqués :"
            grep -n "from freecad_imports import" "$file" | head -3 | sed 's/^/      /'
            
        else
            echo "⏭️  $file - Aucun import FreeCAD trouvé"
        fi
    fi
done

echo ""
echo "📊 Résumé de la migration :"
echo "   Fichiers analysés : $total_files"
echo "   Fichiers modifiés : $modified_files"
echo "   Sauvegardes dans  : $backup_dir"

if [[ $modified_files -gt 0 ]]; then
    echo ""
    echo "🧪 Test des fichiers migrés..."
    
    # Tester quelques fichiers pour vérifier qu'ils se chargent
    test_files=("demo_reload.py" "airPlaneRib.py" "airPlaneWPanel.py")
    
    for test_file in "${test_files[@]}"; do
        if [[ -f "$test_file" ]]; then
            echo "   🔍 Test de $test_file..."
            if python3 -c "import sys; sys.path.insert(0, '.'); import $(basename $test_file .py)" 2>/dev/null; then
                echo "   ✅ $test_file - Import réussi"
            else
                echo "   ⚠️  $test_file - À vérifier manuellement"
            fi
        fi
    done
    
    echo ""
    echo "🎉 Migration terminée avec succès !"
    echo ""
    echo "📋 Prochaines étapes :"
    echo "1. Redémarrez VS Code"
    echo "2. Vérifiez qu'il n'y a plus d'erreurs rouges"
    echo "3. Testez l'autocomplétion avec Ctrl+Space"
    echo "4. Si problème, restaurez depuis $backup_dir"
    
else
    echo ""
    echo "ℹ️  Aucun fichier n'avait besoin de migration"
fi

echo ""
echo "💡 Conseil : Testez maintenant l'autocomplétion en tapant 'App.' dans VS Code !"
