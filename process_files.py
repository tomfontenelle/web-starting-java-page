#!/usr/bin/env python3
"""
Script pour convertir les fichiers HTML en format compatible WordPress Gutenberg
avec animations CSS pures (SEO-friendly)
"""

import re
import os

# Configuration des préfixes pour chaque métier
PREFIX_MAP = {
    'association': 'association',
    'Bar': 'bar',
    'bijouterie': 'bijouterie',
    'Boucher': 'boucher',
    'boulanger': 'boulanger',
    'Boutique-vetement': 'boutiquevetement',
    'camping': 'camping',
    'chambre-hote': 'chambrehote',
    'coach-sport': 'coachsport',
    'DJ': 'dj',
    'ecole-danse': 'ecoledanse',
    'fleuriste': 'fleuriste',
    'foodtruck': 'foodtruck',
    'fromagerie': 'fromagerie',
    'graphiste': 'graphiste',
    'hotel': 'hotel',
    'musiscien': 'musiscien',
    'patissier': 'patissier',
    'photographe': 'photographe',
    'Pizzeria': 'pizzeria',
    'Poissonnerie': 'poissonnerie',
    'Restaurant': 'restaurant',
    'theatre': 'theatre',
    'Traiteur': 'traiteur',
    'videaste': 'videaste'
}

# CSS @keyframes à ajouter
KEYFRAMES_CSS = """
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

def process_html_file(input_path, output_path, prefix):
    """Traite un fichier HTML pour le rendre compatible WordPress Gutenberg"""

    print(f"Traitement de {os.path.basename(input_path)}...")

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extraire juste le contenu (sans DOCTYPE, html, head, body tags)
    # Chercher le <style> et tout ce qui suit
    style_match = re.search(r'<style>', content, re.IGNORECASE)
    if style_match:
        content = content[style_match.start():]

    # 2. Extraire le CSS
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not css_match:
        print(f"  ⚠️ Pas de CSS trouvé dans {input_path}")
        return False

    css_content = css_match.group(1)

    # 3. Traiter le CSS
    # Trouver les @import
    imports = []
    for match in re.finditer(r"@import url\([^)]+\);", css_content):
        imports.append(match.group(0))

    # Supprimer les @import du CSS original
    css_content = re.sub(r"@import url\([^)]+\);\s*", "", css_content)

    # Construire le nouveau CSS avec les imports et les keyframes
    new_css = "\n".join(imports) + "\n" + KEYFRAMES_CSS + "\n" + css_content

    # Supprimer les lignes opacity: 0 et transform: translate dans les CLASSES (pas dans @keyframes)
    # On doit être prudent pour ne pas supprimer dans @keyframes
    lines = new_css.split('\n')
    new_lines = []
    in_keyframes = False

    for line in lines:
        # Détecter si on est dans un @keyframes
        if '@keyframes' in line:
            in_keyframes = True
        elif in_keyframes and line.strip() == '}':
            in_keyframes = False

        # Si on n'est PAS dans @keyframes, supprimer opacity: 0 et transform: translate
        if not in_keyframes:
            # Supprimer opacity: 0
            if re.search(r'opacity:\s*0\s*!important;', line):
                continue
            # Supprimer transform: translateY/translateX
            if re.search(r'transform:\s*translate[XY]\([^)]+\)\s*!important;', line):
                continue

        new_lines.append(line)

    new_css = '\n'.join(new_lines)

    # Supprimer les classes .animate
    new_css = re.sub(r'\.[a-z\-]+\.animate\s*\{[^}]*\}', '', new_css, flags=re.MULTILINE)

    # Ajouter animation aux éléments qui doivent être animés
    # Hero text
    new_css = re.sub(
        rf'(\.{prefix}-hero-text\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInUp 0.8s ease 0.5s both !important;\n  \2',
        new_css,
        flags=re.DOTALL
    )

    # Hero form
    new_css = re.sub(
        rf'(\.{prefix}-hero-form\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInUp 0.8s ease 0.8s both !important;\n  \2',
        new_css,
        flags=re.DOTALL
    )

    # Benefit cards avec animation
    new_css = re.sub(
        rf'(\.{prefix}-benefit-card\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInUp 0.8s ease both !important;\n  \2',
        new_css,
        flags=re.DOTALL
    )

    # Ajouter les animation-delay pour les benefit cards
    # Chercher où insérer les nth-child
    benefit_card_pattern = rf'\.{prefix}-benefit-card\s*\{{[^}}]+\}}'
    benefit_card_match = re.search(benefit_card_pattern, new_css, re.DOTALL)
    if benefit_card_match:
        insert_pos = benefit_card_match.end()
        nth_child_css = f"""
