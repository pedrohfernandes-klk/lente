from pathlib import Path
import functools, itertools, json, os, re, unittest
# Na pasta tests do Lente, a raiz é a pasta de cima; LENTE_RAIZ aponta para outra cópia (nas fontes, antes de o teste ir para o Lente).
R = Path(os.environ.get('LENTE_RAIZ') or Path(__file__).resolve().parents[1])
# As listas do «Repor de um ficheiro» (progresso.mjs nas fontes). 23/10/2026: o caderno publicado ainda é o de 16/10, que exporta e repõe
# todas as chaves sem lista; até o Repor seguro estar publicado, as listas vêm de progresso-aceites.json, que progresso-aceites.mjs gera
# nas fontes e que se copia com este teste para lente/tests. Quando o caderno tiver «var ACEITES=», o teste passa a lê-las de lá.
JSON_LISTAS = Path(__file__).with_name('progresso-aceites.json')

# ---------- recolher as chaves que as páginas escrevem no localStorage (o sessionStorage não vai para o ficheiro) ----------
PULAR = {'.git', 'tests', 'node_modules', '__pycache__'}
ESCRITA = re.compile(r'(?<![\w$.])(?:window\.)?localStorage\s*\.\s*setItem\s*\(')
# a função que embrulha a escrita: «function gravar(k,v){», «gravar=function(k,v){», «gravar:function(k,v){», «gravar(k,v){» ou «gravar=(k,v)=>{»
DONO = re.compile(r'function\s+([\w$]+)\s*\(([^()]*)\)\s*\{|([\w$]+)\s*[:=]\s*function\s*\(([^()]*)\)\s*\{|([\w$]+)\s*=\s*\(([^()]*)\)\s*=>\s*\{|(?<![\w$.])([\w$]+)\s*\(([^()]*)\)\s*\{')
NAO_NOMES = {'if', 'for', 'while', 'switch', 'catch', 'function', 'return', 'with'}
# o próprio «Repor de um ficheiro» escreve as chaves que lê do ficheiro: fica de fora
PROGRESSO = re.compile(r'<script\b[^>]*>(?:(?!</script>).)*?"epi-progresso"(?:(?!</script>).)*</script>', re.S)
LIT = re.compile(r'^"((?:[^"\\]|\\.)*)"$|^\'((?:[^\'\\]|\\.)*)\'$|^`([^`$]*)`$')
# para as partes que mudam (vêm de dados da página): valores plausíveis; uma família de chaves que a lista não conhece falha com todos
ENCHER = ['1', '12', 'ab', 'm1', 'abc', 'abc-def']
# 24/10/2026 (verificação): um atributo que o código escreve («'<input data-check="'+i+'">'») não dá valores do atributo (no histórico
# do pt, «percurso-M4-u'+i+'-check» fazia falhar o teste sem razão)
CONCAT = re.compile(r"'\s*\+|\+\s*'")


def ficheiros(raiz):
    for d, ds, fs in os.walk(raiz):
        ds[:] = [x for x in ds if x not in PULAR]
        for f in fs:
            if f.endswith(('.html', '.js')):
                yield Path(d) / f


def ate(t, i, fim=',)'):
    """o texto desde i até ao primeiro separador de topo (fora de aspas e de parênteses)"""
    d, j, q = 0, i, None
    while j < len(t):
        c = t[j]
        if q:
            if c == '\\':
                j += 2
                continue
            if c == q:
                q = None
        elif c in '"\'`':
            q = c
        elif c in '([{':
            d += 1
        elif c in ')]}':
            if d == 0:
                return t[i:j]
            d -= 1
        elif d == 0 and c in fim:
            return t[i:j]
        j += 1
    return t[i:j]


def fecho(t, i):
    """t[i] é «{»: a posição da chaveta que fecha"""
    d, j, q = 0, i, None
    while j < len(t):
        c = t[j]
        if q:
            if c == '\\':
                j += 2
                continue
            if c == q:
                q = None
        elif c in '"\'`':
            q = c
        elif c == '{':
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                return j
        j += 1
    return len(t)


