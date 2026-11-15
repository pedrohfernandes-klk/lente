"""15/11/2026: revisão geral do Lente (achados confirmados n.º 1, 2, 3, 14, 15, 16, 17, 18 e 24) com as decisões do docente de
15/11/2026 («decide tu mesmo isso tudo já»):

(a) sai o retrato de Stanislávski da oficina do ator (narrativas/oficina-ator), com o crédito e a legenda; o texto fica;
(b) sai o vídeo não oficial de ver-para-fazer/v108 (o embed e a ligação para a republicação): a página continua a abrir com o texto
    que sobra, mas sai da Oficina 12, das contagens de Ver para fazer e dos catálogos da curadoria;
(e) as tarefas de pares e de grupo passam a individuais, com o mesmo objetivo: «O teste do colega» (narrativas/treinar/teste-do-colega,
    o mesmo endereço, o mesmo id e a mesma chave de progresso) passa a «A leitura a frio», o último cartão dos treinos passa a uma
    segunda leitura noutro dia (rótulo «A frio»), e «colega» sai dos treinos, do percurso «Rever», do caderno, de fora-da-pagina (página
    e subpáginas) e das variantes;
(f) «jogo», «folha» e «a pares» trocam-se por palavras permitidas.

Manifesto fechado das trocas literais [antigo, novo, contagem] que levam o main de e4fd171 a esse estado
(tools/trocas/revisao-geral-lente-20261115.json). As trocas que apagam (o retrato, o embed, a linha da Oficina 12 e os registos da
curadoria) levam o texto seguinte como contexto, para a camada se poder desfazer. Nas páginas geradas (títulos, menus, linhas,
lab-dados, mapa, «tudo» e «Seguinte»), as trocas são as que tools/laboratorio.py escreve a partir de assets/laboratorio/percursos.json.

curadoria/ligacoes-atividades-existentes.json tem fim de linha CRLF: a troca escreve-se com LF, como os testes leem os ficheiros, e no
ficheiro sai só a linha do vid-108, sem mexer no fim de linha das outras (tools/creditos_i.py --aplicar e --desfazer escrevem LF; num
ficheiro que já tem a camada, --aplicar não escreve nada).

Os testes que comparam com bases antigas aplicam-no (ou desfazem-no) como a camada mais recente, por cima de todas, com contagem exata,
sem aceitar mais nada."""
import json
import sys
from pathlib import Path
# tools/ no caminho, como em tests/temas_paginas_20261113.py, para o módulo abrir também quando um teste corre sozinho.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import creditos_i  # noqa: E402
MANIFESTO = Path(__file__).resolve().parents[1] / 'tools/trocas/revisao-geral-lente-20261115.json'
TROCAS = creditos_i.literais(creditos_i.ler_manifesto(MANIFESTO))


def aplicar(texto, ficheiro):
    return creditos_i.aplicar(texto, TROCAS.get(ficheiro, []), 'revisão geral do Lente ' + ficheiro)


def desfazer(texto, ficheiro):
    return creditos_i.desfazer(texto, TROCAS.get(ficheiro, []), 'revisão geral do Lente ' + ficheiro)


def alinhar(texto, ficheiro):
    return creditos_i.alinhar(texto, TROCAS.get(ficheiro, []), 'revisão geral do Lente ' + ficheiro)


def alinhar_por_cima(texto, ficheiro, abaixo):
    """Alinha as camadas de baixo (a função «abaixo», da cadeia que chama) e esta por cima delas. Esta camada muda «novo» de camadas
    de baixo (o retrato da oficina do ator com o «i» da lente-3, frases da decisão 154 nos treinos e nas oficinas), por isso o texto
    que já a traz não se alinha por dentro: desfaz-se primeiro, com contagem exata, alinham-se as de baixo e volta a aplicar-se. O
    texto que não a traz alinha-se por baixo e recebe-a por fim. Um estado misto falha, como em creditos_i.alinhar."""
    if creditos_i.ja_tem(texto, TROCAS.get(ficheiro, [])):
        return aplicar(abaixo(desfazer(texto, ficheiro), ficheiro), ficheiro)
    return alinhar(abaixo(texto, ficheiro), ficheiro)
