'use strict';
/* Resultados da turma (28/10/2026): as regras de progresso-registos.js e o resumo e o CSV de resultados-turma.js,
   sem navegador. Correr: node --test tests/resultados_turma.test.cjs */
const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const A = path.join(__dirname, '../assets');

function carregar() {
  const win = {};
  vm.runInNewContext(fs.readFileSync(path.join(A, 'progresso-registos.js'), 'utf8'), {window: win}, {filename: 'progresso-registos.js'});
  vm.runInNewContext(fs.readFileSync(path.join(A, 'resultados-turma.js'), 'utf8'), {window: win}, {filename: 'resultados-turma.js'});
  return {E: win.EPIRegistos, R: win.EPIResultados};
}
const {E, R} = carregar();
const json = o => JSON.stringify(o);
const HOJE = new Date(2026, 9, 28, 14, 5, 0);

test('código: 2 a 12 caracteres de A a Z, 0 a 9 e hífen, em maiúsculas, com um algarismo', () => {
  assert.deepEqual({...E.validarCodigo('10a-07')}, {ok: true, codigo: '10A-07'});
  assert.equal(E.validarCodigo('  10A-07 ').codigo, '10A-07');
  assert.equal(E.validarCodigo('7B').ok, true);
  const nome = E.validarCodigo('Ana');
  assert.equal(nome.ok, false);
  assert.match(nome.erro, /algarismo/);
  assert.match(nome.erro, /Não escrevas o teu nome/);
  assert.match(E.validarCodigo('A').erro, /entre 2 e 12/);
  assert.match(E.validarCodigo('ABCDEFGHIJ123').erro, /entre 2 e 12/);
  assert.match(E.validarCodigo('10 A').erro, /só pode ter letras/);
  assert.match(E.validarCodigo('joão7').erro, /só pode ter letras/);
  assert.match(E.validarCodigo('').erro, /Escreve o código/);
  assert.match(E.validarCodigo(null).erro, /Escreve o código/);
});

test('código: recusa o que o Excel troca por números ao abrir o CSV (28/10/2026)', () => {
  // turmas com a letra E: 10E-07 passa a 0,000001 no Excel e no LibreOffice; a letra vai à frente
  for (const c of ['10E-07', '12E-03', '11E1', '1E5', '10e07']) {
    const v = E.validarCodigo(c);
    assert.equal(v.ok, false, c);
    assert.match(v.erro, /Excel do docente lê este código como um número.*E10-07/, c);
  }
  for (const c of ['007', '123', '1-10', '10-3']) assert.match(E.validarCodigo(c).erro, /pelo menos uma letra/, c);
  for (const c of ['-1A', 'A1-', '--1A']) assert.match(E.validarCodigo(c).erro, /começar nem acabar com hífen/, c);
  for (const c of ['E10-07', '10A-07', '12C-03', '10E', 'E1', '10EA-07', '7B']) assert.equal(E.validarCodigo(c).ok, true, c);
  // e o docente recusa uma entrega com um destes códigos
  assert.match(E.validarFicheiro(entrega({}, {codigo: '10E-07'})).erro, /código da entrega não é válido/);
});

