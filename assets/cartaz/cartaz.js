/* Sistema «Cartaz»: peças comuns (síntese de 24/10/2026). Sem bibliotecas. Só lê as chaves que já existem; não grava nada
   (a única escrita é a da síntese da unidade do Português, feita pela página, no formato de unit-synthesis.js).
   - html.em-projecao com ?projetar=1 ou dentro da moldura; na projeção, a página não lê o progresso deste aparelho (Cartaz.proj)
   - html.entra: o movimento de entrada, uma vez por carregamento (sai aos 2,6 s); nada com prefers-reduced-motion
   - Cartaz.ler(chave), Cartaz.feitas(chave), Cartaz.hoje() (aceita ?hoje=AAAA-MM-DD), Cartaz.dias(), Cartaz.data(), Cartaz.anunciar(texto)
   - [data-mexe]: o título entra palavra a palavra, com máscara
   - [data-decide]: decidir em silêncio (botões [data-opcao], respostas [data-resposta="valor"|"*"], data-marca="#linha" acende «Começa aqui»)
   - [data-olhar]: alterna uma classe noutro elemento (o «Olhar de lado» dos Embaixadores)
   - [data-dobra]: abaixo de 640 px, porta ou unidade que se abre no próprio sítio (botão .porta-abre); Cartaz.abrir(el)
   - [data-alterna]: botão que mostra ou esconde um painel (aria-controls) */
