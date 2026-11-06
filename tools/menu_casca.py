"""05/11/2026: decisão 163 (menus do Laboratório e das lições). Um só construtor para o menu ≡ das quatro famílias que
usam a casca das lições: as sessões do Ideias e do piloto da Cidadania (tools/licoes_lente.py), as peças do Laboratório
(continuacao() de tools/laboratorio.py) e as páginas estáticas da Cidadania (M1, M2 e 25 de Abril, com --estaticas).

O menu responde a três perguntas, por esta ordem: onde estás («Estás em»), como voltas («Voltar a…», a primeira ação) e o
que vem a seguir («Seguinte»). Depois vêm as ações da sessão (os cartões já feitos, a projeção, a versão para imprimir e os
vídeos), o caminho, o tema, as fontes e a nota do aparelho. casca.js e jogo.js não mudam (são cópias do Português): o foco
preso, a posição e os cartões já feitos vivem em assets/licoes/menu.js; o desenho em assets/licoes/menu.css.

Uso: python3 tools/menu_casca.py --estaticas            (escreve as 33 páginas estáticas da Cidadania; idempotente)
     python3 tools/menu_casca.py --estaticas --verificar (falha se alguma página estiver por atualizar)"""
from pathlib import Path
import html, posixpath, re, sys

R = Path(__file__).resolve().parents[1]
ABS = 'https://pedrohfernandes-klk.github.io/lente/'
COMO = ABS + 'como/'
V = '20261105-163'
e = html.escape

IC = {
    'voltar': '<path d="M12.5 4 6.5 10l6 6" fill="none" stroke="currentColor" stroke-width="2"/>',
    'seguinte': '<path d="M7.5 4l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2"/>',
    'rever': '<path d="M4.5 10a5.5 5.5 0 1 0 1.8-4.1M4 3v4h4" fill="none" stroke="currentColor" stroke-width="2"/>',
    'ecra': '<path d="M2.5 4h15v9h-15zM10 13v3M6 17h8" fill="none" stroke="currentColor" stroke-width="2"/>',
    'papel': '<path d="M5.5 7V2.5h9V7M5.5 14h-3V7h15v7h-3M5.5 11h9v6.5h-9z" fill="none" stroke="currentColor" stroke-width="2"/>',
    'como': '<circle cx="10" cy="10" r="7.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8.5 7.5l4 2.5-4 2.5z" fill="currentColor"/>',
}


def ic(nome):
    return f'<svg class="ic" viewBox="0 0 20 20" width="20" height="20" aria-hidden="true" focusable="false">{IC[nome]}</svg>'


def item(href, icone, rotulo, apoio=None, cls='', seta=True, attrs=''):
    tag = 'a' if href is not None else 'button'
    abre = (f'<a{" class=" + chr(34) + cls + chr(34) if cls else ""} href="{e(href)}"{attrs}>' if tag == 'a'
            else f'<button type="button"{" class=" + chr(34) + cls + chr(34) if cls else ""}{attrs}>')
    texto = e(rotulo) + (f'<small>{e(apoio)}</small>' if apoio else '')
    fim = '<span class="seta" aria-hidden="true">→</span>' if seta else '<span class="seta" aria-hidden="true"></span>'
    return f'{abre}{ic(icone)}<span>{texto}</span>{fim}</{tag}>'