test('chaves: aceites, que ficam no aparelho, privadas, provas, proibidas e desconhecidas', () => {
  const c = k => E.classificar(k);
  for (const k of ['licao-m1-f04', 'licao-m1-f04-a1', 'percurso-M3', 'desafio-unidade-v2-M3-u1', 'epi-pt-quiz-M1', 'atlas-PT-1', 'epi-atlas',
    'lente-cidadania-m1-sessoes-v2', 'lente-cidadania-m2-sessoes-v1', 'lente-cidadania-m1-v2', 'epi-cidadania-m1', 'cd-cd1-aula01',
    'cd1-aula1-1', 'lente-justica-licao-2', 'epi-treinos', 'epi-narrativas:visto', 'visita-visita-casa-fernando-pessoa', 'epi-ultima'])
    assert.equal(c(k), 'aceite', k);
  // 28/10/2026: epi-som e epi-cartaz (preferências do aparelho) entram; epi-codigo-entrega sai, porque o código não se guarda
  for (const k of ['epi-theme', 'epi-som', 'epi-cartaz', 'pt-relogio:tarefas/m1-u1:aquecimento', 'epi-projection-text-size', 'pt-exame-sessao-m1'])
    assert.equal(c(k), 'aparelho', k);
  for (const k of ['epi-sala', 'painel-sala-m1-f04', 'rel-abc']) assert.equal(c(k), 'sala', k);
  for (const k of ['epi-pt-prova-m1-a', 'epi-pt-teste-m2']) assert.equal(c(k), 'prova', k);
  for (const k of ['cd1-nome', 'cd2-nome', 'terra-firme-turma']) assert.equal(c(k), 'privada', k);
  for (const k of ['__proto__', 'constructor', 'prototype']) assert.equal(c(k), 'proibida', k);
  for (const k of ['outra-aplicacao', 'epi-pt-' + 'x'.repeat(200)]) assert.equal(c(k), 'desconhecida', k);
  assert.equal(E.aceite('epi-codigo-entrega'), false, 'o código não viaja nos registos');
  assert.equal(c('epi-codigo-entrega'), 'desconhecida', '28/10/2026: nenhuma página escreve esta chave');
  assert.equal(E.registosParaEntrega({'epi-som': 'true', 'epi-cartaz': '{"v":2}', 'epi-theme': 'dark'}).n, 0, 'só preferências: nada para entregar');
  assert.equal(E.grupoDe('lente-cidadania-m2-sessoes-v1'), 'Cidadania e Desenvolvimento');
  assert.equal(E.grupoDe('licao-m1-f04'), 'Português: lições e percursos dos módulos');
  assert.equal(E.grupoDe('epi-som'), E.OUTROS);
});

const APARELHO = {
  'licao-m1-f04': json({versao: '2026-10-24', tentativas: 2, certas: 9, total: 11, melhor: 10, totalMelhor: 11, lida: true, t: 1761650000000}),
  'licao-m1-f04-a1': json({lida: true, t: 1761650000000}),
  'lente-cidadania-m1-sessoes-v2': json({version: 2, sessions: {'01': {done: true}, '03': {stage: 4, done: true}, '04': {stage: 2}}}),
  'cd-cd1-aula01': json({nome: 'Rita Sousa', mesa: 'Mesa 3', palavra: 'justo'}),
  'cd1-nome': 'Rita Sousa',
  'epi-theme': 'dark',
  'epi-sala': json({cod: 'ABCDE', alc: 'Rita', t: 1}),
  'epi-pt-prova-m1-a': json({bloqueio: {c: 'M1-A-XXXX'}}),
  'epi-som': 'true',
  'outra-aplicacao': 'x',
  'epi-narrativas': json({feitas: {'oficina-arco': 1761650000000}}),
  'epi-ver': json({feitas: {v01: 1}, vistos: {v01: 1}}),
  'epi-bairro': '{"feitas":{"<img src=x>":1}}'
};

test('entrega: só as chaves aceites, sem nome, sem o código nos registos, e o topo exato', () => {
  const r = E.registosParaEntrega(APARELHO);
  assert.deepEqual(Object.keys(r.registos).sort(), ['cd-cd1-aula01', 'epi-narrativas', 'epi-ver', 'lente-cidadania-m1-sessoes-v2', 'licao-m1-f04', 'licao-m1-f04-a1']);
  assert.equal(JSON.parse(r.registos['cd-cd1-aula01']).nome, undefined, 'o campo nome sai');
  assert.equal(JSON.parse(r.registos['cd-cd1-aula01']).mesa, 'Mesa 3');
  assert.equal(r.registos['licao-m1-f04'], APARELHO['licao-m1-f04'], 'os outros valores ficam iguais');
  // 28/10/2026: o segundo registo do aparelho é epi-som (o código da entrega já não se guarda)
  assert.deepEqual({...r.fora}, {privada: 1, sala: 1, aparelho: 2, prova: 1, desconhecida: 1, estragada: 1});
  assert.equal(r.n, 6);
  assert.equal(r.texto, 1);
  assert.equal(r.grupos['Cidadania e Desenvolvimento'], 2);
  const d = E.montarEntrega('10A-07', r.registos, HOJE);
  assert.deepEqual(Object.keys(d), ['formato', 'versao', 'codigo', 'data', 'origem', 'registos']);
  assert.equal(d.formato, 'epi-entrega'); assert.equal(d.versao, 1); assert.equal(d.origem, 'lente/caderno');
  assert.equal(d.data, HOJE.toISOString());
  assert.equal(E.nomeEntrega('10A-07', HOJE), 'entrega-10A-07-2026-10-28.json');
  assert(!JSON.stringify(d).includes('Rita'), 'nenhum nome no ficheiro');
  const v = E.validarFicheiro(JSON.stringify(d, null, 1));
  assert.equal(v.erro, undefined, 'o docente lê a entrega que o caderno faz');
  assert.equal(v.codigo, '10A-07'); assert.equal(v.n, 6);
});