.{prefix}-benefit-card:nth-child(1) {{ animation-delay: 0.1s !important; }}
.{prefix}-benefit-card:nth-child(2) {{ animation-delay: 0.2s !important; }}
.{prefix}-benefit-card:nth-child(3) {{ animation-delay: 0.3s !important; }}
.{prefix}-benefit-card:nth-child(4) {{ animation-delay: 0.4s !important; }}
"""
        new_css = new_css[:insert_pos] + '\n' + nth_child_css + new_css[insert_pos:]

    # Features content
    new_css = re.sub(
        rf'(\.{prefix}-features-content\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInLeft 0.8s ease 0.3s both !important;\n  \2',
        new_css,
        flags=re.DOTALL
    )

    # Features visual
    new_css = re.sub(
        rf'(\.{prefix}-features-visual\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInRight 0.8s ease 0.5s both !important;\n  \2',
        new_css,
        flags=re.DOTALL
    )

    # Testimonial cards
    new_css = re.sub(
        rf'(\.{prefix}-testimonial-card\s*\{{[^}}]*?)(transition:[^;]+;)',
        r'\1animation: fadeInUp 0.8s ease both !important;\n  \2',
        new_css,
        flags=re.DOTALL
    )

    # 4. Remplacer le CSS dans le contenu
    content = re.sub(r'<style>.*?</style>', f'<style>\n{new_css}\n</style>', content, flags=re.DOTALL)

    # 5. Extraire et nettoyer le HTML
    html_match = re.search(r'</style>\s*(.*?)\s*<script>', content, re.DOTALL)
    if html_match:
        html_content = html_match.group(1).strip()
    else:
        print(f"  ⚠️ Pas de HTML trouvé dans {input_path}")
        return False

    # Supprimer les classes animate du HTML
    html_content = re.sub(r'\s+class="([^"]*?)animate([^"]*?)"', r' class="\1\2"', html_content)
    html_content = re.sub(r'\s+class="\s*"', '', html_content)  # Nettoyer les class vides

    # 6. Traiter le JavaScript - garder SEULEMENT EmailJS
    js_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if js_match:
        js_content = js_match.group(1)

        # Extraire uniquement le code EmailJS
        # Chercher emailjs.init jusqu'à la fin de la fonction
        emailjs_pattern = r'\(function\(\)\s*\{\s*emailjs\.init.*?\}\)\(\);'
        emailjs_match = re.search(emailjs_pattern, js_content, re.DOTALL)

        if emailjs_match:
            js_content = emailjs_match.group(0)
        else:
            # Fallback: créer le code EmailJS basique
            js_content = f"""(function() {{
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
      subject: 'Nouvelle demande - Site {prefix.title()} - web-starting.fr',
      message: `Nouvelle demande depuis web-starting.fr\\nNom: ${{name}}\\nEmail: ${{email}}\\nProjet: ${{project}}\\nPage: {prefix.title()}\\nDate: ${{new Date().toLocaleString('fr-FR')}}`
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
}})();"""
    else:
        js_content = ""

    # 7. Construire le fichier final
    final_content = f"""<!-- EmailJS Script -->
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>

<style>
{new_css}
</style>



{html_content}



<script>
{js_content}
</script>"""

    # 8. Sauvegarder
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"  ✅ {os.path.basename(output_path)} créé avec succès")
    return True


def main():
    """Traite tous les fichiers"""
    base_dir = '/home/user/web-starting-java-page'
    input_dir = os.path.join(base_dir, 'pages-originales')
    output_dir = os.path.join(base_dir, 'pages-traitees')

    success_count = 0
    error_count = 0

    for filename, prefix in PREFIX_MAP.items():
        input_path = os.path.join(input_dir, f'{filename}.html')
        output_path = os.path.join(output_dir, f'{filename}.html')

        if not os.path.exists(input_path):
            print(f"⚠️ Fichier introuvable: {input_path}")
            error_count += 1
            continue

        try:
            if process_html_file(input_path, output_path, prefix):
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            print(f"❌ Erreur lors du traitement de {filename}: {e}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"Traitement terminé :")
    print(f"  ✅ Succès: {success_count}/{len(PREFIX_MAP)}")
    print(f"  ❌ Erreurs: {error_count}/{len(PREFIX_MAP)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
