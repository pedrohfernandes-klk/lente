"""Regras da Justiça; conferência de legendas exclusivamente local."""
import html
import json
import math
import re
from html.parser import HTMLParser
from pathlib import Path

PROIBIDAS = re.compile(r'\b(?:professor(?:a|es|as)?|jog(?:o|os|ar|a|as|amos|ais|am|ou|ue|uem|uei|aste|aram|ando|ado|ada|ados|adas)|fichas?|folhas?)\b', re.I)


def texto(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))


def textos(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for v in valor.values():
            yield from textos(v)
    elif isinstance(valor, list):
        for v in valor:
            yield from textos(v)


class Visivel(HTMLParser):
    """Conta o original e a tradução; exclui conteúdo fechado e o desenho."""
    def __init__(self):
        super().__init__()
        self.pilha = []
        self.partes = []

    def handle_starttag(self, tag, attrs):
        if tag in ('br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'wbr'):
            return
        a = dict(attrs)
        # 05/11/2026: revisão de 5/11. O crédito dos desenhos (<span class="cred">) é crédito, não leitura: não conta para as 95
        # palavras, como o próprio desenho.
        oculto = tag in ('svg', 'script', 'style') or a.get('class') in ('lado-c', 'mais-c', 'cred')
        self.pilha.append((tag, oculto))

    def handle_endtag(self, tag):
        for i in range(len(self.pilha)-1, -1, -1):
            if self.pilha[i][0] == tag:
                del self.pilha[i:]
                break

    def handle_data(self, data):
        if not any(o for _, o in self.pilha):
            self.partes.append(data)


def palavras_visiveis(item):
    p = Visivel()
    p.feed(item.get('html', ''))
    return len(re.findall(r"[\wÀ-ÿ'’-]+", ' '.join(p.partes) + ' ' + item.get('titulo', '')))


def validar_molde_novo(itens):
    """02/11/2026: produção livre e sucessão na sequência efetivamente apresentada.

    Um cartão ler que pede produção livre em papel declara producao_livre=true.
    Frase e versos ordenam material dado e não são produção livre.
    As variantes devem ser selecionadas antes de chamar esta função.
    """
    erros = []
    fazer = [x for x in itens if x['t'] != 'ler']
    if not 20 <= len(itens) <= 26:
        erros.append('contagem')
    if len(fazer) < 14:
        erros.append('atividades')
    for x in itens:
        if 'producao_livre' in x and (x['t'] != 'ler' or type(x['producao_livre']) is not bool):
            erros.append('marcacao_producao_livre')
    if sum(x['t'] == 'escrita' or (x['t'] == 'ler' and x.get('producao_livre') is True) for x in itens) > 1:
        erros.append('producao_livre')
    if len({x['t'] for x in fazer} - {'escrita'}) < 5:
        erros.append('variedade')
    if any(a['t'] == b['t'] == c['t'] for a, b, c in zip(itens, itens[1:], itens[2:])):
        erros.append('sucessao')
    if sum(x.get('rot') == 'Na aula' for x in itens) != 1:
        erros.append('na_aula')
    if not itens or itens[0].get('rot') != 'Abre' or 'No fim, consegues' not in itens[0].get('html', '') or not re.search(r'<img\b', itens[0].get('html', '')):
        erros.append('abre')
    if len(itens) < 2 or itens[1].get('rot') != 'Olha' or itens[1]['t'] != 'mapa':
        erros.append('olha')
    return erros


def validar_banco(itens, numero, novo=False):
    erros = []
    if not 20 <= len(itens) <= 26:
        erros.append(f'L{numero}: número de cartões fora de 20 a 26')
    curtas, esperado = 0, 0
    for k, item in enumerate(itens, 1):
        onde = f'L{numero} C{k:02}'
        vis = texto(' '.join(textos(item)))
        # Citações literais são a única exceção à pontuação da casa.
        sem_citacoes = re.sub(r'«[^»]*»', '', vis)
        if PROIBIDAS.search(vis):
            erros.append(f'{onde}: palavra proibida')
        if '—' in sem_citacoes or '·' in sem_citacoes:
            erros.append(f'{onde}: pontuação proibida')
        if item['t'] == 'escolha':
            opcoes, certa, fe = item.get('o', []), item.get('c'), item.get('fe', [])
            if len(opcoes) != 4 or not isinstance(fe, list) or len(fe) != 4 or certa not in range(4):
                erros.append(f'{onde}: escolha sem quatro opções e retornos')
                continue
            if not item.get('f') or any((j == certa) != (fe[j] is None) for j in range(4)):
                erros.append(f'{onde}: retornos desalinhados')
            medidas = [len(re.sub(r'\s+', ' ', texto(o)).replace('_', '').replace('*', '').strip()) for o in opcoes]
            if min(medidas) == 0 or max(medidas) > 1.2 * min(medidas):
                erros.append(f'{onde}: opções desequilibradas')
            if len(opcoes[certa]) >= max(len(o) for j, o in enumerate(opcoes) if j != certa):
                erros.append(f'{onde}: certa mais longa')
            curtas += medidas[certa] < min(v for j, v in enumerate(medidas) if j != certa)
            esperado += 1 / len(opcoes)
        if item['t'] == 'vf' and (not isinstance(item.get('v'), bool) or not item.get('f') or not item.get('fe')):
            erros.append(f'{onde}: VF sem valor ou retornos')
        if item['t'] in ('emparelhar', 'ordenar') and (not item.get('f') or not item.get('fe')):
            erros.append(f'{onde}: atividade sem retornos')
        if novo and item['t'] == 'ler' and palavras_visiveis(item) > 95:
            erros.append(f'{onde}: mais de 95 palavras visíveis')
    if curtas > math.ceil(esperado):
        erros.append(f'L{numero}: certa mais curta demasiadas vezes')
    if novo:
        erros.extend(f'L{numero}: molde novo: {erro}' for erro in validar_molde_novo(itens))
    return erros


def extrair_citacoes(pasta):
    resultado = []
    for meta in json.loads((pasta / 'licoes.json').read_text('utf-8')):
        itens = json.loads((pasta / f"bancos/licao-{meta['numero']}.json").read_text('utf-8'))
        for k, item in enumerate(itens, 1):
            for s in textos(item):
                for m in re.finditer(r'<p class="cita-en">(.*?)</p>\s*<p class="trad">(.*?)</p>', s, re.S):
                    tempo = re.search(r'<span class="tempo">(\d+:\d\d)</span>', m[1])
                    if tempo is None:
                        raise ValueError(f"L{meta['numero']} C{k}: citação sem tempo")
                    en = texto(re.sub(r'<span class="tempo">.*?</span>', '', m[1])).strip().strip('«»').strip()
                    resultado.append(dict(licao=meta['numero'],cartao=k,episodio=(meta['aulas'][0]+1)//2,video=meta['video'],tempo=tempo[1],frase=en,traducao=texto(m[2]).strip()))
                # Citações curtas nos retornos e nas razões que se abrem ao toque.
                sem_blocos = re.sub(r'<p class="cita-en">.*?</p>', '', s, flags=re.S)
                for m in re.finditer(r'«([^»]+)»(?:\s*\((\d+:\d\d)\)|,\s*(\d+:\d\d)\)|\s*<span class="tempo">(\d+:\d\d)</span>)', sem_blocos):
                    en = texto(m[1]).strip()
                    resultado.append(dict(licao=meta['numero'],cartao=k,episodio=(meta['aulas'][0]+1)//2,video=meta['video'],tempo=m[2] or m[3] or m[4],frase=en))
    return resultado


def norm(s):
    s = texto(s).lower().replace('’', "'")
    return re.sub(r'\s+', ' ', re.sub(r"[^a-z0-9' ]+", ' ', s)).strip()


def conferir_legendas(citacoes, pasta):
    transcricoes = {}
    erros = []
    for c in citacoes:
        ep = c['episodio']
        if ep not in transcricoes:
            p = pasta / f'ep{ep:02}.en.vtt'
            if not p.exists():
                p = pasta / f'ep{ep}.en.vtt'
            if not p.exists():
                raise ValueError(f'Falta a legenda privada do episódio {ep}.')
            s = p.read_text('utf-8')
            partes = re.findall(r'\d\d:\d\d:\d\d\.\d+ --> [^\n]+\n(.*?)(?:\n\n|\Z)', s, re.S)
            s = norm(' '.join(partes))
            # Gralhas documentadas pelo validador anterior, sem alterar a legenda.
            transcricoes[ep] = s.replace('then a pig satisfied','than a pig satisfied').replace("you're steering wheel works",'your steering wheel works')
        for parte in re.split(r'…|\[\.\.\.\]', c['frase']):
            if norm(parte) not in transcricoes[ep]:
                erros.append(f"L{c['licao']} C{c['cartao']}: citação ausente da legenda do episódio {ep}")
    return erros
