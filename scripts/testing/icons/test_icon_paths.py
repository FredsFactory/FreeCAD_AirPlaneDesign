#!/usr/bin/env python3
"""
Test des chemins d'icônes après la réorganisation des modules
"""
import os


def test_icon_paths():
    print("🧪 Test des chemins d'icônes...")

    base_path = (
        "/Users/frederic.nivoix/Library/Application Support/FreeCAD/Mod/AirPlaneDesign"
    )

    # Test des chemins depuis les modules
    module_plane_path = os.path.join(base_path, "App", "modules", "airPlanePlane")
    icons_path_from_plane = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(module_plane_path))),
        "resources",
        "icons",
    )
    plane_icon = os.path.join(icons_path_from_plane, "plane.png")

    module_wing_path = os.path.join(base_path, "App", "modules", "airPlaneWing")
    icons_path_from_wing = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(module_wing_path))),
        "resources",
        "icons",
    )
    wing_icon = os.path.join(icons_path_from_wing, "wing2.png")
    panel_icon = os.path.join(icons_path_from_wing, "panel.png")

    module_nacelle_path = os.path.join(base_path, "App", "modules", "airPlaneNacelle")
    icons_path_from_nacelle = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(module_nacelle_path))),
        "resources",
        "icons",
    )
    nacelle_icon = os.path.join(icons_path_from_nacelle, "nacelle.png")

    # Test des icônes de rechargement
    reload_icon = os.path.join(base_path, "resources", "icons", "reload.svg")
    auto_reload_icon = os.path.join(base_path, "resources", "icons", "auto_reload.svg")

    icons_to_test = [
        ("plane.png", plane_icon),
        ("wing2.png", wing_icon),
        ("panel.png", panel_icon),
        ("nacelle.png", nacelle_icon),
        ("reload.svg", reload_icon),
        ("auto_reload.svg", auto_reload_icon),
    ]

    all_found = True
    for name, path in icons_to_test:
        if os.path.exists(path):
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} (NON TROUVÉ)")
            all_found = False

    if all_found:
        print("🎉 Toutes les icônes sont accessibles avec les nouveaux chemins!")
    else:
        print("⚠️ Certaines icônes ne sont pas trouvées.")

    return all_found


if __name__ == "__main__":
    test_icon_paths()
