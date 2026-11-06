"""05/11/2026: decisão 163 (menus do Laboratório e das lições). Trocas fechadas do manifesto
tests/fixtures/menus-163-20261105.json, para as comparações com bases antigas: o menu ≡ novo (tools/menu_casca.py), o
menu.css e o menu.js, o «aria-controls» do ≡, o aviso sem JavaScript, a marca «Cidadania» do piloto, a continuação no fim
dos percursos (decisão 163, 2.8) e a ordem do Laboratório na entrada do Lente. Cada troca tem contagem exata; qualquer
outra diferença continua a falhar, como em tests/lab147.py.

«exato» serve as comparações byte a byte; «sem_cache» as que tiram primeiro as versões de cache (?v=…) dos dois lados.

05/11/2026: revisão do commit 192c5e3. O manifesto passa a trazer também o nome acessível do diálogo do menu
(aria-labelledby="m-cab m-t") e a marca da barra com o nome num <span class="c-marca-t"> (peças do Laboratório e páginas
estáticas da Cidadania, estas com o destino e o nome do piloto). Continua fechado: cada troca com contagem exata e nenhuma
outra diferença passa."""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
TROCAS = json.loads((R / 'tests/fixtures/menus-163-20261105.json').read_text(encoding='utf-8'))


def aplicar(texto, ficheiro, sem_cache=False):
    trocas = TROCAS['sem_cache' if sem_cache else 'exato'].get(ficheiro, [])
    if not trocas:  # sem trocas, o ficheiro fica tal e qual (também os binários)
        return texto
    binario = isinstance(texto, bytes)
    if binario:
        texto = texto.decode('utf-8')
    for antigo, novo, quantidade in trocas:
        assert texto.count(antigo) == quantidade, ('decisão 163', ficheiro, antigo[:80])
        texto = texto.replace(antigo, novo)
    return texto.encode('utf-8') if binario else texto


def _ja_fundido(texto, trocas):
    # Uma troca que apaga (novo vazio) conta como feita quando o «antigo» já não aparece, como em lab147.alinhar.
    return all((texto.count(novo) == n) if novo else (texto.count(antigo) == 0) for antigo, novo, n in trocas)


def alinhar(texto, ficheiro, sem_cache=False):
    """06/11/2026: para bases que mudam com o tempo (git merge-base HEAD origin/main). Antes da fusão do #125 a base ainda
    tem cada «antigo» com a contagem exata e recebe as trocas; depois da fusão já tem cada «novo» com a contagem exata e
    fica como está. Qualquer outro estado falha, como em lab147.alinhar."""
    trocas = TROCAS['sem_cache' if sem_cache else 'exato'].get(ficheiro, [])
    if not trocas:
        return texto
    s = texto.decode('utf-8') if isinstance(texto, bytes) else texto
    if _ja_fundido(s, trocas):
        return texto
    if all(s.count(antigo) == n for antigo, novo, n in trocas):
        return aplicar(texto, ficheiro, sem_cache)
    raise AssertionError(('decisão 163 (base em estado misto)', ficheiro))


def acrescentadas(texto, ficheiro, rotulos, sem_cache=False):
    """06/11/2026: quantas vezes cada rótulo entrou pelas trocas deste manifesto numa base que já as traz (contagem exata,
    tirada do próprio manifesto: por troca, as vezes no «novo» menos as vezes no «antigo», vezes a quantidade). Numa base
    anterior à fusão do #125 é zero. Serve as contagens fechadas de renomeacoes_cidadania.renomear: o menu ≡ diz, por
    exemplo, «Módulo 1: Humanos.» e isso não é um resto do nome antigo."""
    trocas = TROCAS['sem_cache' if sem_cache else 'exato'].get(ficheiro, [])
    if not trocas:  # sem trocas, nada a somar (também os binários)
        return {r: 0 for r in rotulos}
    s = texto.decode('utf-8') if isinstance(texto, bytes) else texto
    if not _ja_fundido(s, trocas):
        return {r: 0 for r in rotulos}
    return {r: sum(n * (novo.count(r) - antigo.count(r)) for antigo, novo, n in trocas) for r in rotulos}
