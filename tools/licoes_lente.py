"""Gerador das lições em cartões do Lente (30/10/2026), com o motor único das lições (assets/licoes/, cópia do
Português). A primeira a usá-lo é a Cidadania refeita (decisões do docente de 30/10: cada sessão é uma lição em cartões,
12 a 16 de fazer, um único cartão «Na aula», casos primeiro e nenhuma figura em destaque).

Uso: python3 tools/licoes_lente.py tools/licoes/cidadania-m1-s01.json [...]   (sem argumentos: todos os .json da pasta)
     python3 tools/licoes_lente.py --verificar            (valida e confirma que as páginas estão atualizadas)

O .json é a fonte; a página gerada não se edita à mão. A validação corre sempre antes de escrever: se falhar, nada se
escreve e a razão aparece no terminal.

31/10/2026 (coração do Laboratório, «Ideias»): o gerador passa a servir mais do que uma família de lições. O campo
«familia» do .json escolhe, em FAMILIAS, a chave de progresso, o campo do grupo (o módulo da Cidadania ou a secção do
Laboratório), as migalhas e o texto do menu, a classe do <body>, o CSS da família (ao lado de assets/licoes/cidadania.css)
e o <title>. Sem o campo, a família é a Cidadania: os .json da Cidadania não mudam e as páginas saem iguais byte a byte
(tests/test_licoes_lente.py compara-as). Serve também a Cidadania M2 (decisão 40), que usará o mesmo «modulo».

05/11/2026 (plano do molde da Cidadania, pedido 1): cada família tem o seu cfg (FAMILIAS[…]['cfg']); o da Cidadania fixa a
ordem, tira os pontos, conserva o «feita» ao subir a versão e retoma a meio. Com "molde": "cidadania-2026-11" no .json, a página
leva as peças do molde novo e o validador aplica o contrato do molde (validar_molde); sem o campo, valida como até aqui.
python3 tools/licoes_lente.py --ordem FICHEIRO.json escreve a ordem das opções com a semente do motor."""
import html, json, pathlib, re, sys, importlib.util
from urllib.parse import urljoin

ROOT = pathlib.Path(__file__).resolve().parents[1]
PASTA = ROOT / 'tools' / 'licoes'
_contratos = importlib.util.spec_from_file_location('laboratorio_contratos', ROOT / 'tools/laboratorio_contratos.py')
LC = importlib.util.module_from_spec(_contratos); _contratos.loader.exec_module(LC)
# 05/11/2026: decisão 163. O menu ≡ vem do construtor comum (tools/menu_casca.py), o mesmo das peças e da Cidadania estática.
_menu = importlib.util.spec_from_file_location('menu_casca', ROOT / 'tools/menu_casca.py')
MC = importlib.util.module_from_spec(_menu); _menu.loader.exec_module(MC)
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
# 02/11/2026: cache do motor independente da versão pedagógica e do progresso.
VERSAO_FICHEIROS = '20261102-1'

PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a[sm]?|o|ou|uei|ámos)|fichas?|folhas?)(?![\wÀ-ÿ])|[·—]', re.I)
# a mesma lista de nomes de tests/test_lingua_perguntas.py (#76): «Qual das citações…», nunca «Qual citação…»
NOMES = ['frases?', 'citaç(?:ão|ões)', 'afirmaç(?:ão|ões)', 'perguntas?', 'image(?:m|ns)', 'vers(?:ão|ões)', 'recortes?', 'critérios?', 'conclus(?:ão|ões)', 'formulaç(?:ão|ões)', 'reformulaç(?:ão|ões)', 'propostas?', 'utilizaç(?:ão|ões)', 'raz(?:ão|ões)', 'créditos?', 'obras?', 'detalhes?', 'pormenor(?:es)?', 'decis(?:ão|ões)', 'opç(?:ão|ões)', 'respostas?', 'palavras?', 'versos?', 'estrofes?', 'linhas?', 'comparaç(?:ão|ões)', 'interpretaç(?:ão|ões)', 'revis(?:ão|ões)', 'sínteses?', 'justificaç(?:ão|ões)', 'desenvolvimentos?', 'notas?', 'registos?', 'aç(?:ão|ões)', 'alteraç(?:ão|ões)', 'inícios?', 'par(?:es)?', 'trios?', 'procedimentos?', 'promessas?', 'exemplos?', 'textos?', 'parágrafos?', 'títulos?', 'legendas?', 'cenas?', 'persona(?:gem|gens)', 'argumentos?', 'recursos?', 'sentidos?', 'efeitos?', 'ideias?', 'teses?', 'provas?', 'fontes?', 'planos?', 'acontecimentos?', 'hipóteses?', 'nomes?', 'leituras?', 'testemunh(?:a|as|o|os)']
QUAL_NOME = re.compile(r'(?<![A-Za-zÀ-ÿ])(?:Qual|Quais|qual|quais)\s+(?:' + '|'.join(NOMES) + r')(?![A-Za-zÀ-ÿ])')
ORDINAL = re.compile(r'(?:^|[.;:!?]\s+)[AaOo]s?\s+(?:primeir|segund|terceir|quart|últim)[ao]s?\b(?!\s+(?:parágrafo|linha|artigo|passo|cartão|sessão))|\bopç(?:ão|ões)\s+[A-E]\b')
TIPOS_FAZER = {'escolha', 'vf', 'emparelhar', 'sublinhar', 'ordenar', 'completar', 'frase', 'mapa'}
# 31/10/2026: as famílias de lições. «grupo» é o campo do .json com o nome, o endereço e o número do conjunto (o módulo da
# Cidadania; a secção do Laboratório, com «sessoes» e «rotulo»); «css» é o ficheiro da família em assets/licoes/.
FAMILIAS = {
    'cidadania': {'chave': r'epi-cid-m\d-s\d{2}', 'chave_txt': 'epi-cid-mN-sNN', 'grupo': 'modulo',
                  'classe': 'licao-cidadania', 'css': 'cidadania.css',
                  # 05/11/2026 (plano do molde da Cidadania, pedido 1): o cfg da família. A ordem dos cartões e das opções é
                  # fixa e igual na projeção e em todos os telemóveis (aula); sem pontos nem sequências (semPontos); subir a
                  # versão conserva o «feita» (preservarAnterior); recarregar a meio volta ao mesmo cartão durante 12 horas
                  # (retomar); o fim diz «Sessão feita.» (feita) e «O módulo já a marca.» (fim, em FIM_CIDADANIA). As pistas
                  # e o passo do projeto (depois) vêm do .json de cada sessão, quando os tem.
                  'cfg': {'aula': True, 'semPontos': True, 'preservarAnterior': True, 'retomar': 12, 'feita': 'Sessão feita.'}},
    'laboratorio': {'chave': r'epi-lab-[a-z]+-s\d{2}', 'chave_txt': 'epi-lab-<secção>-sNN', 'grupo': 'seccao',
                    'classe': 'licao-laboratorio', 'css': 'laboratorio.css',
                    # 02/11/2026: o Laboratório conserva o feito antigo e deixa de mostrar pontuações.
                    'cfg': {'semPontos': True, 'preservarAnterior': True}},
}
# 05/11/2026 (plano do molde da Cidadania, pedido 1): o progresso comum das lições (era progresso-laboratorio.js). Entra em
# todas as páginas cujo cfg tem preservarAnterior, porque é ele que leva a conclusão antiga para «antes».
PROGRESSO = 'progresso-licoes.js?v=20261105-1'
# o fim da Cidadania: por baixo de «Sessão feita.», a linha que diz que a página do módulo já a conta (fora da projeção e de
# «Só os que errei», o motor só chama cfg.fim no fim da sessão)
FIM_CIDADANIA = ('CFG.fim=function(){var g=document.querySelector("#baralho .cartao.fim .grande");if(!g||document.querySelector('
                 '"#baralho .fim-modulo"))return;var q=document.createElement("p");q.className="frase-fim fim-modulo";'
                 'q.setAttribute("role","status");q.textContent="O módulo já a marca.";g.parentNode.insertBefore(q,g.nextSibling)};')
