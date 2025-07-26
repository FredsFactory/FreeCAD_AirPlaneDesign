# Recharge automatique du workbench AirPlaneDesign
# Ce module permet de recharger le workbench sans redémarrer FreeCAD

import FreeCAD as App
import FreeCADGui as Gui
import importlib
import sys
import os

def reload_workbench():
    """
    Recharge complètement le workbench AirPlaneDesign
    """
    print("🔄 Début du rechargement du workbench AirPlaneDesign...")
    
    # Liste des modules du workbench à recharger
    workbench_modules = [
        'airPlanePanel',
        'airPlaneRib', 
        'airPlanePlane',
        'airPlaneWPanel',
        'airPlaneWing',
        'airPlaneWingWizard',
        'airPlaneNacelle',
        'airPlaneAirFoil',
        'airPlaneAirFoilNaca',
        'airPlaneDesignProfilUI',
        'airPlaneSWPanel',
        'airPlaneWingUI',
        'libAeroShapes',
        'path_locator',
        'demo_reload',  # Module de démonstration
        'reload_commands',  # Commandes de rechargement
        'keyboard_shortcuts'  # Raccourcis clavier
    ]
    
    try:
        # 1. Recharger tous les modules Python du workbench
        print("📦 Rechargement des modules Python...")
        for module_name in workbench_modules:
            if module_name in sys.modules:
                print(f"  ↻ {module_name}")
                importlib.reload(sys.modules[module_name])
            else:
                print(f"  ⚠️ Module {module_name} non trouvé dans sys.modules")
        
        # 2. Recharger le module principal InitGui
        if 'InitGui' in sys.modules:
            print("  ↻ InitGui")
            importlib.reload(sys.modules['InitGui'])
        
        # 3. Réactiver le workbench
        print("🔧 Réactivation du workbench...")
        current_wb = Gui.activeWorkbench()
        if hasattr(current_wb, '__class__') and 'AirPlaneDesign' in current_wb.__class__.__name__:
            # Si on est déjà dans le workbench, on le désactive puis réactive
            Gui.activateWorkbench("StartWorkbench")  # Workbench temporaire
            Gui.activateWorkbench("AirPlaneDesignWorkbench")
        
        print("✅ Workbench rechargé avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du rechargement : {e}")
        import traceback
        traceback.print_exc()
        return False

def reload_current_file():
    """
    Recharge le fichier Python actuellement ouvert dans l'éditeur FreeCAD
    """
    try:
        # Cette fonction est utile si vous travaillez sur un fichier spécifique
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            filename = frame.f_back.f_code.co_filename
            module_name = os.path.splitext(os.path.basename(filename))[0]
            
            if module_name in sys.modules:
                print(f"🔄 Rechargement de {module_name}...")
                importlib.reload(sys.modules[module_name])
                print(f"✅ {module_name} rechargé !")
                return True
        
        print("⚠️ Impossible de déterminer le module à recharger")
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors du rechargement : {e}")
        return False

def setup_auto_reload():
    """
    Configure le rechargement automatique basé sur les modifications de fichiers
    """
    try:
        import threading
        import time
        from pathlib import Path
        
        # Chemin du workbench
        wb_path = Path(__file__).parent
        
        # Dictionnaire pour stocker les timestamps des fichiers
        file_timestamps = {}
        
        def check_file_changes():
            """Vérifie les modifications de fichiers"""
            while True:
                try:
                    for py_file in wb_path.glob("*.py"):
                        current_time = py_file.stat().st_mtime
                        
                        if str(py_file) in file_timestamps:
                            if current_time > file_timestamps[str(py_file)]:
                                print(f"📝 Modification détectée : {py_file.name}")
                                file_timestamps[str(py_file)] = current_time
                                
                                # Attendre un peu pour éviter les rechargements multiples
                                time.sleep(1)
                                reload_workbench()
                        else:
                            file_timestamps[str(py_file)] = current_time
                    
                    time.sleep(2)  # Vérifier toutes les 2 secondes
                    
                except Exception as e:
                    print(f"⚠️ Erreur dans la surveillance des fichiers : {e}")
                    time.sleep(5)
        
        # Démarrer la surveillance en arrière-plan
        thread = threading.Thread(target=check_file_changes, daemon=True)
        thread.start()
        print("👁️ Surveillance automatique des fichiers activée")
        
    except Exception as e:
        print(f"⚠️ Impossible d'activer la surveillance automatique : {e}")

# Fonctions de commodité pour la console FreeCAD
def reload():
    """Raccourci pour recharger le workbench"""
    return reload_workbench()

def rl():
    """Raccourci ultra-court pour recharger"""
    return reload_workbench()

# Message d'information
print("🔄 Module de rechargement chargé !")
print("💡 Utilisez les commandes suivantes :")
print("   reload_workbench() - Recharge tout le workbench")
print("   reload() - Raccourci pour reload_workbench()")
print("   rl() - Raccourci très court")
print("   setup_auto_reload() - Active la surveillance automatique")
