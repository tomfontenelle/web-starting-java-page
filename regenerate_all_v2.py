#!/usr/bin/env python3
"""
Script de régénération COMPLÈTE de tous les fichiers HTML - Version 2
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
    name = filename.replace('.html', '')
    # Gérer les cas spéciaux
    if 'immo' in name.lower():
        return 'agenceimmo'
    elif 'comptable' in name.lower():
        return 'expertcomptable'
    return name.lower().replace(' ', '').replace('-', '')

def extract_body_content(html):
    """Extrait uniquement le contenu entre <body> et </body>"""
    match = re.search(r'<body>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return html

def clean_css(css, prefix):
    """Nettoie le CSS en retirant opacity: 0, transform initiaux, et classes .animate"""
    lines = css.split('\n')
    cleaned_lines = []
    skip_block = False
    brace_count = 0

    for line in lines:
        # Ignorer les classes .animate
        if f'.{prefix}-' in line and '.animate' in line and '{' in line:
            skip_block = True
            brace_count = 1
            continue

        # Si on skip un bloc, compter les accolades
        if skip_block:
            brace_count += line.count('{')
            brace_count -= line.count('}')
            if brace_count <= 0:
                skip_block = False
            continue

        # Dans les classes normales, retirer opacity: 0 et transform initiaux
        if not '@keyframes' in line:
            if '  opacity: 0 !important;' in line:
                continue
            if '  transform: translateY(30px) !important;' in line:
                continue
            if '  transform: translateX(-30px) !important;' in line:
                continue
            if '  transform: translateX(30px) !important;' in line:
                continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def add_animations_to_css(css, prefix):
    """Ajoute les @keyframes et les animations aux classes ciblées"""

    # Ajouter les keyframes après les imports
    lines = css.split('\n')
    insert_index = 0
    for i, line in enumerate(lines):
        if 'Montserrat' in line:
            insert_index = i + 1
            break

    lines.insert(insert_index, KEYFRAMES_TEMPLATE)
    css = '\n'.join(lines)

    # Définir les animations pour chaque classe
    animations = [
        (f'.{prefix}-hero-text {{', 'animation: fadeInUp 0.8s ease 0.5s both !important;'),
        (f'.{prefix}-hero-form {{', 'animation: fadeInUp 0.8s ease 0.8s both !important;'),
        (f'.{prefix}-benefit-card {{', 'animation: fadeInUp 0.8s ease both !important;'),
        (f'.{prefix}-testimonial-card {{', 'animation: fadeInUp 0.8s ease both !important;'),
        (f'.{prefix}-features-content {{', 'animation: fadeInLeft 0.8s ease 0.3s both !important;'),
        (f'.{prefix}-features-visual {{', 'animation: fadeInRight 0.8s ease 0.5s both !important;'),
    ]

    # Ajouter les animations dans les classes
    for class_selector, animation_line in animations:
        # Trouver la classe et ajouter l'animation juste après l'accolade ouvrante
        pattern = re.compile(re.escape(class_selector) + r'\s*\n', re.MULTILINE)
        replacement = class_selector + '\n  ' + animation_line + '\n'
        css = pattern.sub(replacement, css)

    # Ajouter les nth-child delays pour benefit-card
    benefit_card_selector = f'.{prefix}-benefit-card {{'
    if benefit_card_selector in css:
        # Trouver la position après la fermeture de la classe benefit-card
        pos = css.find(benefit_card_selector)
        # Trouver la prochaine accolade fermante
        brace_count = 0
        insert_pos = pos
        for i in range(pos, len(css)):
            if css[i] == '{':
                brace_count += 1
            elif css[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    insert_pos = i + 1
                    break

        delay_rules = f"""
.{prefix}-benefit-card:nth-child(1) {{ animation-delay: 0.1s !important; }}
.{prefix}-benefit-card:nth-child(2) {{ animation-delay: 0.2s !important; }}
.{prefix}-benefit-card:nth-child(3) {{ animation-delay: 0.3s !important; }}
.{prefix}-benefit-card:nth-child(4) {{ animation-delay: 0.4s !important; }}
"""
        css = css[:insert_pos] + delay_rules + css[insert_pos:]

    return css

def create_simple_emailjs_script(prefix, page_name):
    """Crée un script JavaScript simple UNIQUEMENT pour EmailJS (30 lignes)"""
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
}})();
</script>"""
    return script

def update_onclick_buttons(html, prefix):
    """Met à jour les boutons onclick pour utiliser scrollIntoView simple"""
    # Remplacer les onclick existants
    html = re.sub(
        r'onclick="[^"]*ScrollToForm[^"]*"',
        f'onclick="document.querySelector(\'.{prefix}-hero-form\').scrollIntoView({{ behavior: \'smooth\', block: \'center\' }});"',
        html,
        flags=re.IGNORECASE
    )
    return html

def process_file(filename):
    """Traite un fichier HTML pour appliquer la nouvelle approche"""
    print(f"  Traitement: {filename}")

    original_path = os.path.join(PAGES_ORIGINALES, filename)
    output_path = os.path.join(PAGES_TRAITEES, filename)

    if not os.path.exists(original_path):
        print(f"    ERREUR: Fichier original non trouvé")
        return False

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

    # Extraire le HTML (sans le <style> et sans les scripts)
    html_part = re.sub(r'<style>.*?</style>', '', body_content, flags=re.DOTALL)
    html_part = re.sub(r'<script>.*?</script>', '', html_part, flags=re.DOTALL)

    # Nettoyer le CSS
    css = clean_css(css, prefix)
    css = add_animations_to_css(css, prefix)

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

    print(f"    ✓ Régénéré: {prefix}")
    return True

def main():
    """Fonction principale"""
    print("=" * 80)
    print("RÉGÉNÉRATION DE TOUS LES FICHIERS HTML - VERSION 2")
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
