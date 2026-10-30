"""Cidadania M2: dez sessões (Recupera, Vê, Decide, Faz, Leva) e o guia do docente.

28/10/2026. As peças são as do M1 (tools/cidadania_sessoes_molde.py) e a folha de estilos é a do M1
(assets/cidadania-m1-sessoes.css), com uma folha pequena só para o que o M2 acrescenta: o mapa do Contra-feed,
os materiais numerados do Vê, o vídeo opcional e as tabelas do guia (assets/cidadania-m2-sessoes.css).
O motor é assets/cidadania-sessoes-molde.js, que lê a chave na própria página (data-chave).
O conteúdo vive em tools/cidadania_m2_molde.py.
"""
from html import escape as e
from pathlib import Path
from urllib.parse import quote
import cidadania_sessoes_molde as molde
from cidadania_m2_molde import (PASSOS, LINHA, MARCA, CHAVE, TEMPOS, TEMPOS_MOSTRA, REVISAO_COMUM, CASAS, INSTRUMENTOS,
                                DECISOES, IMAGENS, LISBOA_1907, SESSOES, OBRAS, CASOS_RECICLADOS)

FOLHAS = ['cidadania-m1-sessoes.css?v=20261027-molde-2', 'cidadania-m2-sessoes.css?v=20261028-m2-2']
SCRIPTS = ['cidadania-sessoes-molde.js?v=20261028-m2-1']
R = Path(__file__).resolve().parents[1]
LICENCA = ('CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0')  # o endereço que o Lente já usa (cidade/)
# A imagem da abertura ocupa, no máximo, metade da largura no computador e a largura toda no telemóvel.
TAMANHOS = '(max-width: 900px) 92vw, 560px'
IDS = [f'{n:02}' for n in range(1, 11)]
ATRIBUTOS = ' data-chave="' + CHAVE + '" data-sessoes="' + ' '.join(IDS) + '"'
rel, liga, para, label = molde.rel, molde.ligacao, molde.para, molde.label


def tempos(n):
    return TEMPOS_MOSTRA if SESSOES[n - 1].get('mostra') else TEMPOS


def topo(path):
    marca = '<span class="c10-brand">' + liga(path, 'index.html', 'Lente') + ' / ' + liga(path, 'cidadania/', 'Cidadania') + '</span>'
    projecao = rel(path, 'projetar/') + '?pagina=' + quote('/lente/' + path.rsplit('/', 1)[0] + '/', safe='')
    return molde.topo(marca + liga(path, 'cidadania/m2/', 'Módulo 2') + liga(path, 'cidadania/contra-feed/', 'Contra-feed') + liga(path, 'cidadania/m2/glossario/', 'Palavras'), projecao)


def documento(path, titulo, corpo, num='', atributos=ATRIBUTOS):
    assets = rel(path, 'assets/')
    # 28/10/2026: a fonte do Google deixa de bloquear a página (se o pedido ficar pendurado, a página aparece na mesma).
    return molde.documento(assets, titulo, corpo, topo(path), FOLHAS, SCRIPTS, num, '', atributos, fonte_bloqueante=False)


def licenca(texto_html):
    """A licença CC BY-SA 3.0 leva a ligação ao texto da licença, como a licença pede."""
    t, u = LICENCA
    return texto_html.replace(t, '<a href="' + u + '" rel="license">' + t + '</a>', 1)


def credito(img):
    """O crédito completo de uma imagem: legenda, autoria e licença, e a ligação ao registo."""
    return e(img['legenda']) + ' ' + licenca(e(img['credito'])) + ', <a href="' + e(img['url'], quote=True) + '">Wikimedia Commons</a>.'


def variante(src):
    """A versão com cerca de 700 px de largura, se existir (img/x.webp -> img/x-700.webp)."""
    v = src[:-len('.webp')] + '-700.webp'
    return v if src.endswith('.webp') and (R / v).exists() else None


