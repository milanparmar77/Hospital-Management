/* ==========================================================================
   MediCare+ — shared site-wide JS
   Page-specific interactions (table filters, date min, etc.) live inline
   in each template's {% block extra_js %}. This file is for behavior
   shared across every page.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

  // Auto-dismiss Bootstrap alerts (e.g. Django messages) after 4 seconds
  document.querySelectorAll('.alert[data-auto-dismiss]').forEach(function (alertEl) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      bsAlert.close();
    }, 4000);
  });

  // Enable Bootstrap tooltips wherever data-bs-toggle="tooltip" is used
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

});
