/* Resultados da turma (28/10/2026): o docente escolhe ou arrasta os ficheiros que os alunos entregaram no caderno e vê
   uma tabela por código, o pormenor de cada código e um CSV. Os ficheiros leem-se só neste navegador: nada é enviado e
   nada fica guardado (sem armazenamento local nem pedidos de rede); ao fechar a página, tudo desaparece.
   Tudo o que vem dos ficheiros entra na página por textContent e createElement. As regras de leitura (listas, limites,
   chaves proibidas) são as de progresso-registos.js, que o caderno também usa. */
(function (root, doc) {
  'use strict';
  var E = root.EPIRegistos;
  if (!E || root.EPIResultados) return;

  /* ---------- Resumo dos registos (sem DOM) ---------- */
  var MARCAS = ['qs', 'ob', 'lf', 'fj', 'tp', 'on'];
  var PAISES = {PT: 'Portugal', BR: 'Brasil', AO: 'Angola', MZ: 'Moçambique', CV: 'Cabo Verde', GW: 'Guiné-Bissau', ST: 'São Tomé e Príncipe', TL: 'Timor-Leste'};
  var JUIZO = {justica: 'Justiça', etica: 'Ética', estetica: 'Estética'};
  var SECOES = {apresentar: 'Como se apresenta', bairro: 'Cidade', biblioteca: 'Biblioteca', cartaz: 'Cartaz', cd: 'Cidadania (anterior)', cid: 'Cidadania', cidadania: 'Cidadania', conjunto: 'O conjunto', corta: 'Corta!', direitos: 'Direitos e fontes', ficcao: 'Laboratório', gigantes: 'Gigantes', guiao: 'Laboratório', investigar: 'Como se investiga', justica: 'Justiça', lente: 'Lente', ler: 'Como se lê', literatura: 'Literatura mundial', maquina: 'A Máquina das Palavras', margens: 'Margens', narrativas: 'Laboratório', projetos: 'Projetos', sidequests: 'Sidequests', treinos: 'Ginásio', ver: 'Ver para fazer', vozes: 'vozes.'};
  // Os totais que não mudam sem mudar o desenho do percurso (confirmados pelos testes contra as pastas).
  var SESSOES = {'1': {de: 3, ate: 10}, '2': {de: 1, ate: 10}};
  var APOIOS_M1 = 18;
  // O que se conta em cada percurso, pela ordem em que aparece no resumo.
  var CATS = [
    ['licao', 'lição concluída', 'lições concluídas'],
    ['desafio', 'desafio ganho', 'desafios ganhos'],
    ['sintese', 'síntese registada', 'sínteses registadas'],
    ['nota', 'nota escrita', 'notas escritas'],
    ['tarefa', 'guia de tarefa com registo', 'guias de tarefa com registo'],
    ['exercicio', 'exercício concluído', 'exercícios concluídos'],
    ['questionario', 'questionário feito', 'questionários feitos'],
    ['longo', 'trabalho longo concluído', 'trabalhos longos concluídos'],
    ['pessoa', 'pessoa conhecida', 'pessoas conhecidas'],
    ['pais', 'país conquistado', 'países conquistados'],
    ['missao', 'missão feita', 'missões feitas'],
    ['sessao1', 'M1: {n} de 8 sessões com registo (da 03 à 10)'],
    ['sessao2', 'M2: {n} de 10 sessões com registo'],
    ['apoio1', '{n} de ' + APOIOS_M1 + ' apoios do M1 com trabalho registado'],
    ['anterior', 'passo do percurso anterior', 'passos do percurso anterior'],
    ['caso', 'caso concluído', 'casos concluídos'],
    ['resposta', 'resposta escrita', 'respostas escritas'],
    ['passo', 'passo feito', 'passos feitos'],
    ['treino', 'treino feito', 'treinos feitos'],
    ['texto', 'texto lido', 'textos lidos'],
    ['atividade', 'atividade feita', 'atividades feitas'],
    ['visita', 'visita na fase «depois»', 'visitas na fase «depois»']
  ];

  // Só as propriedades próprias: uma chave vinda do ficheiro («constructor», «toString») nunca devolve o protótipo.
  function de(o, k) { return Object.prototype.hasOwnProperty.call(o, k) ? o[k] : undefined; }
  var MODOS = {oral: 'oral', caderno: 'no caderno', anterior: 'a partir de notas anteriores'};
  function num(x) { return typeof x === 'number' && isFinite(x) && x >= 0 ? Math.floor(x) : 0; }
  function pad(x) { x = String(x); return x.length < 2 ? '0' + x : x; }
  function plural(n, um, muitos) { return n + ' ' + (n === 1 ? um : muitos); }
  function bonito(id) { var s = String(id).replace(/[-_]+/g, ' ').trim(); return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''; }
  function palavras(t) { t = String(t || '').trim(); return t ? t.split(/\s+/).length : 0; }
  function lerJSON(v) { try { return JSON.parse(v); } catch (e) { return undefined; } }
  function chaves(o) { return E.ehObj(o) ? Object.keys(o) : []; }
  function data(ms) {
    if (!num(ms)) return '';
    var d = new Date(ms);
    return isNaN(d.getTime()) ? '' : pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear();
  }
  function dataHora(d) {
    if (!d || isNaN(d.getTime())) return '';
    return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear() + ', ' + pad(d.getHours()) + ':' + pad(d.getMinutes());
  }
  function licaoDeId(id) {
    var m = /^m(\d{1,2})-f(\d{1,3})$/i.exec(String(id));
    return m ? 'M' + m[1] + ', lição F' + pad(m[2]) : bonito(id);
  }

  function baralho(j, fem) {
    if (!E.ehObj(j)) return {feito: false, estado: 'registado'};
    var feito = j.lida === true, mel = num(j.melhor), tot = num(j.totalMelhor) || Math.max(num(j.total), mel), tent = num(j.tentativas);
    var p = [feito ? (fem ? 'concluída' : 'concluído') : 'em curso'];
    if (tot) p.push('melhor resultado ' + mel + ' de ' + tot);
    if (tent) p.push(plural(tent, 'tentativa', 'tentativas'));
    return {feito: feito, estado: p.join(', ')};
  }
  // Os registos de secção {feitas:{id:data}}: quantos e quais.
  function feitas(j, cat, nome, extra) {
    if (!E.ehObj(j) || !E.ehObj(j.feitas)) return null;
    var ids = Object.keys(j.feitas), c = {};
    c[cat] = ids.length;
    var lista = ids.map(function (id) { var x = nome ? nome(id) : bonito(id); return extra ? extra(id, x) : x; });
    return {contas: c, estado: ids.length ? lista.join('; ') : 'nada registado'};
  }
  function valorTexto(v) { return typeof v === 'string' ? v : (E.ehObj(v) && typeof v.t === 'string' ? v.t : (E.ehObj(v) && typeof v.texto === 'string' ? v.texto : '')); }
  function textoDe(o, rotulos) {
    var out = [];
    chaves(o).forEach(function (k) {
      var t = valorTexto(o[k]);
      if (t && t.trim()) out.push((rotulos ? rotulos(k) + ': ' : '') + t.trim());
    });
    return out.join('\n\n');
  }
  // As palavras escritas pelo aluno, sem contar os rótulos dos campos.
  function palavrasDe(o) { var n = 0; chaves(o).forEach(function (k) { n += palavras(valorTexto(o[k])); }); return n; }

  // Cada regra: [expressão, função(m, j, v) → {rotulo, estado, contas, texto} ou null (registo sem pormenor)].
  var REGRAS = [
    [/^epi-ultima$/i, function (m, j) { return E.ehObj(j) && typeof j.id === 'string' ? {rotulo: 'Última lição aberta', estado: licaoDeId(j.id) + (num(j.t) ? ', a ' + data(j.t) : '')} : null; }],
    [/^licao-m(\d{1,2})-f(\d{1,3})$/i, function (m, j) { var b = baralho(j, true); return {rotulo: 'M' + (+m[1]) + ', lição F' + pad(+m[2]), estado: b.estado, contas: {licao: b.feito ? 1 : 0}}; }],
    [/^licao-/i, null],
    [/^(?:desafio-(?:unidade-v2-)?|chefe-)m(\d{1,2})-u(\d{1,2})$/i, function (m, j) {
      // «vencido» é a marca dos desafios ganhos antes de 10/10 (chefe-…); o Português conta as duas.
      var b = baralho(j, false), g = E.ehObj(j) && (j.ganho === true || j.vencido === true);
      return {rotulo: 'M' + (+m[1]) + ', desafio da unidade ' + (+m[2]), estado: (g ? 'ganho' : 'por ganhar') + (b.estado.indexOf('melhor') >= 0 ? ', ' + b.estado.replace(/^[^,]*, /, '') : ''), contas: {desafio: g ? 1 : 0}};
    }],
    [/^percurso-sintese-m(\d{1,2})-u(\d{1,2})$/i, function (m, j) {
      var f = E.ehObj(j) && j.feita === true, modo = E.ehObj(j) && typeof j.modo === 'string' ? de(MODOS, j.modo) : '';
      return {rotulo: 'M' + (+m[1]) + ', síntese da unidade ' + (+m[2]), estado: f ? 'registada' + (modo ? ' (' + modo + ')' : '') : 'por registar', contas: {sintese: f ? 1 : 0}};
    }],
    [/^percurso-(?:v2-)?m(\d{1,2})-u(\d{1,2})$/i, function (m, j, v) {
      var n = palavras(v);
      return {rotulo: 'M' + (+m[1]) + ', notas da unidade ' + (+m[2]), estado: plural(n, 'palavra', 'palavras'), contas: {nota: n ? 1 : 0}, texto: v};
    }],
    [/^percurso-/i, null],
    [/^(rota|balanco)-m(\d{1,2})$/i, function (m, j) {
      if (!E.ehObj(j)) return null;
      var partes = [], textos = [], n = 0;
      Object.keys(j).forEach(function (t) {
        var x = j[t]; if (!E.ehObj(x)) return;
        var feito = Array.isArray(x.feito) ? x.feito.length : 0, auto = chaves(x.auto).length, campos = textoDe(x.campos, bonito);
        var js = chaves(x.auto).map(function (i) { var a = x.auto[i]; return E.ehObj(a) && typeof a.j === 'string' && a.j.trim() ? 'Critério ' + (num(+i) + 1) + (num(a.n) ? ' (nível ' + num(a.n) + ')' : '') + ': ' + a.j.trim() : ''; }).filter(Boolean).join('\n');
        if (!feito && !auto && !campos) return;
        n++;
        partes.push('tarefa ' + bonito(t) + ': ' + plural(feito, 'critério verificado', 'critérios verificados') + (auto ? ', ' + plural(auto, 'autoavaliação', 'autoavaliações') : ''));
        if (campos || js) textos.push('Tarefa ' + bonito(t) + '\n' + [campos, js].filter(Boolean).join('\n\n'));
      });
      return {rotulo: 'M' + (+m[2]) + ', ' + (m[1].toLowerCase() === 'rota' ? 'guia da tarefa' : 'balanço'), estado: partes.join('; ') || 'sem registo', contas: {tarefa: n}, texto: textos.join('\n\n')};
    }],
    [/^epi-pt-quiz-m(\d{1,2})$/i, function (m, j) {
      var ks = chaves(j).filter(function (i) { return /^\d{1,3}$/.test(i) && typeof j[i] === 'number'; });
      return {rotulo: 'M' + (+m[1]) + ', questionários', estado: ks.map(function (i) { return 'questionário ' + (num(+i) + 1) + ' com ' + plural(num(j[i]), 'certa', 'certas'); }).join('; ') || 'sem registo', contas: {questionario: ks.length}};
    }],
    [/^epi-pt-longos$/i, function (m, j) {
      var r = feitas(j, 'longo', function (id) { var x = /^m(\d{1,2})-(.+)$/i.exec(id); return x ? 'M' + x[1] + ', ' + bonito(x[2]) : bonito(id); });
      return r && {rotulo: 'Trabalhos longos', estado: r.estado, contas: r.contas};
    }],
    [/^epi-pt-longos-m(\d{1,2})-(.+)$/i, function (m, j) { return {rotulo: 'M' + (+m[1]) + ', trabalho longo «' + bonito(m[2]) + '»', estado: baralho(j, false).estado}; }],
    [/^epi-pt-ler-a-fundo-tabacaria$/i, function (m, j) {
      if (!E.ehObj(j)) return null;
      var f = j.passo === 5 && typeof j.t5 === 'string' && !!j.t5.trim();
      return {rotulo: 'M7, ler a fundo «Tabacaria»', estado: f ? 'concluído' : 'em curso', contas: {exercicio: f ? 1 : 0}, texto: [j.t4, j.t5].filter(function (t) { return typeof t === 'string' && t.trim(); }).join('\n\n')};
    }],
    [/^epi-pt-(.+)$/i, function (m, j) {
      if (!E.ehObj(j)) return null;
      var n = num(j.n), i = num(j.i), fim = j.fim === true || (n > 0 && i >= n), pts = 0;
      chaves(j.p).forEach(function (k) { pts += num(j.p[k]); });
      var est = fim ? 'concluído' : (i ? 'em curso, passo ' + i + (n ? ' de ' + n : '') : 'começado');
      return {rotulo: 'Exercício «' + bonito(m[1]) + '»', estado: est + (pts ? ', ' + plural(pts, 'ponto', 'pontos') : ''), contas: {exercicio: fim ? 1 : 0}, texto: textoDe(j.r, function (k) { return 'Passo ' + (num(+k) + 1); })};
    }],
    [/^epi-atlas$/i, function (m, j) {
      if (!E.ehObj(j)) return null;
      var con = 0, desc = 0;
      chaves(j.p).forEach(function (q) {
        var x = j.p[q], k = 0;
        if (E.ehObj(x)) MARCAS.forEach(function (mm) { if (x[mm]) k++; });
        if (k >= 2) con++; if (k >= 1) desc++;
      });
      var dom = chaves(j.dom).filter(function (p) { return /^[A-Z]{2}$/.test(p); });
      return {rotulo: 'Atlas', estado: plural(con, 'pessoa conhecida', 'pessoas conhecidas') + ', ' + plural(desc, 'descoberta', 'descobertas') + (dom.length ? '; ' + (dom.length === 1 ? 'país conquistado: ' : 'países conquistados: ') + dom.map(function (p) { return de(PAISES, p) || p; }).join(', ') : ''), contas: {pessoa: con, pais: dom.length}};
    }],
    [/^epi-atlas-v2$/i, null],
    [/^atlas-([a-z]{2})-([a-z0-9-]+)$/i, function (m, j) {
      var b = baralho(j, false), p = m[1].toUpperCase();
      return {rotulo: 'Atlas, ' + (de(PAISES, p) || p) + ', ' + (m[2].toLowerCase() === 'revisao' ? 'revisão' : 'missão ' + m[2]), estado: b.estado.replace(/^concluído/, 'feita').replace(/^em curso/, 'em curso'), contas: {missao: b.feito ? 1 : 0}};
    }],
    [/^epi-bairro$/i, function (m, j) {
      var r = feitas(j, 'missao', function (id) { var x = /^m(\d{1,3})$/i.exec(id); return x ? 'missão ' + x[1] : bonito(id); });
      return r && {rotulo: 'Cidade', estado: r.estado, contas: r.contas};
    }],
    [/^bairro-m(\d{1,3})$/i, function (m, j) { return {rotulo: 'Cidade, missão ' + m[1], estado: baralho(j, false).estado}; }],
    [/^lente-cidadania-m(\d)-sessoes-v\d$/i, function (m, j) {
      if (!E.ehObj(j) || !E.ehObj(j.sessions)) return null;
      var lim = SESSOES[m[1]], ok = [], curso = [], c = {};
      Object.keys(j.sessions).sort().forEach(function (id) {
        var s = j.sessions[id], n = /^\d{2}$/.test(id) ? +id : 0;
        if (!E.ehObj(s) || !lim || n < lim.de || n > lim.ate) return;
        if (s.done === true) ok.push(id); else if (typeof s.stage === 'number') curso.push(id + ' (passo ' + (num(s.stage) + 1) + ')');
      });
      c['sessao' + m[1]] = ok.length;
      return {rotulo: 'Cidadania M' + m[1] + ', sessões', estado: (ok.length ? 'registadas: ' + ok.join(', ') : 'nenhuma registada') + (curso.length ? '; em curso: ' + curso.join(', ') : ''), contas: lim ? c : {}};
    }],
    [/^lente-cidadania-m1-v\d$/i, function (m, j) {
      if (!E.ehObj(j) || !E.ehObj(j.done)) return null;
      var ids = [];
      for (var i = 1; i <= APOIOS_M1; i++) { var id = 'F' + pad(i); if (j.done[id] === true) ids.push(pad(i)); }
      return {rotulo: 'Cidadania M1, apoios', estado: ids.length ? 'com trabalho registado: ' + ids.join(', ') : 'nenhum registado', contas: {apoio1: ids.length}};
    }],
    [/^(?:epi-cid-m\d-.+|epi-cidadania-m\d-butler-singer)-conclusao$/i, function (m, j) {
      var r = feitas(j, 'caso', function (id) { return bonito(String(id).replace(/^cid-m\d-/i, '')); });
      return r && {rotulo: 'Cidadania, casos', estado: r.estado, contas: r.contas};
    }],
    [/^epi-cidadania-m(\d)$/i, function (m, j) {
      var r = feitas(j, 'anterior');
      return r && {rotulo: 'Cidadania M' + m[1] + ', percurso anterior', estado: r.estado, contas: r.contas};
    }],
    [/^epi-(?:cidadania-m\d|cid-m\d)-(.+)$/i, function (m, j) { return {rotulo: 'Cidadania: ' + bonito(m[1]), estado: baralho(j, false).estado}; }],
    [/^cd(\d?)-(.+)$/i, function (m, j, v) {
      var a = /^aula(\d+)-(\d+)$/i.exec(m[2]), b = /^cd(\d)-aula(\d+)$/i.exec(m[2]);
      var rot = a ? 'Cidadania, aula ' + (+a[1]) + ', pergunta ' + (+a[2]) : (b ? 'Cidadania M' + b[1] + ', aula ' + (+b[2]) : 'Cidadania: ' + bonito(m[2]));
      var t, n, pal, uma = false;
      if (E.ehObj(j)) { var copia = {}; chaves(j).forEach(function (k) { if (k !== 'nome') copia[k] = j[k]; }); t = textoDe(copia, bonito); n = t ? t.split('\n\n').length : 0; pal = palavrasDe(copia); }
      else { t = v; n = String(v).trim() ? 1 : 0; pal = palavras(v); uma = true; }
      var est = !n ? 'sem resposta' : (uma ? 'respondida' : plural(n, 'resposta', 'respostas')) + ', ' + plural(pal, 'palavra', 'palavras');
      return {rotulo: rot, estado: est, contas: {resposta: n}, texto: t};
    }],
    [/^lente-(justica|etica|estetica)-licao-(\d)$/i, function (m, j) { var b = baralho(j, true); return {rotulo: de(JUIZO, m[1].toLowerCase()) + ', lição ' + m[2], estado: b.estado, contas: {licao: b.feito ? 1 : 0}}; }],
    [/^epi-[a-z]+(?:-m\d)?(?::visto|:arco|:dupla)$/i, null],
    [/^epi-treinos$/i, function (m, j) {
      var vezes = E.ehObj(j) && E.ehObj(j.vezes) ? j.vezes : {};
      var r = feitas(j, 'treino', null, function (id, x) { var n = num(vezes[id]); return n > 1 ? x + ' (' + n + ' vezes)' : x; });
      return r && {rotulo: 'Ginásio', estado: r.estado, contas: r.contas};
    }],
    [/^epi-ver$/i, function (m, j) {
      if (!E.ehObj(j)) return null;
      var f = chaves(j.feitas), v = chaves(j.vistos);
      return {rotulo: 'Ver para fazer', estado: plural(f.length, 'feita', 'feitas') + (f.length ? ' (' + f.join(', ') + ')' : '') + ', ' + plural(v.length, 'vista', 'vistas'), contas: {atividade: f.length}};
    }],
    [/^epi-(investigar|ler|apresentar|direitos|margens)$/i, function (m, j) { var r = feitas(j, 'passo'); return r && {rotulo: de(SECOES, m[1].toLowerCase()), estado: r.estado, contas: r.contas}; }],
    [/^epi-biblioteca$/i, function (m, j) { var r = feitas(j, 'texto'); return r && {rotulo: 'Biblioteca', estado: r.estado, contas: r.contas}; }],
    [/^epi-([a-z]+)$/i, function (m, j) { var r = feitas(j, 'atividade'); return r && {rotulo: de(SECOES, m[1].toLowerCase()) || bonito(m[1]), estado: r.estado, contas: r.contas}; }],
    [/^epi-justica-sandel-v\d$/i, function (m, j) { var b = baralho(j, false); return {rotulo: 'Justiça, Aplicar (Sandel)', estado: b.estado, contas: {atividade: b.feito ? 1 : 0}}; }],
    [/^epi-(ficcao|guiao|justica)-(.+)$/i, function (m, j) { var b = baralho(j, false); return {rotulo: de(SECOES, m[1].toLowerCase()) + ': ' + bonito(m[2]), estado: b.estado, contas: {atividade: b.feito ? 1 : 0}}; }],
    [/^epi-([a-z]+)-(.+)$/i, function (m, j) { return {rotulo: (de(SECOES, m[1].toLowerCase()) || bonito(m[1])) + ': ' + bonito(m[2]), estado: baralho(j, false).estado}; }],
    [/^visita-(.+)$/i, function (m, j) {
      if (!E.ehObj(j)) return null;
      var notas = Array.isArray(j.notas) ? j.notas.filter(E.ehObj) : [], d = j.fase === 'depois';
      var t = notas.map(function (n) { return [n.paragem, n.texto].filter(function (x) { return typeof x === 'string' && x.trim(); }).join(': '); }).filter(Boolean);
      var campos = textoDe(j.campos, bonito);
      return {rotulo: 'Visita: ' + bonito(String(m[1]).replace(/^visita-/i, '')), estado: (typeof j.fase === 'string' ? 'fase «' + j.fase.slice(0, 20) + '»' : 'sem fase') + ', ' + plural(notas.length, 'nota', 'notas'), contas: {visita: d ? 1 : 0}, texto: t.concat(campos ? [campos] : []).join('\n\n')};
    }]
  ];

  function analisar(k, v) {
    var j = lerJSON(v);
    for (var i = 0; i < REGRAS.length; i++) {
      var m = REGRAS[i][0].exec(k);
      if (!m) continue;
      if (!REGRAS[i][1]) return null;
      var r = REGRAS[i][1](m, j, v);
      if (!r) return null;
      r.chave = k; r.grupo = E.grupoDe(k); r.contas = r.contas || {};
      if (typeof r.texto === 'string' && r.texto.trim()) r.palavras = palavras(r.texto); else delete r.texto;
      return r;
    }
    return null;
  }

  /* A ordem do pormenor (28/10/2026): «Última lição aberta» primeiro; depois por módulo; dentro do módulo, as lições pelo
     número e a seguir cada unidade (desafio, síntese, notas); o guia da tarefa e o balanço no fim do módulo; o que não tem
     módulo, no fim do grupo. Em empate, a ordem natural da chave. */
  var TIPOS = [/^licao-/i, /^(desafio|chefe)-/i, /^percurso-sintese-/i, /^percurso-/i, /^rota-/i, /^balanco-/i];
  function ordemDe(k) {
    if (/^epi-ultima$/i.test(k)) return [-1, 0, 0, 0];
    var m = /(?:^|-)m(\d{1,2})(?=-|$)/i.exec(k), f = /^licao-m\d{1,2}-f(\d{1,3})/i.exec(k), u = /-u(\d{1,2})(?=-|$)/i.exec(k), t = TIPOS.length;
    for (var i = 0; i < TIPOS.length; i++) if (TIPOS[i].test(k)) { t = i; break; }
    return [m ? +m[1] : 1000, f ? 0 : 1, f ? +f[1] : (u ? +u[1] : 1000), t];
  }
  function porOrdem(a, b) {
    var x = ordemDe(a), y = ordemDe(b);
    for (var i = 0; i < x.length; i++) if (x[i] !== y[i]) return x[i] - y[i];
    return a.localeCompare(b, 'pt-PT', {numeric: true});
  }
  function resumir(registos) {
    var G = {};
    Object.keys(registos || {}).sort(porOrdem).forEach(function (k) {
      var g = E.grupoDe(k), x = G[g] || (G[g] = {n: 0, contas: {}, itens: []});
      x.n++;
      var it = analisar(k, registos[k]);
      if (!it) return;
      x.itens.push(it);
      Object.keys(it.contas).forEach(function (c) { x.contas[c] = (x.contas[c] || 0) + num(it.contas[c]); });
    });
    return G;
  }
  function textoGrupo(g) {
    if (!g) return '';
    var p = [];
    CATS.forEach(function (c) {
      if (!(c[0] in g.contas)) return;
      var n = g.contas[c[0]];
      p.push(c.length === 2 ? c[1].replace('{n}', n) : plural(n, c[1], c[2]));
    });
    return p.length ? p.join('; ') : plural(g.n, 'registo', 'registos');
  }
  function foraTexto(f) {
    if (!f) return '';
    var p = [];
    if (f.sala) p.push(plural(f.sala, 'registo da Sala, desligada', 'registos da Sala, desligada'));
    if (f.aparelho) p.push(plural(f.aparelho, 'registo que só serve o aparelho', 'registos que só servem o aparelho'));
    if (f.prova) p.push(plural(f.prova, 'registo de provas e testes, que ficam no aparelho', 'registos de provas e testes, que ficam no aparelho'));
    if (f.privada) p.push(plural(f.privada, 'registo com nome, retirado', 'registos com nome, retirados'));
    if (f.desconhecida) p.push(plural(f.desconhecida, 'registo que o caderno não entrega', 'registos que o caderno não entrega'));
    return p.join('; ');
  }
  function foraTotal(f) { var n = 0; if (f) Object.keys(f).forEach(function (k) { n += num(f[k]); }); return n; }

  /* A linha de um ficheiro aceite (sem DOM): o que a tabela, o pormenor e o CSV mostram. A data vem do ficheiro e o aluno
     controla-a: mais de um dia à frente do relógio deste computador, fica marcada «data no futuro» (28/10/2026). */
  var DIA = 864e5;
  function linha(v, ficheiro, modificado, agora) {
    var ok = v.data && !isNaN(v.data.getTime()), ref = typeof agora === 'number' ? agora : Date.now();
    return {formato: v.formato, codigo: v.codigo, ficheiro: String(ficheiro || ''), rotulo: String(ficheiro || ''), data: ok ? v.data : null,
      futuro: !!ok && v.data.getTime() > ref + DIA, modificado: num(modificado), n: v.n, fora: v.fora, resumo: resumir(v.registos)};
  }
  // Uma data no futuro (ou nenhuma) nunca ganha a uma data plausível.
  function tempo(l) { return l.data && !l.futuro ? l.data.getTime() : -Infinity; }
  // A mais recente de duas linhas com o mesmo código: pela data da entrega, depois pela data do ficheiro, depois pelo nome.
  function maisRecente(a, b) {
    if (tempo(a) !== tempo(b)) return tempo(a) > tempo(b) ? a : b;
    if (a.modificado !== b.modificado) return a.modificado > b.modificado ? a : b;
    return a.ficheiro >= b.ficheiro ? a : b;
  }
  // O texto da data na tabela e no CSV: «(guardado)» nos progressos antigos, «(data no futuro)» quando é suspeita.
  function dataTexto(l) {
    var d = dataHora(l.data);
    if (!d) return 'sem data';
    return d + (l.futuro ? ' (data no futuro)' : (l.formato === 'epi-progresso' ? ' (guardado)' : ''));
  }
  // O aviso de duas entregas com o mesmo código, curto; os nomes dos ficheiros ficam no pormenor.
  function avisoDuplicado(fica, sai) {
    var df = dataHora(fica.data), ds = dataHora(sai.data);
    var qual = function (l, d) { return d ? 'a de ' + d + (l.futuro ? ' (data no futuro)' : '') : 'a que não tem data'; };
    var t = fica.codigo + ' tem duas entregas. ';
    if (sai.futuro && !fica.futuro) return t + 'Ficou ' + qual(fica, df) + '; a outra tem data no futuro (' + ds + ') e ficou de fora.';
    if (df === ds) return t + 'As duas têm a mesma data: ficou «' + fica.ficheiro + '» e «' + sai.ficheiro + '» ficou de fora.';
    return t + 'Ficou ' + qual(fica, df) + '; ' + qual(sai, ds) + ' ficou de fora.';
  }
  function ordenar(L, ordem) {
    var s = ordem === 'desc' ? -1 : 1;
    return L.slice().sort(function (a, b) {
      if (!!a.codigo !== !!b.codigo) return a.codigo ? -1 : 1;
      var x = a.codigo || a.rotulo, y = b.codigo || b.rotulo;
      return s * x.localeCompare(y, 'pt-PT', {numeric: true, sensitivity: 'base'});
    });
  }
  function gruposPresentes(L) {
    return E.GRUPOS.filter(function (g) { return L.some(function (l) { return l.resumo[g] && l.resumo[g].n; }); });
  }

  /* CSV para o Excel em pt-PT: BOM UTF-8, «;», CRLF, todas as células entre aspas (aspas internas duplicadas) e um
     apóstrofo à frente de uma célula que comece por = + - @, tabulação ou retorno (injeção de fórmulas). */
  function celula(v) {
    var s = v == null ? '' : String(v);
    if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;
    return '"' + s.replace(/"/g, '""') + '"';
  }
  function csv(L, grupos) {
    grupos = grupos || gruposPresentes(L);
    var linhas = [['Código', 'Ficheiro', 'Data', 'Registos'].concat(grupos, ['Ficaram de fora'])];
    L.forEach(function (l) {
      linhas.push([l.codigo || 'sem código', l.rotulo, dataTexto(l), l.n].concat(grupos.map(function (g) { return textoGrupo(l.resumo[g]); }), [foraTexto(l.fora)]));
    });
    return '﻿' + linhas.map(function (r) { return r.map(celula).join(';'); }).join('\r\n') + '\r\n';
  }

  // Uma assinatura do conteúdo (FNV-1a), para dar pelo mesmo ficheiro escolhido duas vezes.
  function assinatura(t) {
    var h = 0x811c9dc5;
    for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0; }
    return h.toString(16) + ':' + t.length;
  }

  root.EPIResultados = Object.freeze({analisar: analisar, resumir: resumir, textoGrupo: textoGrupo, foraTexto: foraTexto, linha: linha,
    maisRecente: maisRecente, avisoDuplicado: avisoDuplicado, dataTexto: dataTexto, ordenar: ordenar, gruposPresentes: gruposPresentes,
    celula: celula, csv: csv, assinatura: assinatura, dataHora: dataHora});

  /* ---------- A página ---------- */
  var P = doc && doc.querySelector ? doc.querySelector('[data-rt]') : null;
  if (!P) return;
  var input = P.querySelector('[data-rt-input]'), zona = P.querySelector('[data-rt-zona]'), estadoEl = P.querySelector('[data-rt-estado]'),
    avisosC = P.querySelector('[data-rt-avisos-c]'), avisosL = P.querySelector('[data-rt-avisos]'),
    recusadosC = P.querySelector('[data-rt-recusados-c]'), recusadosL = P.querySelector('[data-rt-recusados]'),
    tabelaC = P.querySelector('[data-rt-tabela-c]'), tabelaD = P.querySelector('[data-rt-tabela-d]'), vazio = P.querySelector('[data-rt-vazio]'), pormenor = P.querySelector('[data-rt-pormenor]'),
    pormenorVazio = P.querySelector('[data-rt-pormenor-vazio]'), bCsv = P.querySelector('[data-rt-csv]'), bLimpar = P.querySelector('[data-rt-limpar]');
  var S = {linhas: [], vistos: {}, ordem: 'asc', seq: 0};

  function el(tag, cls, texto) { var e = doc.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; }
  function dizer(t) { estadoEl.textContent = t; }
  // As duas listas mostram o último lote: um ficheiro corrigido que entra deixa de aparecer como recusado (28/10/2026).
  function lista(ul, cont, itens) {
    ul.textContent = '';
    itens.forEach(function (t) { ul.appendChild(el('li', null, t)); });
    cont.hidden = !ul.children.length;
  }

  function lerTexto(f) {
    if (typeof f.text === 'function') return f.text();
    return new Promise(function (ok, mal) { var r = new FileReader(); r.onload = function () { ok(String(r.result || '')); }; r.onerror = mal; r.readAsText(f); });
  }
  function ler(f) {
    if (f.size > E.LIM.ficheiro) return Promise.resolve({f: f, erro: 'O ficheiro tem mais de 1 MB.'});
    return lerTexto(f).then(function (t) { return {f: f, t: t}; }, function () { return {f: f, erro: 'O navegador não conseguiu ler o ficheiro.'}; });
  }

  function receber(fl) {
    var fs = Array.prototype.slice.call(fl || []);
    if (!fs.length) return;
    dizer(fs.length === 1 ? 'A ler 1 ficheiro…' : 'A ler ' + fs.length + ' ficheiros…');
    Promise.all(fs.map(ler)).then(function (res) {
      var entraram = 0, avisos = [], recusados = [], agora = Date.now();
      res.forEach(function (r) {
        var nome = String(r.f.name || 'sem nome');
        if (r.erro) { recusados.push('«' + nome + '»: ' + r.erro); return; }
        var sig = assinatura(r.t);
        if (S.vistos[sig]) { avisos.push('«' + nome + '» já tinha sido lido: não entrou outra vez.'); return; }
        var v = E.validarFicheiro(r.t);
        if (v.erro) { recusados.push('«' + nome + '»: ' + v.erro); return; }
        S.vistos[sig] = 1;
        var l = linha(v, nome, r.f.lastModified, agora);
        l.id = ++S.seq;
        if (l.formato === 'epi-entrega') {
          var i = -1;
          S.linhas.forEach(function (x, k) { if (x.codigo === l.codigo) i = k; });
          if (i >= 0) {
            var velha = S.linhas[i], fica = maisRecente(l, velha), sai = fica === l ? velha : l;
            avisos.push(avisoDuplicado(fica, sai));
            if (fica === l) { S.linhas[i] = l; entraram++; }
            return;
          }
        } else {
          var iguais = S.linhas.filter(function (x) { return !x.codigo && x.ficheiro === nome; }).length;
          if (iguais) l.rotulo = nome + ' (' + (iguais + 1) + ')';
        }
        S.linhas.push(l); entraram++;
      });
      lista(avisosL, avisosC, avisos);
      lista(recusadosL, recusadosC, recusados);
      desenhar();
      var x = [];
      if (recusados.length) x.push(recusados.length === 1 ? '1 recusado' : recusados.length + ' recusados');
      if (avisos.length) x.push(avisos.length === 1 ? '1 aviso' : avisos.length + ' avisos');
      var t = entraram ? [entraram === 1 ? 'Entrou 1 ficheiro' : 'Entraram ' + entraram + ' ficheiros'].concat(x).join(', ') + '.'
        : 'Não entrou nenhum ficheiro novo' + (x.length ? ': ' + x.join(', ') : '') + '.';
      dizer(t + (S.linhas.length ? ' A tabela tem ' + plural(S.linhas.length, 'linha', 'linhas') + '.' : ''));
    });
  }

  // A célula do código é a ligação para o pormenor: fica sempre à vista, na coluna fixa (28/10/2026).
  function celulaCodigo(l) {
    var c = el('th'), a = el('a', 'rt-ir');
    c.scope = 'row';
    a.href = '#rt-p-' + l.id;
    if (l.codigo) { a.appendChild(el('span', 'rt-cod', l.codigo)); }
    else { a.appendChild(el('span', 'rt-sem', 'sem código')); a.appendChild(el('span', 'rt-ficheiro', l.rotulo)); }
    a.addEventListener('click', function (ev) { ev.preventDefault(); abrirPormenor(l.id); });
    c.appendChild(a);
    return c;
  }
  function abrirPormenor(id) {
    var d = doc.getElementById('rt-p-' + id);
    if (!d) return;
    d.open = true;
    var s = d.querySelector('summary');
    if (s) { s.focus(); }
    if (d.scrollIntoView) d.scrollIntoView({block: 'start'});
  }

  function desenhar() {
    var L = ordenar(S.linhas, S.ordem), grupos = gruposPresentes(L);
    tabelaC.textContent = ''; pormenor.textContent = '';
    vazio.hidden = !!L.length; tabelaC.hidden = !L.length; tabelaD.hidden = !L.length;
    pormenorVazio.textContent = L.length ? 'Carrega num código para abrir o pormenor.' : 'Escolhe ficheiros para veres o pormenor de cada código.';
    bCsv.disabled = !L.length; bLimpar.disabled = !L.length && !avisosL.children.length && !recusadosL.children.length;
    if (!L.length) return;
    // A legenda é curta (só o nome da tabela, para o leitor de ecrã); a explicação fica num parágrafo fora do contentor que desliza.
    var t = el('table', 'guide-table rt-tabela'), cap = el('caption', 'rt-so-leitor', 'Resultados da turma, uma linha por código'),
      th = el('thead'), tr = el('tr'), tb = el('tbody');
    t.appendChild(cap);
    var hc = el('th'); hc.scope = 'col'; hc.setAttribute('aria-sort', S.ordem === 'desc' ? 'descending' : 'ascending');
    var bo = el('button', 'rt-ordenar'); bo.type = 'button';
    bo.appendChild(el('span', null, 'Código'));
    var seta = el('span', null, S.ordem === 'desc' ? '↓' : '↑'); seta.setAttribute('aria-hidden', 'true'); bo.appendChild(seta);
    bo.addEventListener('click', function () { S.ordem = S.ordem === 'desc' ? 'asc' : 'desc'; desenhar(); var b = tabelaC.querySelector('.rt-ordenar'); if (b) b.focus(); dizer('Tabela ordenada pelo código, ' + (S.ordem === 'desc' ? 'de Z para A.' : 'de A para Z.')); });
    hc.appendChild(bo); tr.appendChild(hc);
    ['Data', 'Registos'].concat(grupos).forEach(function (n, i) { var h = el('th', i === 1 ? 'rt-num' : null, n); h.scope = 'col'; tr.appendChild(h); });
    th.appendChild(tr); t.appendChild(th);
    L.forEach(function (l) {
      var r = el('tr');
      r.appendChild(celulaCodigo(l));
      r.appendChild(el('td', l.futuro ? 'rt-suspeita' : null, dataTexto(l)));
      r.appendChild(el('td', 'rt-num', String(l.n)));
      grupos.forEach(function (g) { r.appendChild(el('td', null, l.resumo[g] ? textoGrupo(l.resumo[g]) : '')); });
      tb.appendChild(r);
      pormenor.appendChild(detalhe(l));
    });
    t.appendChild(tb); tabelaC.appendChild(t);
  }

  function detalhe(l) {
    var d = el('details', 'rt-p'); d.id = 'rt-p-' + l.id;
    var s = el('summary');
    if (l.codigo) s.appendChild(el('span', 'rt-cod', l.codigo)); else { s.appendChild(el('span', 'rt-sem', 'sem código')); s.appendChild(el('span', 'rt-ficheiro', l.rotulo)); }
    // Num progresso antigo, a data é a de quando o aluno o guardou, não a de uma entrega.
    var quando = l.formato === 'epi-progresso' ? (l.n === 1 ? ', guardado a ' : ', guardados a ') : (l.n === 1 ? ', entregue a ' : ', entregues a ');
    s.appendChild(el('span', 'rt-p-n', plural(l.n, 'registo', 'registos') + (l.data ? quando + dataHora(l.data) + (l.futuro ? ' (data no futuro)' : '') : ', sem data')));
    d.appendChild(s);
    d.appendChild(el('p', 'rt-p-f', 'Ficheiro: ' + l.ficheiro + (l.formato === 'epi-progresso' ? ' (progresso guardado, sem código)' : '')));
    var f = foraTexto(l.fora);
    if (f) d.appendChild(el('p', 'rt-p-f', 'Ficaram de fora: ' + f + '.'));
    E.GRUPOS.forEach(function (g) {
      var x = l.resumo[g];
      if (!x || !x.n) return;
      d.appendChild(el('h3', null, g));
      d.appendChild(el('p', 'rt-p-res', textoGrupo(x)));
      if (x.itens.length) {
        var ul = el('ul');
        x.itens.forEach(function (it) {
          var li = el('li');
          li.appendChild(el('strong', null, it.rotulo));
          li.appendChild(doc.createTextNode(': ' + it.estado));
          if (it.texto) {
            var dt = el('details', 'rt-t'), st = el('summary', null, 'Ler o que escreveu (' + plural(it.palavras, 'palavra', 'palavras') + ')');
            var txt = it.texto.length > 4000 ? it.texto.slice(0, 4000) + '…' : it.texto;
            dt.appendChild(st); dt.appendChild(el('p', 'rt-texto', txt)); li.appendChild(dt);
          }
          ul.appendChild(li);
        });
        d.appendChild(ul);
      }
      var resto = x.n - x.itens.length;
      if (resto > 0) d.appendChild(el('p', 'rt-p-f', resto === 1 ? 'Mais 1 registo auxiliar (marcas e contagens).' : 'Mais ' + resto + ' registos auxiliares (marcas e contagens).'));
    });
    return d;
  }

  function limpar() {
    S.linhas = []; S.vistos = {}; S.seq = 0;
    avisosL.textContent = ''; recusadosL.textContent = ''; avisosC.hidden = true; recusadosC.hidden = true;
    input.value = '';
    desenhar();
    dizer('A tabela ficou vazia.');
    // O botão fica desativado: o foco passa para o campo dos ficheiros, e não cai no fim da página.
    try { input.focus(); } catch (e) { /* sem foco */ }
  }
  function descarregarCsv() {
    var L = ordenar(S.linhas, S.ordem);
    if (!L.length) return;
    var b = new Blob([csv(L, gruposPresentes(L))], {type: 'text/csv;charset=utf-8'}), u = URL.createObjectURL(b), a = el('a');
    a.href = u; a.download = 'resultados-turma-' + E.hoje() + '.csv';
    doc.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(u); a.remove(); }, 1000);
    dizer('Tabela descarregada em CSV: ' + plural(L.length, 'linha', 'linhas') + '.');
  }

  input.addEventListener('change', function () { var fl = input.files; receber(fl); input.value = ''; });
  bCsv.addEventListener('click', descarregarCsv);
  bLimpar.addEventListener('click', limpar);
  // Arrastar: a caixa acende-se; largar fora dela não abre o ficheiro no navegador.
  function temFicheiros(ev) { var t = ev.dataTransfer && ev.dataTransfer.types; return !!t && Array.prototype.indexOf.call(t, 'Files') >= 0; }
  ['dragenter', 'dragover'].forEach(function (n) {
    zona.addEventListener(n, function (ev) { if (!temFicheiros(ev)) return; ev.preventDefault(); ev.dataTransfer.dropEffect = 'copy'; zona.classList.add('rt-arrastar'); });
  });
  zona.addEventListener('dragleave', function (ev) { if (!ev.relatedTarget || !zona.contains(ev.relatedTarget)) zona.classList.remove('rt-arrastar'); });
  zona.addEventListener('drop', function (ev) { ev.preventDefault(); ev.stopPropagation(); zona.classList.remove('rt-arrastar'); receber(ev.dataTransfer && ev.dataTransfer.files); });
  root.addEventListener('dragover', function (ev) { if (temFicheiros(ev)) ev.preventDefault(); });
  root.addEventListener('drop', function (ev) { if (!temFicheiros(ev)) return; ev.preventDefault(); dizer('Larga os ficheiros dentro da caixa tracejada.'); });
  desenhar();
}(window, typeof document !== 'undefined' ? document : null));