# 05/11/2026 (plano do molde da Cidadania, pedido 1): o molde novo das sessões, por ficheiro. Com "molde": "cidadania-2026-11"
# no .json, a página leva as peças novas (as aulas claras do Português, o cartão de 820 px no computador, a ampliação de todas
# as figuras, o «i» dos créditos, a peça comum dos artefactos e a identidade da Cidadania em body.molde-cidadania) e o
# validador aplica o contrato do molde (validar_molde). Sem o campo, a lição valida e sai como até aqui.
MOLDE = 'cidadania-2026-11'
# 05/11/2026 (pedido 2, s01 do M1 na versão final): a chave sobe para -2 com os acabamentos do bloco do molde em cidadania.css.
# 06/11/2026 (correções da revisão da s01): sobe para 20261106-1 (pista de cada cartão e ordenar sem passos no lugar em jogo.js;
# o Olha na projeção e o Abre a 320 px em cidadania.css).
# 06/11/2026 (s02 no molde): sobe para 20261106-2 (o Olha na projeção com uma fotografia ao alto, em cidadania.css).
# 06/11/2026 (s04 no molde): sobe para 20261106-3 (o cabeçalho das tabelas dos cartões de ler, em cidadania.css).
VERSAO_MOLDE = '20261106-3'
COMO_LENTE = LENTE + 'como/'
# 06/11/2026 (correções da revisão da s01): nas sessões no molde, o fim diz onde fica marcada a sessão (revisor de pt-PT) e a
# retoma dura oito dias (192 horas), para a segunda aula de 90 minutos, noutro dia, continuar no cartão 16 (plano, secção 2,
# «Duas aulas de 90»). As sessões do piloto ficam como estavam (FIM_CIDADANIA e as 12 horas do cfg da família).
FIM_MOLDE = FIM_CIDADANIA.replace('O módulo já a marca.', 'A página do módulo já a marca como feita.')
RETOMAR_MOLDE = 192


def familia(d):
    return FAMILIAS.get(d.get('familia') or 'cidadania')


def visivel(s):
    s = re.sub(r'<[^>]+>', ' ', str(s))
    s = html.unescape(s).replace('**', '').replace('_', '')
    return re.sub(r'\s+', ' ', s).strip()


def textos(c):
    """Todo o texto que o aluno vê num cartão (para as regras de escrita)."""
    t = []
    # 06/11/2026: a pista própria de cada cartão («pista», sessões no molde) também se lê
    for k in ('p', 'p2', 'f', 'titulo', 'html', 'frase', 'pista'):
        if c.get(k):
            t.append(visivel(c[k]))
    fe = c.get('fe')
    t += [visivel(x) for x in (fe if isinstance(fe, list) else [fe]) if x]
    t += [visivel(x) for x in c.get('o', []) + c.get('passos', [])]
    t += [visivel(x) for par in c.get('pares', []) for x in par]
    for L in c.get('lacunas', []):
        t += [visivel(x) for x in L.get('o', [])]
    for imagem in c.get('imagens', []):
        if isinstance(imagem, dict):t += [visivel(imagem.get('alt','')),visivel(imagem.get('credito',''))]
    if c.get('aula'):
        t += [visivel(v) for v in c['aula'].values()]
    # 31/10/2026: o texto de espera do cartão «mapa» e as ligações do retorno («liga») também se leem
    if c.get('rotulo'):
        t.append(visivel(c['rotulo']))
    t += [visivel(l.get('t', '')) for l in c.get('liga', [])]
    return t


