#!/usr/bin/env python3
"""Script pour ajouter les animations CSS aux fichiers qui en manquent"""

import re
import os

# Mapping des fichiers avec leurs bons préfixes
FILES_TO_FIX = {
    'bijouterie.html': 'bijoutier',
    'Boutique-vetement.html': 'boutique-vetements',
    'chambre-hote.html': 'chambre-hotes',
    'coach-sport.html': 'coach-sportif',
    'ecole-danse.html': 'ecole-danse',
    'foodtruck.html': 'food-truck',
    'fromagerie.html': 'fromager',
    'musiscien.html': 'musicien',
    'Poissonnerie.html': 'poissonnier'
}

def add_animations_to_file(filepath, prefix):
    """Ajoute les animations CSS manquantes à un fichier"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraire le CSS
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not css_match:
        return False

    css_content = css_match.group(1)

    # Ajouter animation aux hero-text
    css_content = re.sub(
        rf'(\.{re.escape(prefix)}-hero-text\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInUp 0.8s ease 0.5s both !important;\n  \2',
        css_content,
        flags=re.DOTALL
    )

    # Ajouter animation aux hero-form
    css_content = re.sub(
        rf'(\.{re.escape(prefix)}-hero-form\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInUp 0.8s ease 0.8s both !important;\n  \2',
        css_content,
        flags=re.DOTALL
    )

    # Ajouter animation aux benefit-card
    css_content = re.sub(
        rf'(\.{re.escape(prefix)}-benefit-card\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInUp 0.8s ease both !important;\n  \2',
        css_content,
        flags=re.DOTALL
    )

    # Ajouter les nth-child pour benefit-card
    benefit_card_pattern = rf'\.{re.escape(prefix)}-benefit-card\s*\{{[^}}]+\}}'
    benefit_card_match = re.search(benefit_card_pattern, css_content, re.DOTALL)

    if benefit_card_match:
        # Vérifier si les nth-child n'existent pas déjà
        if f'.{prefix}-benefit-card:nth-child(1)' not in css_content:
            insert_pos = benefit_card_match.end()
            nth_child_css = f"""
.{prefix}-benefit-card:nth-child(1) {{ animation-delay: 0.1s !important; }}
.{prefix}-benefit-card:nth-child(2) {{ animation-delay: 0.2s !important; }}
.{prefix}-benefit-card:nth-child(3) {{ animation-delay: 0.3s !important; }}
.{prefix}-benefit-card:nth-child(4) {{ animation-delay: 0.4s !important; }}
"""
            css_content = css_content[:insert_pos] + '\n' + nth_child_css + css_content[insert_pos:]

    # Ajouter animation aux features-content
    css_content = re.sub(
        rf'(\.{re.escape(prefix)}-features-content\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInLeft 0.8s ease 0.3s both !important;\n  \2',
        css_content,
        flags=re.DOTALL
    )

    # Ajouter animation aux features-visual
    css_content = re.sub(
        rf'(\.{re.escape(prefix)}-features-visual\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInRight 0.8s ease 0.5s both !important;\n  \2',
        css_content,
        flags=re.DOTALL
    )

    # Ajouter animation aux testimonial-card
    css_content = re.sub(
        rf'(\.{re.escape(prefix)}-testimonial-card\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInUp 0.8s ease both !important;\n  \2',
        css_content,
        flags=re.DOTALL
    )

    # Remplacer le CSS dans le contenu
    content = re.sub(r'<style>.*?</style>', f'<style>{css_content}</style>', content, flags=re.DOTALL)

    # Sauvegarder
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    """Corrige tous les fichiers"""
    base_dir = '/home/user/web-starting-java-page/pages-traitees'

    print("Ajout des animations CSS manquantes...")
    print("=" * 60)

    for filename, prefix in FILES_TO_FIX.items():
        filepath = os.path.join(base_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠️ {filename}: FICHIER INTROUVABLE")
            continue

        try:
            if add_animations_to_file(filepath, prefix):
                print(f"✅ {filename} (préfixe: {prefix})")
            else:
                print(f"❌ {filename}: Erreur")
        except Exception as e:
            print(f"❌ {filename}: {e}")

    print("=" * 60)
    print("Correction terminée !")


if __name__ == '__main__':
    main()