function entrega(registos, extra) { return JSON.stringify(Object.assign({formato: 'epi-entrega', versao: 1, codigo: '10A-07', data: HOJE.toISOString(), origem: 'lente/caderno', registos}, extra || {})); }
function progresso(registos, extra) { return JSON.stringify(Object.assign({formato: 'epi-progresso', versao: 1, data: HOJE.toISOString(), origem: 'https://pedrohfernandes-klk.github.io', registos}, extra || {})); }

test('docente: as regras do Repor, estrito nas entregas e tolerante nos progressos antigos', () => {
  const bom = {'licao-m1-f04': APARELHO['licao-m1-f04']};
  assert.equal(E.validarFicheiro(entrega(bom)).n, 1);
  // chave fora da lista: recusa a entrega; num progresso antigo fica de fora e conta-se
  assert.match(E.validarFicheiro(entrega({...bom, 'outra-aplicacao': 'x'})).erro, /não entrega/);
  const p = E.validarFicheiro(progresso({...bom, 'outra-aplicacao': 'x', 'epi-theme': 'dark', 'epi-sala': '{}', 'cd1-nome': 'Rita', 'epi-pt-prova-m1-a': '{}'}));
  assert.equal(p.erro, undefined); assert.equal(p.codigo, ''); assert.equal(p.n, 1);
  assert.deepEqual({...p.fora}, {privada: 1, sala: 1, aparelho: 1, prova: 1, desconhecida: 1});
  // chaves proibidas a qualquer profundidade
  // 28/10/2026: a página mostra ao docente «O ficheiro foi alterado ou não vem do caderno.»; o motivo técnico fica em «motivo»
  const alterado = t => { const v = E.validarFicheiro(t); assert.equal(v.erro, E.ALTERADO); return v.motivo; };
  assert.match(alterado('{"formato":"epi-entrega","versao":1,"codigo":"10A-07","registos":{"__proto__":"x"}}'), /chave proibida: __proto__/);
  assert.match(alterado(entrega({'licao-m1-f04': '{"a":{"b":{"constructor":1}}}'})), /conteúdo proibido/);
  assert.match(alterado(entrega(bom, {prototype: {}})), /chave proibida: prototype/);
  assert.match(alterado('{"formato":"epi-progresso","versao":1,"registos":{"x":{"__proto__":{"y":1}}}}'), /chave proibida/);
  // limites: tamanho, níveis, número de registos, valor
  assert.match(E.validarFicheiro(entrega({'cd1-aula1-1': 'x'.repeat(1048600)})).erro, /mais de 1 MB/);
  let fundo = '1'; for (let i = 0; i < 18; i++) fundo = '{"a":' + fundo + '}';
  assert.match(alterado(entrega({'licao-m1-f04': fundo})), /conteúdo proibido/);
  assert.match(alterado('{"formato":"epi-progresso","versao":1,"registos":' + fundo + '}'), /mais de 16 níveis/);
  const muitos = {}; for (let i = 0; i < 5001; i++) muitos['licao-m1-f' + (i % 999) + (i >= 999 ? '-a' + (1 + (i % 2)) : '')] = '1';
  for (let i = 0; Object.keys(muitos).length <= 5000; i++) muitos['epi-pt-x' + i] = '1';
  assert.match(E.validarFicheiro(progresso(muitos)).erro, /registos a mais/);
  assert.match(E.validarFicheiro(entrega({'cd1-aula1-1': 'x'.repeat(100001)})).erro, /grande demais/);
  assert.match(E.validarFicheiro(entrega({'licao-m1-f04': 7})).erro, /formato certo/);
  // conteúdo: chaves com < > " e campos de código com HTML
  assert.match(alterado(entrega({'epi-bairro': '{"feitas":{"<img src=x onerror=alert(1)>":1}}'})), /conteúdo proibido: epi-bairro/);
  assert.match(alterado(entrega({'epi-ultima': '{"id":"<script>alert(1)</script>"}'})), /conteúdo proibido: epi-ultima/);
  // o texto livre do aluno passa (só se mostra com textContent)
  assert.equal(E.validarFicheiro(entrega({'cd1-aula1-1': '<script>alert(1)</script>'})).n, 1);
  // formato, versão, topo e código
  assert.match(E.validarFicheiro('{"formato":').erro, /estragado/);
  assert.match(E.validarFicheiro('[]').erro, /Não é uma entrega/);
  assert.match(E.validarFicheiro(entrega(bom, {versao: 2})).erro, /versão mais nova/);
  assert.match(E.validarFicheiro(entrega(bom, {versao: '1'})).erro, /versão que o sítio não conhece/);
  assert.match(E.validarFicheiro(entrega(bom, {nome: 'Rita'})).erro, /campos que uma entrega não tem/);
  assert.match(E.validarFicheiro(progresso(bom, {codigo: '10A-07'})).erro, /campos que um progresso guardado não tem/);
  assert.match(E.validarFicheiro(entrega(bom, {codigo: 'ANA'})).erro, /código da entrega não é válido/);
  assert.match(E.validarFicheiro(entrega(bom, {codigo: '10a-07'})).erro, /código da entrega não é válido/);
  assert.match(E.validarFicheiro(entrega('x')).erro, /lista de registos/);
  // o nome sai também dos ficheiros antigos
  const velho = E.validarFicheiro(progresso({'cd-cd2-aula01': json({nome: 'Rui', frase: 'Uma frase.'})}));
  assert.equal(JSON.parse(velho.registos['cd-cd2-aula01']).nome, undefined);
});