def argumentos(t, i):
    out = []
    while True:
        x = ate(t, i)
        out.append(x.strip())
        i += len(x)
        if i >= len(t) or t[i] != ',':
            return out
        i += 1


def escritas(t):
    """as expressões de chave que o ficheiro escreve: as diretas e as que passam por um embrulho (com o parâmetro trocado pelo argumento)"""
    W, out = {}, []
    for e in ESCRITA.finditer(t):
        a = ate(t, e.end()).strip()
        janela = t[max(0, e.start() - 600):e.start()]
        base, dono = e.start() - len(janela), None
        for m in DONO.finditer(janela):
            g = m.groups()
            nome, pars = next((g[i], g[i + 1]) for i in (0, 2, 4, 6) if g[i])
            if nome not in NAO_NOMES and fecho(t, base + m.end() - 1) > e.start():
                dono = (nome, [p.strip() for p in pars.split(',') if p.strip()])
        if dono and dono[1] and re.search(r'(?<![\w$.])(' + '|'.join(map(re.escape, dono[1])) + r')(?![\w$])', a):
            W[dono[0]] = (dono[1], a)
        else:
            out.append(a)
    for nome, (pars, a) in W.items():
        for c in re.finditer(r'(?<![\w$.])' + re.escape(nome) + r'\s*\(', t):
            if re.search(r'function\s*$', t[max(0, c.start() - 12):c.start()]):
                continue
            ar = argumentos(t, c.end())
            # 24/10/2026 (verificação): só se salta a definição em forma de método («gravar(k,v){») e a chamada dentro de outro
            # embrulho (o argumento é parâmetro de uma função à volta). Uma variável com o nome do parâmetro («var k='cd1-'+…;
            # gravar(k,v)», nas aulas 1 e 2 de Cidadania) escreve uma chave a sério e conta: antes ficava de fora sem aviso
            if ar and ar[0] in pars and (re.match(r'\s*\{', t[fim_da_chamada(t, c.end()):]) or parametro_a_volta(t, c.start(), ar[0])):
                continue
            sub = a
            for p, v in zip(pars, ar):
                sub = fora_das_aspas(sub, p, '(' + v + ')')
            out.append(sub)
    return out


def fim_da_chamada(t, i):
    """t[i-1] é «(»: a posição a seguir ao «)» que fecha a chamada"""
    d, j, q = 1, i, None
    while j < len(t):
        c = t[j]
        if q:
            if c == '\\':
                j += 2
                continue
            if c == q:
                q = None
        elif c in '"\'`':
            q = c
        elif c == '(':
            d += 1
        elif c == ')':
            d -= 1
            if d == 0:
                return j + 1
        j += 1
    return len(t)


# o cabeçalho de uma função com nome, anónima ou em seta com chavetas («function(k){», «(k)=>{», «gravar(k,v){»)
CABECA = re.compile(r'function\s*[\w$]*\s*\(([^()]*)\)\s*\{|\(([^()]*)\)\s*=>\s*\{|(?<![\w$.])([\w$]+)\s*\(([^()]*)\)\s*\{')


def parametro_a_volta(t, i, nome):
    """nome é parâmetro de uma função cujo corpo contém a posição i (não conta «if(k){», «catch(k){»…)"""
    janela = t[max(0, i - 600):i]
    base = i - len(janela)
    for m in CABECA.finditer(janela):
        if m.group(3) in NAO_NOMES:
            continue
        pars = next((g for g in (m.group(1), m.group(2), m.group(4)) if g is not None), '')
        if nome in [p.strip() for p in pars.split(',')] and fecho(t, base + m.end() - 1) > i:
            return True
    return False


