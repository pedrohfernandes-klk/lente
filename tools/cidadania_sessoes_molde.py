"""Peças comuns das sessões de Cidadania: topo, abertura, cinco passos (Recupera, Vê, Decide, Faz, Leva),
controlos, registo, cartão de obra e cartão de sessão.

28/10/2026: generalizado a partir de tools/cidadania_m1_layout.py, que passa a usar estas peças sem mudar
um byte do HTML do M1 (tests/test_cidadania_m1_fichas.py volta a gerar o M1 e compara). O M2
(tools/cidadania_m2_sessoes.py) usa as mesmas peças; o que muda de módulo para módulo entra por parâmetro.
Os valores por omissão reproduzem o M1.
"""
from html import escape as e


def para(cls, text):
    return '<p class="' + cls + '">' + e(text) + '</p>' if text else ''


def label(text):
    return '<p class="c10-label">' + e(text) + '</p>'


def recall(items):
    """Recupera: perguntas numeradas; a resposta conceptual abre-se em «Confirmar»."""
    out = '<ol class="c10-recall">'
    for q, a in items:
        out += '<li><p>' + e(q) + '</p>' + ('<details class="c10-check"><summary>Confirmar</summary><div><p>' + e(a) + '</p></div></details>' if a else '') + '</li>'
    return out + '</ol>'


def obra(o, ligar):
    """Cartão da obra: acesso, razão, contexto, pergunta aberta, duas ligações e outra leitura.
    «ligar(caminho, texto)» devolve a ligação relativa à página."""
    out = '<aside class="c10-obra" aria-label="Cartão da obra"><p class="c10-label">Cartão da obra</p><h3>' + e(o['titulo']) + '</h3><p class="c10-obra-meta">' + e(o['autor']) + ', ' + e(o['data']) + '</p>'
    if o.get('citacao'):
        out += '<blockquote><p>«' + e(o['citacao']) + '»</p><footer>' + e(o['citacao_nota']) + '</footer></blockquote>'
    out += '<p class="c10-obra-razao">' + e(o['razao']) + '</p><p class="c10-obra-pergunta">' + e(o['pergunta']) + '</p>'
    out += '<details><summary>Contexto, acesso e outra leitura</summary><div><p>' + e(o['contexto']) + '</p>'
    out += '<h4>Onde encontrar</h4><ul>' + ''.join('<li>' + ('<a href="' + e(u, quote=True) + '">' + e(t) + '</a>' if u else e(t)) + '</li>' for t, u in o['acesso']) + '</ul>'
    if o.get('protegida'):
        out += '<p class="c10-small">Obra protegida: aqui fica descrita, com indicação de onde a encontrar.</p>'
    out += '<h4>Ligações</h4><ul>' + ''.join('<li>' + ligar(u, t) + '</li>' for t, u in o['ligacoes']) + '</ul>'
    out += '<h4>Outra leitura</h4><p>' + e(o['discordante']) + '</p></div></details></aside>'
    return out


def figura(src, alt, legenda_html, cls=''):
    """Uma imagem inteira, com a legenda e o crédito por baixo."""
    return '<figure' + (' class="' + cls + '"' if cls else '') + '><img src="' + src + '" alt="' + e(alt, quote=True) + '" loading="lazy" decoding="async"><figcaption>' + legenda_html + '</figcaption></figure>'


def topo(itens_html, projecao_href):
    """Barra do topo: marca e ligações do módulo, «Imprimir» (aparece com JavaScript) e «Projetar»."""
    return '<nav class="c10-top" aria-label="Navegação do módulo">' + itens_html + '<button type="button" data-print hidden>Imprimir</button><a class="epi-projection-menu-link" href="' + projecao_href + '">Projetar</a></nav>'


def abertura(ident, tema, titulo, pergunta, figura_html, separador=' · '):
    """Abertura: imagem, pergunta curta e «Começar»."""
    return '<header class="c10-hero c10-cover" id="abertura" data-session-intro><div class="c10-cover-text"><p class="c10-eyebrow">Sessão ' + ident + separador + e(tema) + '</p><h1>' + e(titulo) + '</h1><p class="c10-deck">' + e(pergunta) + '</p><a class="c10-action" href="#momento-1" data-start>Começar</a></div>' + figura_html + '</header>'