(function () {
  var d = document.documentElement, q = location.search;
  var proj = /[?&]projetar=1/.test(q);
  try { if (window.self !== window.top) proj = true; } catch (e) { proj = true; }
  d.classList.add('cv'); /* com script: só então as portas e as unidades se dobram no telemóvel (sem script, tudo fica aberto) */
  if (proj) d.classList.add('em-projecao');
  var reduz = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  if (!reduz) d.classList.add('entra');

  function ler(k) { if (proj) return null; try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }
  function feitas(k) { var o = ler(k); return (o && o.feitas && typeof o.feitas === 'object') ? o.feitas : {}; }
  function n(o) { return Object.keys(o || {}).length; }
  function hoje() {
    var m = /[?&]hoje=(\d{4}-\d\d-\d\d)/.exec(q), t = m ? new Date(m[1] + 'T12:00:00') : new Date();
    t.setHours(12, 0, 0, 0); return t;
  }
  function dia(s) { return new Date(s + 'T12:00:00'); }
  function dias(a, b) { return Math.round((b - a) / 864e5); }
  function data(t) { var x = new Date(t); return ('0' + x.getDate()).slice(-2) + '/' + ('0' + (x.getMonth() + 1)).slice(-2); }
  var SEMANA = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];
  function diaSemana(t) { return SEMANA[new Date(t).getDay()]; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var estreito = window.matchMedia ? matchMedia('(max-width: 639px)') : { matches: false };

  /* uma região viva permanente, escondida à vista: o texto muda a cada gesto (anúncio fiável no leitor de ecrã) */
  var viva = null;
  function anunciar(t) {
    if (!viva) { viva = document.createElement('p'); viva.className = 'p-sr'; viva.setAttribute('aria-live', 'polite'); document.body.appendChild(viva); }
    viva.textContent = ''; setTimeout(function () { viva.textContent = t; }, 60);
  }

  function mexe(el) {
    if (el.getAttribute('data-mexido')) return;
    var i = 0;
    (function walk(node) {
      [].slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var frag = document.createDocumentFragment();
          c.nodeValue.split(/(\s+)/).forEach(function (w) {
            if (!w) return;
            if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(w)); return; }
            var m = document.createElement('span'), s = document.createElement('span');
            m.className = 'mascara'; s.className = 'mexe'; s.style.setProperty('--i', i++); s.textContent = w;
            m.appendChild(s); frag.appendChild(m);
          });
          c.parentNode.replaceChild(frag, c);
        } else if (c.nodeType === 1 && !c.classList.contains('mascara') && !c.classList.contains('p-sr')) {
          if (c.getAttribute('aria-hidden') === 'true' && c.textContent.length < 3) {
            var m2 = document.createElement('span'); m2.className = 'mascara'; c.parentNode.insertBefore(m2, c);
            c.classList.add('mexe'); c.style.setProperty('--i', i++); m2.appendChild(c);
          } else walk(c);
        }
      });
    })(el);
    el.setAttribute('data-mexido', '1');
  }

  /* abrir uma porta ou unidade dobrada (só tem efeito visível abaixo de 640 px) */
  function abrir(el, on) {
    if (!el) return;
    on = on !== false;
    el.classList.toggle('aberta', on);
    var b = el.querySelector('.porta-abre');
    if (b) { b.setAttribute('aria-expanded', String(on)); b.setAttribute('aria-label', (on ? 'Fechar ' : 'Abrir ') + (b.getAttribute('data-nome') || '')); }
  }
  function porta(b) {
    var c = b.closest('[data-dobra]');
    b.addEventListener('click', function () { abrir(c, !c.classList.contains('aberta')); });
  }
  /* uma âncora (#m4-f28, #unidade-pedagogica-2, #p-etica) dentro de uma porta fechada abre-a */
  function abrirAncora() {
    if (!location.hash) return null;
    var alvo = null; try { alvo = document.querySelector(location.hash); } catch (e) { return null; }
    if (!alvo) return null;
    var c = alvo.closest('[data-dobra]');
    if (c && !c.classList.contains('aberta')) { abrir(c, true); requestAnimationFrame(function () { alvo.scrollIntoView({ block: 'start' }); }); }
    var li = alvo.closest('li'); if (li && li.closest('.aulas')) { li.classList.add('realce'); setTimeout(function () { li.classList.remove('realce'); }, 1600); }
    return alvo;
  }

  /* mostrar o que se revelou sem saltar: só rola o necessário para o fim do texto entrar no ecrã */
  function aVista(el) {
    if (!el) return;
    var r = el.getBoundingClientRect();
    if (r.bottom > innerHeight - 12) window.scrollBy({ top: Math.min(r.bottom - innerHeight + 24, r.top - 80), behavior: reduz ? 'auto' : 'smooth' });
  }
  /* decidir em silêncio: a resposta não se grava; um segundo toque na mesma opção desfaz */
  function decide(box) {
    var bs = box.querySelectorAll('[data-opcao]'), marca = box.getAttribute('data-marca');
    function mostra(v) {
      [].forEach.call(box.querySelectorAll('[data-resposta]'), function (r) { var k = r.getAttribute('data-resposta'); r.hidden = !(v && (k === v || k === '*')); });
    }
    function linha(on) {
      if (!marca) return;
      var l = document.querySelector(marca); if (!l) return;
      var fim = l.querySelector('.fim'), e = fim && fim.querySelector('.etq.aqui');
      if (on && !e && fim && !l.classList.contains('feita')) { fim.insertAdjacentHTML('afterbegin', '<span class="etq seguir aqui novo">Começa aqui</span>'); l.classList.add('atual'); }
      if (!on && e) { e.remove(); if (!l.getAttribute('data-atual')) l.classList.remove('atual'); }
      if (on) { var c = l.closest('[data-dobra]'); if (c) abrir(c, true); }
    }
    [].forEach.call(bs, function (b) {
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-opcao'), ja = box.getAttribute('data-escolha') === v;
        [].forEach.call(bs, function (x) { x.setAttribute('aria-pressed', String(!ja && x === b)); });
        if (ja) { box.removeAttribute('data-escolha'); mostra(null); linha(false); anunciar('Escolha desfeita.'); return; }
        box.setAttribute('data-escolha', v); mostra(v); linha(true);
        var vis = [].filter.call(box.querySelectorAll('[data-resposta]'), function (x) { return !x.hidden; }); aVista(vis[vis.length - 1]);
        var r = box.querySelector('[data-resposta="' + v + '"]');
        anunciar('Escolheste: ' + (b.getAttribute('data-diz') || b.textContent) + '. ' + (r ? r.textContent.replace(/\s+/g, ' ').trim() : ''));
      });
    });
  }
  /* olhar de lado: o botão alterna uma classe no alvo e o seu próprio texto */
  function olhar(b) {
    var alvo = document.querySelector(b.getAttribute('data-olhar')), dep = document.getElementById(b.getAttribute('aria-controls'));
    var t0 = b.textContent, t1 = b.getAttribute('data-outro') || t0;
    b.setAttribute('aria-pressed', 'false');
    b.addEventListener('click', function () {
      var on = b.getAttribute('aria-pressed') !== 'true';
      b.setAttribute('aria-pressed', String(on)); b.textContent = on ? t1 : t0;
      if (alvo) alvo.classList.toggle('de-lado', on);
      if (dep) { dep.hidden = !on; if (on) aVista(dep); }
      anunciar(on && dep ? dep.textContent.replace(/\s+/g, ' ').trim() : 'De frente outra vez.');
    });
  }
  function alterna(b) {
    var p = document.getElementById(b.getAttribute('aria-controls'));
    if (!p) return;
    b.addEventListener('click', function () {
      var on = b.getAttribute('aria-expanded') !== 'true';
      b.setAttribute('aria-expanded', String(on)); p.hidden = !on;
    });
  }

  window.Cartaz = { ler: ler, feitas: feitas, n: n, hoje: hoje, dia: dia, dias: dias, data: data, diaSemana: diaSemana, esc: esc, proj: proj, reduz: reduz, anunciar: anunciar, abrir: abrir, abrirAncora: abrirAncora, estreito: estreito };

  function pronto() {
    [].forEach.call(document.querySelectorAll('[data-mexe]'), mexe);
    [].forEach.call(document.querySelectorAll('.cartazes>.cartaz'), function (c, i) { c.style.setProperty('--i', i); });
    [].forEach.call(document.querySelectorAll('[data-decide]'), decide);
    [].forEach.call(document.querySelectorAll('[data-olhar]'), olhar);
    [].forEach.call(document.querySelectorAll('.porta-abre'), porta);
    [].forEach.call(document.querySelectorAll('[data-alterna]'), alterna);
    [].forEach.call(document.querySelectorAll('.faixa .nos i'), function (x, k) { x.style.setProperty('--k', k); });
    window.addEventListener('hashchange', abrirAncora);
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (a) setTimeout(abrirAncora, 0);
    });
    setTimeout(function () { d.classList.remove('entra'); }, 2600);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pronto); else pronto();
})();