def validar(d):
    erros = []
    try:
        C = LC.cartoes(d)
    except ValueError as exc:
        return [str(exc)]
    F = familia(d)
    if F is None:
        return [f'família desconhecida «{d.get("familia")}» (conhecidas: {", ".join(FAMILIAS)})']
    for k in ('id', 'chave', 'versao', 'titulo', 'h1', 'saida', 'fontes', F['grupo'], 'marca'):
        if not d.get(k):
            erros.append(f'falta o campo «{k}»')
    # 01/11/2026: o passo do método na marca da casca (só no Laboratório): «Passo N de M» ou «Passos N e N+1 de M»
    if d.get('passo') and not re.fullmatch(r'Passos? \d+(?: e \d+)? de \d+', d['passo']):
        erros.append('«passo» tem de ser «Passo N de M» ou «Passos N e N+1 de M»')
    try:
        antigo = LC.registo(d)
    except ValueError as exc:
        erros.append(str(exc));antigo = None
    if not antigo and not re.fullmatch(F['chave'], d.get('chave', '')):
        erros.append(f'a chave tem de ser {F["chave_txt"]}')
    g = d.get(F['grupo']) or {}
    if g and (not g.get('nome') or not str(g.get('url', '')).startswith(LENTE)):
        erros.append(f'«{F["grupo"]}» precisa de «nome» e de um «url» no Lente')
    fazer = [c for c in C if c.get('t') in TIPOS_FAZER]
    erros += LC.regras63(d, C, TIPOS_FAZER)
    # 05/11/2026 (plano do molde da Cidadania, pedido 1): com "molde", o contrato do molde substitui as contagens antigas
    # (12 a 16 de fazer, um «Na aula») e acrescenta as suas regras (validar_molde); sem o campo, tudo como até aqui.
    molde = d.get('molde')
    if molde is not None and molde != MOLDE:
        erros.append(f'molde desconhecido «{molde}» (conhecido: {MOLDE})')
    molde = molde == MOLDE
    if molde and F['grupo'] != 'modulo':
        erros.append('o molde cidadania-2026-11 só se aplica às sessões da Cidadania')
    if not molde and not d.get('regras63') and not 12 <= len(fazer) <= 16:
        erros.append(f'{len(fazer)} cartões de fazer (têm de ser 12 a 16)')
    if not C or C[0].get('rot') != 'Abre':
        erros.append('o primeiro cartão tem de ser o «Abre»')
    elif '<img' in C[0].get('html', '') or C[0].get('ver'):
        erros.append('o «Abre» não leva imagem (casos primeiro, nenhuma figura em destaque)')
    if not C or C[-1].get('rot') != 'Para levar' or not C[-1].get('escuro'):
        erros.append('o último cartão tem de ser o «Para levar» (escuro)')
    na_aula = [i for i, c in enumerate(C) if c.get('rot') == 'Na aula']
    if molde:
        if na_aula:
            erros.append('no molde não há «Na aula»: o momento da aula é o «Em turma», e o resto vive no guia do docente')
    elif len(na_aula) != 1:
        erros.append(f'{len(na_aula)} cartões «Na aula» (tem de haver exatamente um)')
    else:
        antes = sum(1 for c in C[:na_aula[0]] if c.get('t') in TIPOS_FAZER)
        depois = sum(1 for c in C[na_aula[0]:] if c.get('t') in TIPOS_FAZER)
        if antes < 6 or depois < 3:
            erros.append(f'blocos desequilibrados: {antes} cartões de fazer antes do «Na aula» e {depois} depois')
    leitura = 0
    for i, c in enumerate(C, 1):
        t = c.get('t')
        onde = f'cartão {i} ({t} {c.get("rot") or c.get("g") or ""})'
        linguistico = dict(c)
        if d.get('familia') == 'laboratorio' and c.get('html'):
            limpo, problemas = LC.texto_literal(c['html'])
            erros += [f'{onde}: {e}' for e in problemas]
            linguistico['html'] = limpo
        for x in textos(linguistico):
            m = PROIBIDAS.search(x)
            if m:
                erros.append(f'{onde}: «{m.group(0)}» não pode aparecer')
            m = QUAL_NOME.search(x)
            if m:
                erros.append(f'{onde}: «{m.group(0)}» (escreve «Qual das…» ou «Que…»)')
        if c.get('imagens') is not None:
            imgs=c['imagens'];opcoes=c.get('o',[]) if t=='escolha' else c.get('passos',[])
            if t not in ('escolha','ordenar') or not isinstance(imgs,list) or len(imgs)!=len(opcoes):
                erros.append(f'{onde}: imagens exige uma imagem por opção ou passo')
            elif any(not isinstance(f,dict) or not all(isinstance(f.get(k),str) and f[k].strip() for k in ('src','alt','credito')) or re.match(r'^(?:javascript:|data:)',f.get('src',''),re.I) for f in imgs):
                erros.append(f'{onde}: cada imagem exige src, alt e credito válidos')
        if t == 'ler':
            n = len(visivel(c.get('html', '')).split())
            leitura += n
            if n > 140:
                erros.append(f'{onde}: {n} palavras num cartão de ler (máximo 140)')
            continue
        if t not in TIPOS_FAZER:
            erros.append(f'{onde}: tipo desconhecido')
            continue
        if not c.get('p') or not c.get('p2') or not c.get('f'):
            erros.append(f'{onde}: faltam p, p2 ou f')
        fe = c.get('fe')
        for txt in [c.get('f') or ''] + (fe if isinstance(fe, list) else [fe or '']):
            if ORDINAL.search(visivel(txt)):
                erros.append(f'{onde}: o feedback refere uma opção pela posição')
        if t == 'escolha':
            o, cc = c.get('o') or [], c.get('c')
            if not (2 <= len(o) <= 4) or not isinstance(cc, int) or not 0 <= cc < len(o):
                erros.append(f'{onde}: opções ou certa inválidas')
                continue
            if not isinstance(fe, list) or len(fe) != len(o) or fe[cc] or not all(fe[j] for j in range(len(o)) if j != cc):
                erros.append(f'{onde}: cada opção errada precisa de um «fe» (e a certa de "")')
            L = [len(visivel(x)) for x in o]
            maior_errada = max(L[j] for j in range(len(o)) if j != cc)
            if max(L) / min(L) > 1.20:
                erros.append(f'{onde}: opções com mais de 20 % de diferença {L}')
            if L[cc] >= 1.25 * maior_errada and L[cc] - maior_errada >= 5:
                erros.append(f'{onde}: a certa denuncia-se pelo tamanho {L}')
        elif t == 'vf':
            if not isinstance(c.get('v'), bool) or not fe:
                erros.append(f'{onde}: «v» tem de ser verdadeiro ou falso, com «fe»')
        elif t == 'emparelhar':
            if len(c.get('pares') or []) < 3 or not fe:
                erros.append(f'{onde}: pelo menos três pares, com «fe»')
        elif t == 'sublinhar':
            w = (c.get('frase') or '').split()
            if not c.get('certas') or any(not 0 <= j < len(w) for j in c['certas']):
                erros.append(f'{onde}: «certas» fora da frase')
        elif t == 'ordenar':
            if len(c.get('passos') or []) < 3:
                erros.append(f'{onde}: pelo menos três passos')
        # 30/10/2026: o tipo «mapa» (tocar numa zona de uma figura) entra no Lente com o coração do Laboratório (31/10): uma
        # zona por opção, com o centro na figura e a mesma ordem; a figura é um <svg> com um grupo .op-m por zona (data-j).
        elif t == 'mapa':
            o, cc, cs, fig = c.get('o') or [], c.get('c'), c.get('centros') or [], c.get('fig') or ''
            if not (2 <= len(o) <= 6) or not isinstance(cc, int) or not 0 <= cc < len(o):
                erros.append(f'{onde}: opções ou certa inválidas')
            elif len(cs) != len(o) or not all(isinstance(p, list) and len(p) == 2 and all(isinstance(v, (int, float)) for v in p) for p in cs):
                erros.append(f'{onde}: «centros» tem de ter um ponto [x, y] por opção')
            elif '<svg' not in fig or sorted(int(j) for j in re.findall(r'class="op-m"[^>]*data-j="(\d+)"', fig)) != list(range(len(o))):
                erros.append(f'{onde}: a figura tem de ser um <svg> com uma zona .op-m (data-j) por opção')
            if not isinstance(fe, str) or not fe:
                erros.append(f'{onde}: falta o «fe» de quem erra')
    if leitura > 900:
        erros.append(f'{leitura} palavras de leitura na sessão (máximo 900)')
    # opções da sessão: a certa não pode ser sempre a mais longa (nem sempre a mais curta)
    esc = [c for c in C if c.get('t') == 'escolha']
    if len(esc) >= 3:
        longa = sum(1 for c in esc if len(visivel(c['o'][c['c']])) == max(len(visivel(x)) for x in c['o']))
        curta = sum(1 for c in esc if len(visivel(c['o'][c['c']])) == min(len(visivel(x)) for x in c['o']))
        if longa == len(esc) or curta == len(esc):
            erros.append('a certa é sempre a mais longa ou sempre a mais curta')
    # 05/11/2026 (plano do molde da Cidadania, pedido 1): as pistas e o passo do projeto («depois») também se leem
    for x in [visivel(p) for p in d.get('pistas') or []] + ([visivel(d['depois'])] if d.get('depois') else []):
        m = PROIBIDAS.search(x) or QUAL_NOME.search(x)
        if m:
            erros.append(f'pistas ou «depois»: «{m.group(0)}» não pode aparecer')
    if molde:
        erros += validar_molde(d, C)
    return erros


# 05/11/2026 (plano do molde da Cidadania, pedido 1): a semente do motor (assets/licoes/jogo.js: semear, rnd, mist e opcoes,
# com cfg.aula) em Python, para saber em que lugar fica a resposta certa de cada escolha, igual na projeção e em todos os
# telemóveis. tests/browser_licoes_lente.cjs confere-a com a página.
def _semente(chave, k):
    h = 2166136261
    b = f'{chave}:{k}'.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h = ((h ^ int.from_bytes(b[i:i + 2], 'little')) * 16777619) & 0xFFFFFFFF
    return [h]