test('resumo por percurso: lições, sessões, apoios, Atlas, Ginásio, questionários e texto livre', () => {
  const g = R.resumir({
    'licao-m1-f04': APARELHO['licao-m1-f04'],
    'licao-m1-f05': json({tentativas: 1, certas: 3, total: 8, melhor: 3, lida: false}),
    'licao-m1-f04-a1': json({lida: true}),
    'desafio-unidade-v2-M3-u1': json({melhor: 7, totalMelhor: 8, lida: true, ganho: true}),
    'percurso-sintese-M5-u2': json({feita: true, modo: 'oral'}),
    'percurso-v2-M3-u1': 'Nesta unidade percebi que a voz muda.',
    'epi-pt-quiz-M1': json({0: 5, 3: 6}),
    'epi-pt-candide-jardim': json({i: 7, n: 7, r: {4: 'O jardim é trabalho.'}, p: {1: 10, 2: 10}, fim: true}),
    'epi-atlas': json({v: 3, p: {a: {qs: 1, ob: 2}, b: {qs: 1}, c: {}}, dom: {PT: 1}}),
    'lente-cidadania-m1-sessoes-v2': json({version: 2, sessions: {'01': {done: true}, '03': {stage: 4, done: true}, '04': {stage: 2}}}),
    'lente-cidadania-m2-sessoes-v1': json({version: 1, sessions: {'01': {stage: 4, done: true}, '02': {done: true}}}),
    'lente-cidadania-m1-v2': json({version: 2, done: {F01: true, F02: false, F04: true}}),
    'cd1-aula1-1': 'A minha resposta.',
    'epi-treinos': json({feitas: {'sem-olhos': 1, 'a-lista': 2}, vezes: {'sem-olhos': 2}}),
    'lente-justica-licao-2': json({melhor: 7, totalMelhor: 8, lida: true}),
    'epi-narrativas:visto': '5',
    'epi-som': 'true'
  });
  const t = n => R.textoGrupo(g[n]);
  assert.equal(t('Português: lições e percursos dos módulos'), '1 lição concluída; 1 desafio ganho; 1 síntese registada; 1 nota escrita');
  assert.equal(t('Português: exercícios, questionários e trabalhos longos'), '1 exercício concluído; 2 questionários feitos');
  // 28/10/2026: «países conquistados», como no Atlas; «sessões com registo», e no M1 o total começa na 03
  assert.equal(t('Atlas Lusófono'), '1 pessoa conhecida; 1 país conquistado');
  assert.equal(t('Cidadania e Desenvolvimento'), 'M1: 1 de 8 sessões com registo (da 03 à 10); M2: 2 de 10 sessões com registo; 2 de 18 apoios do M1 com trabalho registado; 1 resposta escrita');
  assert.equal(t('Laboratório: Narrativas e Ginásio'), '2 treinos feitos');
  assert.equal(t('Ter juízo: Justiça, Ética e Estética'), '1 lição concluída');
  assert.equal(t(E.OUTROS), '1 registo');
  const licao = g['Português: lições e percursos dos módulos'].itens.find(i => i.chave === 'licao-m1-f04');
  assert.equal(licao.rotulo, 'M1, lição F04');
  assert.equal(licao.estado, 'concluída, melhor resultado 10 de 11, 2 tentativas');
  const ses = g['Cidadania e Desenvolvimento'].itens.find(i => i.chave === 'lente-cidadania-m1-sessoes-v2');
  assert.equal(ses.estado, 'registadas: 03; em curso: 04 (passo 3)');
  const nota = g['Português: lições e percursos dos módulos'].itens.find(i => i.chave === 'percurso-v2-M3-u1');
  assert.equal(nota.palavras, 7); assert.equal(nota.texto, 'Nesta unidade percebi que a voz muda.');
  assert.equal(g['Laboratório: Narrativas e Ginásio'].itens[0].estado, 'Sem olhos (2 vezes); A lista');
  assert.equal(g['Laboratório: Narrativas e Ginásio'].n, 2, 'o :visto conta como registo, sem pormenor');
});

