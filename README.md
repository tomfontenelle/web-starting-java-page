# 🚀 Processus d'Optimisation SEO pour WordPress Gutenberg

## 📁 Structure

```
pages-originales/    → Vos pages HTML originales (avec JavaScript)
pages-traitees/      → Pages optimisées pour Gutenberg (sans DOCTYPE)
scripts/             → Script EmailJS minimal réutilisable
```

## ⚡ Transformations appliquées

### ✅ Retraits automatiques :
- `<!DOCTYPE html>`
- `<html>` et `</html>`
- `<head>` complet (styles externes déplacés inline)
- `<body>` et `</body>`
- JavaScript d'animations → remplacé par CSS pur

### ✅ Conservé et optimisé :
- Contenu HTML sémantique
- Styles CSS (inline ou dans `<style>`)
- Structure du formulaire
- **JavaScript EmailJS minimal (~30 lignes)**

### ✅ Résultat pour Gutenberg :
- Code prêt à coller dans un bloc HTML Gutenberg
- Contenu immédiatement visible pour Google Bot
- Formulaire 100% fonctionnel avec EmailJS
- Animations CSS automatiques

## 📝 Instructions

1. **Déposez vos pages HTML** dans `pages-originales/`
2. **Indiquez les noms** des fichiers à traiter
3. **Les versions optimisées** seront dans `pages-traitees/`

## 🎨 Exemple de transformation

**Avant (pages-originales/)** :
```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <title>Ma Page</title>
  <script src="animations.js"></script>
</head>
<body>
  <div class="content">...</div>
  <script>
    // 200 lignes de JavaScript...
  </script>
</body>
</html>
```

**Après (pages-traitees/)** :
```html
<style>
  /* Styles inline + animations CSS */
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  .content { animation: fadeIn 0.5s ease-in; }
</style>

<div class="content">...</div>

<script>
  // EmailJS uniquement (30 lignes)
  document.getElementById('form').addEventListener('submit', function(e) {
    e.preventDefault();
    emailjs.sendForm('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', this)
      .then(() => alert('✅ Message envoyé'))
      .catch(() => alert('❌ Erreur'));
  });
</script>
```

---

**Prêt à traiter vos pages !** 🚀