def _mist(s, a):
    a = list(a)
    for q in range(len(a) - 1, 0, -1):
        s[0] = (s[0] * 1664525 + 1013904223) & 0xFFFFFFFF
        j = (s[0] * (q + 1)) >> 32
        a[q], a[j] = a[j], a[q]
    return a


def ordem_opcoes(d):
    """[(índice do cartão, ordem das opções no ecrã)] para cada escolha, como o motor as mostra com cfg.aula."""
    out = []
    for k, c in enumerate(LC.cartoes(d)):
        if c.get('t') != 'escolha' or not isinstance(c.get('c'), int):
            continue
        s, idx, cc = _semente(d['chave'], k), list(range(len(c.get('o') or []))), c['c']
        out.append((k, _mist(s, idx) if len(idx) <= 3 else _mist(s, [cc] + _mist(s, [j for j in idx if j != cc])[:2])))
    return out


def sem_no_lugar(a):
    """06/11/2026: o mesmo que semNoLugar() de assets/licoes/jogo.js (com cfg.aula): roda a ordem até nenhum passo ficar no seu
    lugar, no máximo n vezes; se nenhuma rotação servir, troca os dois primeiros da ordem da semente."""
    a = list(a)
    fica = lambda v: any(k == q for q, k in enumerate(v))
    if len(a) < 2:
        return a
    b, r = a[:], 0
    while r < len(a) and fica(b):
        b = b[1:] + b[:1]
        r += 1
    if fica(b):
        b = a[:]
        b[0], b[1] = b[1], b[0]
    return b


def ordem_ordenar(d, k):
    """06/11/2026: a ordem dos passos de um ordenar no ecrã (semente do motor e sem_no_lugar), igual na projeção, em todos os
    telemóveis e na versão para imprimir."""
    c = LC.cartoes(d)[k]
    return sem_no_lugar(_mist(_semente(d['chave'], k), list(range(len(c.get('passos') or [])))))


def posicoes_certas(d):
    C = LC.cartoes(d)
    return [ordem.index(C[k]['c']) for k, ordem in ordem_opcoes(d)]


def recolha_cfg(d):
    """A configuração da peça comum dos artefactos (assets/licoes/recolha.js) numa sessão no molde: uma chave por módulo."""
    m = re.fullmatch(r'(epi-cid-m\d)-s\d{2}', d.get('chave', ''))
    mod = d.get('modulo') or {}
    return {'chave': (m.group(1) if m else d.get('chave', '')) + '-artefactos', 'sessao': d.get('chave', ''), 'titulo': d.get('titulo', ''),
            'colecao': f'Cidadania, módulo {mod.get("n", "")}, {mod.get("nome", "")}', 'nome': 'artefactos', 'lista': 'Os teus artefactos'}


TIPOS_ITEM = {'reconhecer', 'distinguir', 'aplicar', 'transferir'}
QUATRO_CAMPOS = ('O que se faz', 'Quanto tempo', 'O que fica escrito', 'Se estás sozinho')
RET_PROIBIDO = re.compile(r'(?<![\wÀ-ÿ])(?:d?o\s+exercício|d?a\s+opção)(?![\wÀ-ÿ])', re.I)
GRUPO = re.compile(r'(?<![\wÀ-ÿ])grupos?(?![\wÀ-ÿ])(?!\s+da\s+turma)', re.I)
DOCENTE = re.compile(r'(?<![\wÀ-ÿ])docentes?(?![\wÀ-ÿ])', re.I)
REF_PARTIDA = re.compile(r'(?<![\wÀ-ÿ])(?:n\.º|n\.os|artigos?|art\.|alínea)[ \t\r\n]+(?=\d)', re.I)
# 06/11/2026 (decisão 152, revisão da s01): também as datas («21 de setembro de 1990», «novembro de 1949») e os números com
# unidade ou nome («12 anos», «60 min») não partem; tools/cidadania_molde.py (ref) mete-lhes o espaço inseparável.
MESES = r'(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)'
DATA_PARTIDA = re.compile(r'(?<!\d)\d{1,2}(?:[ \u00a0]+de){1}[ \u00a0]+' + MESES + r'(?:[ \u00a0]+de[ \u00a0]+\d{4})?|' + MESES + r'[ \u00a0]+de[ \u00a0]+\d{4}', re.I)
NUMERO_PARTIDO = re.compile(r'(?<![\w.,/:])\d+ (?!(?:que|com|por|sem|dos|das|nos|nas|não|mas|para|pela|pelo|como|mais|até|foi|era|são)(?![\wÀ-ÿ]))(?=[a-zà-ÿ]{3,})')
LICENCA = re.compile(r'Domínio público|CC0|CC BY(?:-SA)?(?: \d\.\d)?', re.I)
LICENCA_NAO = re.compile(r'CC BY-N[CD]|BY-NC|BY-ND|NoDerivs|NonCommercial', re.I)
CREDITO_A_VISTA = re.compile(r'Domínio público|CC0|CC BY|Wikimedia|Library of Congress|Metropolitan|Fotografia de|licença', re.I)
TIPOS_ROT_GENERICOS = {'Escolhe', 'Verdadeiro ou falso', 'Completa', 'Toca nas palavras', 'Ordena', 'Liga os pares', 'Põe por ordem', 'Faz'}


def sem_details(s):
    """O HTML sem os <details> (o que fica à vista sem abrir nada; os details contam à parte)."""
    s = str(s or '')
    while True:
        n = re.sub(r'<details\b[^>]*>(?:(?!<details\b).)*?</details>', ' ', s, flags=re.S)
        if n == s:
            return s
        s = n


def sem_caso(s):
    """O HTML sem o texto dos casos inventados (elementos com a classe «caso»)."""
    return re.sub(r'<(\w+)\b[^>]*\bclass="[^"]*\bcaso\b[^"]*"[^>]*>.*?</\1>', ' ', str(s or ''), flags=re.S)


# 07/11/2026: decisão 179 (docente, no cartão de opções). A regra da decisão 146 («grupo» só no texto de um caso inventado)
# não se aplica ao texto de um excerto de lei registado em tools/cidadania_fontes.json e copiado letra a letra (o artigo 30.º da
# Convenção diz «conjuntamente com membros do seu grupo»). Só sai da verificação o excerto cujo identificador existe no registo e
# cujos pedaços, entre «[…]», estão todos no texto registado; tudo o resto do cartão continua a ser verificado.
_REGISTO_FONTES = None


def sem_lei_registada(s):
    """O HTML sem os excertos de lei registados e conferidos com o registo (data-fonte), só para a regra de «grupo»."""
    global _REGISTO_FONTES
    if _REGISTO_FONTES is None:
        dados = json.loads((ROOT / 'tools' / 'cidadania_fontes.json').read_text(encoding='utf-8'))
        lista = dados if isinstance(dados, list) else dados.get('excertos', [])
        _REGISTO_FONTES = {e.get('id'): html.unescape(e.get('texto') or '') for e in lista}

    def tirar(m):
        texto = _REGISTO_FONTES.get(m.group(2))
        corpo = html.unescape(re.sub(r'<[^>]+>', '', m.group(3))).replace('\u00a0', ' ')
        corpo = re.sub(r'^.*?«|»\s*$', '', corpo, flags=re.S) if '«' in corpo else corpo
        pedacos = [x.strip(' .,;:') for x in corpo.split('[…]') if x.strip(' .,;:')]
        if texto and pedacos and all(x in texto.replace('\u00a0', ' ') for x in pedacos):
            return ' '
        return m.group(0)
    return re.sub(r'<(p|span)\b[^>]*\bdata-fonte="([^"]+)"[^>]*>(.*?)</\1>', tirar, str(s or ''), flags=re.S)


