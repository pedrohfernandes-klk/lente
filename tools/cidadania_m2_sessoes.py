"""Cidadania M2: dez sessões (Recupera, Vê, Decide, Faz, Leva) e o guia do docente.

28/10/2026. As peças são as do M1 (tools/cidadania_sessoes_molde.py) e a folha de estilos é a do M1
(assets/cidadania-m1-sessoes.css), com uma folha pequena só para o que o M2 acrescenta: o mapa do Contra-feed,
os materiais numerados do Vê, o vídeo opcional e as tabelas do guia (assets/cidadania-m2-sessoes.css).
O motor é assets/cidadania-sessoes-molde.js, que lê a chave na própria página (data-chave).
O conteúdo vive em tools/cidadania_m2_molde.py.
"""
from html import escape as e
from urllib.parse import quote
import cidadania_sessoes_molde as molde
from cidadania_m2_molde import (PASSOS, LINHA, MARCA, CHAVE, TEMPOS, TEMPOS_MOSTRA, REVISAO_COMUM, CASAS, INSTRUMENTOS,
                                DECISOES, IMAGENS, LISBOA_1907, SESSOES, OBRAS)

FOLHAS = ['cidadania-m1-sessoes.css?v=20261027-molde-2', 'cidadania-m2-sessoes.css?v=20261028-m2-1']
SCRIPTS = ['cidadania-sessoes-molde.js?v=20261028-m2-1']
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
    return molde.documento(assets, titulo, corpo, topo(path), FOLHAS, SCRIPTS, num, '', atributos)


def credito(img):
    """O crédito completo de uma imagem: legenda, autoria e licença, e a ligação ao registo."""
    return e(img['legenda']) + ' ' + e(img['credito']) + ', <a href="' + e(img['url'], quote=True) + '">Wikimedia Commons</a>.'


def figura(path, chave, cls=''):
    img = IMAGENS[chave]
    return molde.figura(rel(path, img['src']), img['alt'], credito(img), cls)


def fonte(path, f):
    texto, alvo = f
    return '<p class="c10-credit">' + (liga(path, alvo, texto) if alvo else e(texto)) + '</p>'


def mapa(casa):
    """As dez casas do Contra-feed, com a casa desta sessão em destaque (figura e fundo)."""
    out = '<ol class="c10-mapa" aria-label="Mapa do Contra-feed: dez casas, uma por sessão">'
    for i, (titulo, _) in enumerate(CASAS, 1):
        estado = ' class="c10-mapa-atual" aria-current="step"' if i == casa else (' class="c10-mapa-feita"' if i < casa else '')
        out += '<li' + estado + '><b>' + str(i) + '</b><span>' + e(titulo) + '</span></li>'
    return out + '</ol>'


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
        out += figura(path, s['imagem'], 'c10-material')
    elif tipo in ('ver_imagem', 'ver_passo'):
        if tipo == 'ver_imagem':
            img = IMAGENS[m['imagem']]
            out += '<p><a class="c10-action c10-action-line" href="' + rel(path, 'cidadania/m2/imagens/#' + img['ancora']) + '">Ver a fotografia</a></p><p class="c10-credit">' + credito(img) + '</p>'
        else:
            t, alvo = m['ligacao']
            out += '<p><a class="c10-action c10-action-line" href="' + rel(path, alvo) + '">' + e(t) + '</a></p>'
            out += '<p class="c10-credit">O original: ' + e(LISBOA_1907['legenda'][0].lower() + LISBOA_1907['legenda'][1:]) + ' ' + e(LISBOA_1907['credito']) + ', <a href="' + LISBOA_1907['url'] + '">loc.gov</a>. A versão B foi alterada por nós.</p>'
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
        out += para('c10-small', 'Em papel, na sala.')
    if m.get('revela'):
        out += para('c10-reading', m['revela'])
    if m.get('leitura'):
        out += para('c10-reading', m['leitura'])
    if m.get('aviso'):
        out += para('c10-small', m['aviso'])
    if m.get('fonte'):
        out += fonte(path, m['fonte'])
    return out + '</section>'


def ve(path, n, s):
    out = ''.join(material(path, n, s, j, m, len(s['ve'])) for j, m in enumerate(s['ve'], 1))
    out += para('c10-reading', s.get('leitura', ''))
    if n in OBRAS:
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
    out += para('c10-small', d.get('silencio_mais', ''))
    out += '<p class="c10-small">Três minutos. Escreve a escolha e uma razão no cartão de decisão. Depois, uma volta: cada pessoa lê o seu cartão, sem comentários.</p></div>'
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
        out += '<div class="c10-vsf">' + label('E as três perguntas do Contra-feed') + '<p class="c10-small">Responde a cada uma com «sim», «em parte» ou «ainda não», e uma linha a dizer porquê.</p><dl>' + ''.join('<dt>' + e(a) + '</dt><dd>' + e(b) + '</dd>' for a, b in s['vsf']) + '</dl></div>'
    out += label('Confirma') + '<ul class="c10-checks">' + ''.join('<li>' + e(t) + '</li>' for t in lv['confirma']) + '</ul>'
    if s.get('depois'):
        out += '<div class="c10-depois">' + label('Depois, no telemóvel') + '<p class="c10-small">Dois ou três dias depois da sessão.</p><ul>' + ''.join('<li>' + liga(path, a, t) + '</li>' for t, a in s['depois']) + '</ul></div>'
    return out + molde.registo()