def barra_passos(ident, labels):
    """Abre o fluxo da sessão e a barra dos cinco passos, sempre à vista."""
    return '<div class="c10-flow" data-session-flow><nav class="c10-stagebar" aria-label="Cinco passos da sessão"><a class="c10-stage-home" href="#abertura" data-cover-link>Sessão ' + ident + '</a>' + ''.join('<a href="#momento-' + str(i + 1) + '" data-stage-link><b>' + f'{i + 1:02}' + '</b><span>' + e(lab) + '</span></a>' for i, lab in enumerate(labels)) + '</nav>'


def cabecalho_passo(i, lab, linha, marca):
    """Abre um passo: número, nome, a linha do que se faz e a marca («Sem ecrã», «Em papel»)."""
    n = str(i + 1)
    return '<section class="c10-stage" id="momento-' + n + '" data-stage data-label="' + e(lab, quote=True) + '" tabindex="-1" aria-labelledby="momento-' + n + '-t"><header class="c10-step-head"><span class="c10-step-n" aria-hidden="true">' + f'{i + 1:02}' + '</span><h2 id="momento-' + n + '-t">' + e(lab) + '</h2><p class="c10-step-line">' + e(linha) + '</p>' + ('<p class="c10-mark" data-mark="' + e(marca, quote=True) + '">' + e(marca) + '</p>' if marca else '') + '</header><div class="c10-step-body">'


FECHO_PASSO = '</div></section>'


def registo():
    """O registo do trabalho revisto: só no último passo, nunca em projeção."""
    return '<section class="c10-completion" data-completion hidden aria-label="Registo"><label><input type="checkbox" data-session-done>Registar o trabalho revisto</label><p data-live class="c10-small" role="status" aria-live="polite">O registo fica neste aparelho.</p></section>'


def controlos(href_seguinte, texto_seguinte):
    """Anterior e Seguinte; no fim, a sessão seguinte. Fecha o fluxo aberto por barra_passos."""
    return '<nav class="c10-control" data-step-controls aria-label="Avançar na sessão"><button type="button" data-prev hidden>← Anterior</button><span data-position role="status" aria-live="polite"></span><button type="button" data-next hidden>Seguinte →</button><a class="c10-action" href="' + href_seguinte + '" data-next-session hidden>' + texto_seguinte + '</a></nav></div>'


SEM_JS = '<noscript><p class="c10-small">Os cinco passos estão todos nesta página, uns a seguir aos outros.</p></noscript>'


def cartao_sessao(ident, href, tema, titulo, pergunta):
    """Uma sessão na lista do módulo: número, tema, título, pergunta e o estado (preenchido pelo JavaScript)."""
    return '<li class="c10-card" data-session-card="' + ident + '"><a href="' + href + '"><span class="c10-number">' + ident + '</span><span class="c10-card-text"><span class="c10-topic">' + e(tema) + '</span><h3>' + e(titulo) + '</h3><span class="c10-card-q">' + e(pergunta) + '</span><small data-status></small></span></a></li>'


def documento(assets, titulo, corpo, topo_html, folhas, scripts, num='', cabeca_extra='', atributos=''):
    """A página inteira. «assets» é o caminho relativo da pasta assets/, já com a barra final;
    «folhas» e «scripts» são nomes de ficheiro (com versão) dentro dessa pasta."""
    head = '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + e(titulo) + '</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet"><link rel="stylesheet" href="' + assets + 'appearance.css"><script src="' + assets + 'appearance.js"></script>'
    head += ''.join('<link rel="stylesheet" href="' + assets + f + '">' for f in folhas) + ''.join('<script defer src="' + assets + s + '"></script>' for s in scripts) + cabeca_extra
    return '<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head>' + head + '</head><body class="c10-body"><main class="c10" data-c10' + (' data-session="' + num + '"' if num else '') + atributos + '>' + topo_html + corpo + '</main><script defer src="' + assets + 'projection-launcher.js" data-site="lente"></script></body></html>\n'


def rel(path, target):
    """Caminho relativo de «path» (um ficheiro) até «target» (um caminho da raiz, com «/» final para pastas
    e, se for o caso, «#âncora»). Endereços completos ficam como estão."""
    import posixpath
    if target.startswith(('http://', 'https://')):
        return target
    alvo, _, frag = target.partition('#')
    value = posixpath.relpath(alvo or posixpath.dirname(path) + '/', posixpath.dirname(path))
    if alvo.endswith('/') and not value.endswith('/'):
        value += '/'
    return value + ('#' + frag if frag else '')


def ligacao(path, target, texto, cls=''):
    """Uma ligação relativa à página (ou completa, se o alvo for um endereço)."""
    return '<a' + (' class="' + cls + '"' if cls else '') + ' href="' + e(rel(path, target), quote=True) + '">' + e(texto) + '</a>'