def validar_molde(d, C):
    """O contrato do validador do molde cidadania-2026-11 (plano do molde, secção 5): só para os .json com o campo «molde»."""
    erros = []
    n = len(C)
    if n < 6:
        return ['molde: cartões a menos para o contrato']
    sessao10 = bool(re.search(r'-s10$', d.get('id', '')))
    eh_fazer = [c.get('t') in TIPOS_FAZER for c in C]
    # Abre, Decide e os dois Recupera
    a = C[0]
    if not (a.get('aula') or {}).get('linha'):
        erros.append('molde: o «Abre» precisa da linha «Hoje» (aula.linha)')
    if 'Caso inventado.' not in (a.get('html') or '') and not re.search(r'class="fonte"[^>]*>.*?<a href="https://', a.get('html') or '', re.S):
        erros.append('molde: o «Abre» diz «Caso inventado.» ou traz a fonte oficial do caso real, com ligação')
    dc = C[1]
    h = dc.get('html') or ''
    if dc.get('t') != 'ler' or dc.get('rot') != 'Decide':
        erros.append('molde: o 2.º cartão é o «Decide»')
    elif not re.search(r'class="posicao"[^>]*data-artefacto=', h) or len(re.findall(r'<details class="lado"', h)) != 3 or 'Não há resposta certa' not in h:
        erros.append('molde: o «Decide» tem a posição (.posicao com data-artefacto), três lados e «Não há resposta certa»')
    for k in (2, 3):
        if not eh_fazer[k] or C[k].get('g') != 'recupera':
            erros.append(f'molde: o cartão {k + 1} é um «Recupera» (g «recupera»)')
    if eh_fazer[3] and not C[3].get('origem'):
        erros.append('molde: o 2.º «Recupera» diz a sessão de origem («origem»)')
    # cada exercício
    fazer = [(i, c) for i, c in enumerate(C) if eh_fazer[i]]
    for i, c in fazer:
        onde = f'molde, cartão {i + 1} ({c.get("t")})'
        if not c.get('rot') or c['rot'] in TIPOS_ROT_GENERICOS:
            erros.append(f'{onde}: «rot» próprio, que diz a ideia (nunca «Escolhe»)')
        if not c.get('p2'):
            erros.append(f'{onde}: falta «p2»')
        fe = c.get('fe')
        if not fe or (isinstance(fe, list) and not any(fe)):
            erros.append(f'{onde}: falta o retorno de erro («fe»)')
        for txt in [c.get('f') or ''] + (fe if isinstance(fe, list) else [fe or '']):
            if RET_PROIBIDO.search(visivel(txt)):
                erros.append(f'{onde}: o retorno não fala «do exercício» nem «da opção»')
        if c.get('tipo') not in TIPOS_ITEM or not c.get('conceito'):
            erros.append(f'{onde}: «tipo» (reconhecer, distinguir, aplicar, transferir) e «conceito»')
        if c.get('prod') == 'escrita':
            erros.append(f'{onde}: nenhuma escrita no ecrã (a escrita é em papel)')
        if c.get('g') != 'recupera' and not (c.get('ver') or c.get('cita')) and not any(C[j].get('t') == 'ler' for j in range(2, i)):
            erros.append(f'{onde}: material antes, no mesmo bloco, ou «ver» ou «cita» no próprio cartão')
        # 06/11/2026 (revisão da s01): cada exercício tem a sua pista, que não dá a resposta (a opção certa, as palavras certas
        # de um sublinhar, o lado direito de um par)
        pista = visivel(c.get('pista') or '')
        if not pista:
            erros.append(f'{onde}: falta a pista própria do cartão («pista»)')
        else:
            dar = []
            if c.get('t') == 'escolha' and isinstance(c.get('c'), int) and c.get('o'):
                dar.append(c['o'][c['c']])
            if c.get('t') == 'sublinhar' and c.get('certas'):
                w = (c.get('frase') or '').split()
                dar.append(' '.join(w[j] for j in c['certas'] if 0 <= j < len(w)))
            dar += [par[1] for par in c.get('pares') or []]
            sem = lambda t: ' '.join(re.sub(r'[^\wÀ-ÿ]+', ' ', visivel(t).lower()).split())
            if any(sem(x) and sem(x) in sem(pista) for x in dar):
                erros.append(f'{onde}: a pista dá a resposta («{pista}»)')
        if c.get('t') == 'ordenar' and any(k == q for q, k in enumerate(ordem_ordenar(d, i))):
            erros.append(f'{onde}: um passo fica no seu lugar na ordem do ecrã {ordem_ordenar(d, i)}')
    alvo = 7 if sessao10 else 14
    if len(fazer) != alvo:
        erros.append(f'molde: {len(fazer)} cartões de fazer (têm de ser {alvo})')
    if len({c.get('t') for _, c in fazer}) < 5:
        erros.append('molde: pelo menos cinco tipos de exercício')
    if sum(c.get('t') == 'escolha' for _, c in fazer) > 6:
        erros.append('molde: no máximo seis escolhas')
    if any(C[i].get('t') == C[i + 1].get('t') == C[i + 2].get('t') for i in range(n - 2)):
        erros.append('molde: nunca três cartões seguidos do mesmo tipo (contando os de ler)')
    if not sessao10:
        if sum(c.get('tipo') in ('aplicar', 'transferir') for _, c in fazer) < 6:
            erros.append('molde: pelo menos seis exercícios de aplicar ou transferir')
        if not any(c.get('origem') and c.get('g') != 'recupera' for _, c in fazer):
            erros.append('molde: um conceito espaçado fora dos «Recupera» («origem» de duas ou mais sessões antes)')
    # «Em turma», «Agora, em papel» e Para levar
    turma = [i for i, c in enumerate(C) if c.get('rot') == 'Em turma']
    volta = [i for i, c in enumerate(C) if c.get('rot') == 'Volta ao caso']
    if len(turma) != 1:
        erros.append(f'molde: {len(turma)} cartões «Em turma» (tem de haver exatamente um)')
    else:
        t, ht = turma[0], visivel(C[turma[0]].get('html') or '')
        if C[t].get('t') != 'ler' or not volta or volta[0] > t:
            erros.append('molde: o «Em turma» é um cartão de ler, na parte 2, depois da «Volta ao caso»')
        if not all(x in ht for x in QUATRO_CAMPOS):
            erros.append('molde: o «Em turma» tem os quatro campos (O que se faz, Quanto tempo, O que fica escrito, Se estás sozinho)')
        if 'class="posicao"' not in (C[t].get('html') or ''):
            erros.append('molde: o «Em turma» tem a posição depois do material (.posicao)')
        if sum(eh_fazer[t + 1:]) < 3:
            erros.append('molde: pelo menos três cartões de fazer depois do «Em turma»')
    papel = C[-2]
    hp = visivel(papel.get('html') or '')
    if papel.get('rot') != 'Agora, em papel' or 'O que conta' not in hp or 'código' not in hp.lower():
        erros.append('molde: «Agora, em papel» em penúltimo, com «O que conta» e «código»')
    if not d.get('depois'):
        erros.append('molde: falta «depois» (o passo de hoje do projeto, no fim)')
    # palavras à vista e tempos
    total = 0
    for i, c in enumerate(C):
        if c.get('t') != 'ler':
            continue
        nv = len(visivel(sem_details(c.get('html') or '')).split())
        total += nv
        if nv > (90 if i == 0 else 80):
            erros.append(f'molde, cartão {i + 1} ({c.get("rot")}): {nv} palavras à vista (máximo {90 if i == 0 else 80}; os details contam à parte)')
    if total > 650:
        erros.append(f'molde: {total} palavras à vista nos cartões de ler (máximo 650)')
    tempos = d.get('tempos')
    if any(not isinstance(c.get('min'), int) or c['min'] <= 0 for c in C) or not isinstance(tempos, dict) \
            or any(not isinstance(v, int) or v < 0 for v in tempos.values()):
        erros.append('molde: cada cartão tem «min» e a sessão tem «tempos» (folga, pausa, projeto, entrega), em minutos')
    else:
        soma = sum(c['min'] for c in C) + sum(tempos.values())
        if not 175 <= soma <= 185:
            erros.append(f'molde: {soma} minutos (entre 175 e 185)')
    # turma, docente, imagens e referências
    for i, c in enumerate(C):
        onde = f'molde, cartão {i + 1} ({c.get("t")} {c.get("rot") or ""})'
        partes = [sem_caso(c.get('html') or '')] + [c.get(k) or '' for k in ('p', 'p2', 'f', 'frase', 'cita', 'pista')]
        fe = c.get('fe')
        partes += (fe if isinstance(fe, list) else [fe or '']) + list(c.get('o') or []) + list(c.get('passos') or [])
        partes += [x for par in c.get('pares') or [] for x in par] + [str(v) for v in (c.get('aula') or {}).values()]
        for txt in partes:
            v = visivel(txt)
            if GRUPO.search(visivel(sem_lei_registada(txt))):
                erros.append(f'{onde}: «grupo» só no texto de um caso inventado (decisão 146)')
            if DOCENTE.search(v):
                erros.append(f'{onde}: nenhuma instrução ao aluno depende do docente (decisão 154)')
            sem_tags = html.unescape(re.sub(r'<[^>]+>', ' ', str(txt)))
            if REF_PARTIDA.search(sem_tags):
                erros.append(f'{onde}: referência com espaço que parte («n.º 2», «artigo 12.º»): usa o espaço inseparável (decisão 152)')
            if any(' ' in m.group(0) for m in DATA_PARTIDA.finditer(sem_tags)) or NUMERO_PARTIDO.search(sem_tags):
                erros.append(f'{onde}: data ou número com unidade com espaço que parte («21 de setembro de 1990», «12 anos»): usa o espaço inseparável (decisão 152)')
        for bloco in [c.get('html') or '', c.get('ver') or '']:
            for fig in re.findall(r'<figure\b.*?</figure>', bloco, flags=re.S):
                if '<img' not in fig:
                    continue
                m = re.search(r'<details class="info-i(?: info-i--linha)?" name="info-i"><summary aria-label="(?:Créditos|Fonte)[^"]*"><span aria-hidden="true">i</span></summary><p class="info-i-texto">(.*?)</p></details>', fig, flags=re.S)
                if not m:
                    erros.append(f'{onde}: cada imagem tem o crédito atrás do «i» (details.info-i, decisão 153)')
                    continue
                if not LICENCA.search(m.group(1)) or LICENCA_NAO.search(m.group(1)) or '<a href="https://' not in m.group(1):
                    erros.append(f'{onde}: o «i» diz a licença (domínio público, CC0, CC BY ou CC BY-SA) e liga à fonte')
                if re.search(r'<span class="moldura[^"]*"', fig):
                    erros.append(f'{onde}: a moldura com «i» é um div, não um span')
                cap = re.search(r'<figcaption>(.*?)</figcaption>', fig, flags=re.S)
                if cap and CREDITO_A_VISTA.search(visivel(cap.group(1))):
                    erros.append(f'{onde}: o crédito vai para o «i»; a legenda só diz o que serve a pergunta')
    # a posição da certa, com a semente do motor
    pos = posicoes_certas(d)
    if pos:
        mais = max(pos.count(p) for p in set(pos))
        if len(pos) >= 3 and mais > len(pos) / 2:
            erros.append(f'molde: a certa cai no mesmo lugar em mais de metade das escolhas {pos}')
        if any(pos[i] == pos[i + 1] == pos[i + 2] for i in range(len(pos) - 2)):
            erros.append(f'molde: a certa cai no mesmo lugar três vezes seguidas {pos}')
    return erros