def figura(path, chave, cls='', capa=False):
    img = IMAGENS[chave]
    v = variante(img['src'])
    srcset = rel(path, v) + ' 700w, ' + rel(path, img['src']) + ' 1100w' if v else ''
    return molde.figura(rel(path, img['src']), img['alt'], credito(img), cls, srcset, TAMANHOS if v else '', capa)


def fonte(path, f):
    texto, alvo = f
    return '<p class="c10-credit">' + (liga(path, alvo, texto) if alvo else e(texto)) + '</p>'


def mapa(casa):
    """As dez casas do Contra-feed, com a casa desta sessão em destaque (figura e fundo).
    28/10/2026: o estado de cada casa também se diz por palavras (para o leitor de ecrã) e numa legenda."""
    out = '<ol class="c10-mapa" aria-label="Mapa do Contra-feed: dez casas, uma por sessão">'
    for i, (titulo, _) in enumerate(CASAS, 1):
        if i == casa:
            estado, sr = ' class="c10-mapa-atual" aria-current="step"', 'casa de hoje'
        elif i < casa:
            estado, sr = ' class="c10-mapa-feita"', 'casa anterior'
        else:
            estado, sr = '', 'casa seguinte'
        out += '<li' + estado + '><b>' + str(i) + '</b><span>' + e(titulo) + '</span><span class="c10-sr"> (' + sr + ')</span></li>'
    legenda = (['Contorno cheio: casas anteriores.'] if casa > 1 else []) + ['Preenchida: a casa de hoje.'] + (['Tracejado: casas seguintes.'] if casa < len(CASAS) else [])
    return out + '</ol>' + para('c10-small c10-mapa-legenda', ' '.join(legenda))


# Os cinco passos -----------------------------------------------------------------------------------------

def recupera(path, n, s):
    out = para('c10-instruction', s.get('entrada', ''))
    if s.get('recupera_de'):
        out += para('c10-small', s['recupera_de'])
    return out + molde.recall(s['recupera'])


def material(path, n, s, j, m, total):
    out = '<section class="c10-mat" aria-labelledby="mat-' + str(j) + '-t"><p class="c10-label c10-mat-n" id="mat-' + str(j) + '-t">Material ' + str(j) + ' de ' + str(total) + (': ' + e(m['titulo']) if m.get('titulo') else '') + '</p>'
    tipo = m['tipo']
    if tipo != 'video':
        out += para('c10-instruction', m['instrucao'])
    if tipo == 'imagem':
        # 28/10/2026: o material que se observa fica à vista, no próprio material (nunca atrás de uma ligação).
        out += figura(path, m.get('imagem', s['imagem']), 'c10-material')
        if m.get('citacao'):
            out += '<blockquote class="c10-document c10-quote"><p>«' + e(m['citacao']) + '»</p></blockquote>'
    elif tipo == 'par':
        # As duas fotografias de Lisboa, lado a lado (A e B). O crédito não diz qual foi alterada.
        out += '<figure class="c10-par"><div class="c10-par-imgs">' + ''.join(
            '<div class="c10-par-img"><p class="c10-par-r" aria-hidden="true">' + k.upper() + '</p><img src="' + rel(path, LISBOA_1907[k]['src']) + '" alt="' + e(LISBOA_1907[k]['alt'], quote=True) + '" loading="lazy" decoding="async"></div>'
            for k in ('a', 'b')) + '</div><figcaption>' + e(LISBOA_1907['credito']) + ', <a href="' + e(LISBOA_1907['url'], quote=True) + '">loc.gov</a>. Uma das versões foi alterada por nós.</figcaption></figure>'
    elif tipo == 'texto':
        out += '<div class="c10-document">' + e(m['texto']) + '</div>'
    elif tipo == 'citacao':
        out += '<blockquote class="c10-document c10-quote"><p>' + e(m['texto']) + '</p></blockquote>'
    elif tipo == 'lista':
        out += '<ol class="c10-document c10-frases">' + ''.join('<li>' + e(t) + '</li>' for t in m['itens']) + '</ol>'
    elif tipo == 'colunas':
        out += '<ol class="c10-evidence c10-colunas">' + ''.join('<li><b>' + e(a) + '</b><span>' + e(b) + '</span></li>' for a, b in m['colunas']) + '</ol>'
    elif tipo == 'fontes':
        out += '<div class="c10-document">' + e(m['texto']) + '</div>'
        out += ''.join('<details class="c10-fonte"><summary>Fonte ' + str(k) + ': ' + e(a) + '</summary><div><p>' + e(b) + '</p></div></details>' for k, (a, b) in enumerate(m['fontes'], 1))
    elif tipo == 'video':
        out += '<div class="c10-video"><p class="c10-mark">Opcional</p><p>' + e(m['sobre']) + '</p>'
        out += '<p class="c10-instruction"><b>Antes de ver.</b> ' + e(m['antes']) + '</p>'
        out += '<p class="c10-video-links"><a class="c10-action c10-action-line" href="' + e(m['url'], quote=True) + '">Abrir o excerto no YouTube</a>' + liga(path, m['licao'][1], m['licao'][0]) + '</p>'
        out += '<p class="c10-instruction"><b>Depois de ver.</b> ' + e(m['depois']) + '</p>'
        out += '<details class="c10-sem-video"><summary>Sem vídeo: os números da conta</summary><div><p>' + e(m['sem_video']) + '</p></div></details></div>'
    elif tipo == 'papel':
        out += '<div class="c10-document c10-papel">' + e(m['texto']) + '</div>'
    if m.get('revela'):
        out += para('c10-reading', m['revela'])
    if m.get('leitura'):
        out += para('c10-reading', m['leitura'])
    if m.get('aviso'):
        out += para('c10-small', m['aviso'])
    if m.get('fonte'):
        out += fonte(path, m['fonte'])
    return out + '</section>'