test('desafios ganhos antes de 10/10 («vencido») contam como ganhos (28/10/2026)', () => {
  const g = R.resumir({
    'chefe-M3-u1': json({vencido: true, melhor: 7, total: 8, lida: true, tentativas: 1}),
    'desafio-M4-u2': json({vencido: true, melhor: 6, total: 8}),
    'desafio-unidade-v2-M5-u1': json({melhor: 3, total: 8, tentativas: 2})
  });
  const p = g['Português: lições e percursos dos módulos'];
  assert.deepEqual({...p.contas}, {desafio: 2});
  assert.equal(R.textoGrupo(p), '2 desafios ganhos');
  const chefe = p.itens.find(i => i.chave === 'chefe-M3-u1');
  assert.equal(chefe.rotulo, 'M3, desafio da unidade 1');
  assert.equal(chefe.estado, 'ganho, melhor resultado 7 de 8, 1 tentativa');
  assert.match(p.itens.find(i => i.chave === 'desafio-unidade-v2-M5-u1').estado, /^por ganhar/);
});

test('pormenor: rótulos sem dois pontos repetidos, «modo» só das propriedades próprias e itens por módulo (28/10/2026)', () => {
  const g = R.resumir({
    'percurso-v2-M3-u1': 'Notas da unidade.',
    'epi-ultima': json({id: 'm1-f04', t: 1761650000000}),
    'licao-m1-f04': json({lida: true}),
    'licao-m4-f27': json({lida: false}),
    'percurso-sintese-M5-u2': json({feita: true, modo: 'oral'}),
    'desafio-unidade-v2-M3-u1': json({ganho: true, melhor: 7, totalMelhor: 8}),
    'licao-m3-f12': json({lida: true}),
    'rota-M3': json({t1: {feito: [1, 2]}}),
    'percurso-sintese-M3-u1': json({feita: true, modo: 'constructor'}),
    'percurso-sintese-M3-u2': json({feita: true, modo: '__proto__'}),
    'percurso-sintese-M4-u1': json({feita: true, modo: 'toString'})
  });
  const p = g['Português: lições e percursos dos módulos'];
  assert.deepEqual([...p.itens].map(i => i.rotulo), [
    'Última lição aberta', 'M1, lição F04',
    'M3, lição F12', 'M3, desafio da unidade 1', 'M3, síntese da unidade 1', 'M3, notas da unidade 1', 'M3, síntese da unidade 2', 'M3, guia da tarefa',
    'M4, lição F27', 'M4, síntese da unidade 1', 'M5, síntese da unidade 2'
  ]);
  const est = Object.fromEntries(p.itens.map(i => [i.chave, i.estado]));
  assert.equal(est['percurso-sintese-M5-u2'], 'registada (oral)');
  for (const k of ['percurso-sintese-M3-u1', 'percurso-sintese-M3-u2', 'percurso-sintese-M4-u1'])
    assert.equal(est[k], 'registada', 'sem funções nativas no texto: ' + k);
  const c = R.resumir({
    'cd1-aula1-1': 'Uma mesa vazia.',
    'cd-cd1-aula01': json({mesa: 'Mesa 3', palavra: 'justo'}),
    'epi-pt-candide-jardim': json({i: 7, n: 7, p: {1: 10, 2: 10}, fim: true}),
    'epi-pt-quiz-M1': json({0: 5, 3: 6}),
    'epi-atlas': json({dom: {PT: 1, BR: 1}})
  });
  const it = (gr, k) => c[gr].itens.find(i => i.chave === k);
  const C = 'Cidadania e Desenvolvimento', X = 'Português: exercícios, questionários e trabalhos longos';
  assert.equal(it(C, 'cd1-aula1-1').rotulo + ': ' + it(C, 'cd1-aula1-1').estado, 'Cidadania, aula 1, pergunta 1: respondida, 3 palavras');
  assert.equal(it(C, 'cd-cd1-aula01').rotulo + ': ' + it(C, 'cd-cd1-aula01').estado, 'Cidadania M1, aula 1: 2 respostas, 3 palavras');
  assert.equal(it(X, 'epi-pt-candide-jardim').rotulo + ': ' + it(X, 'epi-pt-candide-jardim').estado, 'Exercício «Candide jardim»: concluído, 20 pontos');
  assert.equal(it(X, 'epi-pt-quiz-M1').rotulo + ': ' + it(X, 'epi-pt-quiz-M1').estado, 'M1, questionários: questionário 1 com 5 certas; questionário 4 com 6 certas');
  assert.match(c['Atlas Lusófono'].itens[0].estado, /países conquistados: Portugal, Brasil$/);
  assert.equal(R.textoGrupo(c['Atlas Lusófono']), '0 pessoas conhecidas; 2 países conquistados');
});

