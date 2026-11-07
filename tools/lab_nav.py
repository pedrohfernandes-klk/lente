"""05/11/2026: decisão 163 (menus do Laboratório). Peças comuns da navegação do Laboratório, usadas por
tools/laboratorio.py e tools/ideias_piloto.py:

- barra(): a barra única «Lente › Laboratório» (decisão 44: papel, filete a tinta, o atual sublinhado a vermelho);
- fio(): as quatro partes do Laboratório (Ideias, Observar, Treinar, Criar), só com os nomes;
- sessoes_publicadas(): as sessões do Ideias publicadas, para a entrada do Laboratório.
07/11/2026: decisão 180 (docente). As três portas não são passos de um método com ordem. Saem cartaz(), extenso(),
rotulo_porta() e liga_ideias(), que davam a cada porta e a cada percurso os «passos» do Ideias.

Quando a barra comum do Lente (decisão 44, tarefa 156) entrar, troca-se a barra só aqui."""
from pathlib import Path
import html, json, posixpath, re

R = Path(__file__).resolve().parents[1]
D = json.loads((R / 'assets/laboratorio/percursos.json').read_text('utf-8'))
ABS = 'https://pedrohfernandes-klk.github.io/lente/'
# versão dos ficheiros novos (lab3.css, percursos.js), para a cache do navegador
# 07/11/2026: decisão 180, o fio novo muda lab3.css: versão nova para não servir a folha antiga em cache.
V = '20261107-180'
e = html.escape


def link(base, path):
    return posixpath.relpath(path or '.', base) + ('/' if not path or path.endswith('/') else '')


def bloco(bid):
    return next(b for b in D['blocks'] if b['id'] == bid)


def barra(base, entrada=False):
    lab = link(base, 'narrativas/')
    atual = ' aria-current="page"' if entrada else ''
    return ('<header class="lab-barra"><div class="pg"><nav class="migalhas" aria-label="Onde estás">'
            f'<a href="{e(link(base, ""))}">Lente</a><span class="sep" aria-hidden="true">›</span>'
            f'<a href="{e(lab)}"{atual}>Laboratório</a></nav><span data-appearance-control></span></div></header>')


def fio(base, atual=None, modo='page'):
    """atual: 'ideias', 'ver', 'treinar', 'criar' ou None; modo: 'page' na própria página, 'true' dentro de uma porta."""
    # 07/11/2026: decisão 180 (docente). As portas não são passos de um método com ordem: o fio diz só os nomes das quatro
    # partes. Antes, cada parte levava os seus «passos» (Ideias 1 a 5, Observar 1, Treinar 2 e 3, Criar 4 e 5).
    # 07/11/2026: nota do docente à decisão 180: «Ideias é a primeira de todas as coisas, com ou sem ordem, é a espinha dorsal».
    # O Ideias vem à cabeça, destacado; as três portas vêm juntas a seguir, num grupo sem sequência (lab3.css).
    def item(bid, nome):
        cur = f' aria-current="{modo}"' if bid == atual else ''
        return f'<a href="{e(link(base, "narrativas/" + bid + "/"))}"{cur}><b>{nome}</b></a>'
    return ('<nav class="lab-fio" aria-label="Partes do Laboratório">' + item('ideias', 'Ideias')
            + '<span class="fio-portas" role="group" aria-label="As três portas">' + ''.join(item(b['id'], b['title']) for b in D['blocks'])
            + '</span></nav>')


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


# 05/11/2026 (revisão): a classe da projeção entra no <head>, antes das folhas de estilo, para a raiz crescer (22 px) antes da
# primeira pintura, sem salto de layout; percursos.js e entrada.js continuam a pô-la (sem efeito).
PROJ = ("<script>if(/[?&]projetar=1(&|$)/.test(location.search)||self!==top)"
        "document.documentElement.classList.add('em-projecao')</script>")


def css(base):
    return f'<link rel="stylesheet" href="{e(link(base, "assets/laboratorio/lab3.css"))}?v={V}">'