def caso_reciclado(n):
    """30/10/2026: reciclagem dos gigantes (decisão do docente).
    Escolhe no caderno antes de abrir as razões; controlos nativos, também sem JavaScript.
    """
    import json
    c = CASOS_RECICLADOS[n]
    out = '<section class="c10-mat" id="caso-reciclado"><h3>' + e(c['titulo']) + '</h3>'
    out += para('c10-instruction', 'Caso inventado. Lê e guarda uma decisão provisória antes de consultar o relato.')
    out += para('c10-document', c['caso'])
    out += '<details class="c10-more"><summary>Ler o relato em português</summary><div class="c10-reading">' + c['relato'] + '</div></details>'
    out += '<p class="c10-small">' + e(c['fonte']) + ' <a href="' + e(c['url'], quote=True) + '">Consultar o original</a>.</p>'
    for q in c['perguntas']:
        out += '<section class="c10-mat"><h4>' + e(q['p']) + '</h4><p>Escolhe e justifica no caderno. Depois, abre a opção para comparar razões.</p>'
        out += '<script type="application/json" data-opcoes-reciclagem>' + json.dumps(q, ensure_ascii=False).replace('</', '<\\/') + '</script>'
        for i, opcao in enumerate(q['o']):
            certo = i == q['c']
            out += '<details class="c10-feedback"><summary>' + e(opcao) + '</summary><div><p><b>' + ('Correto. ' if certo else 'Revê. ') + '</b>' + e(q['f'] if certo else q['fe'][i]) + '</p></div></details>'
        out += '</section>'
    return out + '<h4>Outra leitura</h4>' + para('c10-reading', c['outra']) + '<h4>Para o Contra-feed</h4>' + para('c10-reading', c['transferencia']) + '</section>'


def ve(path, n, s):
    out = ''.join(material(path, n, s, j, m, len(s['ve'])) for j, m in enumerate(s['ve'], 1))
    out += para('c10-reading', s.get('leitura', ''))
    if n in CASOS_RECICLADOS:
        out += caso_reciclado(n)
    elif n in OBRAS:
        out += molde.obra(OBRAS[n], lambda u, t: liga(path, u, t))
    lista = [('Etapa ' + f'{n:02}' + ': ' + s['etapa'], f'cidadania/m2/aulas/{n:02}/')]
    vistos = {lista[0][1]}
    for m in s['ve']:
        f = m.get('fonte') or m.get('licao')
        if f and f[1] and not f[1].startswith('http') and f[1] not in vistos:
            vistos.add(f[1]); lista.append(f)
    return out + '<details class="c10-more"><summary>Obras e materiais</summary><div><ul>' + ''.join('<li>' + liga(path, a, t) + '</li>' for t, a in lista) + '</ul></div></details>'


