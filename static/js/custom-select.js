/**
 * Custom Select — replaces native <select> with styled dropdowns.
 * Auto-initialises on DOMContentLoaded; also exposes initCustomSelects()
 * so pages that build selects dynamically can re-run it.
 */
(function () {
  'use strict';

  function initCustomSelects(root) {
    const container = root || document;
    const selects = container.querySelectorAll('select:not([data-custom-done])');

    selects.forEach(function (sel) {
      sel.setAttribute('data-custom-done', '1');

      // Wrapper
      const wrap = document.createElement('div');
      wrap.className = 'cs-wrap';

      // Trigger button
      const trigger = document.createElement('button');
      trigger.type = 'button';
      trigger.className = 'cs-trigger';

      const label = document.createElement('span');
      label.className = 'cs-label';

      const arrow = document.createElement('span');
      arrow.className = 'cs-arrow';
      arrow.innerHTML = '<svg width="12" height="7" viewBox="0 0 12 7" fill="none"><path d="M1 1l5 5 5-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

      trigger.appendChild(label);
      trigger.appendChild(arrow);

      // Dropdown list
      const list = document.createElement('ul');
      list.className = 'cs-list';

      function buildOptions() {
        list.innerHTML = '';
        Array.from(sel.options).forEach(function (opt, i) {
          const li = document.createElement('li');
          li.className = 'cs-option' + (i === sel.selectedIndex ? ' selected' : '');
          li.textContent = opt.textContent;
          li.dataset.value = opt.value;
          li.dataset.index = i;
          list.appendChild(li);
        });
        label.textContent = sel.options[sel.selectedIndex]
          ? sel.options[sel.selectedIndex].textContent
          : '';
      }

      buildOptions();

      // Insert into DOM
      sel.parentNode.insertBefore(wrap, sel);
      wrap.appendChild(trigger);
      wrap.appendChild(list);
      wrap.appendChild(sel);
      sel.style.display = 'none';
      sel.tabIndex = -1;

      // Open / close
      function open() {
        // Close any other open selects first
        document.querySelectorAll('.cs-wrap.open').forEach(function (w) {
          if (w !== wrap) w.classList.remove('open');
        });
        wrap.classList.add('open');
        // Scroll selected into view
        const cur = list.querySelector('.cs-option.selected');
        if (cur) cur.scrollIntoView({ block: 'nearest' });
      }

      function close() {
        wrap.classList.remove('open');
      }

      trigger.addEventListener('click', function (e) {
        e.stopPropagation();
        if (wrap.classList.contains('open')) close();
        else open();
      });

      // Select option
      list.addEventListener('click', function (e) {
        const li = e.target.closest('.cs-option');
        if (!li) return;

        sel.selectedIndex = Number(li.dataset.index);
        sel.dispatchEvent(new Event('change', { bubbles: true }));

        list.querySelectorAll('.cs-option').forEach(function (o) { o.classList.remove('selected'); });
        li.classList.add('selected');
        label.textContent = li.textContent;
        close();
      });

      // Close on outside click
      document.addEventListener('click', function (e) {
        if (!wrap.contains(e.target)) close();
      });

      // Close on Escape
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') close();
      });

      // Watch for programmatic changes (e.g. swap button)
      const observer = new MutationObserver(buildOptions);
      observer.observe(sel, { childList: true, attributes: true, subtree: true });

      // Also listen for value changes via JS
      sel.addEventListener('change', function () {
        buildOptions();
      });
    });
  }

  // Auto-init on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { initCustomSelects(); });
  } else {
    initCustomSelects();
  }

  // Expose globally
  window.initCustomSelects = initCustomSelects;
})();
