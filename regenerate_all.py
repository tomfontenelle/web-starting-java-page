#!/usr/bin/env python3
"""
Script de régénération COMPLÈTE de tous les fichiers HTML
Applique l'approche EXACTE avec :
- EmailJS CDN en haut
- CSS avec @keyframes automatiques
- PAS d'opacity: 0 initial dans les classes CSS
- PAS d'IntersectionObserver JavaScript
- JavaScript uniquement pour EmailJS (30 lignes)
- Scroll to form simple avec onclick
"""

import os
import re
from pathlib import Path

# Chemins
PAGES_ORIGINALES = "/home/user/web-starting-java-page/pages-originales"
PAGES_TRAITEES = "/home/user/web-starting-java-page/pages-traitees"

# Template @keyframes
KEYFRAMES_TEMPLATE = """
/* ANIMATIONS AUTOMATIQUES */
@keyframes fadeInUp {
  from {
    opacity: 0 !important;
    transform: translateY(30px) !important;
  }
  to {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0 !important;
    transform: translateX(-30px) !important;
  }
  to {
    opacity: 1 !important;
    transform: translateX(0) !important;
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0 !important;
    transform: translateX(30px) !important;
  }
  to {
    opacity: 1 !important;
    transform: translateX(0) !important;
  }
}
"""

def extract_prefix(filename):
    """Extrait le préfixe CSS d'un fichier (ex: 'Electricien.html' -> 'electricien')"""
    return filename.replace('.html', '').lower()

