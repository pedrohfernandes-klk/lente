"""Vídeos escolhidos pelo docente (28/10/2026): cartões «Para ver» nos baralhos do Lente.

Lê tools/videos-escolhidos.json e, em cada página, insere um cartão de leitura (t: "ler") com a marca
"pv" junto do cartão indicado. Não reescreve os outros cartões: só acrescenta texto à lista. Os cartões
de leitura não contam para a pontuação, e o motor só guarda tentativas e melhores resultados, por isso
o progresso já guardado nos aparelhos não muda. Idempotente: os cartões com a marca saem antes de entrar.

Uso: python3 tools/videos_escolhidos.py [--verificar]
"""
import html
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / 'tools' / 'videos-escolhidos.json'
ID = re.compile(r'^[A-Za-z0-9_-]{11}$')
PROIBIDAS = ('professor', 'jogar', 'ficha', 'folha', '—')


def lista(s):
    """Posição [início, fim) da lista itens:[...] passada a EPIJogo.montar."""
    i = s.find('EPIJogo.montar(')
    j = s.find('itens:[', i)
    if i < 0 or j < 0:
        raise ValueError('sem EPIJogo.montar(...itens:[')
    k = j + len('itens:')
    fundo, texto, escape = 0, False, False
    for p in range(k, len(s)):
        c = s[p]
        if texto:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == '"':
                texto = False
        elif c == '"':
            texto = True
        elif c == '[':
            fundo += 1
        elif c == ']':
            fundo -= 1
            if fundo == 0:
                return k, p + 1
    raise ValueError('lista de cartões por fechar')


def cartoes(bruto):
    """Cada cartão da lista, com o seu troço de texto (para inserir sem reescrever os outros)."""
    dec = json.JSONDecoder()
    out, p = [], 1
    while True:
        while bruto[p] in ' \n\r\t,':
            p += 1
        if bruto[p] == ']':
            return out
        obj, fim = dec.raw_decode(bruto, p)
        out.append((obj, p, fim))
        p = fim


def esc(t):
    return html.escape(t, quote=True)


def video_html(v, titulo):
    t = v.get('rotulo') or v['original']
    meta = (v.get('serie') or v['canal']) + '. Em inglês.'
    rotulo = titulo + ': ' + v['original'] + ' (' + v['canal'] + ', YouTube)'
    attrs = {'data-yt': v['yt'], 'data-dur': v['dur'], 'data-t': t, 'data-m': meta, 'data-titulo': rotulo}
    if v.get('ini'):
        attrs['data-ini'] = str(v['ini'])
    if v.get('fim'):
        attrs['data-fim'] = str(v['fim'])
    a = ''.join(' %s="%s"' % (k, esc(x)) for k, x in attrs.items())
    return ('<div class="pv-video"%s><p class="pv-t" lang="en">%s</p><p class="pv-m">%s</p>'
            '<button type="button">Ver o vídeo <span>(%s)</span></button></div>') % (a, esc(t), esc(meta), esc(v['dur']))


def cartao(c):
    vs = c['videos']
    primeiro = vs[0]
    antes = c.get('antes') or primeiro['antes']
    depois = c.get('depois') or primeiro['depois']
    h = ['<div class="pv" data-pv="%s">' % esc(c['id'])]
    h.append('<p class="pv-ctx">%s</p>' % c['contexto'])
    h.append('<p class="pv-antes"><b>Antes de ver</b><span>%s</span></p>' % esc(antes))
    if len(vs) > 1:
        h.append('<ul class="pv-opcoes" aria-label="Escolhe o vídeo">')
        for n, v in enumerate(vs):
            d = {'data-yt': v['yt'], 'data-dur': v['dur'], 'data-t': v.get('rotulo') or v['original'], 'data-m': (v.get('serie') or v['canal']) + '. Em inglês.',
                 'data-titulo': v['opcao'] + ': ' + v['original'] + ' (' + v['canal'] + ', YouTube)',
                 'data-antes': v['antes'], 'data-depois': v['depois']}
            a = ''.join(' %s="%s"' % (k, esc(x)) for k, x in d.items())
            h.append('<li><button type="button" aria-pressed="%s"%s>%s<small>%s</small></button></li>'
                     % ('true' if n == 0 else 'false', a, esc(v['opcao']), esc(v['dur'])))
        h.append('</ul>')
    h.append(video_html(primeiro, c['titulo']))
    h.append('<p class="pv-yt"><a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">Ver no YouTube</a></p>' % primeiro['yt'])
    h.append('<p class="pv-depois"><b>Depois de ver</b><span>%s</span></p>' % esc(depois))
    if c.get('nota'):
        h.append('<p class="pv-nota">%s</p>' % esc(c['nota']))
    h.append('</div>')
    return {'t': 'ler', 'rot': 'Para ver', 'titulo': c['titulo'], 'html': ''.join(h), 'pv': c['id']}


