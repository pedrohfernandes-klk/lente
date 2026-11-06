"""05/11/2026: decisão 163 (menus do Laboratório). Peças comuns da navegação do Laboratório, usadas por
tools/laboratorio.py e tools/ideias_piloto.py:

- barra(): a barra única «Lente › Laboratório» (decisão 44: papel, filete a tinta, o atual sublinhado a vermelho);
- fio(): as quatro partes do Laboratório (Ideias, Observar, Treinar, Criar) com os passos do método (decisão 97);
- sessoes_publicadas() e liga_ideias(): a ligação de uma porta ou de um percurso às sessões do Ideias, calculada pelo
  campo «passo» das sessões publicadas (nada se inventa; quando saírem as sessões 3 a 7, as ligações aparecem sozinhas).

Quando a barra comum do Lente (decisão 44, tarefa 156) entrar, troca-se a barra só aqui."""
from pathlib import Path
import html, json, posixpath, re

R = Path(__file__).resolve().parents[1]
D = json.loads((R / 'assets/laboratorio/percursos.json').read_text('utf-8'))
ABS = 'https://pedrohfernandes-klk.github.io/lente/'
# versão dos ficheiros novos (lab3.css, percursos.js), para a cache do navegador
V = '20261105-163'
e = html.escape


def link(base, path):
    return posixpath.relpath(path or '.', base) + ('/' if not path or path.endswith('/') else '')


def bloco(bid):
    return next(b for b in D['blocks'] if b['id'] == bid)


def cartaz(passos):
    """O número do método em cartaz: «1», «2–3», «4–5» (meia-risca de intervalo)."""
    return str(passos[0]) if len(passos) == 1 else f'{passos[0]}–{passos[-1]}'


def extenso(passos):
    """«Passo 1», «Passos 2 e 3»: (palavra, números)."""
    if len(passos) == 1:
        return 'Passo ', str(passos[0])
    return 'Passos ', ', '.join(map(str, passos[:-1])) + ' e ' + str(passos[-1])


def rotulo_porta(b):
    """«Observar, passo 1» / «Treinar, passos 2 e 3» (rótulo das páginas de percurso)."""
    p, n = extenso(b['passos'])
    return f'{b["title"]}, {p.strip().lower()} {n}'


def barra(base, entrada=False):
    lab = link(base, 'narrativas/')
    atual = ' aria-current="page"' if entrada else ''
    return ('<header class="lab-barra"><div class="pg"><nav class="migalhas" aria-label="Onde estás">'
            f'<a href="{e(link(base, ""))}">Lente</a><span class="sep" aria-hidden="true">›</span>'
            f'<a href="{e(lab)}"{atual}>Laboratório</a></nav><span data-appearance-control></span></div></header>')


def fio(base, atual=None, modo='page'):
    """atual: 'ideias', 'ver', 'treinar', 'criar' ou None; modo: 'page' na própria página, 'true' dentro de uma porta."""
    itens = [('ideias', 'Ideias', 'Passos ', '1 a 5')] + [(b['id'], b['title'], *extenso(b['passos'])) for b in D['blocks']]
    out = '<nav class="lab-fio" aria-label="Partes do Laboratório">'
    for bid, nome, pl, n in itens:
        cur = f' aria-current="{modo}"' if bid == atual else ''
        out += (f'<a href="{e(link(base, "narrativas/" + bid + "/"))}"{cur}><span class="n"><span class="pl">{pl}</span>{n}</span>'
                f'<b>{nome}</b></a>')
    return out + '</nav>'


def sessoes_publicadas():
    """As sessões do Ideias publicadas (as mesmas de ideias_publicadas(): não piloto e com o ficheiro de saída)."""
    out = []
    for p in sorted((R / 'tools/licoes').glob('ideias-s*.json')):
        d = json.loads(p.read_text('utf-8'))
        if d.get('piloto') or not (R / d['saida']).exists():
            continue
        m = re.match(r'Sessão (\d+): (.+)$', d['titulo'])
        passo = re.match(r'Passo (\d+) de 5', d.get('passo') or '')
        out.append({'n': int(m[1]), 'titulo': m[2], 'chave': d['chave'], 'versao': d['versao'],
                    'url': d['saida'].removesuffix('index.html'), 'passo': int(passo[1]) if passo else None})
    return out


def liga_ideias(base, passos, sessao=None):
    """«No Ideias, este passo faz-se na sessão 1, «Ver ou observar?», e na sessão 2, «O cocheiro».» Só com sessões."""
    ss = [s for s in sessoes_publicadas() if (s['n'] == sessao if sessao else s['passo'] in passos)]
    if not ss:
        return ''
    partes = [f'na sessão {s["n"]}, «<a href="{e(link(base, s["url"]))}">{e(s["titulo"])}</a>»' for s in ss]
    lista = partes[0] if len(partes) == 1 else ', '.join(partes[:-1]) + ', e ' + partes[-1]
    suj = 'este passo faz-se' if len(passos) == 1 else 'estes passos fazem-se'
    return f'<p class="liga-ideias">No Ideias, {suj} {lista}.</p>'


def css(base):
    return f'<link rel="stylesheet" href="{e(link(base, "assets/laboratorio/lab3.css"))}?v={V}">'
