// 02/11/2026: decisão 137. Motor comum dos fundos animados a traço, igual no Português e no Lente
// (propostas F2 e F4 de melhorias-ngg/fundos.md). Cada fundo é um elemento com data-fundo="<prefixo>" e
// data-fundo-ciclo="<segundos de um ciclo>"; o desenho parado está escrito no SVG e o movimento é a classe <prefixo>-anda.
// Pára: fora do ecrã e com o separador escondido (em pausa), ao fim de dois ciclos e quando o aluno carrega em
// «Parar o desenho» (vale para esta visita: o motor não grava nada no aparelho).
// Nunca anda: com movimento reduzido, na projeção (mesmo que a marca chegue depois de carregar), com poupança de dados
// ou com pouca memória. Sem este script, fica o desenho parado e o botão escondido.
(function () {
  var html = document.documentElement;
  var fundos = [].slice.call(document.querySelectorAll('[data-fundo]'));
  if (!fundos.length) return;
  function projetada() {
    return /[?&]projetar=1(&|$)/.test(location.search) || window.self !== window.top ||
      /(^|\s)(em-projecao|epi-projection)(\s|$)/.test(html.className) ||
      html.hasAttribute('data-cz-projection') || html.hasAttribute('data-cz-reduce');
  }
  var reduzido = !window.matchMedia || !matchMedia('(prefers-reduced-motion: no-preference)').matches;
  var rede = navigator.connection, poupa = !!(rede && rede.saveData) || (navigator.deviceMemory > 0 && navigator.deviceMemory <= 2);
  fundos.forEach(function (f) {
    var p = f.getAttribute('data-fundo'), ciclo = (+f.getAttribute('data-fundo-ciclo') || 40) * 1000;
    var botao = document.querySelector('[data-fundo-botao="' + p + '"]'), relogio = null, visivel = true;
    function anda() { return f.classList.contains(p + '-anda'); }
    function texto() { if (botao) botao.textContent = anda() ? 'Parar o desenho' : 'Pôr o desenho a andar'; }
    function parar() { clearTimeout(relogio); f.classList.remove(p + '-anda'); texto(); }
    function arrancar() {
      if (projetada()) return desligar();
      f.classList.add(p + '-anda'); clearTimeout(relogio); relogio = setTimeout(parar, 2 * ciclo); texto();
    }
    function desligar() { parar(); if (botao) botao.hidden = true; }
    function pausa() { f.classList.toggle('fundo-pausa', !visivel || document.hidden); }
    if (reduzido || poupa || projetada()) return desligar();
    if (botao) {
      botao.hidden = false;
      botao.addEventListener('click', function () { if (anda()) parar(); else arrancar(); });
    }
    arrancar();
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visivel = e[e.length - 1].isIntersecting; pausa(); }).observe(f);
    document.addEventListener('visibilitychange', pausa);
    if ('MutationObserver' in window) new MutationObserver(function () { if (projetada()) desligar(); })
      .observe(html, { attributes: true, attributeFilter: ['class', 'data-cz-projection', 'data-cz-reduce'] });
  });
})();