def fora_das_aspas(e, p, v):
    """troca o nome p por v na expressão, sem tocar no que está entre aspas (em «"-u"+n», o «u» não é o parâmetro u)"""
    out, i, q = [], 0, None
    while i < len(e):
        c = e[i]
        if q:
            out.append(e[i:i + 2] if c == '\\' else c)
            if c == q:
                q = None
            i += 2 if c == '\\' else 1
            continue
        if c in '"\'`':
            q = c
            out.append(c)
            i += 1
            continue
        m = re.match(r'[\w$]+', e[i:])
        if m:
            w = m.group(0)
            out.append(v if w == p and (i == 0 or e[i - 1] != '.') else w)
            i += len(w)
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def partir(e, sep):
    out, d, q, i, ini = [], 0, None, 0, 0
    while i < len(e):
        c = e[i]
        if q:
            if c == '\\':
                i += 2
                continue
            if c == q:
                q = None
        elif c in '"\'`':
            q = c
        elif c in '([{':
            d += 1
        elif c in ')]}':
            d -= 1
        elif d == 0 and e.startswith(sep, i) and not (sep == '+' and e.startswith('++', i)):
            out.append(e[ini:i])
            i += len(sep)
            ini = i
            continue
        i += 1
    out.append(e[ini:])
    return [x.strip() for x in out]


def sem_parenteses(e):
    e = e.strip()
    while e.startswith('(') and e.endswith(')') and fecho(e.replace('(', '{').replace(')', '}'), 0) == len(e) - 1:
        e = e[1:-1].strip()
    return e


def atribuicoes(t, nome):
    out = []
    # (não conta um atributo do HTML com o mesmo nome, como data-k="1")
    for m in re.finditer(r'(?<![\w$.-])(?:window\.)?' + re.escape(nome) + r'\s*=(?![=>])', t):
        r = ate(t, m.end(), ',;)').strip()
        # um valor que não pode ser chave (lista, objeto, número, função) é outra variável com o mesmo nome
        if r and not re.match(r'(?:[\[{\d!]|function\b|new\b|true\b|false\b|null\b)', r):
            out.append(r)
    return out


def completo(x):
    return '{' not in x


def resolver(e, t, attrs, prof=0, pilha=()):
    """os moldes de chave de uma expressão; o que não se sabe fica entre chavetas («epi-pt-{E.id}»); pilha: os nomes que já se estão a
    resolver (K=cfg.chave e montar({chave:K}) dão uma volta que não acrescenta nada)"""
    e = sem_parenteses(e)
    if prof > 6:
        return ['{' + e + '}']
    # 24/10/2026 (verificação): «c?a:b» dá as chaves dos dois ramos (no histórico do pt, «(DES?"desafio-":"chefe-")+M+"-u"+u.n»
    # ficava por ler e fazia falhar o teste sem razão)
    q = partir(e, '?')
    if len(q) == 2 and len(partir(q[1], ':')) == 2:
        return [x for p in partir(q[1], ':') for x in resolver(p, t, attrs, prof + 1, pilha)]
    ou = partir(e, '||')
    if len(ou) > 1:
        alt = [resolver(p, t, attrs, prof + 1, pilha) for p in ou if not re.fullmatch(r'\[\]|\{\}|""|\'\'', p)]
        # «a||b»: se «a» se lê por inteiro (um atributo que a página tem), «b» nunca chega a ser usado
        if alt and alt[0] and all(completo(x) for x in alt[0]):
            return alt[0]
        return [x for a in alt for x in a]
    m = LIT.match(e)
    if m:
        return [next(g for g in m.groups() if g is not None)]
    mais = partir(e, '+')
    if len(mais) > 1:
        return [''.join(c) for c in itertools.product(*[resolver(p, t, attrs, prof + 1, pilha) for p in mais])][:300]
    if re.fullmatch(r'[\w$]+', e):
        if e in pilha:
            return []
        # nomes de uma ou duas letras minúsculas são parâmetros e contadores: só conta a atribuição que começa por um texto
        # («var k="percurso-"+M+"-u"+n»)
        rhs = atribuicoes(t, e)
        if len(e) <= 2 and e.islower():
            rhs = [r for r in rhs if r[:1] in '"\'`']
        if rhs:
            alt = [resolver(r, t, attrs, prof + 1, pilha + (e,)) for r in rhs]
            # várias variáveis com o mesmo nome no ficheiro: se alguma dá chaves inteiras, as que ficam de todo desconhecidas são outras
            if any(a and all(completo(x) for x in a) for a in alt):
                alt = [a for a in alt if not all(re.fullmatch(r'\{[^{}]*\}', x) for x in a)]
            return [x for a in alt for x in a]
        return ['{' + e + '}']
    if re.fullmatch(r'(?:[\w$]+\.)+chave', e):
        # a chave que a página dá ao motor dos baralhos em montar({…, chave: …})
        if 'cfg.chave' in pilha:
            return []
        v = sorted({x for c in chaves_de_montar(t) for x in resolver(c, t, attrs, prof + 1, pilha + ('cfg.chave',))})
        return v or ['{cfg.chave}']
    m = re.fullmatch(r'(?:[\w$]+\.)*dataset\.([\w$]+)', e)
    if m:
        # um atributo data-…: os valores da própria página ou, num ficheiro .js, os das páginas do sítio
        at = 'data-' + re.sub(r'([A-Z])', lambda x: '-' + x.group(1).lower(), m.group(1))
        v = sorted(set(x for x in re.findall(re.escape(at) + r'="([^"]*)"', t) if not CONCAT.search(x))) or sorted(attrs.get(at, ()))
        if v:
            return v
    if re.fullmatch(r'window\.[\w$]+', e):
        return resolver(e.split('.', 1)[1], t, attrs, prof + 1, pilha)
    return ['{' + e + '}']


