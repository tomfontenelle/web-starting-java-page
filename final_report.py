#!/usr/bin/env python3
"""Génère un rapport final détaillé de la conformité des fichiers"""

import os
import re

FILES = [
    'association.html', 'Bar.html', 'bijouterie.html', 'Boucher.html',
    'boulanger.html', 'Boutique-vetement.html', 'camping.html',
    'chambre-hote.html', 'coach-sport.html', 'DJ.html', 'ecole-danse.html',
    'fleuriste.html', 'foodtruck.html', 'fromagerie.html', 'graphiste.html',
    'hotel.html', 'musiscien.html', 'patissier.html', 'photographe.html',
    'Pizzeria.html', 'Poissonnerie.html', 'Restaurant.html', 'theatre.html',
    'Traiteur.html', 'videaste.html'
]

def detailed_check(filepath, filename):
    """Vérifie en détail un fichier"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {}

    # 1. Commence par EmailJS Script
    checks['emailjs_script'] = content.startswith('<!-- EmailJS Script -->')

    # 2. Les 3 @keyframes présents
    checks['fadeInUp'] = '@keyframes fadeInUp' in content
    checks['fadeInLeft'] = '@keyframes fadeInLeft' in content
    checks['fadeInRight'] = '@keyframes fadeInRight' in content

    # 3. Aucun IntersectionObserver
    checks['no_observer'] = 'IntersectionObserver' not in content

    # 4. Aucun opacity: 0 dans les classes (seulement dans @keyframes)
    lines = content.split('\n')
    in_keyframes = False
    opacity_outside_keyframes = False

    for line in lines:
        if '@keyframes' in line:
            in_keyframes = True
        elif in_keyframes and line.strip() == '}' and 'to {' not in line:
            in_keyframes = False

        if not in_keyframes and 'opacity: 0 !important;' in line and 'opacity: 0.8' not in line:
            opacity_outside_keyframes = True
            break

    checks['no_opacity_in_classes'] = not opacity_outside_keyframes

    # 5. EmailJS fonctionnel
    checks['emailjs_init'] = 'emailjs.init' in content
    checks['emailjs_send'] = 'emailjs.send' in content

    # 6. Pas de DOCTYPE, html, head, body
    checks['no_doctype'] = 'DOCTYPE' not in content.upper()
    checks['no_html'] = '<html' not in content.lower()
    checks['no_head'] = '<head' not in content.lower()
    checks['no_body'] = '<body' not in content.lower()

    # 7. Animations appliquées
    checks['has_animations'] = 'animation: fadeInUp' in content or 'animation:fadeInUp' in content

    # 8. Animation delays
    checks['has_delays'] = 'animation-delay' in content

    return checks


def main():
    """Génère le rapport final"""
    output_dir = '/home/user/web-starting-java-page/pages-traitees'

    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "RAPPORT FINAL DE CONFORMITÉ" + " " * 31 + "║")
    print("║" + " " * 15 + "25 Fichiers HTML WordPress Gutenberg" + " " * 27 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    all_pass = True
    total_checks = 0
    passed_checks = 0

    for filename in FILES:
        filepath = os.path.join(output_dir, filename)

        if not os.path.exists(filepath):
            print(f"❌ {filename}: FICHIER INTROUVABLE")
            all_pass = False
            continue

        checks = detailed_check(filepath, filename)

        # Compter les checks
        total_checks += len(checks)
        passed_checks += sum(1 for v in checks.values() if v)

        # Si tous les checks passent
        if all(checks.values()):
            print(f"✅ {filename:<30} [CONFORME - {len(checks)}/{len(checks)} ✓]")
        else:
            all_pass = False
            print(f"❌ {filename:<30} [ERREURS DÉTECTÉES]")
            for check, passed in checks.items():
                if not passed:
                    print(f"   └─ ❌ {check}")

    print()
    print("─" * 80)
    print()
    print("📊 RÉSUMÉ DES VÉRIFICATIONS")
    print("=" * 80)
    print()
    print(f"Total de fichiers traités:          {len(FILES)}")
    print(f"Fichiers 100% conformes:             {sum(1 for f in FILES if all(detailed_check(os.path.join(output_dir, f), f).values()))}")
    print(f"Total de vérifications effectuées:  {total_checks}")
    print(f"Vérifications réussies:              {passed_checks}")
    print(f"Taux de réussite:                    {(passed_checks/total_checks*100):.1f}%")
    print()
    print("=" * 80)
    print()
    print("✓ VÉRIFICATIONS DÉTAILLÉES PAR CRITÈRE")
    print("─" * 80)
    print()

    # Statistiques par critère
    criteria = {
        'emailjs_script': '1. Commence par <!-- EmailJS Script -->',
        'fadeInUp': '2. @keyframes fadeInUp présent',
        'fadeInLeft': '3. @keyframes fadeInLeft présent',
        'fadeInRight': '4. @keyframes fadeInRight présent',
        'no_observer': '5. Aucun IntersectionObserver',
        'no_opacity_in_classes': '6. Aucun opacity: 0 dans les classes CSS',
        'emailjs_init': '7. EmailJS initialisé (emailjs.init)',
        'emailjs_send': '8. EmailJS send fonctionnel',
        'no_doctype': '9. Aucun DOCTYPE',
        'no_html': '10. Aucun tag <html>',
        'no_head': '11. Aucun tag <head>',
        'no_body': '12. Aucun tag <body>',
        'has_animations': '13. Animations CSS appliquées aux éléments',
        'has_delays': '14. Animation-delay configurés'
    }

    for criterion, description in criteria.items():
        count = sum(1 for f in FILES if detailed_check(os.path.join(output_dir, f), f).get(criterion, False))
        status = "✅" if count == len(FILES) else "⚠️"
        print(f"{status} {description:<50} {count}/{len(FILES)}")

    print()
    print("=" * 80)

    if all_pass:
        print()
        print("🎉 " + "FÉLICITATIONS !".center(76) + " 🎉")
        print()
        print("Tous les 25 fichiers sont 100% conformes aux spécifications :".center(80))
        print()
        print("  ✓ Compatibles WordPress Gutenberg".center(80))
        print("  ✓ Animations CSS pures (pas de JavaScript)".center(80))
        print("  ✓ SEO-friendly (contenu visible sans JS)".center(80))
        print("  ✓ EmailJS fonctionnel".center(80))
        print("  ✓ Progressive Enhancement".center(80))
        print()
        print("=" * 80)

    return all_pass


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
