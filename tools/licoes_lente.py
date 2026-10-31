"""Gerador das lições em cartões do Lente (30/10/2026), com o motor único das lições (assets/licoes/, cópia do
Português). A primeira a usá-lo é a Cidadania refeita (decisões do docente de 30/10: cada sessão é uma lição em cartões,
12 a 16 de fazer, um único cartão «Na aula», casos primeiro e nenhuma figura em destaque).

Uso: python3 tools/licoes_lente.py tools/licoes/cidadania-m1-s01.json [...]   (sem argumentos: todos os .json da pasta)
     python3 tools/licoes_lente.py --verificar            (valida e confirma que as páginas estão atualizadas)

O .json é a fonte; a página gerada não se edita à mão. A validação corre sempre antes de escrever: se falhar, nada se
escreve e a razão aparece no terminal."""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PASTA = ROOT / 'tools' / 'licoes'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'

PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a[sm]?|o|ou|uei|ámos)|fichas?|folhas?)(?![\wÀ-ÿ])|[·—]', re.I)
# a mesma lista de nomes de tests/test_lingua_perguntas.py (#76): «Qual das citações…», nunca «Qual citação…»
NOMES = ['frases?', 'citaç(?:ão|ões)', 'afirmaç(?:ão|ões)', 'perguntas?', 'image(?:m|ns)', 'vers(?:ão|ões)', 'recortes?', 'critérios?', 'conclus(?:ão|ões)', 'formulaç(?:ão|ões)', 'reformulaç(?:ão|ões)', 'propostas?', 'utilizaç(?:ão|ões)', 'raz(?:ão|ões)', 'créditos?', 'obras?', 'detalhes?', 'pormenor(?:es)?', 'decis(?:ão|ões)', 'opç(?:ão|ões)', 'respostas?', 'palavras?', 'versos?', 'estrofes?', 'linhas?', 'comparaç(?:ão|ões)', 'interpretaç(?:ão|ões)', 'revis(?:ão|ões)', 'sínteses?', 'justificaç(?:ão|ões)', 'desenvolvimentos?', 'notas?', 'registos?', 'aç(?:ão|ões)', 'alteraç(?:ão|ões)', 'inícios?', 'par(?:es)?', 'trios?', 'procedimentos?', 'promessas?', 'exemplos?', 'textos?', 'parágrafos?', 'títulos?', 'legendas?', 'cenas?', 'persona(?:gem|gens)', 'argumentos?', 'recursos?', 'sentidos?', 'efeitos?', 'ideias?', 'teses?', 'provas?', 'fontes?', 'planos?', 'acontecimentos?', 'hipóteses?', 'nomes?', 'leituras?', 'testemunh(?:a|as|o|os)']
QUAL_NOME = re.compile(r'(?<![A-Za-zÀ-ÿ])(?:Qual|Quais|qual|quais)\s+(?:' + '|'.join(NOMES) + r')(?![A-Za-zÀ-ÿ])')
ORDINAL = re.compile(r'(?:^|[.;:!?]\s+)[AaOo]s?\s+(?:primeir|segund|terceir|quart|últim)[ao]s?\b(?!\s+(?:parágrafo|linha|artigo|passo|cartão|sessão))|\bopç(?:ão|ões)\s+[A-E]\b')
TIPOS_FAZER = {'escolha', 'vf', 'emparelhar', 'sublinhar', 'ordenar', 'completar', 'frase', 'mapa'}


def visivel(s):
    s = re.sub(r'<[^>]+>', ' ', str(s))
    s = html.unescape(s).replace('**', '').replace('_', '')
    return re.sub(r'\s+', ' ', s).strip()


def textos(c):
    """Todo o texto que o aluno vê num cartão (para as regras de escrita)."""
    t = []
    for k in ('p', 'p2', 'f', 'titulo', 'html', 'frase'):
        if c.get(k):
            t.append(visivel(c[k]))
    fe = c.get('fe')
    t += [visivel(x) for x in (fe if isinstance(fe, list) else [fe]) if x]
    t += [visivel(x) for x in c.get('o', []) + c.get('passos', [])]
    t += [visivel(x) for par in c.get('pares', []) for x in par]
    for L in c.get('lacunas', []):
        t += [visivel(x) for x in L.get('o', [])]
    if c.get('aula'):
        t += [visivel(v) for v in c['aula'].values()]
    return t