def sem_textos(e):
    """e com o que está entre aspas trocado por «_» (as aspas ficam e o comprimento não muda)"""
    out, i, q = list(e), 0, None
    while i < len(e):
        c = e[i]
        if q:
            if c == '\\':
                out[i:i + 2] = '_' * len(out[i:i + 2])
                i += 2
                continue
            if c == q:
                q = None
            else:
                out[i] = '_'
        elif c in '"\'`':
            q = c
        i += 1
    return ''.join(out)


@functools.lru_cache(maxsize=8)
def chaves_de_montar(t):
    out = []
    for m in re.finditer(r'(?<![\w$])montar\s*\(\s*\{', t):
        obj = t[m.end() - 1:fecho(t, m.end() - 1) + 1]
        # 24/10/2026 (verificação): «chave:» procura-se fora dos textos, e a profundidade conta-se sem eles (no histórico do pt, as
        # pistas de uma lição diziam «é a chave: o herói é símbolo», e isso dava uma chave que não existe; «palavra-chave:» num cartão
        # faria o mesmo)
        so = sem_textos(obj)
        for c in re.finditer(r'(?<![\w$"])chave\s*:\s*', so):
            if so[:c.start()].count('{') - so[:c.start()].count('}') == 1:
                out.append(ate(obj, c.end(), ',}'))
    return tuple(out)


def recolher(raiz):
    """{molde de chave: [ficheiros que a escrevem]} para todas as páginas e scripts do sítio"""
    textos = {}
    for f in ficheiros(raiz):
        t = f.read_text('utf-8', errors='replace')
        if 'setItem' in t or 'montar' in t or 'data-' in t:
            textos[f] = PROGRESSO.sub('', t)
    attrs = {}
    for t in textos.values():
        for a, v in re.findall(r'\b(data-[a-z-]+)="([^"<>]{1,60})"', t):
            if not CONCAT.search(v):
                attrs.setdefault(a, set()).add(v)
    moldes, sufixos, montadas = {}, set(), set()
    for f, t in textos.items():
        if 'setItem' not in t and 'montar' not in t:
            continue
        ks = [x for a in escritas(t) for x in resolver(a, t, attrs)]
        # o motor dos baralhos grava na chave de montar({…, chave: …}) (e em «chave-a1», «chave-v2»…)
        dadas = [x for c in chaves_de_montar(t) for x in resolver(c, t, attrs)]
        ks += dadas
        montadas.update(dadas)
        if re.search(r'function\s+montar\s*\(', t):
            # num motor partilhado (jogo.js), «cfg.chave» é a chave que cada página lhe dá: junta-se às de montar no fim
            sufixos.update(k[len('{cfg.chave}'):] for k in ks if k.startswith('{cfg.chave}'))
            ks = [k for k in ks if not k.startswith('{cfg.chave}')]
        for k in ks:
            moldes.setdefault(k, set()).add(str(f.relative_to(raiz)))
    for s in sufixos - {''}:
        for k in montadas:
            moldes.setdefault(k + s, set()).add('(motor dos baralhos: «' + s + '»)')
    return moldes