test('valores estranhos não partem o resumo', () => {
  const g = R.resumir({'licao-m1-f04': '123', 'epi-atlas': '"x"', 'lente-cidadania-m1-sessoes-v2': '[]', 'epi-treinos': '{"feitas":[1,2]}', 'percurso-M3-u1': '', 'rota-M2': 'null'});
  assert.equal(R.textoGrupo(g['Português: lições e percursos dos módulos']), '0 lições concluídas; 0 notas escritas');
  assert.equal(R.textoGrupo(g['Atlas Lusófono']), '1 registo');
});

test('CSV: BOM, «;», CRLF, aspas e proteção contra fórmulas', () => {
  for (const [v, e] of [['=1+1', '"\'=1+1"'], ['+351', '"\'+351"'], ['-07', '"\'-07"'], ['@SUM(A1)', '"\'@SUM(A1)"'], ['\tx', '"\'\tx"'], ['\rx', '"\'\rx"'], ['diz "olá"', '"diz ""olá"""'], ['a;b', '"a;b"'], [12, '"12"'], [null, '""']])
    assert.equal(R.celula(v), e, String(v));
  const v1 = E.validarFicheiro(entrega({'licao-m1-f04': APARELHO['licao-m1-f04']}));
  const v2 = E.validarFicheiro(progresso({'epi-treinos': json({feitas: {'sem-olhos': 1}})}));
  const L = R.ordenar([R.linha(v2, '=HYPERLINK("x").json', 0), R.linha(v1, 'entrega-10A-07-2026-10-28.json', 0)], 'asc');
  const s = R.csv(L);
  // 28/10/2026: a coluna chama-se «Data» (nos progressos antigos é a data em que o aluno guardou, marcada «(guardado)»)
  assert(s.startsWith('﻿"Código";"Ficheiro";"Data";"Registos";'), s.slice(0, 80));
  assert(s.endsWith('\r\n'));
  const linhas = s.slice(1).split('\r\n');
  assert.equal(linhas.length, 4);
  assert.equal(linhas[0], '"Código";"Ficheiro";"Data";"Registos";"Português: lições e percursos dos módulos";"Laboratório: Narrativas e Ginásio";"Ficaram de fora"');
  assert.equal(linhas[1], '"10A-07";"entrega-10A-07-2026-10-28.json";"28/10/2026, 14:05";"1";"1 lição concluída";"";""');
  assert.equal(linhas[2], '"sem código";"\'=HYPERLINK(""x"").json";"28/10/2026, 14:05 (guardado)";"1";"";"1 treino feito";""');
});

