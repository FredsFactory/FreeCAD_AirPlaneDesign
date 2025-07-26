"""
Générateur d'icônes simples pour les commandes de rechargement
"""

def create_reload_icon():
    """Crée une icône SVG simple pour le rechargement"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="#2196F3" stroke-width="2">
    <!-- Flèche circulaire -->
    <path d="M 8 16 A 8 8 0 1 1 24 16 A 8 8 0 0 1 16 24" stroke-linecap="round"/>
    <!-- Pointe de flèche -->
    <path d="M 20 20 L 24 16 L 20 12" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <!-- Cercle central -->
  <circle cx="16" cy="16" r="2" fill="#2196F3"/>
</svg>'''
    return svg_content

def create_auto_reload_icon():
    """Crée une icône SVG pour l'auto-rechargement"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="#4CAF50" stroke-width="2">
    <!-- Double flèche circulaire -->
    <path d="M 6 16 A 10 10 0 1 1 26 16" stroke-linecap="round"/>
    <path d="M 26 16 A 10 10 0 1 1 6 16" stroke-linecap="round"/>
    <!-- Pointes de flèches -->
    <path d="M 22 12 L 26 16 L 22 20" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 10 20 L 6 16 L 10 12" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <!-- Point central automatique -->
  <circle cx="16" cy="16" r="1.5" fill="#4CAF50"/>
  <text x="16" y="8" text-anchor="middle" font-family="Arial" font-size="6" fill="#4CAF50">AUTO</text>
</svg>'''
    return svg_content

# Créer les fichiers d'icônes
import os

icons_dir = os.path.join(os.path.dirname(__file__), 'resources', 'icons')

# Créer le fichier reload.svg
reload_svg_path = os.path.join(icons_dir, 'reload.svg')
with open(reload_svg_path, 'w', encoding='utf-8') as f:
    f.write(create_reload_icon())

# Créer le fichier auto_reload.svg  
auto_reload_svg_path = os.path.join(icons_dir, 'auto_reload.svg')
with open(auto_reload_svg_path, 'w', encoding='utf-8') as f:
    f.write(create_auto_reload_icon())

print(f"✅ Icônes créées :")
print(f"   - {reload_svg_path}")
print(f"   - {auto_reload_svg_path}")
