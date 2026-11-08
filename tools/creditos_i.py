"""08/11/2026: decisões 153, 162 e 176 (pedido lente-3 do plano plano-creditos-i-20261105.md, secção 2.3, ponto 3).

Aplica, desfaz e confere um manifesto fechado de trocas literais do «i» dos créditos, também quando o HTML vive dentro dos
JSON dos cartões (EPIJogo.montar(...) e os dados das páginas que montam o HTML no navegador).

O manifesto é um objeto JSON {ficheiro: [[antigo, novo, n] ou [antigo, novo, n, modo], ...]}, como as outras camadas de
tools/trocas/. Cada troca é exata: «antigo» aparece n vezes no ficheiro antes de se aplicar, e «novo» aparece n vezes depois.
Sem «modo», «antigo» e «novo» estão escritos como estão no ficheiro (HTML corrido, código). Com «modo», estão escritos em
HTML corrido e vivem dentro de uma cadeia JSON; o utilitário trata o escape:

- «json»: a barra invertida passa a «\\\\» e as aspas a «\\"», como nos cartões;
- «json/»: o mesmo e, além disso, «</» passa a «<\\/», como nos cartões que escapam o fecho das etiquetas.

Assim o manifesto lê-se como HTML e continua fechado (contagem exata) e reversível (desfazer devolve o texto de partida).

Uso:
  python tools/creditos_i.py --verificar   cada ficheiro do manifesto está na versão nova, com as contagens exatas, e desfazer
                                           seguido de aplicar devolve o mesmo texto (por omissão, o manifesto do pedido lente-3)
  python tools/creditos_i.py --aplicar     aplica o manifesto aos ficheiros que ainda não o têm (os que já o têm ficam iguais)
  python tools/creditos_i.py --desfazer    devolve os ficheiros à versão de partida
  --manifesto CAMINHO                      outro manifesto com o mesmo formato
"""
import argparse
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
MANIFESTO = R / 'tools/trocas/creditos-i-lente3-20261108.json'
MODOS = ('json', 'json/')


def escapar(html, modo=None):
    """O texto literal com que «html» aparece no ficheiro, conforme o modo da troca."""
    if modo is None:
        return html
    if modo not in MODOS:
        raise ValueError('modo desconhecido: ' + repr(modo))
    s = html.replace('\\', '\\\\').replace('"', '\\"')
    if modo == 'json/':
        s = s.replace('</', '<\\/')
    return s


def desescapar(literal, modo=None):
    """O inverso de escapar (só para os modos deste utilitário)."""
    if modo is None:
        return literal
    s = literal
    if modo == 'json/':
        s = s.replace('<\\/', '</')
    return s.replace('\\"', '"').replace('\\\\', '\\')


def ler_manifesto(caminho=MANIFESTO):
    dados = json.loads(Path(caminho).read_text(encoding='utf-8'))
    if not isinstance(dados, dict):
        raise ValueError('o manifesto tem de ser um objeto {ficheiro: [trocas]}')
    return dados


def literais(dados):
    """{ficheiro: [(antigo, novo, n)]} com o escape já feito: a forma que as camadas dos testes usam."""
    out = {}
    for ficheiro, trocas in dados.items():
        lista = []
        for t in trocas:
            if len(t) not in (3, 4):
                raise ValueError((ficheiro, 'troca com forma inválida', t[:1]))
            antigo, novo, n = t[0], t[1], t[2]
            modo = t[3] if len(t) == 4 else None
            if not isinstance(n, int) or n < 1:
                raise ValueError((ficheiro, 'contagem inválida', antigo[:60]))
            lista.append((escapar(antigo, modo), escapar(novo, modo), n))
        out[ficheiro] = lista
    return out


def aplicar(texto, trocas, rotulo='créditos i'):
    for antigo, novo, n in trocas:
        if texto.count(antigo) != n:
            raise AssertionError((rotulo, 'aplicar', texto.count(antigo), n, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, trocas, rotulo='créditos i'):
    for antigo, novo, n in reversed(trocas):
        if texto.count(novo) != n:
            raise AssertionError((rotulo, 'desfazer', texto.count(novo), n, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def ja_tem(texto, trocas):
    """A camada já está no texto: cada «novo» com a contagem exata e o «antigo» só onde vem dentro de um «novo»."""
    if not trocas:
        return False
    for antigo, novo, n in trocas:
        if texto.count(novo) != n:
            return False
        dentro = sum(m * novo2.count(antigo) for _, novo2, m in trocas)
        if texto.count(antigo) != dentro:
            return False
    return True


def alinhar(texto, trocas, rotulo='créditos i'):
    """Para bases que mudam com o tempo: se a base já traz a camada, fica como está; senão recebe-a com contagem exata. Um
    estado misto falha."""
    if ja_tem(texto, trocas):
        return texto
    return aplicar(texto, trocas, rotulo)


def verificar(dados, raiz=R):
    """Erros do manifesto e dos ficheiros (lista vazia quando está tudo certo)."""
    erros = []
    for ficheiro, trocas in literais(dados).items():
        p = raiz / ficheiro
        if not p.is_file():
            erros.append(f'{ficheiro}: o ficheiro não existe')
            continue
        texto = p.read_text(encoding='utf-8')
        for antigo, novo, n in trocas:
            if antigo == novo:
                erros.append(f'{ficheiro}: troca sem efeito ({antigo[:60]!r})')
            if antigo in novo:
                erros.append(f'{ficheiro}: o «antigo» está dentro do «novo» ({antigo[:60]!r})')
            if texto.count(novo) != n:
                erros.append(f'{ficheiro}: «novo» aparece {texto.count(novo)} vezes, esperava {n} ({novo[:60]!r})')
        try:
            base = desfazer(texto, trocas, ficheiro)
            if aplicar(base, trocas, ficheiro) != texto:
                erros.append(f'{ficheiro}: desfazer e voltar a aplicar não devolve o mesmo texto')
            if ja_tem(base, trocas):
                erros.append(f'{ficheiro}: a versão de partida já parece ter a camada')
        except AssertionError as e:
            erros.append(f'{ficheiro}: {e}')
    for ficheiro, trocas in dados.items():
        for t in trocas:
            if len(t) == 4:
                modo = t[3]
                for parte in t[:2]:
                    if desescapar(escapar(parte, modo), modo) != parte:
                        erros.append(f'{ficheiro}: o escape {modo!r} não é reversível ({parte[:60]!r})')
    return erros


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--verificar', action='store_true')
    g.add_argument('--aplicar', action='store_true')
    g.add_argument('--desfazer', action='store_true')
    ap.add_argument('--manifesto', default=str(MANIFESTO))
    a = ap.parse_args(argv)
    dados = ler_manifesto(a.manifesto)
    if a.verificar:
        erros = verificar(dados)
        for e in erros:
            print(e)
        total = sum(len(t) for t in dados.values())
        print(('com erros: ' if erros else 'certo: ') + f'{len(dados)} ficheiros, {total} trocas')
        return 1 if erros else 0
    for ficheiro, trocas in literais(dados).items():
        p = R / ficheiro
        texto = p.read_text(encoding='utf-8')
        novo = alinhar(texto, trocas, ficheiro) if a.aplicar else (desfazer(texto, trocas, ficheiro) if ja_tem(texto, trocas) else texto)
        if novo != texto:
            p.write_text(novo, encoding='utf-8')
            print(('aplicado: ' if a.aplicar else 'desfeito: ') + ficheiro)
    return 0


if __name__ == '__main__':
    sys.exit(main())
