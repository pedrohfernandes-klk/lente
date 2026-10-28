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
    for n in range(1, 11):
        p = f'cidadania/m2/aulas/{n:02}/index.html'
        linha = '<div class="links sessao-m2"><a href="' + LENTE + f'cidadania/m2/sessoes/{n:02}/">Abrir a sessão {n:02}: Recupera, Vê, Decide, Faz e Leva</a></div>'
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
    s = s.replace('var M=[{"id":"m2","chave":"epi-cidadania-m2","ids":["passo-01","passo-02","passo-03","passo-04","passo-05","passo-06","passo-07","passo-08"]}];', 'var M=[];')
    assert 'Dez sessões: ver as regras' in s and 'data-prog="m2">10 sessões<' in s and 'var M=[];' in s
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
