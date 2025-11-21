/**
 * 📧 EmailJS Minimal - Script optimisé SEO
 * ✅ 30 lignes encapsulées
 * ✅ Feedback visuel (⏳ → ✅ → ❌)
 * ✅ Compatible WordPress Gutenberg
 */

(function() {
  const form = document.getElementById('contact-form');
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalText = submitBtn.innerHTML;

  form.addEventListener('submit', function(e) {
    e.preventDefault();

    // État : Envoi en cours
    submitBtn.disabled = true;
    submitBtn.innerHTML = '⏳ Envoi en cours...';
    submitBtn.style.opacity = '0.6';

    // Configuration EmailJS
    const serviceID = 'YOUR_SERVICE_ID';
    const templateID = 'YOUR_TEMPLATE_ID';

    emailjs.sendForm(serviceID, templateID, this)
      .then(function() {
        // Succès ✅
        submitBtn.innerHTML = '✅ Message envoyé !';
        submitBtn.style.background = '#10b981';
        form.reset();
        setTimeout(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
          submitBtn.style.opacity = '1';
          submitBtn.style.background = '';
        }, 3000);
      })
      .catch(function(error) {
        // Erreur ❌
        console.error('Erreur EmailJS:', error);
        submitBtn.innerHTML = '❌ Erreur, réessayez';
        submitBtn.style.background = '#ef4444';
        setTimeout(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
          submitBtn.style.opacity = '1';
          submitBtn.style.background = '';
        }, 3000);
      });
  });
})();