def menu(ctx):
    """05/11/2026 (revisão): o nome acessível do diálogo junta o cabeçalho e o título («Laboratório, Criar Exposição, nó,
    desenlace»), para o leitor de ecrã dizer que é o menu e onde se está.
    ctx: cab, titulo, onde, voltar=(href, rotulo, apoio), seguinte=(href, rotulo, apoio)|None, papel=(href, rotulo)|None,
    projecao (bool), caminho=[(rotulo, href)], fontes (HTML)|None; opcionais: nota (HTML; a nota própria da página, em vez da
    nota do aparelho) e mais (uma <nav class="m-orig"> com as ligações e os botões de um motor próprio, que ficam como estão)."""
    v = ctx['voltar']
    nav = item(v[0], 'voltar', v[1], v[2], cls='principal', seta=False)
    if ctx.get('seguinte'):
        s = ctx['seguinte']
        nav += item(s[0], 'seguinte', s[1], s[2])
    nav += '<span class="grupo" aria-hidden="true"></span>'
    nav += item(None, 'rever', 'Ver os cartões já feitos', 'Só para ler. O que fizeste fica guardado.', seta=False,
                attrs=' data-c-rever hidden')
    if ctx.get('projecao', True):
        nav += item('?projetar=1', 'ecra', 'Projetar na aula', 'Letra grande, um passo de cada vez.', cls='so-normal')
        nav += item('?', 'ecra', 'Sair da projeção', cls='so-aula', attrs=' hidden')
    if ctx.get('papel'):
        nav += item(ctx['papel'][0], 'papel', ctx['papel'][1])
    nav += item(ctx.get('como') or COMO, 'como', 'Como se faz (vídeos)')
    caminho = ''.join(f'<li><a href="{e(h)}">{e(r)}</a></li>' for r, h in ctx['caminho'])
    fontes = (f'<details class="m-fontes"><summary>Fontes e créditos</summary><p>{ctx["fontes"]}</p></details>'
              if ctx.get('fontes') else '')
    return ('<div class="casca-menu m2" data-c-painel hidden>'
            '<div class="c-menu-in" id="c-menu" role="dialog" aria-modal="true" aria-labelledby="m-cab m-t">'
            f'<div class="c-menu-cab"><p id="m-cab">{e(ctx["cab"])}</p>'
            '<button type="button" class="c-ic" data-c-fecha-menu aria-label="Fechar o menu">✕</button></div>'
            f'<div class="m-aqui"><p class="k">Estás em</p><p class="t" id="m-t">{e(ctx["titulo"])}</p>'
            f'<p class="pos">{e(ctx["onde"])} <span data-c-pos></span></p></div>'
            f'<nav aria-label="Menu">{nav}</nav>{ctx.get("mais") or ""}'
            f'<ol class="m-caminho" aria-label="Onde estás">{caminho}</ol>'
            '<div class="m-pe"><span>Tema</span><span data-appearance-control></span></div>'
            f'{fontes}<p class="m-nota">{ctx.get("nota") or "O que fazes fica só neste aparelho."}</p></div></div>')


def semjs(ctx, tipo='peça'):
    """O aviso sem JavaScript, dentro de main.casca-corpo (os cartões precisam do motor)."""
    v = ctx['voltar']
    acao = re.sub(r'^Voltar\b', 'volta', v[1])  # «Voltar ao percurso» → «volta ao percurso» (imperativo, com «tu»)
    papel = f' ou abre a <a href="{e(ctx["papel"][0])}">versão para imprimir</a>' if ctx.get('papel') else ''
    artigo = 'desta' if tipo in ('peça', 'sessão') else 'deste'
    return (f'<noscript><p class="c-semjs">Os cartões {artigo} {tipo} precisam de JavaScript. Sem ele, '
            f'<a href="{e(v[0])}">{e(acao)}</a>{papel}.</p></noscript>')


def fim_div(s, i):
    """Índice a seguir ao </div> que fecha o <div> que começa em i (conta as aberturas e os fechos)."""
    n = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        n += 1 if m.group(0) == '<div' else -1
        if n == 0:
            return i + m.end()
    raise ValueError('div sem fecho')


def com_controls(s):
    """O ≡ da barra leva aria-controls="c-menu" (o id do painel); casca.js continua a atualizar aria-expanded."""
    if 'aria-controls="c-menu"' in s:
        return s
    s, n = re.subn(r'(<button type="button" class="c-ic" data-c-menu aria-label="Menu" aria-expanded="false")', r'\1 aria-controls="c-menu"', s, count=1)
    assert n == 1, 'botão ≡ por encontrar'
    return s


def trocar_menu(s, novo):
    i = s.find('<div class="casca-menu')
    if i < 0:
        raise ValueError('página sem casca-menu')
    j = fim_div(s, i)
    return s[:i] + novo + s[j:]


