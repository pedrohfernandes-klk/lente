"""Gera as dez sessões de Cidadania M2 e o guia do docente, e integra-as no sítio.

Executar na raiz: python3 tools/generate_cidadania_m2.py

28/10/2026. Tudo é idempotente e aplicado sobre o conteúdo atual (como as integrações de
tools/generate_cidadania_m1.py): correr duas vezes dá o mesmo resultado, e o que outros trabalhos mudaram
fora destes blocos fica intacto. O M1 não é tocado (tests/test_cidadania_m2_molde.py compara-o com origin/main).
"""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cidadania_m2_correcoes as correcoes  # noqa: E402
from cidadania_m2_molde import CHAVE, SESSOES  # noqa: E402
from cidadania_m2_sessoes import build, bloco_indice, FOLHAS, SCRIPTS  # noqa: E402

R = Path(__file__).resolve().parents[1]
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
INICIO, FIM = '<!-- sessoes-m2 -->', '<!-- /sessoes-m2 -->'
# O cartão do M2 no portal de Cidadania: quantas sessões estão registadas neste aparelho (só lê; nunca grava).
PORTAL_SESSOES = ('<script>(function(){try{var S=JSON.parse(localStorage.getItem("' + CHAVE + '")||"null"),'
                  's=S&&S.version===1&&S.sessions&&typeof S.sessions==="object"&&!Array.isArray(S.sessions)?S.sessions:{},n=0;'
                  'for(var k in s)if(/^(0[1-9]|10)$/.test(k)&&s[k]&&s[k].done===true)n++;'
                  'var p=document.querySelector(\'[data-prog="m2"]\');if(p&&n)p.textContent=n+" de 10 sessões registadas"}catch(x){}})();</script>')


def ler(path):
    return (R / path).read_text('utf-8')


def write(path, s):
    p = R / path
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_text('utf-8') != s:
        p.write_text(s, encoding='utf-8')


def bloco(s, novo, antigo=None, antes=None):
    """Põe «novo» entre os marcadores INICIO e FIM: substitui o bloco que já lá esteja; na primeira vez,
    substitui «antigo» ou insere antes de «antes»."""
    marcado = INICIO + novo + FIM
    if INICIO in s:
        return re.sub(re.escape(INICIO) + '.*?' + re.escape(FIM), lambda m: marcado, s, count=1, flags=re.S)
    if antigo is not None:
        assert s.count(antigo) == 1, antigo
        return s.replace(antigo, marcado)
    assert s.count(antes) >= 1, antes
    return s.replace(antes, marcado + antes, 1)


def corrigir():
    correcoes.aplicar_tudo(ler, write)


def etapas():
    """Uma linha em cada etapa (cidadania/m2/aulas/NN/) para a sessão com o mesmo número; e uma no índice das etapas."""
    # 28/10/2026: a linha diz a relação entre a etapa e a sessão, fica afastada do botão de projeção (que a página põe
    # por baixo do cabeçalho) e tem o aspeto de uma ação secundária (contorno, como os botões do Lente).
    for n in range(1, 11):
        p = f'cidadania/m2/aulas/{n:02}/index.html'
        linha = ('<div class="sessao-m2" style="margin:24px 0 8px"><p style="margin:0 0 8px">Esta etapa faz-se na sessão ' + f'{n:02}' + ', com Recupera, Vê, Decide, Faz e Leva.</p>'
                 '<p class="links" style="margin:0"><a href="' + LENTE + f'cidadania/m2/sessoes/{n:02}/" style="padding:8px 16px;border:2px solid currentColor;font-weight:700;text-decoration:none">Abrir a sessão {n:02} →</a></p></div>')
        write(p, bloco(ler(p), linha, antes='<section>'))
    p = 'cidadania/m2/aulas/index.html'
    linha = '<div class="links sessao-m2"><a href="' + LENTE + 'cidadania/m2/#dez-sessoes">As dez sessões, com Recupera, Vê, Decide, Faz e Leva</a></div>'
    write(p, bloco(ler(p), linha, antes='<h2>'))


