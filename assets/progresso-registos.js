/* Registos do progresso: as regras comuns a «Entregar ao docente» (caderno) e a «Resultados da turma» (área do docente).
   28/10/2026. Lógica pura: sem DOM, sem armazenamento e sem rede, para se poder testar em vm.
   As listas e os limites vêm do «Repor» validado de 17/10 (progresso.mjs, nas fontes, revisto a 23 e 24/10), com o que
   faltava a 28/10: as sessões e os apoios de Cidadania (lente-cidadania-…), que entram; as preferências do aparelho (tema,
   som e o cartaz que já rodou: epi-theme, epi-som, epi-cartaz) e o relógio das tarefas (pt-relogio:…), que ficam no
   aparelho sem recusar o ficheiro. O nome do aluno nunca viaja: as chaves com nome (cd1-nome, terra-firme-…) e o campo
   «nome» das respostas de Cidadania (cd-…) ficam de fora. O código da entrega não se guarda no aparelho. */
(function (root) {
  'use strict';
  if (root.EPIRegistos) return;

  var VERSAO = 1;
  var LIM = {ficheiro: 1048576, valor: 100000, registos: 5000, niveis: 16, chave: 160};
  // Uma função e não um objeto: num objeto literal, «'__proto__': 1» muda o protótipo em vez de criar a chave.
  function proibida(k) { return k === '__proto__' || k === 'constructor' || k === 'prototype'; }

  // As chaves que os dois sítios escrevem e que viajam (cada expressão é inteira, com a marca «i»).
  var ACEITES = [
    "^licao-m\\d{1,2}-f\\d{1,3}(-a[12]|-ler)?$",
    "^percurso-m\\d{1,2}(-festa|-antes-unidades|-u\\d{1,2}(-check|-copiada)?)?$",
    "^percurso-v2-m\\d{1,2}-u\\d{1,2}(-check|-copiada)?$",
    "^percurso-sintese-m\\d{1,2}-u\\d{1,2}(-inicializada)?$",
    "^desafio-(unidade-v2-)?m\\d{1,2}-u\\d{1,2}$",
    "^(rota|balanco)-m\\d{1,2}$",
    "^epi-pt-[a-z0-9-]{1,120}$",
    "^epi-(apresentar|atlas|bairro|biblioteca|cd|cid|cidadania(-m\\d)?|conjunto|corta|direitos|ficcao|gigantes|guiao|investigar|justica|lente|ler|literatura|maquina|margens|narrativas|projetos|sidequests|treinos|ultima|ver|vozes)(-[a-z0-9-]{1,120})?(:visto|:arco|:dupla)?$",
    "^lente-(justica|etica|estetica)-licao-\\d$",
    "^lente-cidadania-m\\d-(sessoes-)?v\\d$",
    "^atlas-[a-z]{2}-[a-z0-9-]{1,40}$",
    "^atlas-j\\d{1,3}$",
    "^chefe-m\\d{1,2}-u\\d{1,2}$",
    "^bairro-[a-z0-9-]{1,40}$",
    "^como-[a-z0-9-]{1,60}$",
    "^visita-[a-z0-9-]{1,120}$",
    "^cd\\d?-[a-z0-9-]{1,80}$",
    "^terra-firme-[a-z0-9-]{1,120}$",
    "^fabrica-de-jogos$"
  ];
  // A Sala, desligada a 17/10: não viaja, mas não recusa o ficheiro.
  var IGNORADAS_SALA = ["^epi-sala(-atlas)?$", "^painel-sala-[a-z0-9-]{1,40}$", "^rel-[a-z0-9-]{1,60}$"];
  // O que só serve o aparelho onde se escreveu: não viaja, mas não recusa o ficheiro.
  var IGNORADAS_APARELHO = [
    "^epi-projection-text-size$",
    "^epi-sugestao-editorial-02-[a-z0-9-]{1,40}$",
    "^pt-exame-sessao-[a-z0-9-]{1,40}$",
    "^epi-theme$",
    "^epi-som$",
    "^epi-cartaz$",
    "^pt-relogio:[a-z0-9/:-]{1,150}$"
  ];
  var IGNORADAS = IGNORADAS_SALA.concat(IGNORADAS_APARELHO);
  // Cabem em ACEITES mas não viajam: as provas rápidas e os testes ficam no aparelho onde se fizeram.
  var DE_FORA = ["^epi-pt-(prova|teste)-[a-z0-9-]{1,120}$"];
  // Cabem em ACEITES mas levam o nome do aluno: nunca viajam.
  var PRIVADAS = ["^cd\\d?-nome$", "^terra-firme-"];
  // De que percurso é cada registo (a primeira expressão que servir).
  var GRUPOS = [
    ["^(licao-|percurso-|desafio-|chefe-|rota-|balanco-|epi-ultima$)", "Português: lições e percursos dos módulos"],
    ["^epi-pt-", "Português: exercícios, questionários e trabalhos longos"],
    ["^(epi-atlas|atlas-)", "Atlas Lusófono"],
    ["^(epi-bairro|bairro-)", "A cidade antes da aula"],
    ["^(epi-cidadania|epi-cid-|epi-cd-|cd\\d?-|lente-cidadania-)", "Cidadania e Desenvolvimento"],
    ["^(epi-justica|lente-(justica|etica|estetica)-)", "Ter juízo: Justiça, Ética e Estética"],
    ["^epi-(narrativas|treinos|ficcao|guiao)", "Laboratório: Narrativas e Ginásio"],
    ["^epi-margens", "Margens"],
    ["^epi-gigantes", "Aos ombros de gigantes"],
    ["^epi-biblioteca", "Biblioteca"],
    ["^epi-sidequests", "Sidequests"],
    ["^epi-projetos", "Projetos"],
    ["^epi-investigar", "Como se investiga"],
    ["^epi-ler", "Como se lê"],
    ["^epi-direitos", "Direitos e fontes"],
    ["^epi-apresentar", "Como se apresenta"],
    ["^epi-corta", "Corta! Muda a cena"],
    ["^epi-maquina", "A Máquina das Palavras"],
    ["^epi-literatura", "Literatura mundial"],
    ["^epi-vozes", "vozes."],
    ["^epi-ver", "Ver para fazer"],
    ["^epi-lente", "Lente: Ética, Estética e Fachada"],
    ["^como-", "Como se faz"],
    ["^visita-", "Visitas de estudo"]
  ];
  var OUTROS = 'Outros registos';
  // Famílias com texto escrito pelo aluno (para a pré-visualização dizer que as respostas também vão).
  var COM_TEXTO = ["^cd\\d?-", "^percurso-(v2-)?m\\d{1,2}-u\\d{1,2}$", "^rota-m\\d{1,2}$", "^visita-", "^epi-pt-(?!quiz-|longos)"];

  function re(L) { return L.map(function (r) { return new RegExp(r, 'i'); }); }
  var R_ACEITES = re(ACEITES), R_SALA = re(IGNORADAS_SALA), R_APARELHO = re(IGNORADAS_APARELHO), R_DE_FORA = re(DE_FORA),
    R_PRIVADAS = re(PRIVADAS), R_TEXTO = re(COM_TEXTO),
    R_GRUPOS = GRUPOS.map(function (g) { return [new RegExp(g[0], 'i'), g[1]]; });

  function bate(L, k) { for (var i = 0; i < L.length; i++) if (L[i].test(k)) return true; return false; }
  function tem(o, k) { return Object.prototype.hasOwnProperty.call(o, k); }
  function ehObj(v) { return Object.prototype.toString.call(v) === '[object Object]'; }

  /* O que acontece a uma chave: «aceite» (viaja), «privada», «sala», «aparelho» e «prova» (ficam de fora sem recusar),
     «proibida» (recusa sempre) ou «desconhecida». */
  function classificar(k) {
    if (typeof k !== 'string' || proibida(k)) return 'proibida';
    if (k.length > LIM.chave) return 'desconhecida';
    if (bate(R_ACEITES, k)) {
      if (bate(R_PRIVADAS, k)) return 'privada';
      if (bate(R_DE_FORA, k)) return 'prova';
      return 'aceite';
    }
    if (bate(R_SALA, k)) return 'sala';
    if (bate(R_APARELHO, k)) return 'aparelho';
    return 'desconhecida';
  }
  function aceite(k) { return classificar(k) === 'aceite'; }
  function grupoDe(k) { for (var i = 0; i < R_GRUPOS.length; i++) if (R_GRUPOS[i][0].test(k)) return R_GRUPOS[i][1]; return OUTROS; }
  function comTexto(k) { return bate(R_TEXTO, k); }

  /* Sem chaves proibidas e com poucos níveis em qualquer ponto do valor; chaves curtas e sem < > " acento grave nem
     caracteres de controlo; nos campos de código («id», «c», «cod»), nenhum < > " ' (17/10). */
  var CHAVE_MA = /[<>"`\u0000-\u001f]/, COD_MA = /[<>"']/, CAMPOS_COD = {id: 1, c: 1, cod: 1};
  function limpo(v, n) {
    if (n > LIM.niveis) return false;
    if (v && typeof v === 'object') {
      var ks = Object.keys(v);
      for (var i = 0; i < ks.length; i++) {
        var k = ks[i], x = v[k];
        if (proibida(k) || k.length > 120 || CHAVE_MA.test(k)) return false;
        if (tem(CAMPOS_COD, k) && typeof x === 'string' && COD_MA.test(x)) return false;
        if (!limpo(x, n + 1)) return false;
      }
    }
    return true;
  }
  // Uma chave proibida em qualquer ponto do documento (também no topo e no mapa dos registos) e o número de níveis.
  function proibidaEm(v, n) {
    if (n > LIM.niveis) return {niveis: true};
    if (v && typeof v === 'object') {
      var ks = Object.keys(v);
      for (var i = 0; i < ks.length; i++) {
        if (proibida(ks[i])) return {chave: ks[i]};
        var r = proibidaEm(v[ks[i]], n + 1);
        if (r) return r;
      }
    }
    return null;
  }
  function lerJSON(t) { try { return {ok: true, v: JSON.parse(t)}; } catch (e) { return {ok: false}; } }

  // Tira o nome do aluno de um valor: o campo «nome» das respostas de Cidadania (cd-…).
  function semNome(k, v) {
    if (typeof v !== 'string' || !/^cd\d?-/i.test(k)) return v;
    var j = lerJSON(v);
    if (!j.ok || !ehObj(j.v) || !tem(j.v, 'nome')) return v;
    delete j.v.nome;
    return JSON.stringify(j.v);
  }
  // Um valor que pode viajar: texto, até 100 000 caracteres e, se for JSON, limpo.
  function valorBom(v) {
    if (typeof v !== 'string' || v.length > LIM.valor) return false;
    var j = lerJSON(v);
    return !j.ok || limpo(j.v, 0);
  }

  function pad(x) { return (x < 10 ? '0' : '') + x; }
  function hoje(d) { d = d || new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }

  /* O código que o docente deu ao aluno: 2 a 12 caracteres, de A a Z, 0 a 9 e hífen, em maiúsculas, com pelo menos um
     algarismo (desencoraja nomes). 28/10/2026: e com pelo menos uma letra, sem hífen no início nem no fim e sem a forma
     da notação científica (10E-07, 11E1), porque o Excel e o LibreOffice trocam esses códigos por números ao abrir o CSV
     (007 passa a 7, 10E-07 a 0,000001) e a linha deixa de bater com a lista do docente. */
  function validarCodigo(t) {
    var c = String(t == null ? '' : t).trim().toUpperCase();
    if (!c) return {ok: false, codigo: c, erro: 'Escreve o código que o docente te deu.'};
    if (!/^[A-Z0-9-]+$/.test(c)) return {ok: false, codigo: c, erro: 'O código só pode ter letras de A a Z, algarismos e hífen, sem espaços nem acentos.'};
    if (c.length < 2 || c.length > 12) return {ok: false, codigo: c, erro: 'O código tem de ter entre 2 e 12 caracteres.'};
    if (!/\d/.test(c)) return {ok: false, codigo: c, erro: 'O código tem de ter pelo menos um algarismo, como 10A-07. Não escrevas o teu nome.'};
    if (!/[A-Z]/.test(c)) return {ok: false, codigo: c, erro: 'O código tem de ter pelo menos uma letra, como 10A-07: só com algarismos, o Excel do docente troca-o por um número ou por uma data.'};
    if (/^-|-$/.test(c)) return {ok: false, codigo: c, erro: 'O código não pode começar nem acabar com hífen.'};
    if (/^\d+E-?\d+$/.test(c)) return {ok: false, codigo: c, erro: 'O Excel do docente lê este código como um número (10E-07 passa a 0,000001). Pede ao docente o código com a letra à frente, como E10-07.'};
    return {ok: true, codigo: c};
  }

  /* Os registos que «Guardar num ficheiro» leva, filtrados pela lista: só as chaves aceites, sem nome, com valores que o
     docente consegue ler. mapa = {chave: valor} (o que o aparelho guarda). */
  function registosParaEntrega(mapa) {
    var R = {}, n = 0, grupos = {}, fora = {privada: 0, sala: 0, aparelho: 0, prova: 0, desconhecida: 0, estragada: 0}, texto = 0;
    Object.keys(mapa || {}).sort().forEach(function (k) {
      var c = classificar(k), v = mapa[k];
      if (c !== 'aceite') { if (c !== 'proibida') fora[c]++; return; }
      if (!valorBom(v)) { fora.estragada++; return; }
      R[k] = semNome(k, v); n++;
      var g = grupoDe(k); grupos[g] = (grupos[g] || 0) + 1;
      if (comTexto(k)) texto++;
    });
    return {registos: R, n: n, grupos: grupos, fora: fora, texto: texto};
  }
  function montarEntrega(codigo, registos, agora) {
    return {formato: 'epi-entrega', versao: VERSAO, codigo: codigo, data: (agora || new Date()).toISOString(), origem: 'lente/caderno', registos: registos};
  }
  function nomeEntrega(codigo, agora) { return 'entrega-' + codigo + '-' + hoje(agora) + '.json'; }

  /* Lê um ficheiro na área do docente, com as regras do «Repor»: tamanho, JSON, formato e versão, campos de topo, chaves
     proibidas a qualquer profundidade, número de registos, valores e conteúdo. Uma entrega é estrita (uma chave que o
     caderno não entrega recusa o ficheiro); um «epi-progresso» antigo leva tudo o que o aparelho tinha, por isso as chaves
     que não se reconhecem ficam de fora e contam-se, sem recusar. Devolve {erro} ou os dados limpos. */
  var TOPO = {
    'epi-entrega': {formato: 1, versao: 1, codigo: 1, data: 1, origem: 1, registos: 1},
    'epi-progresso': {formato: 1, versao: 1, data: 1, origem: 1, registos: 1}
  };
  /* 28/10/2026: as razões técnicas (chave proibida, níveis a mais, conteúdo proibido) não dizem nada ao docente; a página
     mostra esta frase e o motivo técnico fica em «motivo», para os testes. */
  var ALTERADO = 'O ficheiro foi alterado ou não vem do caderno.';
  function curto(k) { k = String(k); return k.length > 40 ? k.slice(0, 40) + '…' : k; }
  function validarFicheiro(texto) {
    if (typeof texto !== 'string') return {erro: 'O ficheiro não se lê.'};
    if (texto.length > LIM.ficheiro) return {erro: 'O ficheiro tem mais de 1 MB.'};
    var j = lerJSON(texto);
    if (!j.ok) return {erro: 'O ficheiro está estragado: o conteúdo não se lê.'};
    var d = j.v;
    if (!ehObj(d) || !tem(TOPO, d.formato)) return {erro: 'Não é uma entrega do caderno nem um progresso guardado.'};
    var p = proibidaEm(d, 0);
    if (p && p.chave) return {erro: ALTERADO, motivo: 'chave proibida: ' + p.chave};
    if (p && p.niveis) return {erro: ALTERADO, motivo: 'mais de ' + LIM.niveis + ' níveis'};
    if (d.versao !== VERSAO) return {erro: typeof d.versao === 'number' && d.versao > VERSAO ? 'O ficheiro vem de uma versão mais nova do sítio. Atualiza esta página.' : 'O ficheiro tem uma versão que o sítio não conhece.'};
    var topo = TOPO[d.formato], kt = Object.keys(d);
    for (var t = 0; t < kt.length; t++) if (!tem(topo, kt[t])) return {erro: 'O ficheiro tem campos que ' + (d.formato === 'epi-entrega' ? 'uma entrega' : 'um progresso guardado') + ' não tem («' + curto(kt[t]) + '»).'};
    var entrega = d.formato === 'epi-entrega', codigo = '';
    if (entrega) {
      var vc = validarCodigo(d.codigo);
      if (typeof d.codigo !== 'string' || !vc.ok || vc.codigo !== d.codigo) return {erro: 'O código da entrega não é válido.'};
      codigo = vc.codigo;
    }
    if (!ehObj(d.registos)) return {erro: 'O ficheiro não tem a lista de registos.'};
    var ks = Object.keys(d.registos);
    if (ks.length > LIM.registos) return {erro: 'O ficheiro tem registos a mais (mais de ' + LIM.registos + ').'};
    var R = {}, n = 0, grupos = {}, fora = {privada: 0, sala: 0, aparelho: 0, prova: 0, desconhecida: 0};
    for (var i = 0; i < ks.length; i++) {
      var k = ks[i], v = d.registos[k], c = classificar(k);
      if (c === 'proibida') return {erro: ALTERADO, motivo: 'registo proibido: ' + curto(k)};
      if (c === 'desconhecida') {
        if (entrega) return {erro: 'O ficheiro tem um registo que o caderno não entrega («' + curto(k) + '»).'};
        fora.desconhecida++; continue;
      }
      if (c !== 'aceite') { fora[c]++; continue; }
      if (typeof v !== 'string') return {erro: 'O registo «' + curto(k) + '» não está no formato certo.'};
      if (v.length > LIM.valor) return {erro: 'O registo «' + curto(k) + '» é grande demais.'};
      var jv = lerJSON(v);
      if (jv.ok && !limpo(jv.v, 0)) return {erro: ALTERADO, motivo: 'conteúdo proibido: ' + curto(k)};
      R[k] = semNome(k, v); n++;
      var g = grupoDe(k); grupos[g] = (grupos[g] || 0) + 1;
    }
    var dt = typeof d.data === 'string' ? new Date(d.data) : null;
    if (dt && isNaN(dt.getTime())) dt = null;
    return {formato: d.formato, codigo: codigo, data: dt, origem: typeof d.origem === 'string' ? d.origem.slice(0, 80) : '', registos: R, n: n, grupos: grupos, fora: fora};
  }

  root.EPIRegistos = Object.freeze({
    VERSAO: VERSAO, LIM: LIM, OUTROS: OUTROS, ALTERADO: ALTERADO,
    ACEITES: ACEITES.slice(), IGNORADAS: IGNORADAS.slice(), DE_FORA: DE_FORA.slice(), PRIVADAS: PRIVADAS.slice(),
    GRUPOS: GRUPOS.map(function (g) { return g[1]; }).concat([OUTROS]),
    classificar: classificar, aceite: aceite, grupoDe: grupoDe, comTexto: comTexto, ehObj: ehObj, limpo: limpo,
    semNome: semNome, hoje: hoje, validarCodigo: validarCodigo, registosParaEntrega: registosParaEntrega,
    montarEntrega: montarEntrega, nomeEntrega: nomeEntrega, validarFicheiro: validarFicheiro
  });
}(typeof window !== 'undefined' ? window : this));