PASSO = [recupera, ve, decide, faz, leva]


def sessao(n, s):
    ident = f'{n:02}'
    path = f'cidadania/m2/sessoes/{ident}/index.html'
    body = molde.abertura(ident, s['tema'], s['titulo'], s['pergunta'], figura(path, s['imagem'], 'c10-cover-img'), separador=' / ')
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
    body += '<p>Os passos 00 a 08 e os cinco casos não mudam: ficam no fim de cada sessão, em «Depois, no telemóvel», para dois ou três dias depois. A chave epi-cidadania-m2 e o contador de 11 atividades mantêm-se. O registo das sessões usa uma chave própria, ' + CHAVE + ', fica só no aparelho de cada aluno e não é gravado em projeção.</p>'
    body += '<p>As páginas das sessões mostram a turma; este guia mostra a condução. Para abrir o Recupera seguinte, escolher uma resposta do Leva.</p></section>'
    body += '<section class="c10-reference" id="decisoes"><h2>Decisões provisórias</h2><p>As cinco perguntas do plano ficaram com uma decisão provisória, a confirmar pelo docente.</p><ol class="c10-decisoes">'
    body += ''.join('<li><p class="c10-label">Decisão provisória ' + str(i) + ': ' + e(t) + '</p><p>' + e(txt) + '</p></li>' for i, (t, txt) in enumerate(DECISOES, 1)) + '</ol></section>'
    body += '<section class="c10-reference" id="mapa"><h2>O mapa do Contra-feed</h2><p>Cada grupo tem um mapa com dez casas, num A3 ou numa página do ficheiro do grupo. O Faz de cada sessão preenche uma casa. O mapa só organiza o que o Contra-feed já pede: não cria entregas nem pesos.</p>'
    body += tabela(['Casa', 'Sessão', 'Conteúdo'], [(str(i) + '. ' + t, f'{i:02}', c) for i, (t, c) in enumerate(CASAS, 1)], 'As dez casas, uma por sessão')
    body += '<p><b>Recuperação espaçada.</b> O Recupera traz a sessão anterior. O Decide volta a casas antigas: a casa 1 regressa na sessão 07, a casa 4 na 08 e na 10, a casa 5 na 07 e na 10. Os passos ficam para dois ou três dias depois.</p></section>'
    body += '<section class="c10-reference" id="avaliacao"><h2>Onde nasce cada evidência</h2><p>Os pesos são os do Contra-feed; nenhum é novo.</p>'
    body += tabela(['Instrumento', 'Peso', 'Sessões', 'Evidência'], INSTRUMENTOS, 'Os quatro instrumentos de avaliação')
    body += '<p>Os cartões do Leva e as respostas Vi, Situei e Fiz são evidência formativa, sem peso. Nenhuma posição moral é pontuada. O limite de faltas do módulo continua a ser de 6 horas.</p>' + liga(path, 'cidadania/contra-feed/', 'Projeto, requisitos e avaliação do Contra-feed') + '</section>'
    body += '<section class="c10-reference" id="tempos"><h2>Tempos</h2>'
    body += tabela(['Sessões'] + PASSOS, [('01 a 09',) + tuple(str(t) for t in TEMPOS), ('10',) + tuple(str(t) for t in TEMPOS_MOSTRA)], 'Minutos por passo')
    body += '<p>O Faz inclui a pausa de 10 minutos e cerca de 20 minutos de revisão. Na sessão 10, 125 minutos dão para sete grupos com cerca de 8 minutos de mostra, 7 de defesa e 2 de transição.</p></section>'
    body += '<section class="c10-reference" id="regras"><h2>Regras comuns</h2><ul class="c10-regras">'
    body += '<li><b>Recupera.</b> Duas perguntas conceptuais sobre a sessão anterior, com resposta em «Confirmar», e uma pergunta pessoal sobre o produto, sem resposta.</li>'
    body += '<li><b>Vê.</b> Um material de cada vez, com a instrução junto dele. Primeiro observa, depois lê.</li>'
    body += '<li><b>Decide.</b> Sem ecrã e sem pontuar posições. Três minutos em silêncio, com um cartão de decisão; uma volta, sem comentários; as três tarefas em grupo; o grupo regista a decisão e uma razão vencida; o docente projeta «Comparar razões».</li>'
    body += '<li><b>Faz.</b> Em papel ou no ficheiro do grupo. Fecha com revisão por outra pessoa, que marca uma coisa que se percebe e uma que falta, e faz uma pergunta. A versão revista guarda-se na casa da sessão.</li>'
    body += '<li><b>Leva.</b> Uma pergunta de saída, em papel, com três critérios em «Confirma».</li>'
    body += '<li><b>Vídeos.</b> Pergunta antes, pergunta depois e alternativa escrita. Nenhum é obrigatório. Os vídeos «em revisão» de Ver para fazer não entram.</li></ul></section>'
    for n, s in enumerate(SESSOES, 1):
        ident = f'{n:02}'
        body += '<section class="c10-stage c10-guia-sessao" id="sessao-' + ident + '"><p class="c10-eyebrow">Sessão ' + ident + ' / ' + e(s['tema']) + '</p><h2>' + e(s['titulo']) + '</h2><p class="c10-guia-q">' + e(s['pergunta']) + '</p>'
        body += '<ol class="c10-guia-tempos">' + ''.join('<li><b>' + e(l) + '</b><span>' + str(t) + ' min</span></li>' for l, t in zip(PASSOS, tempos(n))) + '</ol>'
        body += '<p><b>Casa ' + str(n) + ':</b> ' + e(CASAS[n - 1][1]) + '</p>'
        body += '<p><b>Cartão de obra:</b> ' + (e(OBRAS[n]['autor'] + ', ' + OBRAS[n]['titulo']) + '.' if n in OBRAS else 'nenhum, como na sessão 10 do Módulo 1.') + '</p>'
        body += '<p>' + e(s['docente']) + '</p>'
        body += '<p><b>Inclusão.</b> ' + e(' '.join(s['inclusao'])) + '</p>'
        if s.get('depois'):
            body += '<p><b>Depois, no telemóvel.</b></p><ul>' + ''.join('<li>' + liga(path, a, t) + '</li>' for t, a in s['depois']) + '</ul>'
        body += '<p class="c10-guia-links">' + liga(path, f'cidadania/m2/sessoes/{ident}/', 'Abrir a sessão ' + ident) + liga(path, f'cidadania/m2/aulas/{ident}/', 'Etapa ' + ident + ': ' + s['etapa']) + '</p></section>'
    body += '<section class="c10-reference" id="riscos"><h2>Riscos de calendário</h2><ul class="c10-regras">'
    body += '<li><b>O diário.</b> Se a sessão 02 acontecer menos de sete dias depois da 01, a análise do diário passa para o início da 03.</li>'
    body += '<li><b>Sessões densas.</b> A 01 (feed de papel, duas versões e início do diário) e a 06 (escolha do caso e análise). Se faltar tempo, a análise da 06 termina no início da 07.</li></ul></section>'
    body += '<footer class="c10-support">' + liga(path, 'cidadania/m2/#dez-sessoes', 'Sessões do Módulo 2') + liga(path, 'cidadania/contra-feed/', 'Contra-feed') + liga(path, 'cidadania/m2/aulas/', 'As dez etapas') + liga(path, 'cidadania/m2/imagens/', 'Imagens e créditos') + '</footer>'
    return path, documento(path, 'Guia das dez sessões / Cidadania M2', body)