def decide(path, n, s):
    d = s['decide']
    out = '<div class="c10-decide"><div class="c10-solo">' + label('Primeiro, em silêncio') + '<p class="c10-prompt">' + e(d['silencio']) + '</p>'
    if d.get('silencio_lista'):  # frases para classificar: uma por linha, com letra, para se poderem referir
        out += '<ol class="c10-document c10-frases" type="A">' + ''.join('<li>' + e(t) + '</li>' for t in d['silencio_lista']) + '</ol>'
    # 28/10/2026: «a tua resposta» serve todas as tarefas (um número, uma regra, uma classificação), não só escolhas.
    out += para('c10-small', d.get('protocolo', 'Três minutos. Escreve a tua resposta e uma razão no cartão de decisão. Depois, uma volta: cada pessoa lê o seu cartão, sem comentários.'))
    out += para('c10-small', d.get('silencio_mais', '')) + '</div>'
    out += '<div class="c10-group">' + label(d.get('grupo_rotulo', 'Depois, em grupo')) + '<ol class="c10-tasks">' + ''.join('<li>' + e(t) + '</li>' for t in d['grupo']) + '</ol>'
    out += '<p class="c10-small">No fim, registem a decisão e uma razão que ficou vencida.</p></div></div>'
    return out + '<details data-feedback><summary>Comparar razões</summary><div><p>' + e(d['comparar']) + '</p></div></details>'


def faz(path, n, s):
    f = s['faz']
    out = para('c10-instruction', f.get('intro', ''))
    out += '<ol class="c10-tasks c10-faz">' + ''.join('<li>' + e(t) + '</li>' for t in f['tarefas']) + '</ol>'
    if f.get('apoio'):
        out += '<ul class="c10-apoio">' + ''.join('<li>' + liga(path, a, t) + '</li>' for t, a in f['apoio']) + '</ul>'
    out += para('c10-small', f.get('nota', ''))
    out += '<div class="c10-review">' + label('Rever com outra pessoa') + '<p>' + e(f['revisao']) + '</p>' + (para('c10-small', REVISAO_COMUM) if f.get('comum', True) else '') + '</div>'
    titulo, conteudo = CASAS[n - 1]
    out += '<div class="c10-casa"><p class="c10-output"><b>Guardar</b><span>Casa ' + str(n) + ' do mapa do Contra-feed: ' + e(titulo) + '</span></p>'
    return out + para('c10-casa-c', conteudo) + mapa(n) + '</div>'


def leva(path, n, s):
    lv = s['leva']
    out = '<div class="c10-exit">' + label('Em papel, antes de sair') + '<p class="c10-exit-q">' + e(lv['pergunta']) + '</p></div>'
    if s.get('vsf'):
        out += '<div class="c10-vsf">' + label('As três perguntas do Contra-feed') + '<p class="c10-small">Responde a cada uma com «sim», «em parte» ou «ainda não», e uma linha a dizer porquê.</p><dl>' + ''.join('<dt>' + e(a) + '</dt><dd>' + e(b) + '</dd>' for a, b in s['vsf']) + '</dl></div>'
    out += label('Confirma') + '<ul class="c10-checks">' + ''.join('<li>' + e(t) + '</li>' for t in lv['confirma']) + '</ul>'
    if s.get('depois'):
        out += '<div class="c10-depois">' + label('Depois, no telemóvel') + '<p class="c10-small">Dois ou três dias depois da sessão.</p><ul>' + ''.join('<li>' + liga(path, a, t) + '</li>' for t, a in s['depois']) + '</ul></div>'
    return out + molde.registo()


PASSO = [recupera, ve, decide, faz, leva]