# ---------- as listas do Repor ----------
def listas_de(pagina):
    """ACEITES, IGNORADAS e DE_FORA de uma página com o Repor seguro, ou do JSON ao lado, se a página ainda não o tiver"""
    s = pagina.read_text('utf-8') if pagina.exists() else ''
    m = re.search(r'var ACEITES=\[', s)
    if m:
        dec, L = json.JSONDecoder(), {}
        for nome in ('ACEITES', 'IGNORADAS', 'DE_FORA'):
            i = s.index(nome + '=[', m.start()) + len(nome) + 1
            L[nome] = dec.raw_decode(s, i)[0]
        return L, str(pagina)
    return json.loads(JSON_LISTAS.read_text('utf-8')), JSON_LISTAS.name


def decisao(L):
    """o que o Repor faz a uma chave: «repõe», «fica de fora» (sem recusar o ficheiro) ou «recusa» o ficheiro inteiro (como validar())"""
    A, I, F = ([re.compile(r, re.I) for r in L[n]] for n in ('ACEITES', 'IGNORADAS', 'DE_FORA'))
    bate = lambda Ls, k: any(r.search(k) for r in Ls)
    def d(k):
        if len(k) > 160 or k in ('__proto__', 'constructor', 'prototype'):
            return 'recusa'
        if bate(A, k) and not bate(F, k):
            return 'repõe'
        return 'fica de fora' if bate(I, k) or bate(F, k) else 'recusa'
    return d


def recusadas(moldes, d):
    """os moldes que fariam o Repor recusar o ficheiro; uma parte que muda passa se algum valor plausível passar"""
    mal = []
    for k, onde in sorted(moldes.items()):
        partes = re.split(r'\{[^{}]*\}', k)
        if len(partes) > 5:
            mal.append((k, sorted(onde)[:3]))
            continue
        bons = any(d(''.join(p + (v[i] if i < len(v) else '') for i, p in enumerate(partes))) != 'recusa'
                   for v in itertools.product(ENCHER, repeat=len(partes) - 1))
        if not bons:
            mal.append((k, sorted(onde)[:3]))
    return mal