# O bloco das sessões no índice do módulo ----------------------------------------------------------------

def bloco_indice():
    """A lista das dez sessões dentro de cidadania/m2/ (o índice mantém os passos, os casos e o contador)."""
    path = 'cidadania/m2/index.html'
    out = '<section class="c10 c10-indice" id="dez-sessoes" data-c10' + ATRIBUTOS + ' aria-labelledby="dez-sessoes-t">'
    out += '<div class="c10-sectionhead"><h2 id="dez-sessoes-t">Dez sessões</h2><p class="c10-small" data-count></p></div>'
    out += '<p><a class="c10-action" href="sessoes/01/" data-continue data-continue-base="sessoes/" data-fim-href="../contra-feed/" data-fim-texto="Rever o Contra-feed">Começar na sessão 01</a></p>'
    out += '<ol class="c10-session-list">' + ''.join(molde.cartao_sessao(f'{n:02}', f'sessoes/{n:02}/', s['tema'], s['titulo'], s['pergunta']) for n, s in enumerate(SESSOES, 1)) + '</ol>'
    out += '<p class="c10-indice-mais"><a href="https://pedrohfernandes-klk.github.io/lente/cidadania/m2/aulas/">As dez etapas, em texto</a>' + liga(path, 'cidadania/m2/sessoes/', 'Guia do docente') + '</p></section>'
    return out


def build(write):
    for n, s in enumerate(SESSOES, 1):
        write(*sessao(n, s))
    write(*guia())