def esc(s):
    return html.escape(str(s), quote=True)


# 31/10/2026 (revisão de pt-PT): títulos de obras em itálico também nas fontes. Converte _…_ em <i>…</i> depois de escapar,
# com a guarda do motor (assets/licoes/jogo.js, função it): só quando o _ não está colado a letras, a algarismos ou a «/»,
# para não estragar endereços como convencao_sobre_direitos_da_crianca.pdf ou File:William_Edward_Kilburn_-_View….
ITALICO = re.compile(r'(^|[^0-9A-Za-zÀ-ÖØ-öø-ÿ_/])_([^_\n<>]{1,100}?)_(?![0-9A-Za-zÀ-ÖØ-öø-ÿ_])')


def esc_it(s):
    return ITALICO.sub(r'\1<i>\2</i>', esc(s))


# 01/11/2026 (correção 2 do coração do Laboratório, diretor de arte): o navegador parte a linha no hífen de uma forma verbal
# com pronome («largá-|lo», «subiu-|lhe») sem repetir o hífen na linha seguinte, como manda o AO90 (base XX). nq() envolve
# essas formas em <span class="nq"> (white-space:nowrap no CSS da família), só no texto e nunca dentro das etiquetas nem
# duas vezes. Usam-na o Laboratório (tools/licoes/ideias-sNN.py, nos cartões de ler, e tools/ideias_piloto.py); a Cidadania
# não a chama, e as suas páginas ficam iguais byte a byte.
NQ_RE = re.compile(r'(?<![\w-])([^\W\d_]+(?:-(?:lo|la|los|las|lhe|lhes|se|me|te|nos|vos|o|a|os|as|no|na|nas))+'
                   r'(?:-(?:á|ás|ão|ei|emos|eis|ia|ias|íamos|íeis|iam))?)(?![\w-])')


def nq(s):
    partes = re.split(r'(<[^>]+>)', s)
    for i in range(0, len(partes), 2):
        if not (i and partes[i - 1] == '<span class="nq">'):
            partes[i] = NQ_RE.sub(r'<span class="nq">\1</span>', partes[i])
    return ''.join(partes)


