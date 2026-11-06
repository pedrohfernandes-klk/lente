// 05/11/2026: decisão 153. Melhora a peça «i» (assets/info-i.css); sem este ficheiro, a <details> abre e fecha na mesma.
// Fechada ao carregar e nunca grava nada no aparelho. Escape fecha a aberta e devolve o foco ao «i» (o diálogo de ampliar
// trata o Escape antes, na fase de captura); um toque ou clique fora fecha; abrir um fecha o outro (o name="info-i" já o faz
// nos navegadores atuais; isto cobre os outros); na projeção, tudo fechado.
(function (d) {
  'use strict';
  if (window.EPIInfoI) return;
  var SEL = 'details.info-i', html = d.documentElement;
  function abertos() { return [].slice.call(d.querySelectorAll(SEL + '[open]')); }
  d.addEventListener('toggle', function (e) {
    var t = e.target;
    if (!t || !t.matches || !t.matches(SEL) || !t.open) return;
    abertos().forEach(function (x) { if (x !== t) x.open = false; });
  }, true);
  d.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' && e.key !== 'Esc') return;
    var x = abertos()[0];
    if (!x) return;
    x.open = false;
    if (x.contains(d.activeElement) || d.activeElement === d.body) { var s = x.querySelector('summary'); if (s) s.focus(); }
  });
  d.addEventListener('click', function (e) {
    abertos().forEach(function (x) { if (!x.contains(e.target)) x.open = false; });
  });
  function projetada() {
    return /[?&]projetar=1(&|$)/.test(location.search) || /(^|\s)(em-projecao|epi-projection)(\s|$)/.test(html.className) || html.hasAttribute('data-cz-projection');
  }
  function fechaNaProjecao() { if (projetada()) abertos().forEach(function (x) { x.open = false; }); }
  if ('MutationObserver' in window) new MutationObserver(fechaNaProjecao).observe(html, { attributes: true, attributeFilter: ['class', 'data-cz-projection'] });
  window.EPIInfoI = { fechar: function () { abertos().forEach(function (x) { x.open = false; }); } };
})(document);
