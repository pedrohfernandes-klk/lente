/* 01/11/2026: decisão 57, D4/D5. Sem leitura ou escrita de progresso.
 * O adaptador de cada família fornece done/next/date a stateLabel.
 * No HTML, todas as details.cz-fold têm open. Carregar com defer. */
(function (root) {
  'use strict';
  function stateLabel({done = false, next = false, date = null} = {}) {
    if (!done) return next ? 'A seguir' : '';
    // Só datas ISO de calendário; não inferir a data de uma visita.
    const match = typeof date === 'string' && /^(\d{4})-(\d{2})-(\d{2})(?:T.*)?$/.exec(date);
    if (!match) return 'Feita';
    const check = new Date(`${match[1]}-${match[2]}-${match[3]}T12:00:00Z`);
    return Number.isFinite(check.getTime()) && check.toISOString().slice(0,10) === match[0].slice(0,10)
      ? `Feita ${match[3]}/${match[2]}` : 'Feita';
  }
  const initialized = new WeakSet();
  function init(doc = root.document) {
    if (!doc || initialized.has(doc)) return;
    const folds = [...doc.querySelectorAll('[data-cartaz="2"] details.cz-fold')];
    if (!folds.length) return;
    initialized.add(doc);
    const mobile = root.matchMedia('(max-width: 639px)');
    let printing = false, saved = null;
    const projection = () => new URLSearchParams(root.location.search).get('projetar') === '1'
      || doc.documentElement.classList.contains('em-projecao');
    function anchor() {
      try { return doc.getElementById(decodeURIComponent(root.location.hash.slice(1))); }
      catch { return null; }
    }
    function update(reset) {
      const target = anchor();
      for (const fold of folds) {
        if (printing || projection() || !mobile.matches || fold.contains(target)
          || fold.querySelector('[data-cz-next]')) fold.open = true;
        else if (reset) fold.open = false;
      }
    }
    update(true);
    root.addEventListener('hashchange', () => update(false));
    mobile.addEventListener('change', () => update(true));
    new root.MutationObserver(() => update(false)).observe(doc.documentElement, {attributes:true, attributeFilter:['class']});
    root.addEventListener('beforeprint', () => { saved = folds.map(f => f.open); printing = true; update(false); });
    root.addEventListener('afterprint', () => { printing = false; folds.forEach((f,i) => { f.open = saved?.[i] ?? true; }); update(false); });
  }
  const api = {stateLabel, init};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else { root.EPICartaz = api; init(); }
})(typeof window === 'undefined' ? globalThis : window);