def sessao(n, s):
    ident = f'{n:02}'
    path = f'cidadania/m2/sessoes/{ident}/index.html'
    body = molde.abertura(ident, s['tema'], s['titulo'], s['pergunta'], ('' if n in CASOS_RECICLADOS else figura(path, s['imagem'], 'c10-cover-img', capa=True)), separador=' / ')
    body += molde.barra_passos(ident, PASSOS)
    for i, lab in enumerate(PASSOS):
        body += molde.cabecalho_passo(i, lab, s.get('linhas', {}).get(lab, LINHA[lab]), s.get('marcas', {}).get(lab, MARCA.get(lab)))
        body += PASSO[i](path, n, s) + molde.FECHO_PASSO
    seguinte = f'cidadania/m2/sessoes/{n + 1:02}/' if n < 10 else 'cidadania/m2/'
    body += molde.controlos(rel(path, seguinte), 'Sessão seguinte' if n < 10 else 'Voltar ao módulo')
    body += molde.SEM_JS + '<footer class="c10-support">' + liga(path, 'cidadania/m2/#dez-sessoes', 'Todas as sessões') + liga(path, f'cidadania/m2/aulas/{ident}/', 'Etapa ' + ident) + liga(path, 'cidadania/m2/imagens/', 'Imagens e créditos') + liga(path, f'cidadania/m2/sessoes/#sessao-{ident}', 'Guia do docente') + '</footer>'
    return path, documento(path, s['titulo'] + ' / Sessão ' + ident + ' / Cidadania M2', body, ident)


# O guia do docente ---------------------------------------------------------------------------------------

def tabela(cabecalho, linhas, legenda):
    out = '<table class="c10-tabela"><caption>' + e(legenda) + '</caption><thead><tr>' + ''.join('<th scope="col">' + e(c) + '</th>' for c in cabecalho) + '</tr></thead><tbody>'
    for linha in linhas:
        out += '<tr><th scope="row">' + e(linha[0]) + '</th>' + ''.join('<td data-rotulo="' + e(r, quote=True) + '">' + e(c) + '</td>' for r, c in zip(cabecalho[1:], linha[1:])) + '</tr>'
    return out + '</tbody></table>'