def ativos(s, rel):
    """menu.css antes de </head> e menu.js (defer) antes de </body>, uma vez. Se já lá estão, ficam no mesmo sítio (só a
    versão se atualiza), para não disputar o fim do <head> com outros passos (tools/videos_escolhidos.py)."""
    css = f'<link rel="stylesheet" href="{rel}assets/licoes/menu.css?v={V}">'
    js = f'<script defer src="{rel}assets/licoes/menu.js?v={V}"></script>'
    assert s.count('</head>') == 1 and s.count('</body>') == 1
    s, n = re.subn(r'<link rel="stylesheet" href="[^"]*assets/licoes/menu\.css\?v=[^"]*">', lambda m: css, s)
    if not n:
        s = s.replace('</head>', css + '</head>', 1)
    s, n = re.subn(r'<script defer src="[^"]*assets/licoes/menu\.js\?v=[^"]*"></script>', lambda m: js, s)
    if not n:
        s = s.replace('</body>', js + '</body>', 1)
    return s


def com_semjs(s, ctx, tipo):
    s = re.sub(r'<noscript><p class="c-semjs">.*?</p></noscript>', '', s)
    if '<noscript' in s:  # a página já tem o seu aviso (25 de Abril): fica o dela
        return s
    alvo = '<main class="casca-corpo" id="casca-corpo" tabindex="-1">'
    assert s.count(alvo) == 1, 'main.casca-corpo'
    return s.replace(alvo, alvo + semjs(ctx, tipo), 1)


# --- páginas estáticas da Cidadania (cópias do Português, sem gerador próprio) -------------------------------------
MODULOS = {'1': 'Humanos', '2': 'Algoritmos'}


def estaticas():
    fs = sorted((R / 'cidadania/m1').glob('*/index.html')) + sorted((R / 'cidadania/m2').glob('*/index.html'))
    fs = [f for f in fs if '<div class="casca-menu' in f.read_text('utf-8')] + [R / 'cidadania/25-de-abril/index.html']
    return fs


def titulo_de(url):
    """O título de uma página do sítio (para «Seguinte»), lido da própria página: «Estás em» do menu ou o <title>."""
    if not url.startswith(ABS):
        return None
    f = R / url[len(ABS):] / 'index.html'
    if not f.exists():
        return None
    s = f.read_text('utf-8')
    m = re.search(r'id="m-t">([^<]*)<', s) or re.search(r'<span class="aqui"[^>]*>Estás em: ([^<]*)<', s)
    if m:
        return html.unescape(m[1])
    t = re.search(r'<title>([^<]*)</title>', s)
    return html.unescape(re.split(r' \| | · ', t[1])[0]) if t else None


CASA = re.compile(r'<a class="c-marca" href="[^"]*" aria-label="[^"]*">(<svg class="c-casa"[^>]*>.*?</svg>)(?:<span class="c-marca-t">)?Cidadania(?:</span>)?</a>')


def com_marca(s, ctx):
    """05/11/2026 (revisão): a marca da barra das páginas estáticas, como no piloto. Nas M1 e M2 leva ao módulo e chama-se
    «Cidadania, módulo N» (antes ia à entrada do Lente com «Página inicial (Cidadania)», o mesmo destino que o caminho do menu
    chama «Lente»); no 25 de Abril continua a levar à Cidadania e chama-se «Cidadania». O nome visível vai num <span>, que
    assets/licoes/menu.css esconde abaixo de 400 px (o nome acessível continua a dizê-lo). Idempotente."""
    m = re.match(r'Cidadania, módulo (\d)$', ctx['cab'])
    if m:
        href, nome = f'{ABS}cidadania/m{m[1]}/', f'Cidadania, módulo {m[1]}'
        assert ctx['voltar'][0] == href, (ctx['voltar'][0], href)
    else:
        href, nome = None, 'Cidadania'
    i = s.find('<header class="casca-topo">')
    j = s.find('</header>', i)
    assert i >= 0 and j > i, 'casca-topo'
    def nova(x):
        destino = e(href) if href else re.search(r'href="([^"]*)"', x[0])[1]
        return f'<a class="c-marca" href="{destino}" aria-label="{e(nome)}">{x[1]}<span class="c-marca-t">Cidadania</span></a>'
    topo, n = CASA.subn(nova, s[i:j], count=1)
    assert n == 1, 'marca da barra'
    return s[:i] + topo + s[j:]