test('duplicados e ordem: fica a entrega mais recente; sem código no fim; ordem natural', () => {
  const nova = R.linha(E.validarFicheiro(entrega({}, {data: '2026-10-28T10:00:00Z'})), 'b.json', 1);
  const velha = R.linha(E.validarFicheiro(entrega({}, {data: '2026-10-20T10:00:00Z'})), 'a.json', 9);
  assert.equal(R.maisRecente(nova, velha), nova);
  assert.equal(R.maisRecente(velha, nova), nova);
  const semData = R.linha(E.validarFicheiro(entrega({}, {data: 'ontem'})), 'c.json', 5);
  assert.equal(R.maisRecente(semData, velha), velha, 'uma data que não se lê perde');
  // 28/10/2026: a data vem do ficheiro; mais de um dia à frente do relógio do docente, não ganha e fica marcada
  const AGORA = Date.parse('2026-10-28T12:00:00Z');
  const certa = R.linha(E.validarFicheiro(entrega({}, {codigo: '10B-01', data: '2026-10-28T10:00:00Z'})), 'entrega-10B-01-2026-10-28.json', 1, AGORA);
  const falsa = R.linha(E.validarFicheiro(entrega({}, {codigo: '10B-01', data: '2099-01-01T00:00:00Z'})), 'entrega-10B-01-falso.json', 9, AGORA);
  assert.equal(falsa.futuro, true); assert.equal(certa.futuro, false);
  assert.equal(R.maisRecente(falsa, certa), certa); assert.equal(R.maisRecente(certa, falsa), certa);
  assert.match(R.avisoDuplicado(certa, falsa), /^10B-01 tem duas entregas\. Ficou a de 28\/10\/2026, \d\d:00; a outra tem data no futuro \(01\/01\/2099, \d\d:00\) e ficou de fora\.$/);
  assert.match(R.dataTexto(falsa), /^01\/01\/2099, \d\d:00 \(data no futuro\)$/);
  const amanha = R.linha(E.validarFicheiro(entrega({}, {data: '2026-10-29T06:00:00Z'})), 'x.json', 0, AGORA);
  assert.equal(amanha.futuro, false, 'até um dia à frente (fusos, relógios atrasados) não é suspeito');
  assert.match(R.avisoDuplicado(nova, velha), /^10A-07 tem duas entregas\. Ficou a de 28\/10\/2026, \d\d:00; a de 20\/10\/2026, \d\d:00 ficou de fora\.$/);
  const x = (c, f) => ({codigo: c, rotulo: f || c});
  assert.deepEqual(R.ordenar([x('', 'z.json'), x('10A-10'), x('10A-2'), x('9B-1'), x('', 'a.json')], 'asc').map(l => l.codigo || l.rotulo), ['9B-1', '10A-2', '10A-10', 'a.json', 'z.json']);
  assert.deepEqual(R.ordenar([x('10A-10'), x('10A-2'), x('', 'a.json')], 'desc').map(l => l.codigo || l.rotulo), ['10A-10', '10A-2', 'a.json']);
  assert.equal(R.assinatura('abc'), R.assinatura('abc'));
  assert.notEqual(R.assinatura('abc'), R.assinatura('abd'));
});

test('sem DOM nem armazenamento nem rede nos dois ficheiros de regras', () => {
  for (const f of ['progresso-registos.js', 'resultados-turma.js']) {
    const s = fs.readFileSync(path.join(A, f), 'utf8');
    for (const proibido of ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'WebSocket', 'EventSource', 'localStorage', 'sessionStorage', 'indexedDB', 'innerHTML', 'outerHTML', 'insertAdjacentHTML', 'document.write', 'new Image', 'importScripts'])
      assert(!s.includes(proibido), f + ': ' + proibido);
  }
});
