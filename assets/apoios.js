/* Apoios comuns: os destinos docentes mantêm-se, reunidos na boia. */
(function () {
  'use strict';
  var script = document.currentScript;
  var root = new URL('../', script.src);
  function mount() {
    if (document.querySelector('.boia, .epi-boia')) return;
    var links = Array.from(document.querySelectorAll('a[href]')).filter(function (a) {
      return /^Para o docente(?:\s|:|$)/i.test(a.textContent.trim());
    });
    var dock = document.createElement('details');
    dock.className = 'epi-boia';
    dock.innerHTML = '<summary aria-label="Abrir apoios"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="m5.6 5.6 3.6 3.6m5.6 5.6 3.6 3.6m0-12.8-3.6 3.6m-5.6 5.6-3.6 3.6"/></svg></summary><nav aria-label="Apoios"></nav>';
    var nav = dock.querySelector('nav');
    links.forEach(function (a) { a.textContent = 'Guia do docente'; nav.appendChild(a); });
    if (!links.length) {
      var a = document.createElement('a');
      a.href = new URL('docente/', root).href;
      a.textContent = 'Materiais do docente';
      nav.appendChild(a);
    }
    var help = document.createElement('a');
    help.href = new URL('como/', root).href;
    help.textContent = 'Como se usa';
    nav.appendChild(help);
    dock.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { dock.open = false; dock.querySelector('summary').focus(); }
    });
    document.body.classList.add('com-boia');
    document.body.appendChild(dock);
  }
  var css = document.createElement('link');
  css.rel = 'stylesheet'; css.href = new URL('assets/apoios.css?v=20261103-1', root).href;
  document.head.appendChild(css);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once:true});
  else mount();
}());