def validar(d):
    erros = []
    C = d.get('cartoes') or []
    for k in ('id', 'chave', 'versao', 'titulo', 'h1', 'saida', 'fontes', 'modulo', 'marca'):
        if not d.get(k):
            erros.append(f'falta o campo «{k}»')
    if not re.fullmatch(r'epi-cid-m\d-s\d{2}', d.get('chave', '')):
        erros.append('a chave tem de ser epi-cid-mN-sNN')
    fazer = [c for c in C if c.get('t') in TIPOS_FAZER]
    if not 12 <= len(fazer) <= 16:
        erros.append(f'{len(fazer)} cartões de fazer (têm de ser 12 a 16)')
    if not C or C[0].get('rot') != 'Abre':
        erros.append('o primeiro cartão tem de ser o «Abre»')
    elif '<img' in C[0].get('html', '') or C[0].get('ver'):
        erros.append('o «Abre» não leva imagem (casos primeiro, nenhuma figura em destaque)')
    if not C or C[-1].get('rot') != 'Para levar' or not C[-1].get('escuro'):
        erros.append('o último cartão tem de ser o «Para levar» (escuro)')
    na_aula = [i for i, c in enumerate(C) if c.get('rot') == 'Na aula']
    if len(na_aula) != 1:
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
        for x in textos(c):
            m = PROIBIDAS.search(x)
            if m:
                erros.append(f'{onde}: «{m.group(0)}» não pode aparecer')
            m = QUAL_NOME.search(x)
            if m:
                erros.append(f'{onde}: «{m.group(0)}» (escreve «Qual das…» ou «Que…»)')
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
    if leitura > 900:
        erros.append(f'{leitura} palavras de leitura na sessão (máximo 900)')
    # opções da sessão: a certa não pode ser sempre a mais longa (nem sempre a mais curta)
    esc = [c for c in C if c.get('t') == 'escolha']
    if len(esc) >= 3:
        longa = sum(1 for c in esc if len(visivel(c['o'][c['c']])) == max(len(visivel(x)) for x in c['o']))
        curta = sum(1 for c in esc if len(visivel(c['o'][c['c']])) == min(len(visivel(x)) for x in c['o']))
        if longa == len(esc) or curta == len(esc):
            erros.append('a certa é sempre a mais longa ou sempre a mais curta')
    return erros


def esc(s):
    return html.escape(str(s), quote=True)


# 31/10/2026 (revisão de pt-PT): títulos de obras em itálico também nas fontes. Converte _…_ em <i>…</i> depois de escapar,
# com a guarda do motor (assets/licoes/jogo.js, função it): só quando o _ não está colado a letras, a algarismos ou a «/»,
# para não estragar endereços como convencao_sobre_direitos_da_crianca.pdf ou File:William_Edward_Kilburn_-_View….
ITALICO = re.compile(r'(^|[^0-9A-Za-zÀ-ÖØ-öø-ÿ_/])_([^_\n<>]{1,100}?)_(?![0-9A-Za-zÀ-ÖØ-öø-ÿ_])')


def esc_it(s):
    return ITALICO.sub(r'\1<i>\2</i>', esc(s))