def guia():
    path = 'cidadania/m2/sessoes/index.html'
    body = '<header class="c10-hero"><div><p class="c10-eyebrow">Para o docente</p><h1>Dez sessões</h1><p class="c10-deck">Tempos, materiais e condução do Módulo 2.</p></div>' + figura(path, 'turco') + '</header>'
    body += '<section class="c10-reference" id="como"><h2>Como se usa</h2>'
    body += '<p>Cada sessão tem três horas e o mesmo molde do Módulo 1: Recupera, Vê, Decide, Faz e Leva. Cada sessão corresponde à etapa com o mesmo número, em ' + liga(path, 'cidadania/m2/aulas/', 'As dez etapas') + '; as etapas continuam publicadas, cada uma com uma linha para a sua sessão.</p>'
    body += '<p>Os passos 00 a 08 e os cinco casos não mudam: ficam no fim de cada sessão, em «Depois, no telemóvel», para dois ou três dias depois. O registo dos passos e o contador das 11 atividades mantêm-se. O registo das sessões é separado, fica só no aparelho de cada aluno e não é gravado em projeção.</p>'
    body += '<p>As páginas das sessões são para a turma; este guia é para conduzir. Na sessão seguinte, abrir o Recupera com uma resposta do Leva, lida em voz alta e sem nome.</p></section>'
    body += '<section class="c10-reference" id="decisoes"><h2>Decisões provisórias</h2><p>As cinco perguntas do plano ficaram com uma decisão provisória, a confirmar pelo docente.</p><ol class="c10-decisoes">'
    body += ''.join('<li><p class="c10-label">Decisão provisória ' + str(i) + ': ' + e(t) + '</p><p>' + e(txt) + '</p></li>' for i, (t, txt) in enumerate(DECISOES, 1)) + '</ol></section>'
    body += '<section class="c10-reference" id="mapa"><h2>O mapa do Contra-feed</h2><p>Cada grupo tem um mapa com dez casas, num A3 ou numa página do ficheiro do grupo. O Faz de cada sessão preenche uma casa. O mapa só organiza o que o Contra-feed já pede: não cria entregas nem pesos.</p>'
    body += tabela(['Casa', 'Sessão', 'Conteúdo'], [(str(i) + '. ' + t, f'{i:02}', c) for i, (t, c) in enumerate(CASAS, 1)], 'As dez casas, uma por sessão')
    body += '<p><b>Recuperação espaçada.</b> O Recupera traz a sessão anterior. O Decide volta a casas antigas: a casa 1 regressa na sessão 07; a casa 4, na 07, na 08 e na 10; a casa 5, na 07. Na 10, o Vê usa as notas de autoria da casa 5. Os passos ficam para dois ou três dias depois.</p></section>'
    body += '<section class="c10-reference" id="avaliacao"><h2>Onde nasce cada evidência</h2><p>Os pesos são os do Contra-feed; nenhum é novo.</p>'
    body += tabela(['Instrumento', 'Peso', 'Sessões', 'Evidência'], INSTRUMENTOS, 'Os quatro instrumentos de avaliação')
    body += '<p>Os cartões do Leva e as respostas Vi, Situei e Fiz são evidência formativa, sem peso. Nenhuma posição moral é pontuada. O limite de faltas do módulo continua a ser de 6 horas.</p>' + liga(path, 'cidadania/contra-feed/', 'Projeto, requisitos e avaliação do Contra-feed') + '</section>'
    body += '<section class="c10-reference" id="tempos"><h2>Tempos</h2>'
    body += tabela(['Sessões'] + PASSOS, [('01 a 09',) + tuple(str(t) for t in TEMPOS), ('10',) + tuple(str(t) for t in TEMPOS_MOSTRA)], 'Minutos por passo')
    body += '<p>O Faz inclui a pausa de 10 minutos e cerca de 20 minutos de revisão. Na sessão 10, 125 minutos dão para sete grupos com cerca de 8 minutos de mostra, 7 de defesa e 2 de transição.</p></section>'
    body += '<section class="c10-reference" id="regras"><h2>Regras comuns</h2><ul class="c10-regras">'
    body += '<li><b>Recupera.</b> Duas perguntas conceptuais sobre a sessão anterior, com resposta em «Confirmar», e uma pergunta pessoal sobre o próprio trabalho, sem resposta.</li>'
    body += '<li><b>Vê.</b> Um material de cada vez, com a instrução junto dele. Primeiro observa, depois lê.</li>'
    body += '<li><b>Decide.</b> Sem ecrã para a turma e sem pontuar posições. Três minutos em silêncio, com um cartão de decisão; uma volta, sem comentários; as três tarefas em grupo; o grupo regista a decisão e uma razão vencida. No fim, o docente projeta «Comparar razões».</li>'
    body += '<li><b>Faz.</b> Em papel ou no ficheiro do grupo. Fecha com revisão por outra pessoa, que marca uma coisa que se percebe e uma que falta, e faz uma pergunta. A versão revista guarda-se na casa da sessão.</li>'
    body += '<li><b>Leva.</b> Uma pergunta de saída, em papel, com três critérios em «Confirma».</li>'
    body += '<li><b>Vídeos.</b> Pergunta antes, pergunta depois e alternativa escrita. Nenhum é obrigatório. Os vídeos «em revisão» de Ver para fazer não entram.</li></ul></section>'
    for n, s in enumerate(SESSOES, 1):
        ident = f'{n:02}'
        body += '<section class="c10-stage c10-guia-sessao" id="sessao-' + ident + '"><p class="c10-eyebrow">Sessão ' + ident + ' / ' + e(s['tema']) + '</p><h2>' + e(s['titulo']) + '</h2><p class="c10-guia-q">' + e(s['pergunta']) + '</p>'
        body += '<ol class="c10-guia-tempos">' + ''.join('<li><b>' + e(l) + '</b><span>' + str(t) + ' min</span></li>' for l, t in zip(PASSOS, tempos(n))) + '</ol>'
        body += '<p><b>Casa ' + str(n) + ':</b> ' + e(CASAS[n - 1][1]) + '</p>'
        if n in OBRAS:
            obra = OBRAS[n]['autor'] + ', ' + OBRAS[n]['titulo']
            obra += '' if obra[-1] in '?!.' else '.'  # sem pontuação dupla («Bat?.»)
        body += ('<p><b>Caso em português:</b> ' + e(CASOS_RECICLADOS[n]['titulo']) + '</p>' if n in CASOS_RECICLADOS else '<p><b>Cartão de obra:</b> ' + (e(obra) if n in OBRAS else 'nenhum, como na sessão 10 do Módulo 1.') + '</p>')
        body += '<p>' + e(s['docente']) + '</p>'
        body += '<p><b>Inclusão.</b> ' + e(' '.join(s['inclusao'])) + '</p>'
        if s.get('depois'):
            body += '<p><b>Depois, no telemóvel.</b></p><ul>' + ''.join('<li>' + liga(path, a, t) + '</li>' for t, a in s['depois']) + '</ul>'
        body += '<p class="c10-guia-links">' + liga(path, f'cidadania/m2/sessoes/{ident}/', 'Abrir a sessão ' + ident) + liga(path, f'cidadania/m2/aulas/{ident}/', 'Etapa ' + ident + ': ' + s['etapa']) + '</p></section>'
    body += '<section class="c10-reference" id="riscos"><h2>Riscos de calendário</h2><ul class="c10-regras">'
    body += '<li><b>O diário.</b> Se a sessão 02 acontecer menos de sete dias depois da 01, a análise do diário fica a meio na 02 e acaba nos primeiros minutos da 03, antes da entrega.</li>'
    body += '<li><b>Sessões densas.</b> A 01 (feed de papel, duas versões e início do diário) e a 06 (escolha do caso e análise). Se faltar tempo, a análise da 06 fica a meio e acaba nos primeiros minutos da 07, antes da entrega.</li></ul></section>'
    body += '<footer class="c10-support">' + liga(path, 'cidadania/m2/#dez-sessoes', 'Sessões do Módulo 2') + liga(path, 'cidadania/contra-feed/', 'Contra-feed') + liga(path, 'cidadania/m2/aulas/', 'As dez etapas') + liga(path, 'cidadania/m2/imagens/', 'Imagens e créditos') + '</footer>'
    return path, documento(path, 'Guia das dez sessões / Cidadania M2', body)