class ChavesDoLente(unittest.TestCase):
    """Um ficheiro de progresso feito hoje nunca é recusado pelo «Repor de um ficheiro» seguro (plano de reestruturação do Lente,
    lote 0, alínea e; 23/10/2026): cada chave que as páginas do Lente escrevem no localStorage é aceite ou fica de fora de propósito.
    O caderno de 16/10 exporta todas as chaves do aparelho, e o Repor seguro recusa o ficheiro inteiro por uma só chave que não conheça."""

    @classmethod
    def setUpClass(cls):
        cls.L, cls.de = listas_de(R / 'caderno' / 'index.html')
        cls.d = staticmethod(decisao(cls.L))
        cls.moldes = recolher(R)

    def test_as_listas_sao_expressoes_inteiras(self):
        for nome in ('ACEITES', 'IGNORADAS', 'DE_FORA'):
            for r in self.L[nome]:
                self.assertTrue(r.startswith('^') and r.endswith('$'), (nome, r))
                re.compile(r)

    def test_o_coletor_encontra_as_chaves_que_ja_se_conhecem(self):
        # o Ginásio, a Justiça, um piloto das vozes, o Duchamp e o som do motor: se o coletor deixar de as ver, deixou de ler as páginas
        for k in ('epi-treinos', 'epi-treinos-interromper', 'lente-justica-licao-1', 'epi-vozes-warhol-v2', 'epi-narrativas-duchamp', 'epi-som'):
            self.assertIn(k, self.moldes, k)

    def test_o_coletor_le_os_embrulhos(self):
        # 24/10/2026 (verificação): uma variável com o nome do parâmetro do embrulho conta (antes ficava de fora sem aviso); o que está
        # entre aspas não se troca pelo argumento; a definição em forma de método e a chamada dentro de outro embrulho não contam
        def ks(t):
            return sorted(x for a in escritas(t) for x in resolver(a, t, {}))
        self.assertEqual(ks('function gravar(k,v){try{localStorage.setItem(k,v)}catch(e){}}var k="nova-"+X;gravar(k,"1")'), ['nova-{X}'])
        self.assertEqual(ks('function partir(n,u){localStorage.setItem("percurso-"+M+"-u"+n+"-copiada","1")}var M="M1";partir(N,U)'),
                         ['percurso-M1-u{N}-copiada'])
        self.assertEqual(ks('function gravar(k,v){localStorage.setItem(k,v)}function salvar(k,v){gravar(k,v)}var o={gravar(k,v){return 1}}'), [])

    def test_o_coletor_nao_inventa_chaves(self):
        # 24/10/2026 (verificação): três casos do histórico do pt que davam chaves que não existem (e o teste falhava sem razão): «chave:»
        # dentro de um texto do baralho, os dois ramos de «c?a:b» e um atributo data-… que o próprio código escreve
        def ks(t):
            return sorted(x for a in escritas(t) for x in resolver(a, t, {}))
        self.assertEqual(chaves_de_montar('EPIJogo.montar({el:b,itens:[{"f":"Distinguir mito e história é a chave: o herói é símbolo"}],'
                                          'pistas:["palavra-chave: mito"],chave:K,fim:function(s){st=s}})'), ('K',))
        self.assertEqual(ks('var M="M1";localStorage.setItem((DES?"desafio-":"chefe-")+M+"-u2","1")'), ['chefe-M1-u2', 'desafio-M1-u2'])
        self.assertEqual(ks('h+=\'<input data-check="\'+i+\'">\';var k="percurso-"+M+"-u"+c.dataset.check+"-check";localStorage.setItem(k,"1")'),
                         ['percurso-{M}-u{c.dataset.check}-check'])

    def test_cada_chave_que_as_paginas_escrevem_e_aceite(self):
        mal = recusadas(self.moldes, self.d)
        self.assertEqual(mal, [], f'chaves que fariam recusar o ficheiro (listas de {self.de}): acrescenta-as a ACEITES ou IGNORADAS em progresso.mjs')

    def test_um_ficheiro_de_hoje_passa(self):
        # o que um aluno tem hoje: um treino, a Justiça, um caso de Cidadania, uma voz, e o que o caderno de 16/10 também exporta
        hoje = {'epi-treinos': 'repõe', 'epi-treinos-sem-olhos': 'repõe', 'lente-justica-licao-1': 'repõe', 'epi-justica-sandel-v1': 'repõe',
                'epi-cid-m1-guardar-ou-partilhar': 'repõe', 'epi-cid-m1-guardar-ou-partilhar-conclusao': 'repõe', 'epi-vozes': 'repõe',
                'epi-vozes-warhol-v2': 'repõe', 'epi-som': 'repõe', 'epi-projection-text-size': 'fica de fora',
                'epi-sugestao-editorial-02-lente': 'fica de fora', 'epi-sala': 'fica de fora'}
        self.assertEqual({k: self.d(k) for k in hoje}, hoje)

    def test_um_ficheiro_antigo_passa(self):
        # 24/10/2026 (verificação): chaves que as páginas já não escrevem mas que um aparelho ainda tem (o caderno de 16/10 exporta
        # tudo): as lições do Português até 10/10 («-ler», «-a2»), o «Chefe da unidade», o jogo do Atlas, o cartaz do ano completo e a
        # Literatura mundial (10 a 16/10, histórico do pt), e os passos do sítio antigo de Cidadania na mesma origem (14 e 15/10)
        antigas = ['licao-m1-f01-ler', 'licao-m2-f06-a2', 'chefe-M1-u2', 'atlas-j3', 'epi-conjunto-1', 'epi-literatura',
                   'epi-literatura-alice', 'epi-literatura-frag', 'epi-cd-mode-v2', 'epi-cd-m1-v1-01', 'epi-cd-m1-v2-10']
        self.assertEqual({k: self.d(k) for k in antigas}, {k: 'repõe' for k in antigas})


if __name__ == '__main__':
    unittest.main()
