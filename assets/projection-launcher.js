(function () {
  'use strict';

  if (window.self !== window.top) return;
  if (window.__EPI_PROJECTION_LAUNCHER__) return;
  window.__EPI_PROJECTION_LAUNCHER__ = true;

  var script = document.currentScript || Array.prototype.slice.call(document.scripts).reverse().find(function (candidate) {
    return /projection-launcher\.js(?:\?|$)/.test(candidate.src || '');
  });

  if (!script) return;

  var site = (script.dataset.site || document.documentElement.dataset.site || '').trim();
  if (!site) return;

  var root = new URL('../', script.src || document.baseURI);
  var publicRoot = '/' + site + '/';
  var currentPath = location.pathname || '/';
  var start = currentPath.indexOf(publicRoot);

  if (start < 0 || /\/projetar\/?$/.test(currentPath)) return;
  if (/\/pt\/m[1-9]\/painel-m[1-9]-f\d+\/?$/.test(currentPath)) return;

  var style = document.getElementById('epi-projection-launcher-style') || document.createElement('style');
  style.id = 'epi-projection-launcher-style';
  style.textContent = [
    '.epi-projection-launcher{display:inline-flex!important;align-items:center;justify-content:center;gap:8px;width:auto;height:44px;min-width:44px;min-height:44px;box-sizing:border-box;padding:0 12px;border:1px solid var(--tinta,#000);background:var(--papel,#fff);color:var(--tinta,#000);text-decoration:none;font:700 .82rem/1.1 Arial,Helvetica,sans-serif;letter-spacing:.04em;text-transform:uppercase;cursor:pointer;white-space:nowrap;}',
    '.epi-projection-launcher:hover,.epi-projection-launcher:focus-visible,.epi-projection-menu-link:hover,.epi-projection-menu-link:focus-visible{outline:3px solid var(--tinta,#000);outline-offset:2px;text-decoration:underline;}',
    '.epi-projection-launcher svg{width:18px;height:18px;flex:0 0 18px;}',
    '.epi-projection-launcher .epi-projection-label{display:inline-block;max-width:24ch;overflow:hidden;text-overflow:ellipsis;}',
    '.epi-projection-launcher.epi-projection-compact{padding:0 10px;}',
    '.epi-projection-launcher.epi-projection-deck{padding:0 12px;}',
    '.epi-projection-menu-link{display:inline-flex;align-items:center;gap:8px;min-height:44px;font:700 .82rem/1.1 Arial,Helvetica,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:inherit;text-decoration:none;}',
    '.epi-projection-menu-link svg{width:18px;height:18px;}',
    '.epi-projection-deck-nav{display:flex;align-items:center;gap:8px;}'
  ].join('');
  if (!style.parentNode) document.head.appendChild(style);

  var link = document.createElement('a');
  link.className = 'epi-projection-launcher';
  link.setAttribute('data-projection-version', '20261019.4');
  link.setAttribute('aria-label', 'Projetar esta página com QR para a turma');
  link.title = 'Projetar esta página com QR para a turma';
  link.setAttribute('role', 'button');
  link.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false"><rect x="2" y="3" width="20" height="14" rx="1"></rect><path d="M8 21h8M12 17v4M4 7h16"></path></svg><span class="epi-projection-label">Projetar</span>';

  function target() {
    var url = new URL('projetar/', root);
    url.searchParams.set('pagina', publicRoot + currentPath.slice(start + publicRoot.length) + location.hash);
    return url.href;
  }

  function updateLinks() {
    var href = target();
    link.href = href;
    link.setAttribute('aria-label', 'Projetar esta página com QR para a turma');
    document.querySelectorAll('.epi-projection-menu-link,[data-projetar]').forEach(function (anchor) {
      anchor.href = href;
      if (anchor.tagName === 'A') anchor.setAttribute('aria-label', 'Projetar esta página com QR para a turma');
    });
  }

  function mount() {
    upgradeLegacy();

    var bars = Array.prototype.filter.call(document.querySelectorAll('.casca:not([hidden]) .casca-topo'), function (element) {
      return !!element.getClientRects().length;
    });
    var bar = bars[bars.length - 1];
    var deck = document.querySelector('.deck .topo .l1');
    var main = document.querySelector('main:not(.casca-corpo)');
    var breadcrumb = document.querySelector('nav.migalhas');

    if (deck && breadcrumb) breadcrumb.classList.add('epi-projection-deck-nav');

    var host = bar || (deck && breadcrumb) || deck || document.querySelector('nav.migalhas,.atelier-breadcrumb') || (main && main.querySelector(':scope > header,:scope > nav')) || document.querySelector('body');
    if (!host) return;

    link.classList.toggle('epi-projection-compact', !!bar);
    link.classList.toggle('epi-projection-deck', !!deck && !bar);

    var label = link.querySelector('.epi-projection-label');
    if (label) label.textContent = bar ? 'Projetar' : 'Projetar esta página · QR para a turma';

    if (link.parentNode !== host) {
      var menuButton = bar && bar.querySelector('[data-c-menu]');
      if (menuButton) host.insertBefore(link, menuButton);
      else if (host === main || host === document.body) host.insertBefore(link, host.firstChild);
      else host.appendChild(link);
    }

    document.querySelectorAll('.casca-menu .c-menu-in > nav').forEach(function (nav) {
      if (nav.querySelector('.epi-projection-menu-link,[data-projetar]')) return;
      var menuLink = document.createElement('a');
      menuLink.className = 'epi-projection-menu-link';
      menuLink.href = target();
      menuLink.textContent = 'Projetar esta página · QR para a turma';
      menuLink.setAttribute('aria-label', 'Projetar esta página com QR para a turma');
      nav.appendChild(menuLink);
    });

    updateLinks();
  }

  function upgradeLegacy() {
    document.querySelectorAll('[data-projetar]:not([data-epi-projection-ready]),a[href*="projetar=1"]:not([data-epi-projection-ready])').forEach(function (old) {
      var replacement;

      if (old.tagName === 'A') {
        replacement = old.cloneNode(true);
      } else {
        replacement = document.createElement('a');
        Array.prototype.forEach.call(old.attributes, function (attribute) {
          if (!/^(?:type|disabled|onclick|role|aria-pressed)$/i.test(attribute.name)) {
            replacement.setAttribute(attribute.name, attribute.value);
          }
        });
        replacement.style.cssText += ';display:inline-flex;align-items:center;min-height:44px;color:inherit;cursor:pointer;';
      }

      replacement.removeAttribute('onclick');
      replacement.setAttribute('data-projetar', '');
      replacement.setAttribute('data-epi-projection-ready', '');
      replacement.setAttribute('aria-label', 'Projetar esta página com QR para a turma');
      replacement.textContent = old.tagName === 'A' ? 'Projetar esta página · QR para a turma' : 'Projetar · QR';

      if (old.closest('.casca-menu')) replacement.classList.add('epi-projection-menu-link');
      old.replaceWith(replacement);
    });
  }

  mount();
  window.addEventListener('hashchange', updateLinks);

  ['click', 'keydown', 'focusin', 'contextmenu'].forEach(function (eventName) {
    document.addEventListener(eventName, function (event) {
      var entry = event.target && event.target.closest && event.target.closest('.epi-projection-launcher,.epi-projection-menu-link,a[data-projetar]');
      if (!entry) return;

      updateLinks();

      var isPrimaryClick = eventName === 'click' && event.button === 0 && !event.defaultPrevented;
      var isKeyboardAction = eventName === 'keydown' && (event.key === 'Enter' || event.key === ' ');

      if (isPrimaryClick || isKeyboardAction) {
        event.stopImmediatePropagation();
        if (!event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey) {
          event.preventDefault();
          location.assign(entry.href);
        }
      }
    }, true);
  });

  var scheduled = false;
  new MutationObserver(function (changes) {
    var shellChanged = !link.isConnected || changes.some(function (change) {
      if (change.type === 'attributes') {
        return change.target.matches && (change.target.matches('.casca,.deck,html,body') || !!change.target.querySelector('.casca-topo'));
      }
      return Array.prototype.some.call(change.addedNodes || [], function (node) {
        return node.nodeType === 1 && node.matches && node.matches('.casca,.casca-topo,.casca-menu,.deck,[data-projetar]:not([data-epi-projection-ready]),a[href*="projetar=1"]:not([data-epi-projection-ready])');
      });
    });

    if (!shellChanged || scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      mount();
    });
  }).observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['hidden', 'class', 'style'] });
}());