# O bloco das sessões no índice do módulo ----------------------------------------------------------------

def bloco_indice():
    """A lista das dez sessões dentro de cidadania/m2/ (o índice mantém os passos, os casos e o contador)."""
    path = 'cidadania/m2/index.html'
    out = '<section class="c10 c10-indice" id="dez-sessoes" data-c10' + ATRIBUTOS + ' aria-labelledby="dez-sessoes-t">'
    # 28/10/2026: o título usa o h2 das outras secções da página (class="secao"), para a página ter um só sistema.
    out += '<h2 class="secao" id="dez-sessoes-t">Dez sessões</h2><p class="c10-small" data-count></p>'
    out += '<p><a class="c10-action" href="sessoes/01/" data-continue data-continue-base="sessoes/" data-fim-href="../contra-feed/" data-fim-texto="Rever o Contra-feed">Começar na sessão 01</a></p>'
    out += '<ol class="c10-session-list">' + ''.join(molde.cartao_sessao(f'{n:02}', f'sessoes/{n:02}/', s['tema'], s['titulo'], s['pergunta']) for n, s in enumerate(SESSOES, 1)) + '</ol>'
    out += '<p class="c10-indice-mais"><a href="https://pedrohfernandes-klk.github.io/lente/cidadania/m2/aulas/">As dez etapas, em texto</a>' + liga(path, 'cidadania/m2/sessoes/', 'Guia do docente') + '</p></section>'
    return out


def build(write):
    for n, s in enumerate(SESSOES, 1):
        write(*sessao(n, s))
    write(*guia())
