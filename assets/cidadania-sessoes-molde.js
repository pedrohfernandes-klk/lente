/* Sessões de Cidadania: abertura, depois cinco passos (Recupera, Vê, Decide, Faz, Leva), um de cada vez.
   28/10/2026: generalizado a partir de assets/cidadania-m1-sessoes.js (que fica como está, com a chave do M1,
   porque o HTML do M1 não muda). A página diz qual é a sua chave e que sessões contam:
     <main data-c10 data-chave="lente-cidadania-m2-sessoes-v1" data-sessoes="01 02 ... 10" data-session="03">
   Numa lista de sessões (sem data-session), pinta os estados e o botão «Começar» ou «Continuar» (data-continue).
   O registo fica neste aparelho; em projeção (moldura ou ?projetar=1) nada é gravado. Só lê e escreve a sua chave. */
(function () {
  'use strict';
  var root = document.querySelector('[data-c10][data-chave]');
  if (!root) return;
  var KEY = root.dataset.chave,
    CONTAM = (root.dataset.sessoes || '').split(/\s+/).filter(Boolean),
    state = { version: 1, sessions: {} },
    projected = self !== top || new URLSearchParams(location.search).get('projetar') === '1',
    num = root.dataset.session || '',
    stages = Array.from(root.querySelectorAll('[data-stage]')),
    current = 0, started = false, printState = null,
    intro = root.querySelector('[data-session-intro]'),
    flow = root.querySelector('[data-session-flow]'),
    start = root.querySelector('[data-start]'),
    check = root.querySelector('[data-session-done]'),
    live = root.querySelector('[data-live]');

  function say(t) { if (live) live.textContent = t; }
  function read() {
    try {
      var d = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (d && d.version === 1 && d.sessions && typeof d.sessions === 'object' && !Array.isArray(d.sessions)) state = d;
    } catch (e) { /* sem armazenamento: a página funciona na mesma */ }
    return state;
  }
  function save() {
    if (projected) return false;
    try { localStorage.setItem(KEY, JSON.stringify(state)); return true; }
    catch (e) { say('Este navegador não permite guardar. Conserva o registo no caderno.'); return false; }
  }
  function feita(id) { var s = state.sessions[id]; return !!(s && s.done === true); }

  /* Listas de sessões (guia): «Registado», «Em curso» e a próxima sessão. */
  function paint() {
    read();
    var count = 0, proxima = null;
    CONTAM.forEach(function (id) {
      if (feita(id)) count++; else if (!proxima) proxima = id;
      root.querySelectorAll('[data-session-card="' + id + '"]').forEach(function (card) {
        card.dataset.complete = String(feita(id));
        card.dataset.current = String(false);
        var t = card.querySelector('[data-status]');
        if (t) t.textContent = feita(id) ? 'Registado' : state.sessions[id] ? 'Em curso' : '';
      });
    });
    if (proxima) root.querySelectorAll('[data-session-card="' + proxima + '"]').forEach(function (c) { c.dataset.current = 'true'; });
    var c = root.querySelector('[data-count]');
    if (c) c.textContent = count ? count + (count === 1 ? ' registo de trabalho' : ' registos de trabalho') : '';
    if (check) check.checked = feita(num);
    /* Começar ou continuar: a primeira sessão por registar; no fim, o destino que a página indicar. */
    var go = root.querySelector('[data-continue]');
    if (go) {
      var algum = CONTAM.some(function (id) { return !!state.sessions[id]; });
      if (proxima) { go.href = (go.dataset.continueBase || '') + proxima + '/'; go.textContent = (algum ? 'Continuar na sessão ' : 'Começar na sessão ') + proxima; }
      else if (go.dataset.fimHref) { go.href = go.dataset.fimHref; go.textContent = go.dataset.fimTexto || go.textContent; }
    }
  }

  function show(i, move, remember) {
    if (!stages.length) return;
    current = Math.max(0, Math.min(stages.length - 1, i));
    stages.forEach(function (s, n) { s.hidden = n !== current; });
    root.querySelectorAll('[data-stage-link]').forEach(function (a, n) {
      if (n === current) a.setAttribute('aria-current', 'step'); else a.removeAttribute('aria-current');
    });
    var last = stages.length - 1,
      p = root.querySelector('[data-prev]'), q = root.querySelector('[data-next]'),
      end = root.querySelector('[data-next-session]'), pos = root.querySelector('[data-position]'),
      completion = root.querySelector('[data-completion]');
    if (p) { p.hidden = false; p.disabled = current === 0; }
    if (q) q.hidden = current === last;
    if (end) end.hidden = current !== last;
    if (pos) pos.textContent = (current + 1) + ' / ' + stages.length;
    if (completion) completion.hidden = current !== last;
    if (move) { stages[current].focus({ preventScroll: true }); stages[current].scrollIntoView({ block: 'start', behavior: 'auto' }); }
    if (remember && !projected) { read(); state.sessions[num] = Object.assign({}, state.sessions[num], { stage: current }); save(); }
  }
  function begin(i, move) {
    started = true;
    if (intro) intro.hidden = true;
    if (flow) flow.hidden = false;
    root.classList.add('c10-running');
    show(i, move, true);
    history.replaceState(null, '', '#' + stages[current].id);
  }

  paint();
  if (stages.length) {
    var saved = state.sessions[num];
    if (saved && Number.isInteger(saved.stage)) current = Math.max(0, Math.min(stages.length - 1, saved.stage));
    if (start && current > 0) start.textContent = 'Retomar no passo ' + (current + 1);
    if (flow) flow.hidden = true;
    show(current, false, false);
    var hash = location.hash.slice(1), found = stages.findIndex(function (s) { return s.id === hash; });
    if (found >= 0) begin(found, false);
  }
  if (start) start.addEventListener('click', function (e) { e.preventDefault(); begin(current, true); });
  root.querySelectorAll('[data-stage-link]').forEach(function (a, n) {
    a.addEventListener('click', function (e) { e.preventDefault(); begin(n, true); });
  });
  var prev = root.querySelector('[data-prev]'), next = root.querySelector('[data-next]');
  if (prev) prev.onclick = function () { begin(current - 1, true); };
  if (next) next.onclick = function () { begin(current + 1, true); };
  var cover = root.querySelector('[data-cover-link]');
  if (cover) cover.onclick = function (e) {
    e.preventDefault(); started = false;
    if (flow) flow.hidden = true;
    if (intro) intro.hidden = false;
    root.classList.remove('c10-running');
    history.replaceState(null, '', location.pathname + location.search);
    if (start) { start.textContent = current ? 'Retomar no passo ' + (current + 1) : 'Começar'; start.focus(); }
    if (intro) intro.scrollIntoView({ block: 'start' });
  };
  root.addEventListener('keydown', function (e) {
    if (!started || e.target.closest('input,textarea,select,summary,button,a') || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); begin(current + (e.key === 'ArrowRight' ? 1 : -1), true); }
  });
  if (check) {
    if (projected) { check.disabled = true; say('Projeção: o registo individual não é alterado.'); }
    else check.addEventListener('change', function () {
      read();
      state.sessions[num] = Object.assign({}, state.sessions[num], { done: check.checked, stage: current });
      if (save()) say('Registo guardado neste aparelho.');
      paint();
    });
  }
  root.querySelectorAll('[data-print]').forEach(function (b) { b.hidden = false; b.onclick = function () { window.print(); }; });
  window.addEventListener('beforeprint', function () {
    printState = { started: started, details: Array.from(root.querySelectorAll('details')).map(function (d) { var o = d.open; d.open = true; return [d, o]; }) };
    if (intro) intro.hidden = false;
    if (flow) flow.hidden = false;
    stages.forEach(function (s) { s.hidden = false; });
  });
  window.addEventListener('afterprint', function () {
    if (!printState) return;
    printState.details.forEach(function (p) { p[0].open = p[1]; });
    if (intro) intro.hidden = printState.started;
    if (flow) flow.hidden = !printState.started;
    show(current, false, false);
    printState = null;
  });
  window.addEventListener('hashchange', function () {
    var id = location.hash.slice(1), n = stages.findIndex(function (s) { return s.id === id; });
    if (n >= 0) begin(n, false);
  });
  window.addEventListener('storage', function (e) { if (e.key === KEY) paint(); });
  window.addEventListener('pageshow', paint);
}());
