/Applications/FreeCAD.app/Contents/Resources/bin/python -v

# install debugpy

/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install debugpy

# configure VSCODE launcher

{
// Debug config for Freecad with VS Code
"version": "0.2.0",
"configurations": [

        {
            "name": "Attach to FreeCAD",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/Users/XXXXXXX/Library/Application Support/FreeCAD/Mod/AirPlaneDesign"
                }
            ],
            "justMyCode": false,
            "subProcess": true
        },
        {
            "name": "Python: Attach using Process ID",
            "type": "debugpy",
            "request": "attach",
            "processId": "${command:pickProcess}",
            "justMyCode": false
        }
    ]

}

# in initGUI.py add

def setup_debug():
"""Configuration du débogueur VS Code pour FreeCAD"""
try:
import debugpy

        # Port pour le débogage
        debug_port = 5678

        # Vérifier si debugpy est déjà en écoute
        if not debugpy.is_client_connected():
            # Configurer debugpy
            debugpy.configure(python="python")

            # Démarrer le serveur de débogage
            debugpy.listen(("localhost", debug_port))

            print(f"🔧 Debug server started on port {debug_port}")
            print("📋 Instructions to connect:")
            print("   1. In VS Code, open the Command Palette (Cmd+Shift+P)")
            print(
                "   2. Type 'Python: Attach using Process ID' or use the launch.json configuration"
            )
            print("   3. Or use 'Python: Attach to Local Process' and select FreeCAD")
            print("⏳ Waiting for debugger to connect...")

            # Optionnel : attendre la connexion (décommentez si nécessaire)
            # debugpy.wait_for_client()
            # print("✅ Débogueur VS Code connecté à FreeCAD")
        else:
            print("✅ Débogueur déjà connecté")

    except ImportError:
        print("⚠️ debugpy n'est pas installé. Installez-le avec : pip install debugpy")
        print("⚠️ debugpy is not installed. Install it with: pip install debugpy")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation du débogueur : {e}")

# Start Debug

setup_debug()

# luanch Freecad in a console and attach the debugger in VSCODE
/Applications/FreeCAD.app/Contents/MacOS/FreeCAD


# install stubs

/Applications/FreeCAD.app/Contents/Resources/bin/python -m pip install FreeCAD-stubs