def serial(obj):
    return json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


def ancora(c, objs):
    alvo = c.get('antes_de') or c.get('depois_de')
    (campo, valor), = alvo.items()
    hits = [n for n, o in enumerate(objs) if (o.get(campo) or '').strip() == valor]
    if len(hits) != 1:
        raise ValueError('%s: âncora %s=%r encontrada %d vezes' % (c['id'], campo, valor, len(hits)))
    return hits[0] if 'antes_de' in c else hits[0] + 1


def recursos(s, profundidade, versao):
    pre = '../' * profundidade
    css = '<link rel="stylesheet" href="%sassets/para-ver.css?v=%s">' % (pre, versao)
    js = '<script defer src="%sassets/para-ver.js?v=%s"></script>' % (pre, versao)
    s = re.sub(r'<link rel="stylesheet" href="[./]*assets/para-ver\.css\?v=[^"]*">', '', s)
    s = re.sub(r'<script defer src="[./]*assets/para-ver\.js\?v=[^"]*"></script>', '', s)
    s = s.replace('</head>', css + '</head>', 1)
    i = s.rfind('</body>')
    return s[:i] + js + s[i:]


def aplicar(p, versao):
    caminho = RAIZ / p['pagina']
    s = caminho.read_text('utf-8')
    a, b = lista(s)
    bruto = s[a:b]
    itens = [x for x in cartoes(bruto) if 'pv' not in x[0]]
    novos = {}
    objs = [x[0] for x in itens]
    for c in p['cartoes']:
        novos.setdefault(ancora(c, objs), []).append(cartao(c))
    partes = []
    for n, (obj, i, f) in enumerate(itens):
        partes.extend(serial(x) for x in novos.get(n, []))
        partes.append(bruto[i:f])
    partes.extend(serial(x) for x in novos.get(len(itens), []))
    s = s[:a] + '[' + ', '.join(partes) + ']' + s[b:]
    s = recursos(s, len(Path(p['pagina']).parts) - 1, versao)
    a, b = lista(s)
    json.loads(s[a:b])
    return caminho, s


def verificar(dados):
    erros = []
    for p in dados['paginas']:
        for c in p['cartoes']:
            for v in c['videos']:
                if not ID.match(v['yt']):
                    erros.append('%s: id inválido %s' % (c['id'], v['yt']))
            texto = ' '.join([c['titulo'], c['contexto'], c.get('antes', ''), c.get('depois', ''), c.get('nota', '')] +
                             [v.get(k, '') for v in c['videos'] for k in ('opcao', 'antes', 'depois')]).lower()
            for w in PROIBIDAS:
                if re.search(r'\b' + re.escape(w), texto) if w.isalpha() else w in texto:
                    erros.append('%s: «%s» no texto' % (c['id'], w))
            if '·' in texto:
                erros.append('%s: «·» no texto' % c['id'])
    return erros


def main():
    dados = json.loads(DADOS.read_text('utf-8'))
    erros = verificar(dados)
    if erros:
        print('\n'.join(erros))
        sys.exit(1)
    mudou = []
    for p in dados['paginas']:
        caminho, s = aplicar(p, dados['versao'])
        if caminho.read_text('utf-8') != s:
            mudou.append(p['pagina'])
            if '--verificar' not in sys.argv:
                caminho.write_text(s, 'utf-8')
    if '--verificar' in sys.argv and mudou:
        print('Por aplicar: ' + ', '.join(mudou))
        sys.exit(1)
    n = sum(len(c['videos']) for p in dados['paginas'] for c in p['cartoes'])
    print('%d cartões «Para ver», %d vídeos, %d páginas%s' % (sum(len(p['cartoes']) for p in dados['paginas']), n,
                                                           len(dados['paginas']), (': ' + ', '.join(mudou)) if mudou else ' (sem mudanças)'))


if __name__ == '__main__':
    main()