def _ctx_cidadania(d, mod):
    # 05/11/2026: decisão 163. «Lente» e «Cidadania» (decisão 150, nomes de uma palavra) em vez de «Página inicial» e
    # «Cidadania e Desenvolvimento»; o mesmo destino tem sempre o mesmo nome; as fontes de hoje, inteiras, num details.
    # 06/11/2026: fusão do main (com a sessão 1 da Cidadania, #126). O menu ≡ serve também as sessões no molde novo
    # (cidadania/m1/sessoes/01/), que este gerador escreve como as do piloto. «Como se faz (vídeos)» vai para os vídeos do Lente
    # (COMO_LENTE, que o molde pedia, é o mesmo endereço que menu_casca.COMO) em todas as sessões, no molde e fora dele.
    modulo = f'Módulo {mod["n"]}: {mod["nome"]}'
    return {'cab': f'Cidadania, módulo {mod["n"]}', 'titulo': d['titulo'], 'onde': modulo + '.',
            'voltar': (mod['url'], 'Voltar ao módulo', modulo), 'seguinte': _seguinte(d, mod), 'papel': None, 'projecao': True,
            'caminho': [('Lente', LENTE), ('Cidadania', LENTE + 'cidadania/'), (modulo, mod['url'])],
            'fontes': f'EPI, Escola Profissional de Imagem. Cidadania e Desenvolvimento 2026/2027. {esc(d["titulo"])}. Fontes: {esc_it(d["fontes"])} O que marcas fica só neste aparelho.'}


def _ctx_laboratorio(d, sec):
    # 31/10/2026 (revisão de pt-PT): o ponto final só se junta a um título que não acabe já em «?» ou «!» (era «observar?.»)
    tit = esc(d['titulo']) + ('' if d['titulo'].rstrip().endswith(('?', '!')) else '.')
    passo = (d['passo'][0].lower() + d['passo'][1:]) if d.get('passo') else ''
    return {'cab': f'Laboratório, {sec["nome"]}', 'titulo': d['titulo'], 'onde': f'{sec["nome"]}' + (f', {passo}.' if passo else '.'),
            'voltar': (sec['url'], f'Voltar ao {sec["nome"]}', 'As sessões e o método'), 'seguinte': _seguinte(d, sec),
            'papel': (sec['url'] + 'guiao/', 'Guião para imprimir'), 'projecao': True,
            'caminho': [('Lente', LENTE), ('Laboratório', LENTE + 'narrativas/'), (sec['nome'], sec['url'])],
            'fontes': f'EPI, Escola Profissional de Imagem. Laboratório, {esc(sec["nome"])}: {esc(sec["subtitulo"])}. {tit} Fontes: {esc_it(d["fontes"])} O que marcas fica só neste aparelho.'}


def _seguinte(d, grupo):
    """«Seguinte» no menu só quando o destino é diferente do de «Voltar»."""
    if not d.get('seguinte') or urljoin(LENTE + d['saida'], d['seguinte']) == grupo['url']:
        return None
    rot = d.get('seguinteRotulo') or ''
    return (d['seguinte'], 'Seguinte', rot)