def extract_body_content(html):
    """Extrait uniquement le contenu entre <body> et </body>"""
    match = re.search(r'<body>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return html

def remove_opacity_from_css(css, prefix):
    """Retire tous les 'opacity: 0' des classes CSS (sauf dans @keyframes)"""
    # Retirer les lignes avec opacity: 0 et transform: translate dans les classes
    pattern = rf'\.{prefix}-[a-z-]+\s*{{[^}}]*opacity:\s*0[^}}]*}}'

    # On va plutôt faire une approche simple : retirer opacity: 0 et transform de toutes les classes
    # sauf si elles sont dans @keyframes
    lines = css.split('\n')
    new_lines = []
    in_keyframes = False
    skip_next_opacity = False

    for i, line in enumerate(lines):
        if '@keyframes' in line:
            in_keyframes = True
            new_lines.append(line)
            continue

        if in_keyframes and '}' in line:
            # Check si c'est la fin des keyframes
            if line.strip() == '}' and i > 0 and not '{' in line:
                in_keyframes = False
            new_lines.append(line)
            continue

        # Si on est dans une classe normale (pas keyframes)
        if not in_keyframes:
            # Retirer opacity: 0 et les transform: translateY/X initiales
            if 'opacity: 0 !important;' in line:
                continue
            if 'transform: translateY(30px) !important;' in line:
                continue
            if 'transform: translateX(-30px) !important;' in line:
                continue
            if 'transform: translateX(30px) !important;' in line:
                continue
            # Retirer aussi les classes .animate
            if f'.{prefix}-' in line and '.animate' in line:
                continue

        new_lines.append(line)

    return '\n'.join(new_lines)

def add_keyframes_animations(css, prefix):
    """Ajoute les animations automatiques avec @keyframes"""
    # Ajouter les keyframes juste après les imports
    import_end = css.find('@import url(\'https://fonts.googleapis.com/css2?family=Montserrat')
    if import_end == -1:
        # Essayer de trouver la fin des imports
        import_end = css.find('/* RESET COMPLET')

    if import_end != -1:
        # Trouver la fin de la ligne
        next_newline = css.find('\n', import_end)
        if next_newline != -1:
            next_newline = css.find('\n', next_newline + 1)  # Deuxième ligne
            css = css[:next_newline] + KEYFRAMES_TEMPLATE + css[next_newline:]

    # Ajouter les animations aux classes ciblées
    animations_map = {
        f'.{prefix}-hero-text': 'animation: fadeInUp 0.8s ease 0.5s both !important;',
        f'.{prefix}-hero-form': 'animation: fadeInUp 0.8s ease 0.8s both !important;',
        f'.{prefix}-benefit-card': 'animation: fadeInUp 0.8s ease both !important;',
        f'.{prefix}-testimonial-card': 'animation: fadeInUp 0.8s ease both !important;',
        f'.{prefix}-features-content': 'animation: fadeInLeft 0.8s ease 0.3s both !important;',
        f'.{prefix}-features-visual': 'animation: fadeInRight 0.8s ease 0.5s both !important;',
    }

    # Ajouter les animations après chaque classe
    for class_name, animation in animations_map.items():
        # Trouver la classe et ajouter l'animation
        pattern = rf'({re.escape(class_name)}\s*{{[^}}]*)'
        replacement = rf'\1\n  {animation}\n'
        css = re.sub(pattern, replacement, css)

    # Ajouter des delays progressifs pour les cartes
    benefit_card_pattern = rf'\.{prefix}-benefit-card\s*{{'
    match = re.search(benefit_card_pattern, css)
    if match:
        insert_pos = css.find('}', match.end()) + 1
        delay_css = f"""
.{prefix}-benefit-card:nth-child(1) {{ animation-delay: 0.1s !important; }}
.{prefix}-benefit-card:nth-child(2) {{ animation-delay: 0.2s !important; }}
.{prefix}-benefit-card:nth-child(3) {{ animation-delay: 0.3s !important; }}
.{prefix}-benefit-card:nth-child(4) {{ animation-delay: 0.4s !important; }}
"""
        css = css[:insert_pos] + delay_css + css[insert_pos:]

    return css

def create_simple_emailjs_script(prefix, page_name):
    """Crée un script JavaScript simple UNIQUEMENT pour EmailJS"""
    script = f"""<script>
(function() {{
  emailjs.init('EbZUccJ9uKukb5WRE');

  const form = document.getElementById('{prefix}-contact-form');
  const button = form.querySelector('.{prefix}-cta-button');

  form.addEventListener('submit', function(e) {{
    e.preventDefault();

    const name = document.getElementById('{prefix}-name').value;
    const email = document.getElementById('{prefix}-email').value;
    const project = document.getElementById('{prefix}-project').value;

    if (!name || !email || !project) {{
      alert('Veuillez remplir tous les champs.');
      return;
    }}

    button.innerHTML = '⏳ Envoi en cours...';
    button.disabled = true;

    emailjs.send('service_btbtgzn', 'template_m06wtf1', {{
      from_name: name,
      from_email: email,
      project_description: project,
      to_email: 'contact.capitainepub@gmail.com',
      subject: 'Nouvelle demande - Site {page_name} - web-starting.fr',
      message: `Nouvelle demande depuis web-starting.fr\\nNom: ${{name}}\\nEmail: ${{email}}\\nProjet: ${{project}}\\nPage: {page_name}\\nDate: ${{new Date().toLocaleString('fr-FR')}}`
    }}, 'EbZUccJ9uKukb5WRE')
    .then(function() {{
      button.innerHTML = '✅ Demande envoyée !';
      button.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
      setTimeout(() => {{
        button.innerHTML = 'RÉSERVEZ VOTRE RENDEZ-VOUS GRATUIT';
        button.style.background = 'linear-gradient(135deg, #e8ff45 0%, #d4f442 100%)';
        button.disabled = false;
        form.reset();
      }}, 3000);
    }})
    .catch(function() {{
      button.innerHTML = '❌ Erreur';
      button.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
      setTimeout(() => {{
        button.innerHTML = 'RÉSERVEZ VOTRE RENDEZ-VOUS GRATUIT';
        button.style.background = 'linear-gradient(135deg, #e8ff45 0%, #d4f442 100%)';
        button.disabled = false;
      }}, 3000);
    }});
  }});

  // Fonction scroll to form
  window.{prefix}ScrollToForm = function() {{
    document.querySelector('.{prefix}-hero-form').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
  }};
}})();
</script>"""
    return script

def update_onclick_buttons(html, prefix):
    """Met à jour les boutons onclick pour utiliser la fonction simple"""
    html = re.sub(
        r'onclick="[^"]*"',
        f'onclick="document.querySelector(\'.{prefix}-hero-form\').scrollIntoView({{ behavior: \'smooth\', block: \'center\' }});"',
        html
    )
    return html

def process_file(filename):
    """Traite un fichier HTML pour appliquer la nouvelle approche"""
    print(f"  Traitement: {filename}")

    original_path = os.path.join(PAGES_ORIGINALES, filename)
    output_path = os.path.join(PAGES_TRAITEES, filename)

    # Lire le fichier original
    with open(original_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraire le préfixe
    prefix = extract_prefix(filename)
    page_name = filename.replace('.html', '')

    # Extraire le contenu du body
    body_content = extract_body_content(content)

    # Extraire le CSS
    css_match = re.search(r'<style>(.*?)</style>', body_content, re.DOTALL)
    if not css_match:
        print(f"    ERREUR: Pas de CSS trouvé dans {filename}")
        return False

    css = css_match.group(1)

    # Extraire le HTML (sans le <style> et </style>)
    html_part = re.sub(r'<style>.*?</style>', '', body_content, flags=re.DOTALL)
    # Retirer aussi l'ancien script
    html_part = re.sub(r'<script>.*?</script>', '', html_part, flags=re.DOTALL)

    # Transformer le CSS
    css = remove_opacity_from_css(css, prefix)
    css = add_keyframes_animations(css, prefix)

    # Mettre à jour les onclick dans le HTML
    html_part = update_onclick_buttons(html_part, prefix)

    # Créer le nouveau script
    new_script = create_simple_emailjs_script(prefix, page_name)

    # Construire le fichier final
    final_content = f"""<!-- EmailJS Script -->
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>

<style>
{css}
</style>

{html_part}

{new_script}"""

    # Écrire le fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    return True

def main():
    """Fonction principale"""
    print("=" * 80)
    print("RÉGÉNÉRATION DE TOUS LES FICHIERS HTML")
    print("=" * 80)
    print()

    # Lister tous les fichiers
    files = sorted([f for f in os.listdir(PAGES_ORIGINALES) if f.endswith('.html')])

    print(f"Fichiers à traiter: {len(files)}")
    print()

    success_count = 0
    for i, filename in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {filename}")
        if process_file(filename):
            success_count += 1
        print()

    print("=" * 80)
    print(f"RÉSULTAT: {success_count}/{len(files)} fichiers régénérés avec succès")
    print("=" * 80)

if __name__ == '__main__':
    main()
