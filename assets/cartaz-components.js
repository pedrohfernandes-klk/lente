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
/* 01/11/2026: movimento Cartaz. */(function(w){'use strict';if(!w.document)return;const d=w.document,h=d.documentElement,q=w.matchMedia('(prefers-reduced-motion: reduce)'),B=new Map(),V=new Set();let P=false;const ks=['title','poster','line','correct','error','fold'];function F(el){return P||q.matches||h.hasAttribute('data-cz-reduce')||h.hasAttribute('data-cz-projection')||new URLSearchParams(w.location.search).get('projetar')==='1'||h.matches('.em-projecao,.epi-projection')||!!el.closest('[data-cz-static]');}function sync(){h.toggleAttribute('data-cz-motion-enabled',!F(h));for(const [r,C] of B)if(F(r))C();d.querySelectorAll('[data-cz-motion-region]').forEach(el=>el.toggleAttribute('data-cz-motion-off',F(el)));}function S(el,k){if(!el?.classList.contains('cz-motion-'+k)||!el.isConnected||!el.closest('[data-cartaz="2"]')||el.closest('.cz-next')||el.querySelector('.cz-next'))return!1;const r=el.closest('[data-cz-motion-region]');if(!r||F(el))return!1;if([...B.keys()].some(r=>r.contains(r)||r.contains(r)))return!1;const ps=/^(title|poster)$/.test(k)?[...el.querySelectorAll('.cz-motion-part')].slice(0,4):[el];if(!ps.length)return!1;let i=0,tm;function C(){clearTimeout(tm);for(const p of ps){p.removeEventListener('animationend',E);p.removeEventListener('animationcancel',C);p.classList.remove('cz-motion-active');}B.delete(r);}function E(e){if(!e.animationName.startsWith('cz-'))return;const p=ps[i];p.removeEventListener('animationend',E);p.removeEventListener('animationcancel',C);p.classList.remove('cz-motion-active');if(++i<ps.length&&!F(el))R();else C();}function R(){const p=ps[i];p.addEventListener('animationend',E);p.addEventListener('animationcancel',C);p.classList.add('cz-motion-active');}B.set(r,C);tm=setTimeout(C,800);R();return!0;}function play(el){const k=ks.find(k=>el?.classList.contains('cz-motion-'+k));return k?S(el,k):false;}function complete(el,{before,after,event}={}){if(before!==false||after!==true||typeof event!=='string'||!event||V.has(event))return!1;V.add(event);return S(el,'point');}function number(el,before,after){if(!Number.isInteger(before)||!Number.isInteger(after)||before<0||after>999||after<=before)return!1;const roll=el?.querySelector('.cz-motion-roll');if(!roll)return!1;roll.replaceChildren(...[before,after].map(n=>{const b=d.createElement('b');b.textContent=n;return b;}));return S(el,'number');}w.EPICartaz.motion={play,complete,number,sync,stop:()=>{for(const C of [...B.values()])C();}};q.addEventListener('change',sync);w.addEventListener('popstate',sync);w.addEventListener('beforeprint',()=>{P=true;sync();});w.addEventListener('afterprint',()=>{P=false;sync();});new MutationObserver(sync).observe(h,{attributes:true,attributeFilter:['class','data-cz-reduce','data-cz-projection']});sync();})(typeof window==='undefined'?globalThis:window);/* fim */