def pagina(d):
    saida = d['saida']
    prof = saida.count('/')
    base = '../' * prof
    mod = d['modulo']
    piloto = d.get('piloto')
    dados = json.dumps(d['cartoes'], ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    menu = (
        f'<div class="casca-menu" data-c-painel hidden><div class="c-menu-in" role="dialog" aria-label="Menu"><div class="c-menu-cab"><p>Cidadania, módulo {mod["n"]}<br>{esc(mod["nome"])}</p>'
        # 31/10/2026 (revisão do diretor de arte): o botão do tema vai para o menu (appearance.js usa este lugar); fora da barra,
        # a casca deixa de passar a largura do ecrã a 320 e 360 px.
        '<span data-appearance-control></span><button type="button" class="c-ic" data-c-fecha-menu aria-label="Fechar o menu">✕</button></div><nav><ol class="c-migalhas" aria-label="Onde estás">'
        f'<li style="--k:0"><a href="{LENTE}">Lente</a></li><li style="--k:1"><a href="{LENTE}cidadania/">Cidadania</a></li>'
        f'<li style="--k:2"><a href="{esc(mod["url"])}">Módulo {mod["n"]}: {esc(mod["nome"])}</a></li><li><span class="aqui" style="--k:3">Estás em: {esc(d["titulo"])}</span></li></ol>'
        f'<a href="{esc(mod["url"])}">As sessões do módulo</a><a href="https://pedrohfernandes-klk.github.io/pt/como/">Como se faz (vídeos)</a></nav>'
        f'<p class="c-menu-extra">EPI, Escola Profissional de Imagem. Cidadania e Desenvolvimento 2026/2027. {esc(d["titulo"])}. Fontes: {esc_it(d["fontes"])} O que marcas fica só neste aparelho.</p></div></div>')
    cfg = {'versao': d['versao'], 'marca': d['marca'], 'chave': d['chave'], 'titulo': d['titulo'], 'variar': False}
    # 31/10/2026 (revisão do diretor de arte, sistema 6.11): o ecrã final leva «A seguir» (a sessão seguinte) e o módulo.
    if d.get('seguinte'):
        cfg.update({'percurso': mod['url'], 'percursoRotulo': 'As 10 sessões', 'seguinte': d['seguinte'], 'seguinteRotulo': d.get('seguinteRotulo')})
    # 30/10/2026: o leitor de vídeo (cópia do do Português) só entra quando há um cartão com vídeo.
    tem_video = any('data-yt=' in (c.get('html') or '') for c in d['cartoes'])
    return (
        '<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f'<title>{esc(d["titulo"])} · Cidadania · Lente</title>'
        + ('<meta name="robots" content="noindex, nofollow">' if piloto else '')
        + f'<meta name="description" content="{esc(d["h1"])}">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Special+Elite&display=swap" rel="stylesheet">'
        f'<link rel="stylesheet" href="{base}assets/licoes/lesson.css?v={d["versao"]}"><link rel="stylesheet" href="{base}assets/licoes/cidadania.css?v={d["versao"]}">'
        f'<link rel="stylesheet" href="{base}assets/appearance.css"><script src="{base}assets/appearance.js"></script>'
        f'</head><body class="licao-lente licao-cidadania" data-licao="{esc(d["id"])}">'
        '<div class="casca" data-casca>'
        f'<header class="casca-topo"><a class="c-marca" href="{esc(mod["url"])}" aria-label="Voltar ao módulo {mod["n"]} de Cidadania"><svg class="c-casa" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8.2 8 2.6l6 5.6M4 7v7h3v-4h2v4h3V7"/></svg>{esc(d["marca"])}</a>'
        '<span class="c-num" data-c-num></span><button type="button" class="c-barra" data-c-barra aria-label="Ver os cartões já feitos" disabled><svg viewBox="0 0 1 10" preserveAspectRatio="none" aria-hidden="true"></svg></button>'
        '<span class="c-modo" data-c-modo hidden></span><button type="button" class="c-ic" data-c-como aria-label="Como se faz" title="Como se faz" hidden><span class="c-roda">?</span></button>'
        '<button type="button" class="c-ic" data-c-som aria-pressed="false" aria-label="Som" title="Som ligado ou desligado"><span class="c-roda">♪</span></button>'
        '<button type="button" class="c-ic" data-c-menu aria-label="Menu" aria-expanded="false" title="Menu"><span class="c-tres"></span></button></header>'
        f'<h1 class="c-sr">{esc(d["h1"])}</h1><main class="casca-corpo" id="casca-corpo" tabindex="-1"><div id="baralho" class="jogo-alvo"></div></main>'
        '<footer class="casca-acoes" data-c-acoes></footer><section class="casca-folha" data-c-folha role="status" aria-live="polite" hidden></section>'
        + menu + '</div><div id="aviso" role="status"></div>'
        f'<script src="{base}assets/licoes/casca.js?v={d["versao"]}"></script><script src="{base}assets/licoes/jogo.js?v={d["versao"]}"></script>'
        + (f'<script defer src="{base}assets/licoes/video-youtube.js?v={d["versao"]}"></script>' if tem_video else '')
        + f'<script defer src="{base}assets/projection-launcher.js" data-site="lente"></script>'
        '<script>(function(){"use strict";var CARTOES=' + dados + ',CFG=' + json.dumps(cfg, ensure_ascii=False) + ';'
        'var el=document.getElementById("baralho");CFG.el=el;CFG.itens=CARTOES;CFG.casca=window.EPICasca?EPICasca.pagina():null;'
        'if(window.EPIJogo)EPIJogo.montar(CFG);})();</script></body></html>\n')


def carregar(p):
    return json.loads(pathlib.Path(p).read_text('utf-8'))


def main(argv):
    verificar = '--verificar' in argv
    fontes = [pathlib.Path(a) for a in argv if not a.startswith('--')] or sorted(PASTA.glob('*.json'))
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
            alvo.write_text(novo, 'utf-8')
            print(f'{p.name}: escrito {d["saida"]}')
    return 1 if falhou else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