def pagina(d):
    saida = d['saida']
    prof = saida.count('/')
    base = '../' * prof
    F = familia(d)
    lab = F['grupo'] == 'seccao'
    mod = d[F['grupo']]
    piloto = d.get('piloto')
    dados = json.dumps(LC.cartoes(d), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    ctx = _ctx_laboratorio(d, mod) if lab else _ctx_cidadania(d, mod)
    menu = MC.menu(ctx)
    cfg = {'versao': d['versao'], 'marca': d['marca'], 'chave': d['chave'], 'titulo': d['titulo'], 'variar': False}
    # 02/11/2026: o Laboratório conserva o feito antigo e deixa de mostrar pontuações.
    # 05/11/2026 (plano do molde da Cidadania, pedido 1): o cfg vem da família (FAMILIAS[…]['cfg']); na Cidadania, as pistas e o
    # passo do projeto («depois») vêm da sessão, quando os tem.
    cfg.update(F.get('cfg', {}))
    if not lab:
        for k in ('pistas', 'depois'):
            if d.get(k):
                cfg[k] = d[k]
    molde = d.get('molde') == MOLDE
    if molde:
        cfg['retomar'] = RETOMAR_MOLDE  # 06/11/2026: oito dias, ver RETOMAR_MOLDE
    # 31/10/2026 (revisão do diretor de arte, sistema 6.11): o ecrã final leva «A seguir» (a sessão seguinte) e o módulo.
    # Verificação final: quando a seguinte já é o módulo (a s10 aponta para ../m1/), o módulo não se repete ao lado, como
    # ligação e como botão para o mesmo destino; fica só o botão.
    if d.get('seguinte'):
        if urljoin(LENTE + d['saida'], d['seguinte']) != mod['url']:
            cfg.update({'percurso': mod['url'], 'percursoRotulo': mod['rotulo'] if lab else 'As 10 sessões'})
        # 31/10/2026 (quarta correção, diretor de arte): espaço inseparável depois das palavras de uma letra, para o rótulo do
        # botão não acabar a linha em «A» («Sessão 02: A / imagem dos outros», a 320 px, com text-wrap:balance).
        cfg.update({'seguinte': d['seguinte'], 'seguinteRotulo': re.sub(r'(?<!\S)(\w) ', '\\1\u00a0', d.get('seguinteRotulo') or '') or None})
    extra = ''
    if lab and d.get('registo'):
        nav, extra = LC.continuacao(d)
        cfg.update(nav)
    # 30/10/2026: o leitor de vídeo (cópia do do Português) só entra quando há um cartão com vídeo.
    tem_video = any('data-yt=' in (c.get('html') or '') for c in d['cartoes'])
    # 31/10/2026: <title>, classe do <body>, CSS e marca da casca pela família (a Cidadania como estava; o Laboratório com o
    # padrão das peças do Laboratório: «título | secção | Laboratório | Lente»).
    titulo = (f'{esc(d["titulo"])} | {esc(mod["nome"])} | Laboratório | Lente' if lab else f'{esc(d["titulo"])} · Cidadania · Lente')
    # 01/11/2026 (método): no Laboratório, com o campo «passo», o <title> diz também o passo do método («Sessão 1: Ver ou
    # observar? (passo 1 de 5) | Ideias | Laboratório | Lente»), porque abaixo de 430 px a marca da casca não tem lugar para ele
    if lab and d.get('passo'):
        titulo = f'{esc(d["titulo"])} ({esc(d["passo"][0].lower() + d["passo"][1:])}) | {esc(mod["nome"])} | Laboratório | Lente'
    # 05/11/2026: decisão 163. Na Cidadania, «CD» passa a «Cidadania» (escondida abaixo de 400 px, como a do Laboratório) e o
    # nome acessível começa pelo texto visível; o «marca» dos JSON, que o motor usa, não muda.
    # 05/11/2026 (revisão): no Laboratório, o nome acessível da marca passa a «Laboratório, Ideias» (paralelo a «Cidadania, módulo N»
    # e ao cabeçalho do menu); «Voltar a Ideias» dava ao mesmo destino outro nome que o primeiro item do menu («Voltar ao Ideias»).
    marca = (f'<a class="c-marca" href="{esc(mod["url"])}" aria-label="Laboratório, {esc(mod["nome"])}">' if lab
             else f'<a class="c-marca" href="{esc(mod["url"])}" aria-label="Cidadania, módulo {mod["n"]}">')
    # 01/11/2026 (correção 2 do coração do Laboratório, diretor de arte): no Laboratório, o nome da marca vai num <span>, que
    # assets/licoes/laboratorio.css esconde abaixo de 400 px («Ideias» tem 81 px e empurrava o botão Menu para fora do ecrã a
    # 320 e 360 px); o aria-label continua a dizer o nome. A Cidadania fica como estava, byte a byte.
    marca_t = f'<span class="c-marca-t">{esc(d["marca"])}</span>' if lab else '<span class="c-marca-t">Cidadania</span>'
    # 01/11/2026 (método do coração do Laboratório): no Laboratório, o passo do método («Passo 1 de 5») segue a marca numa
    # <span> própria, à vista em todos os cartões; assets/licoes/laboratorio.css junta-lhe a vírgula quando o nome se vê e
    # deixa-o sozinho abaixo de 400 px. Sem o campo «passo» (e na Cidadania) a barra fica como estava, byte a byte.
    # 05/11/2026: decisão 163. Sai: o passo ficava encostado ao contador «1/21» como um segundo contador; passa para o menu
    # («Ideias, passo 1 de 5.») e continua no <title>.
    return (
        '<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f'<title>{titulo}</title>'
        + ('<meta name="robots" content="noindex, nofollow">' if piloto else '')
        + f'<meta name="description" content="{esc(d["h1"])}">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Special+Elite&display=swap" rel="stylesheet">'
        f'<link rel="stylesheet" href="{base}assets/licoes/lesson.css?v={VERSAO_FICHEIROS}">'
        # 05/11/2026 (plano do molde da Cidadania, pedido 1): no molde novo, as peças do Português e as comuns entram antes do CSS
        # da família, que tem a última palavra.
        + (''.join(f'<link rel="stylesheet" href="{base}assets/{f}?v={VERSAO_MOLDE}">' for f in (
            'licoes/aula-clara.css', 'licoes/casca-pc.css', 'licoes/ampliar-documentos.css', 'licoes/recolha.css', 'info-i.css')) if molde else '')
        + f'<link rel="stylesheet" href="{base}assets/licoes/{F["css"]}?v={VERSAO_MOLDE if molde else VERSAO_FICHEIROS}">'
        f'<link rel="stylesheet" href="{base}assets/appearance.css"><script src="{base}assets/appearance.js"></script>'
        f'<link rel="stylesheet" href="{base}assets/licoes/menu.css?v={MC.V}"></head><body class="licao-lente {F["classe"]}{" molde-cidadania" if molde else ""}" data-licao="{esc(d["id"])}">'
        '<div class="casca" data-casca>'
        f'<header class="casca-topo">{marca}<svg class="c-casa" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8.2 8 2.6l6 5.6M4 7v7h3v-4h2v4h3V7"/></svg>{marca_t}</a>'
        '<span class="c-num" data-c-num></span><button type="button" class="c-barra" data-c-barra aria-label="Ver os cartões já feitos" disabled><svg viewBox="0 0 1 10" preserveAspectRatio="none" aria-hidden="true"></svg></button>'
        '<span class="c-modo" data-c-modo hidden></span><button type="button" class="c-ic" data-c-como aria-label="Como se faz" title="Como se faz" hidden><span class="c-roda">?</span></button>'
        '<button type="button" class="c-ic" data-c-som aria-pressed="false" aria-label="Som" title="Som ligado ou desligado"><span class="c-roda">♪</span></button>'
        '<button type="button" class="c-ic" data-c-menu aria-label="Menu" aria-expanded="false" aria-controls="c-menu" title="Menu"><span class="c-tres"></span></button></header>'
        f'<h1 class="c-sr">{esc(d["h1"])}</h1><main class="casca-corpo" id="casca-corpo" tabindex="-1">{MC.semjs(ctx, "sessão")}<div id="baralho" class="jogo-alvo"></div></main>'
        '<footer class="casca-acoes" data-c-acoes></footer><section class="casca-folha" data-c-folha role="status" aria-live="polite" hidden></section>'
        + menu + extra + '</div><div id="aviso" role="status"></div>'
        # 05/11/2026 (plano do molde da Cidadania, pedido 1): o progresso comum entra onde o cfg pede preservarAnterior
        + (f'<script src="{base}assets/licoes/{PROGRESSO}"></script>' if cfg.get('preservarAnterior') else '')
        + (f'<script defer src="{base}assets/licoes/relogio.js?v={VERSAO_FICHEIROS}"></script>' if (lab or molde) and any('data-relogio=' in c.get('html','') for c in LC.cartoes(d)) else '')
        + (''.join(f'<script src="{base}assets/{f}?v={VERSAO_MOLDE}"></script>' for f in (
            'licoes/aula-clara.js', 'licoes/ampliar-documentos.js', 'info-i.js', 'licoes/recolha.js')) if molde else '')
        # 05/11/2026: no molde, o motor e a casca (com a retoma e o COMO do Lente) entram com a chave de cache nova
        +f'<script src="{base}assets/licoes/casca.js?v={VERSAO_MOLDE if molde else VERSAO_FICHEIROS}"></script><script src="{base}assets/licoes/jogo.js?v={VERSAO_MOLDE if molde else VERSAO_FICHEIROS}"></script>'
        + f'<script defer src="{base}assets/licoes/menu.js?v={MC.V}"></script>'
        + (f'<script defer src="{base}assets/licoes/video-youtube.js?v={VERSAO_FICHEIROS}"></script>' if tem_video else '')
        + f'<script defer src="{base}assets/projection-launcher.js" data-site="lente"></script>'
        '<script>(function(){"use strict";var CARTOES=' + dados + ',CFG=' + json.dumps(cfg, ensure_ascii=False) + ';'
        'var el=document.getElementById("baralho");CFG.el=el;CFG.itens=CARTOES;CFG.casca=window.EPICasca?EPICasca.pagina():null;'
        + (LC.fim_registo(d) if lab else FIM_MOLDE if molde else FIM_CIDADANIA)
        + (f'if(window.EPIRecolha)EPIRecolha.ligar({json.dumps(recolha_cfg(d), ensure_ascii=False)});' if molde else '')
        + 'if(window.EPIJogo)EPIJogo.montar(CFG);})();</script></body></html>\n')


def carregar(p):
    return json.loads(pathlib.Path(p).read_text('utf-8'))


def main(argv):
    verificar = '--verificar' in argv
    fontes = [pathlib.Path(a) for a in argv if not a.startswith('--')] or sorted(PASTA.glob('*.json'))
    # 05/11/2026 (plano do molde da Cidadania, pedido 1): --ordem escreve, em JSON, a ordem das opções de cada escolha com a
    # semente do motor (cfg.aula), para tests/browser_licoes_lente.cjs a conferir com a página. Não escreve páginas.
    if '--ordem' in argv:
        print(json.dumps({carregar(p)['chave']: ordem_opcoes(carregar(p)) for p in fontes}))
        return 0
    falhou = False
    for p in fontes:
        d = carregar(p)
        erros = validar(d)
        if erros:
            falhou = True
            print(f'{p.name}: {len(erros)} problema(s)')
            for e in erros:
                print('  -', e)
            continue
        alvo = ROOT / d['saida']
        novo = pagina(d)
        if verificar:
            if not alvo.exists() or alvo.read_text('utf-8') != novo:
                falhou = True
                print(f'{p.name}: {d["saida"]} está desatualizada (corre o gerador)')
            else:
                print(f'{p.name}: ok')
        else:
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_bytes(novo.encode('utf-8'))
            print(f'{p.name}: escrito {d["saida"]}')
    return 1 if falhou else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
