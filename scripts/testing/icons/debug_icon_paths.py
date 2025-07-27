#!/usr/bin/env python3
"""
Debug des chemins d'icônes exactement comme les modules les construisent
"""
import os


def debug_module_icon_paths():
    print("🔍 Debug des chemins d'icônes depuis les modules...")

    # Simuler le chemin depuis airPlanePlane (4 niveaux)
    plane_module_file = "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign/App/modules/airPlanePlane/airPlanePlane.py"
    smWB_icons_path_plane = os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(plane_module_file)))
        ),
        "resources",
        "icons",
    )
    plane_icon = os.path.join(smWB_icons_path_plane, "plane.png")

    # Simuler le chemin depuis airPlaneWing (4 niveaux)
    wing_module_file = "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign/App/modules/airPlaneWing/airPlaneWing.py"
    smWB_icons_path_wing = os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(wing_module_file)))
        ),
        "resources",
        "icons",
    )
    wing2_icon = os.path.join(smWB_icons_path_wing, "wing2.png")

    # Simuler le chemin depuis airPlaneWPanel (4 niveaux)
    wpanel_module_file = "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign/App/modules/airPlaneWing/airPlaneWPanel.py"
    smWB_icons_path_wpanel = os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(wpanel_module_file)))
        ),
        "resources",
        "icons",
    )
    panel_icon = os.path.join(smWB_icons_path_wpanel, "panel.png")

    # Simuler le chemin depuis airPlaneNacelle (4 niveaux)
    nacelle_module_file = "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign/App/modules/airPlaneNacelle/airPlaneNacelle.py"
    apWB_resources_path = os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(nacelle_module_file)))
        ),
        "resources",
    )
    apWB_icons_path = os.path.join(apWB_resources_path, "icons")
    nacelle_icon = os.path.join(apWB_icons_path, "nacelle.png")

    print("\n📍 Chemins calculés depuis les modules :")
    print(f"Plane module: {plane_module_file}")
    print(f"  → smWB_icons_path: {smWB_icons_path_plane}")
    print(f"  → plane.png: {plane_icon}")
    print(f"  → Existe: {'✅' if os.path.exists(plane_icon) else '❌'}")

    print(f"\nWing module: {wing_module_file}")
    print(f"  → smWB_icons_path: {smWB_icons_path_wing}")
    print(f"  → wing2.png: {wing2_icon}")
    print(f"  → Existe: {'✅' if os.path.exists(wing2_icon) else '❌'}")

    print(f"\nWPanel module: {wpanel_module_file}")
    print(f"  → smWB_icons_path: {smWB_icons_path_wpanel}")
    print(f"  → panel.png: {panel_icon}")
    print(f"  → Existe: {'✅' if os.path.exists(panel_icon) else '❌'}")

    print(f"\nNacelle module: {nacelle_module_file}")
    print(f"  → apWB_resources_path: {apWB_resources_path}")
    print(f"  → apWB_icons_path: {apWB_icons_path}")
    print(f"  → nacelle.png: {nacelle_icon}")
    print(f"  → Existe: {'✅' if os.path.exists(nacelle_icon) else '❌'}")

    # Vérifier où FreeCAD cherche (erreur mentionnée)
    error_paths = [
        "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign/./App/resources/icons/plane.png",
        "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign/./App/resources/icons/wing2.png",
        "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign/./App/resources/icons/panel.png",
        "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign/./App/resources/icons/nacelle.png",
    ]

    print("\n🚨 Chemins d'erreur mentionnés par FreeCAD :")
    for error_path in error_paths:
        print(
            f"  {error_path} → Existe: {'✅' if os.path.exists(error_path) else '❌'}"
        )

    print("\n💡 Analyse :")
    print(
        "Si les chemins calculés sont corrects mais que FreeCAD cherche dans ./App/resources/,"
    )
    print(
        "cela suggère qu'il y a un problème dans la façon dont os.path.dirname(__file__) est évalué"
    )
    print("ou qu'il y a un cache/rechargement nécessaire.")


if __name__ == "__main__":
    debug_module_icon_paths()
