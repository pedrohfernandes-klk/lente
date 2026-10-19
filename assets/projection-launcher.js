(function () {
  'use strict';
  if (window.self !== window.top || document.getElementById('epi-projection-launcher-style')) return;

  var script = document.currentScript;
  var root = new URL('../', script.src);
  var site = script.dataset.site;
  var publicRoot = '/' + site + '/';
  var start = location.pathname.indexOf(publicRoot);
  if (start < 0 || /\/projetar\/?$/.test(location.pathname)) return;
  // Live classroom panels already have a student QR and their own fullscreen
  // control. Keep their session, handlers and F shortcut intact.
  if (/\/pt\/m[1-9]\/painel-m[1-9]-f\d+\/?$/.test(location.pathname)) return;

  var style = document.createElement('style');
  style.id = 'epi-projection-launcher-style';
  style.textContent = '.epi-projection-launcher{display:inline-flex!important;align-items:center;justify-content:center;gap:0;width:44px;height:44px;min-width:44px;min-height:44px;box-sizing:border-box;flex-shrink:0;margin:6px 0;padding:10px;border:1px solid #ad7663;color:#8f4635;background:transparent;text-decoration:none;font:700 .8rem/1 Arial,sans-serif;max-width:100%}.epi-projection-launcher svg{width:20px;height:20px;flex-shrink:0}.epi-projection-label{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}.epi-projection-launcher:hover{background:#96503c0d}.epi-projection-launcher:focus-visible,.epi-projection-menu-link:focus-visible{outline:3px solid currentColor;outline-offset:3px}.epi-projection-launcher.epi-projection-compact{margin:0 2px;padding:10px}.epi-projection-menu-link{display:flex;align-items:center;min-height:44px;padding:10px 0;color:#8f4635}.epi-projection-deck{margin:0 8px!important}.epi-projection-deck-nav{display:flex!important;align-items:center;gap:8px}.epi-projection-deck-nav>ol{flex:1;min-width:0;margin:0!important;flex-wrap:wrap}.epi-projection-deck-nav>.epi-projection-deck{flex-shrink:0}@media(prefers-color-scheme:dark){.epi-projection-launcher,.epi-projection-menu-link{color:#e9b39e}.epi-projection-launcher{border-color:#c79780}.epi-projection-launcher:hover{background:#e9b39e12}}@media(max-width:600px){.epi-projection-compact{display:none!important}}@media print{.epi-projection-launcher,.epi-projection-menu-link{display:none!important}}';
  document.head.appendChild(style);

  var link = document.createElement('a');
  link.className = 'epi-projection-launcher';
  link.setAttribute('data-projection-version', '20261019.4');
  link.setAttribute('aria-label', 'Projetar esta página com QR para a turma');
  link.title = 'Projetar esta página com QR para a turma';
  link.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false"><rect x="2" y="3" width="20" height="14" rx="1"/><path d="M12 17v4m-5 0h10M6 7h4v4H6zm8 0h4v4h-4zM6 13h4m4 0h4"/></svg><span class="epi-projection-label">Projetar esta página · QR para a turma</span>';

  function target() {
    var url = new URL('projetar/', root);
    url.searchParams.set('pagina', publicRoot + location.pathname.slice(start + publicRoot.length) + location.hash);
    return url.href;
  }

  function updateLinks() {
    link.href = target();
    document.querySelectorAll('.epi-projection-menu-link,[data-projetar]').forEach(function (a) { a.href = link.href; });
  }

  function mount() {
    upgradeLegacy();
    var bars = Array.prototype.filter.call(document.querySelectorAll('.casca:not([hidden]) .casca-topo'), function (e) { return e.getClientRects().length > 0; });
    var bar = bars[bars.length - 1];
    var deck = document.querySelector('.deck .topo .l1');
    var main = document.querySelector('main:not(.casca-corpo)');
    var breadcrumb = document.querySelector('nav.migalhas');
    if (deck && breadcrumb) breadcrumb.classList.add('epi-projection-deck-nav');
    var host = bar || (deck && breadcrumb) || deck || document.querySelector('nav.migalhas,.atelier-breadcrumb') || (main && main.querySelector(':scope > header,:scope > nav')) || document.querySelector('.topo > .l1') || main || document.body;
    link.classList.toggle('epi-projection-compact', !!bar);
    link.classList.toggle('epi-projection-deck', !!deck && !bar);
    link.querySelector('.epi-projection-label').textContent = bar ? 'Projetar' : 'Projetar esta página · QR para a turma';
    if (link.parentNode !== host) {
      var menuButton = bar && bar.querySelector('[data-c-menu]');
      if (menuButton) host.insertBefore(link, menuButton);
      else if (host === main || host === document.body) host.insertBefore(link, host.firstChild);
      else host.appendChild(link);
    }
    document.querySelectorAll('.casca-menu .c-menu-in > nav').forEach(function (nav) {
      if (nav.querySelector('.epi-projection-menu-link,[data-projetar]')) return;
      var a = document.createElement('a');
      a.className = 'epi-projection-menu-link';
      a.textContent = 'Projetar esta página · QR para a turma';
      nav.appendChild(a);
    });
    updateLinks();
  }

  function upgradeLegacy() {
  document.querySelectorAll('[data-projetar]:not([data-epi-projection-ready]),a[href*="projetar=1"]:not([data-epi-projection-ready])').forEach(function (old) {
    var replacement;
    if (old.tagName === 'A') replacement = old.cloneNode(true);
    else {
      replacement = document.createElement('a');
      Array.prototype.forEach.call(old.attributes, function (a) { if (!/^(?:type|disabled|onclick|role|aria-pressed)$/i.test(a.name)) replacement.setAttribute(a.name, a.value); });
      replacement.style.cssText += ';display:inline-flex;align-items:center;min-height:44px;color:inherit;cursor:pointer;';
    }
    replacement.removeAttribute('onclick');
    replacement.setAttribute('data-projetar', '');
    replacement.setAttribute('data-epi-projection-ready', '');
    if (old.closest('.casca-menu')) replacement.classList.add('epi-projection-menu-link');
    replacement.setAttribute('aria-label', 'Projetar esta página com QR para a turma');
    replacement.textContent = old.tagName === 'A' ? 'Projetar esta página · QR para a turma' : 'Projetar · QR';
    old.replaceWith(replacement);
  });
  }
  mount();
  window.addEventListener('hashchange', updateLinks);
  ['click', 'keydown', 'focusin', 'contextmenu'].forEach(function (name) {
    document.addEventListener(name, function (event) {
      var entry = event.target.closest && event.target.closest('.epi-projection-launcher,.epi-projection-menu-link,a[data-projetar]');
      if (!entry) return;
      updateLinks();
      // Slide decks can use a click anywhere to advance. Opening projection
      // must remain navigation and must not advance the underlying activity.
      if ((name === 'click' && event.button === 0) || (name === 'keydown' && event.key === 'Enter')) {
        event.stopImmediatePropagation();
        if (!event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey) {
          event.preventDefault();
          location.assign(entry.href);
        }
      }
    }, true);
  });

  // A lesson can open its shell after the page loads. Keep the access in its
  // toolbar, never in the changing activity area, and restore it on close.
  var scheduled = false;
  new MutationObserver(function (changes) {
    var shellChanged = !link.isConnected || changes.some(function (change) {
      if (change.type === 'attributes') return change.target.matches('.casca,.deck,html,body') || !!change.target.querySelector('.casca-topo');
      return Array.prototype.some.call(change.addedNodes, function (node) {
        return node.nodeType === 1 && (node.matches('.casca,.casca-topo,.casca-menu,.deck,[data-projetar]:not([data-epi-projection-ready]),a[href*="projetar=1"]:not([data-epi-projection-ready])') || node.querySelector('.casca-topo,.casca-menu,[data-projetar]:not([data-epi-projection-ready])'));
      });
    });
    if (!shellChanged || scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () { scheduled = false; mount(); });
  }).observe(document.documentElement, {childList: true, subtree: true, attributes: true, attributeFilter: ['hidden', 'class', 'style']});
}());