def ctx_estatica(f, s):
    rel = posixpath.relpath('.', f.parent.relative_to(R).as_posix()) + '/'
    menu_html = s[s.find('<div class="casca-menu'):fim_div(s, s.find('<div class="casca-menu'))]
    if 'class="casca-menu m2"' in menu_html:  # segunda volta: lê o menu novo
        caminho = [(html.unescape(r), h) for h, r in re.findall(r'<li><a href="([^"]*)">([^<]*)</a></li>', menu_html)]
        titulo = html.unescape(re.search(r'id="m-t">([^<]*)<', menu_html)[1])
        papel = re.search(r'<a href="([^"]*)"><svg class="ic"[^>]*>' + re.escape(IC['papel']) + r'</svg><span>([^<]*)</span>', menu_html)
        papel = (html.unescape(papel[1]), html.unescape(papel[2])) if papel else None
    else:
        ol = re.search(r'<ol class="c-migalhas"[^>]*>(.*?)</ol>', menu_html, re.S)
        if not ol:
            raise ValueError(f'{f}: sem migalhas no menu')
        niveis = re.findall(r'<a href="([^"]*)">(?:<svg.*?</svg>)?([^<]*)</a>', ol[1])
        aqui = re.search(r'Estás em: ([^<]*)<', ol[1])
        if not niveis or not aqui:
            raise ValueError(f'{f}: migalhas por ler')
        nomes = {'Página inicial': 'Lente', 'Cidadania e Desenvolvimento': 'Cidadania'}
        caminho = [(nomes.get(html.unescape(r), html.unescape(r)), h) for h, r in niveis]
        titulo = html.unescape(aqui[1])
        resto = menu_html[menu_html.find('</ol>'):]
        papel = None
        for h, r in re.findall(r'<a href="([^"]*)">([^<]*)</a>', resto):
            if 'papel' in r or 'imprimir' in r.lower():
                papel = (h, html.unescape(r))
    m = re.match(r'Módulo (\d): (.+)$', caminho[-1][0])
    if m:
        n, nome = m[1], m[2]
        if MODULOS.get(n) != nome:
            raise ValueError(f'{f}: módulo {n} desconhecido')
        cab, onde = f'Cidadania, módulo {n}', f'Módulo {n}: {nome}.'
        voltar = (caminho[-1][1], 'Voltar ao módulo', f'Módulo {n}: {nome}')
    elif caminho[-1][0] == 'Cidadania':
        cab, onde = 'Cidadania', 'Cidadania.'
        voltar = (caminho[-1][1], 'Voltar à Cidadania', 'Cidadania')
    else:
        raise ValueError(f'{f}: caminho por ler {caminho}')
    seguinte = None
    cfg = re.search(r'EPIJogo\.montar\(\{.*?\}\)', s, re.S)
    sg = re.search(r'[{,]seguinte:"([^"]*)"', cfg[0]) if cfg else None
    if sg:
        alvo = sg[1] if sg[1].startswith('http') else ABS + posixpath.normpath(posixpath.join(f.parent.relative_to(R).as_posix(), sg[1])) + '/'
        if alvo.rstrip('/') != voltar[0].rstrip('/'):
            t = titulo_de(alvo)
            if not t:
                raise ValueError(f'{f}: título do seguinte por ler ({alvo})')
            seguinte = (sg[1], 'Seguinte', t)
    return {'cab': cab, 'titulo': titulo, 'onde': onde, 'voltar': voltar, 'seguinte': seguinte, 'papel': papel,
            'projecao': True, 'caminho': caminho, 'fontes': None}, rel


def main(argv):
    if '--estaticas' not in argv:
        print(__doc__)
        return 2
    verificar = '--verificar' in argv
    novos, mudou = {}, 0
    for f in estaticas():
        s = f.read_text('utf-8')
        ctx, rel = ctx_estatica(f, s)
        t = trocar_menu(s, menu(ctx))
        t = com_controls(t)
        t = com_marca(t, ctx)
        t = re.sub(r'<style id="mg-css">.*?</style>', '', t, count=1, flags=re.S)
        t = com_semjs(t, ctx, 'sessão' if ctx['cab'] != 'Cidadania' else 'página')
        t = ativos(t, rel)
        novos[f] = t
        if t != s:
            mudou += 1
    if verificar:
        print(f'{mudou} página(s) por atualizar')
        return 1 if mudou else 0
    for f, t in novos.items():  # tudo lido e construído antes de escrever: nada fica meio feito
        if f.read_text('utf-8') != t:
            f.write_bytes(t.encode('utf-8'))
    print(f'{len(novos)} páginas estáticas da Cidadania; {mudou} mudaram.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
