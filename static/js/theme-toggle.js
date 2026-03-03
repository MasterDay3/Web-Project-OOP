(function() {
  'use strict';
  var STORAGE_KEY = 'numerix-theme';
  var html = document.documentElement;
  var toggle = document.getElementById('theme-toggle');
  if (!toggle) return;

  function isDark() {
    return html.getAttribute('data-theme') === 'dark';
  }

  function updateToggle() {
    var dark = isDark();
    var iconEl = toggle.querySelector('[data-lucide]');
    if (iconEl) {
      iconEl.setAttribute('data-lucide', dark ? 'sun' : 'moon');
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }
    var labelEl = toggle.querySelector('.theme-toggle-label');
    if (labelEl) {
      labelEl.textContent = dark ? 'Світла тема' : 'Темна тема';
    }
  }

  toggle.addEventListener('click', function() {
    var newTheme = isDark() ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem(STORAGE_KEY, newTheme);
    updateToggle();
  });

  updateToggle();
})();
