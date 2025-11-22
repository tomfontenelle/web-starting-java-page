#!/usr/bin/env python3
"""Script de vérification de conformité des fichiers traités"""

import os
import re

def verify_file(filepath, filename):
    """Vérifie qu'un fichier est conforme aux exigences"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    warnings = []
    
    # 1. Vérifier que le fichier commence par le script EmailJS
    if not content.startswith('<!-- EmailJS Script -->'):
        errors.append("❌ Ne commence pas par <!-- EmailJS Script -->")
    
    # 2. Vérifier présence des 3 @keyframes
    if '@keyframes fadeInUp' not in content:
        errors.append("❌ @keyframes fadeInUp manquant")
    if '@keyframes fadeInLeft' not in content:
        errors.append("❌ @keyframes fadeInLeft manquant")
    if '@keyframes fadeInRight' not in content:
        errors.append("❌ @keyframes fadeInRight manquant")
    
    # 3. Vérifier absence de IntersectionObserver
    if 'IntersectionObserver' in content:
        errors.append("❌ IntersectionObserver présent dans le code")
    
    # 4. Vérifier présence de emailjs
    if 'emailjs.init' not in content:
        errors.append("❌ emailjs.init manquant")
    
    # 5. Vérifier absence de DOCTYPE, html, head, body
    if '<!DOCTYPE' in content or '<!doctype' in content.lower():
        errors.append("❌ DOCTYPE présent")
    if '<html' in content.lower():
        errors.append("❌ Tag <html> présent")
    if '<head' in content.lower():
        errors.append("❌ Tag <head> présent")
    if '<body' in content.lower():
        errors.append("❌ Tag <body> présent")
    
    # 6. Vérifier que opacity: 0 n'est QUE dans @keyframes
    lines = content.split('\n')
    in_keyframes = False
    for i, line in enumerate(lines, 1):
        if '@keyframes' in line:
            in_keyframes = True
        elif in_keyframes and line.strip() == '}':
            # Chercher la fin du keyframe (après le dernier })
            if i < len(lines) and '}' not in lines[i]:
                in_keyframes = False
        
        # Si opacity: 0 en dehors des keyframes
        if not in_keyframes and 'opacity: 0 !important;' in line and 'opacity: 0.8' not in line:
            warnings.append(f"⚠️ opacity: 0 trouvé en dehors de @keyframes à la ligne {i}")
    
    # 7. Vérifier présence des animations
    if 'animation: fadeInUp' not in content and 'animation:fadeInUp' not in content:
        warnings.append("⚠️ Aucune animation fadeInUp appliquée aux éléments")
    
    # 8. Vérifier animation-delay
    if 'animation-delay:' not in content and 'animation-delay :' not in content:
        warnings.append("⚠️ Aucun animation-delay trouvé")
    
    return errors, warnings


def main():
    """Vérifie tous les fichiers"""
    output_dir = '/home/user/web-starting-java-page/pages-traitees'
    
    files = [
        'association.html', 'Bar.html', 'bijouterie.html', 'Boucher.html',
        'boulanger.html', 'Boutique-vetement.html', 'camping.html',
        'chambre-hote.html', 'coach-sport.html', 'DJ.html', 'ecole-danse.html',
        'fleuriste.html', 'foodtruck.html', 'fromagerie.html', 'graphiste.html',
        'hotel.html', 'musiscien.html', 'patissier.html', 'photographe.html',
        'Pizzeria.html', 'Poissonnerie.html', 'Restaurant.html', 'theatre.html',
        'Traiteur.html', 'videaste.html'
    ]
    
    total_errors = 0
    total_warnings = 0
    
    print("=" * 80)
    print("VÉRIFICATION DE CONFORMITÉ DES 25 FICHIERS TRAITÉS")
    print("=" * 80)
    print()
    
    for filename in files:
        filepath = os.path.join(output_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ {filename}: FICHIER INTROUVABLE")
            total_errors += 1
            continue
        
        errors, warnings = verify_file(filepath, filename)
        
        if not errors and not warnings:
            print(f"✅ {filename}: CONFORME")
        else:
            print(f"\n📄 {filename}:")
            for error in errors:
                print(f"   {error}")
                total_errors += 1
            for warning in warnings:
                print(f"   {warning}")
                total_warnings += 1
    
    print()
    print("=" * 80)
    print(f"RÉSULTAT FINAL:")
    print(f"  Fichiers vérifiés: {len(files)}")
    print(f"  ✅ Conformes: {len(files) - (total_errors > 0)}")
    print(f"  ❌ Erreurs totales: {total_errors}")
    print(f"  ⚠️ Avertissements: {total_warnings}")
    print("=" * 80)


if __name__ == '__main__':
    main()