def indice_m2():
    """O índice do módulo passa a abrir com as dez sessões (começar ou continuar); passos, casos, contador e
    tabelas ficam como estavam."""
    p = 'cidadania/m2/index.html'
    s = ler(p)
    antigo = '<p class="cid-extra"><a class="cid-action" href="' + LENTE + 'cidadania/m2/aulas/">Começar o percurso · dez etapas</a></p>'
    s = bloco(s, bloco_indice(), antigo=antigo)
    # 28/10/2026: um só «começa aqui». Sem nenhum passo feito, o cartão do passo 00 não se destaca nem diz «Sugerida:
    # começa por aqui» (o ponto de partida é a sessão 01, no bloco de cima); depois do primeiro passo, volta «Sugerida: a seguir».
    sugerida, so_depois = 'p=!!prox&&prox.id===id;', 'p=!!prox&&prox.id===id&&feitas.length>0;'
    assert s.count(sugerida) + s.count(so_depois) == 1, 'o script dos passos do índice do M2 mudou'
    s = s.replace(sugerida, so_depois)
    # As folhas e o motor das sessões, só uma vez, no fim do <head>.
    cabeca = ''.join('<link rel="stylesheet" href="../../assets/' + f + '">' for f in FOLHAS) + ''.join('<script defer src="../../assets/' + j + '"></script>' for j in SCRIPTS)
    marca_i, marca_f = '<!-- sessoes-m2-cabeca -->', '<!-- /sessoes-m2-cabeca -->'
    if marca_i in s:
        s = re.sub(re.escape(marca_i) + '.*?' + re.escape(marca_f), lambda m: marca_i + cabeca + marca_f, s, count=1, flags=re.S)
    else:
        s = s.replace('</head>', marca_i + cabeca + marca_f + '</head>', 1)
    write(p, s)


def portal():
    """cidadania/index.html: o cartão do M2 passa a falar das dez sessões, como o do M1; o progresso das
    sessões vive na página do módulo (a chave epi-cidadania-m2 não é tocada)."""
    p = 'cidadania/index.html'
    s = ler(p)
    s = s.replace('Analisar regras, atenção e autoria; criar um Contra-feed.', 'Dez sessões: ver as regras, pô-las à prova e criar um Contra-feed.')
    s = s.replace('<span class="pt-p" data-prog="m2">8 passos</span>', '<span class="pt-p" data-prog="m2">10 sessões</span>')
    # 28/10/2026: o contador dos passos sai (como no M1) e entra o das sessões, só em leitura da chave nova.
    antigo = re.search(r'<script>\(function\(\)\{var M=\[\{"id":"m2","chave":"epi-cidadania-m2".*?</script>', s, re.S)
    if antigo:
        s = s.replace(antigo.group(0), PORTAL_SESSOES)
    assert 'Dez sessões: ver as regras' in s and 'data-prog="m2">10 sessões<' in s and s.count(PORTAL_SESSOES) == 1
    write(p, s)


def docente():
    p = 'docente/index.html'
    s = ler(p)
    novo = '<p class="m1-teacher-update"><a href="../cidadania/m2/sessoes/">Cidadania M2: guia das dez sessões →</a></p>'
    if novo not in s:
        m1 = '<p class="m1-teacher-update"><a href="../cidadania/m1/sessoes/">Cidadania M1: guia das dez sessões →</a></p>'
        s = s.replace(m1, m1 + novo, 1) if m1 in s else s.replace('</main>', novo + '</main>', 1)
    write(p, s)


if __name__ == '__main__':
    assert len(SESSOES) == 10 and CHAVE == 'lente-cidadania-m2-sessoes-v1'
    build(write)
    corrigir()
    etapas()
    indice_m2()
    portal()
    docente()
    print('Cidadania M2: dez sessões e guia gerados; correções, etapas, índice, portal e guia do docente integrados.')
