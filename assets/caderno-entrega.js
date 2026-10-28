/* «Entregar ao docente», no caderno (28/10/2026). O aluno escreve o código que o docente lhe deu (nunca o nome), vê uma
   pré-visualização curta e descarrega entrega-<CÓDIGO>-<AAAA-MM-DD>.json, que envia pelo canal combinado na turma.
   Os registos são os de «Guardar num ficheiro» filtrados pela lista de progresso-registos.js (só as chaves aceites, sem
   nome). O código não fica guardado no aparelho: num aparelho partilhado, o aluno seguinte não encontra o código do
   anterior (28/10/2026, revisão). Só lê o armazenamento; não escreve nele. Sem rede. */
(function (root, doc) {
  'use strict';
  var E = root.EPIRegistos, S = doc.getElementById('entregar');
  if (!S || !E) return;
  var form = S.querySelector('[data-pe-form]'), campo = S.querySelector('[data-pe-codigo]'), erro = S.querySelector('[data-pe-erro]'),
    pre = S.querySelector('[data-pe-pre]'), estado = S.querySelector('[data-pe-estado]'), PEND = null;

  function diz(t, c) { estado.textContent = t; estado.className = 'pf-e' + (c ? ' ' + c : ''); }
  function mostraErro(t) { erro.textContent = t || ''; campo.setAttribute('aria-invalid', t ? 'true' : 'false'); }
  function aparelho() {
    var m = {};
    try { for (var i = 0; i < root.localStorage.length; i++) { var k = root.localStorage.key(i); if (k) m[k] = root.localStorage.getItem(k); } }
    catch (e) { /* armazenamento bloqueado: não há registos */ }
    return m;
  }
  function fechar() { pre.hidden = true; PEND = null; }
  function plural(n, um, muitos) { return n + ' ' + (n === 1 ? um : muitos); }

  function mostrar(codigo, r) {
    S.querySelector('[data-pe-cod]').textContent = 'Código: ' + codigo;
    var ng = Object.keys(r.grupos).length;
    S.querySelector('[data-pe-resumo]').textContent = (r.n === 1 ? 'Vai 1 registo' : 'Vão ' + r.n + ' registos') + (ng === 1 ? ', deste percurso:' : ', destes percursos:');
    var ul = S.querySelector('[data-pe-lista]');
    ul.textContent = '';
    E.GRUPOS.forEach(function (g) {
      if (!r.grupos[g]) return;
      var li = doc.createElement('li');
      li.textContent = g + ' (' + r.grupos[g] + ')';
      ul.appendChild(li);
    });
    var nota = [], f = r.fora;
    if (r.texto) nota.push('Vão também as respostas que escreveste nos percursos.');
    if (f.prova) nota.push('As provas e os testes ficam neste aparelho.');
    if (f.privada) nota.push(f.privada === 1 ? 'Fica de fora 1 registo com o teu nome.' : 'Ficam de fora ' + f.privada + ' registos com o teu nome.');
    if (f.estragada) nota.push(f.estragada === 1 ? 'Fica de fora 1 registo que não se consegue ler.' : 'Ficam de fora ' + f.estragada + ' registos que não se conseguem ler.');
    var pn = S.querySelector('[data-pe-nota]');
    pn.textContent = nota.join(' ');
    pn.hidden = !nota.length;
    pre.hidden = false;
    diz('');
    try { S.querySelector('[data-pe-pre-t]').focus(); } catch (e) { /* sem foco */ }
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    fechar();
    var c = E.validarCodigo(campo.value);
    if (!c.ok) { mostraErro(c.erro); diz(''); campo.focus(); return; }
    mostraErro('');
    campo.value = c.codigo;
    var r = E.registosParaEntrega(aparelho());
    if (!r.n) { diz('Ainda não há registos para entregar neste aparelho.', 'mal'); return; }
    if (r.n > E.LIM.registos) { diz('Há registos a mais para um só ficheiro. Fala com o docente.', 'mal'); return; }
    var agora = new Date(), texto = JSON.stringify(E.montarEntrega(c.codigo, r.registos, agora), null, 1), b;
    try { b = new Blob([texto], {type: 'application/json'}); } catch (e) { diz('Não consegui preparar o ficheiro neste navegador.', 'mal'); return; }
    if (b.size > E.LIM.ficheiro) { diz('O teu progresso passa de 1 MB e não cabe num ficheiro de entrega. Fala com o docente.', 'mal'); return; }
    PEND = {blob: b, nome: E.nomeEntrega(c.codigo, agora), n: r.n};
    mostrar(c.codigo, r);
  });
  campo.addEventListener('input', function () { if (PEND) { fechar(); diz(''); } });

  S.querySelector('[data-pe-sim]').addEventListener('click', function () {
    if (!PEND) return;
    var p = PEND;
    try {
      var u = URL.createObjectURL(p.blob), a = doc.createElement('a');
      a.href = u; a.download = p.nome; doc.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(u); a.remove(); }, 1000);
      fechar();
      // O passo que falta (enviar) tem o peso de um bloco, e não só de uma linha a verde.
      diz('Falta um passo: envia o ficheiro ' + p.nome + ' (' + plural(p.n, 'registo', 'registos') + ') ao docente, pelo canal combinado na turma. Se não o encontrares, procura nas transferências do telemóvel ou do computador.', 'pe-feito');
    } catch (e) { diz('Não consegui descarregar o ficheiro neste navegador.', 'mal'); }
    try { campo.focus(); } catch (e) { /* sem foco */ }
  });
  S.querySelector('[data-pe-nao]').addEventListener('click', function () {
    fechar();
    diz('Cancelaste: nada foi descarregado.');
    try { campo.focus(); } catch (e) { /* sem foco */ }
  });
}(window, document));
