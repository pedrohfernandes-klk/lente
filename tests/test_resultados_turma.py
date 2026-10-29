"""Resultados da turma (28/10/2026): entrega com código no caderno e página «Resultados da turma» na área do docente.

Estrutura das páginas, regras de escrita, noindex, nenhuma chamada de rede nos JS novos, ligação no hub, o código da
entrega nunca guardado no aparelho, Guardar e Repor iguais ao que estava publicado, e os totais embutidos conferidos
com as pastas. O comportamento corre em tests/resultados_turma.test.cjs (node) e tests/browser_resultados_turma.cjs."""
from html.parser import HTMLParser
from pathlib import Path
import json
import hashlib
import re
import unittest

R = Path(__file__).resolve().parents[1]
PAGINA = 'docente/resultados/index.html'
JS_NOVOS = ['assets/progresso-registos.js', 'assets/resultados-turma.js', 'assets/caderno-entrega.js']
CSS_NOVO = 'assets/resultados-turma.css'
DOC = 'docs/pedagogia/resultados-turma.md'
# 28/10/2026: o caderno publicado antes desta mudança (origin/main, 60ad7a3) fica conferido por sha256, sem «git show»:
# o teste corre também numa cópia sem .git ou num clone raso. Os valores saem de `git show 60ad7a3:caderno/index.html`
# com as funções script() e secao() de Caderno.test_guardar_e_repor_ficam_iguais.
SHA_SCRIPT_BASE = '7a265b6eda3e127b702cdd455dc36275d9a1887583a02abbaeb6dca5f38550c9'
SHA_SECAO_BASE = 'e8d6c2a28508f2462bdccceaa15f4f3699e22cf69dc7d1ff41266051933b9628'
# 28/10/2026: a única frase de «O teu progresso» que mudou (o aluno mostra o progresso ao docente com «Entregar ao docente»)
FRASE_ANTES = 'Para o levares para outro telemóvel, ou para o mostrares ao docente, guarda-o num ficheiro; para o trazeres de volta, repõe o ficheiro.'
FRASE_AGORA = 'Para o levares para outro telemóvel, guarda-o num ficheiro; para o trazeres de volta, repõe o ficheiro. Para o mostrares ao docente, usa «Entregar ao docente», aqui em baixo.'
CHAVE = 'epi-codigo-entrega'


def ler(p):
    return (R / p).read_text('utf-8')


class Pagina(HTMLParser):
    """ids, ligações, scripts, metas e o texto visível (sem <title>, <script> e <style>)."""

    def __init__(self, s):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.scripts, self.metas, self.texto, self.pilha = [], [], [], [], [], []
        self.ancoras = []  # (href, ids dos antepassados)
        self.feed(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
        for k in ('href', 'src'):
            if a.get(k) is not None:
                self.refs.append(a[k])
        if tag == 'script':
            self.scripts.append(a.get('src'))
        if tag == 'meta':
            self.metas.append(a)
        if tag == 'a':
            self.ancoras.append((a.get('href'), [x[1] for x in self.pilha if x[1]]))
        if tag not in ('meta', 'link', 'input', 'br', 'img'):
            self.pilha.append((tag, a.get('id')))

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                del self.pilha[i:]
                break

    def handle_data(self, d):
        if not any(t in ('script', 'style', 'title') for t, _ in self.pilha):
            self.texto.append(d)


def textos_js(s):
    """os textos entre aspas simples de um ficheiro JS (o que pode aparecer na página)."""
    return re.findall(r"'((?:[^'\\\n]|\\.)*)'", s)


def lista_js(s, nome):
    m = re.search(r'var ' + nome + r' = (\[.*?\]);', s, re.S)
    return json.loads(m.group(1))


class PaginaDoDocente(unittest.TestCase):
    def setUp(self):
        self.s = ler(PAGINA)
        self.p = Pagina(self.s)

    def test_estrutura_e_sistema_visual_da_area_do_docente(self):
        s = self.s
        self.assertTrue(s.startswith('<!doctype html><html lang="pt-PT" data-appearance-site="lente">'))
        self.assertIn('<body class="atelier-document"><main class="atelier-page rt" data-rt>', s)
        for css in ('../../assets/atelier-pages.css', '../../assets/docente-hub.css', '../../assets/resultados-turma.css', '../../assets/appearance.css'):
            self.assertIn('href="' + css, s)
        self.assertEqual([x.split('?')[0] for x in self.p.scripts], ['../../assets/appearance.js', '../../assets/progresso-registos.js', '../../assets/resultados-turma.js'])
        self.assertNotIn('projection-launcher', s, 'a tabela da turma não vai para o projetor')
        self.assertIn('<nav class="atelier-breadcrumb" aria-label="Onde estás"><a href="../../">Lente</a>', s)
        self.assertIn('<a href="../">Para o docente</a>', s)
        self.assertIn('<span aria-current="page">Resultados da turma</span>', s)
        self.assertIn('<h1 class="teacher-hub-title">Resultados da turma<span aria-hidden="true">.</span></h1>', s)
        self.assertEqual(len(self.p.ids), len(set(self.p.ids)))
        for ref in self.p.refs:
            self.assertFalse(re.match(r'(?i)(https?:)?//', ref), 'só ficheiros locais: ' + ref)
            alvo = (R / PAGINA).parent / ref.split('?')[0].split('#')[0]
            if alvo.is_dir():
                alvo = alvo / 'index.html'
            self.assertTrue(alvo.exists(), ref)
        self.assertIn('href="../../caderno/#entregar"', s)
        self.assertIn('id="entregar"', ler('caderno/index.html'))

    def test_noindex_csp_e_linha_de_privacidade(self):
        metas = {m.get('name') or m.get('http-equiv'): m.get('content') for m in self.p.metas if m.get('content')}
        self.assertIn('noindex', metas['robots'])
        csp = metas['Content-Security-Policy']
        for regra in ("default-src 'self'", "script-src 'self'", "connect-src 'none'", "form-action 'none'", "object-src 'none'", "base-uri 'none'"):
            self.assertIn(regra, csp)
        self.assertNotIn('unsafe', csp)
        self.assertTrue(all(self.p.scripts), 'sem scripts inline (a CSP só deixa os ficheiros do sítio)')
        self.assertNotIn(' style="', self.s)
        # 28/10/2026: as regras dos códigos estão antes do primeiro passo (o docente dá os códigos antes de tudo)
        antes = self.s.index('<p class="rt-antes">')
        self.assertLess(antes, self.s.index('id="rt-t1"'))
        for t in ('letras e algarismos', 'de 2 a 12 caracteres', 'sem espaços nem acentos', 'E10-07', '10E-07'):
            self.assertIn(t, self.s[antes:self.s.index('</p>', antes)])
        self.assertIn('<p class="rt-privacidade">Os ficheiros leem-se só neste navegador: nada é enviado, nada fica guardado e, ao fechar a página, tudo desaparece.</p>', self.s)

    def test_zona_de_ficheiros_tabela_csv_limpar_e_estado(self):
        s = self.s
        self.assertRegex(s, r'<label class="rt-zona" data-rt-zona><input type="file" multiple accept="\.json,application/json" data-rt-input>')
        self.assertIn('<p class="rt-estado" data-rt-estado aria-live="polite"></p>', s)
        # 28/10/2026: a explicação da tabela fica fora do contentor que desliza, ligada por aria-describedby
        self.assertIn('role="region" aria-labelledby="rt-t2" aria-describedby="rt-tabela-d" tabindex="0" data-rt-tabela-c', s)
        self.assertIn('id="rt-tabela-d" data-rt-tabela-d hidden>Uma linha por código.', s)
        self.assertIn('>Descarregar a tabela (CSV)</button>', s)
        self.assertIn('>Limpar a tabela</button>', s)
        self.assertIn('data-rt-recusados', s)
        self.assertIn('data-rt-avisos', s)
        self.assertIn('data-rt-pormenor', s)
        css = ler(CSS_NOVO)
        self.assertIn('.rt-tabela-c{max-width:100%;overflow-x:auto', css, 'a tabela desliza dentro do seu contentor')
        self.assertIn('.rt-zona:focus-within{outline:3px solid var(--ink)', css)
        self.assertNotRegex(css, r'--(tinta|vermelho)\b', 'tokens da área do docente')
        self.assertNotIn('border-radius', css)
        self.assertNotIn('box-shadow', css)
        # 28/10/2026: a coluna Código fica fixa; os resumos do pormenor mostram «+» e «−»
        self.assertIn('.rt-tabela thead th:first-child,.rt-tabela tbody th{position:sticky;left:0;', css)
        self.assertIn('.rt-p>summary::before{content:"+"', css)
        self.assertIn('.rt-p[open]>summary::before{content:"\\2212"}', css)
        self.assertIn('Pede a estes alunos que voltem a fazer «Entregar ao docente» no caderno', s)

    def test_textos_que_nao_prometem_mais_do_que_ha(self):
        """28/10/2026: o nome, as provas e a data dizem o que o ficheiro de facto leva."""
        t = ' '.join(self.p.texto)
        self.assertNotIn('O nome do aluno não vem no ficheiro', t)
        self.assertIn('O ficheiro não leva o campo do nome', t)
        self.assertIn('As respostas escritas vão como o aluno as escreveu', t)
        self.assertIn('nos progressos antigos são retirados ao ler', t)
        self.assertIn('data no futuro', t)
        self.assertIn('as sessões 01 e 02 não têm registo: o total é 8', t)
        self.assertNotIn('a tabela soma-os', t)


class Escrita(unittest.TestCase):
    """pt-PT com AO90; «docente», nunca «professor»; nunca «jogar», «ficha» nem «folha»; sem «—» e sem «·» nas frases."""

    def textos(self):
        p = Pagina(ler(PAGINA))
        caderno = ler('caderno/index.html')
        secao = caderno[caderno.index('<section class="prog-f" id="entregar"'):caderno.index('</section>', caderno.index('id="entregar"'))]
        out = {PAGINA: ' '.join(p.texto), 'caderno #entregar': ' '.join(Pagina(secao).texto), DOC: ler(DOC)}
        for js in JS_NOVOS:
            out[js] = ' '.join(textos_js(ler(js)))
        return out

    def test_regras_de_escrita(self):
        for onde, t in self.textos().items():
            with self.subTest(onde=onde):
                self.assertNotRegex(t, r'(?i)\bprofessor', 'docente, nunca professor')
                self.assertNotRegex(t, r'(?i)\bjogar\b')
                self.assertNotRegex(t, r'(?i)\bfich(a|as)\b')
                self.assertNotRegex(t, r'(?i)\bfolhas?\b')
                self.assertNotIn('—', t)
                self.assertNotIn('·', t)
                for antigo in ('lêem', 'vêem', 'crêem', 'acção', 'acções', 'actual', 'direcção', 'colecção', 'óptim', 'objectiv', 'exacto', 'efectiv', 'selecção'):
                    self.assertNotIn(antigo, t.lower(), 'AO90: ' + antigo)

    def test_ficheiros_novos_sem_travessao_nem_ponto_medio(self):
        for f in JS_NOVOS + [CSS_NOVO, PAGINA, DOC]:
            s = ler(f)
            self.assertNotIn('—', s, f)
            if f != PAGINA:
                self.assertNotIn('·', s, f)
        # na página, só o <title> segue a convenção «Página · Lente» das outras páginas
        self.assertEqual(ler(PAGINA).count('·'), 1)

    def test_hub_sem_ficha_nem_folha_no_bloco_da_ligacao(self):
        """28/10/2026: o bloco 03 do hub, onde está a ligação nova, cumpre a regra «nunca ficha nem folha»."""
        s = ler('docente/index.html')
        bloco = s[s.index('<article id="tarefa-90">'):s.index('</article>', s.index('<article id="tarefa-90">'))]
        t = ' '.join(Pagina(bloco).texto)
        self.assertNotRegex(t, r'(?i)\bfich(a|as)\b')
        self.assertNotRegex(t, r'(?i)\bfolhas?\b')


class SemRede(unittest.TestCase):
    PROIBIDOS = ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'WebSocket', 'EventSource', 'new Image', 'importScripts', 'serviceWorker', 'navigator.share', 'http://', 'https://', '.src =', '.src=']
    HTML = ['innerHTML', 'outerHTML', 'insertAdjacentHTML', 'document.write', 'eval(', 'new Function', 'setAttribute(\'on']

    def test_nenhuma_chamada_de_rede_nem_html_vindo_de_ficheiros(self):
        for f in JS_NOVOS:
            s = ler(f)
            for x in self.PROIBIDOS + self.HTML:
                self.assertNotIn(x, s, f + ': ' + x)

    def test_a_pagina_do_docente_nao_guarda_nada(self):
        for f in ('assets/progresso-registos.js', 'assets/resultados-turma.js'):
            s = ler(f)
            for x in ('localStorage', 'sessionStorage', 'indexedDB', 'document.cookie', 'caches.'):
                self.assertNotIn(x, s, f + ': ' + x)
        # 28/10/2026: o caderno só lê o próprio aparelho; o código da entrega não se guarda (aparelhos partilhados)
        s = ler('assets/caderno-entrega.js')
        self.assertEqual(re.findall(r'\.(setItem|removeItem|clear)\(', s), [])
        self.assertNotIn(CHAVE, s)


class Hub(unittest.TestCase):
    def test_ligacao_em_acompanhar(self):
        p = Pagina(ler('docente/index.html'))
        ligacoes = [ids for href, ids in p.ancoras if href == 'resultados/']
        self.assertEqual(len(ligacoes), 1)
        self.assertEqual(ligacoes[0], ['tarefa-90'], 'filha direta de article#tarefa-90 (03 · ACOMPANHAR)')
        # 28/10/2026: com um subtítulo próprio dentro do bloco, e a seta presa à última palavra (espaço inseparável)
        self.assertIn('<h3>Entregas do caderno</h3><a href="resultados/">Resultados da turma: ler as entregas do caderno&nbsp;→</a></article>', ler('docente/index.html'))
        self.assertIn('.teacher-hub h3{', ler('assets/docente-hub.css'))
        self.assertTrue((R / PAGINA).is_file())


class Caderno(unittest.TestCase):
    def setUp(self):
        self.s = ler('caderno/index.html')

    def test_entregar_ao_docente_a_seguir_ao_progresso(self):
        s = self.s
        i, j = s.index('id="progresso"'), s.index('id="entregar"')
        self.assertLess(i, j)
        inicio = s.rindex('<section', 0, j)
        entre = s[s.index('</section>', i) + len('</section>'):inicio]
        self.assertRegex(entre, r'(?s)^<script>(?:(?!</script>).)*</script>$', 'entre as duas secções, só o script do progresso')
        sec = s[inicio:s.index('</section>', j)]
        self.assertIn('<h2 id="pe-t">Entregar ao docente</h2>', sec)
        self.assertIn('<label class="pe-l" for="pe-codigo">O teu código</label>', sec)
        self.assertIn('<p class="pf-n" id="pe-ajuda">Escreve o código que o docente te deu. Não escrevas o teu nome.</p>', sec)
        self.assertIn('aria-describedby="pe-ajuda pe-erro"', sec)
        self.assertRegex(sec, r'<input class="pe-i" id="pe-codigo" type="text"[^>]*autocomplete="off"')
        self.assertNotRegex(sec, r'<input[^>]*\bname=', 'sem name: nada viaja num envio de formulário')
        self.assertIn('<p class="pf-e" data-pe-estado aria-live="polite"></p>', sec)
        self.assertIn('id="pe-erro" data-pe-erro aria-live="polite"', sec)
        self.assertIn('<strong>Não vai o teu nome.</strong>', sec)
        self.assertIn('>Descarregar o ficheiro para entregar</button>', sec)
        self.assertIn('>Cancelar</button>', sec)
        a, b = s.index('../assets/progresso-registos.js'), s.index('../assets/caderno-entrega.js')
        self.assertLess(j, a)
        self.assertLess(a, b)

    def test_codigo_nunca_guardado_no_aparelho(self):
        # 28/10/2026: o código deixou de ser lembrado no aparelho (revisão: aparelhos partilhados); por isso o Guardar
        # volta a ser exatamente o publicado e nenhuma lista precisa da chave epi-codigo-entrega.
        self.assertIn('function chaves(){var L=[];for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k)L.push(k)}return L.sort()}', self.s)
        js = ler('assets/progresso-registos.js')
        self.assertNotIn(CHAVE, js)
        self.assertNotIn('CHAVE_CODIGO', js + ler('assets/caderno-entrega.js'))
        self.assertFalse(any(re.search(r, CHAVE, re.I) for r in lista_js(js, 'ACEITES')), 'não cabe na lista das chaves que viajam')

    def test_guardar_e_repor_ficam_iguais(self):
        def script(s):
            i = s.index('<section class="prog-f" id="progresso"')
            return s[s.index('<script>', i):s.index('</script>', i)]
        def secao(s):
            return s[s.index('<section class="prog-f" id="progresso"'):s.index('</section>', s.index('id="progresso"'))]
        sha = lambda t: hashlib.sha256(t.encode('utf-8')).hexdigest()
        self.assertEqual(sha(script(self.s)), SHA_SCRIPT_BASE, 'o script de Guardar e Repor fica igual ao publicado')
        # 28/10/2026: na secção, só a frase que mandava mostrar o «Guardar» ao docente muda; os botões ficam iguais
        sec = secao(self.s)
        self.assertEqual(sec.count(FRASE_AGORA), 1)
        self.assertEqual(sha(sec.replace(FRASE_AGORA, FRASE_ANTES)), SHA_SECAO_BASE, 'os botões e o resto do texto ficam iguais')

    def test_caderno_diz_onde_se_entrega_e_quem_envia(self):
        """28/10/2026: o caderno em papel abre-se na mesa; o progresso do sítio entrega-se por «Entregar ao docente», e é
        o aluno quem envia o ficheiro (o sítio não envia nada)."""
        s = self.s
        sec = s[s.index('<section class="prog-f" id="entregar"'):s.index('</section>', s.index('id="entregar"'))]
        self.assertIn('O caderno em papel continua a abrir-se na mesa (ver «Como se mostra»).', sec)
        self.assertIn('envia-lo ao docente pelo canal combinado na turma', sec)
        self.assertIn('O sítio não envia nada e não pede conta', sec)
        self.assertNotIn('sem enviar nada para a internet', sec)
        self.assertIn('.prog-f .pf-e.pe-feito{', s)


class Listas(unittest.TestCase):
    def test_chaves_de_cidadania_e_do_aparelho(self):
        js = ler('assets/progresso-registos.js')
        aceites = [re.compile(r, re.I) for r in lista_js(js, 'ACEITES')]
        aparelho = [re.compile(r, re.I) for r in lista_js(js, 'IGNORADAS_APARELHO')]
        bate = lambda L, k: any(r.search(k) for r in L)
        for k in ('lente-cidadania-m1-sessoes-v2', 'lente-cidadania-m1-v2', 'lente-cidadania-m2-sessoes-v1'):
            self.assertTrue(bate(aceites, k), k)
        # 28/10/2026: epi-som e epi-cartaz são preferências do aparelho (som, cartaz que já rodou): não viajam
        for k in ('epi-theme', 'pt-relogio:tarefas/m1-u1:aquecimento', 'epi-som', 'epi-cartaz'):
            self.assertTrue(bate(aparelho, k), k)
            self.assertFalse(bate(aceites, k), k)
        # as chaves que as páginas de Cidadania escrevem hoje
        self.assertIn("KEY='lente-cidadania-m1-sessoes-v2'", ler('assets/cidadania-m1-sessoes.js'))
        self.assertIn("KEY='lente-cidadania-m1-v2'", ler('assets/cidadania-m1.js'))
        self.assertIn('data-chave="lente-cidadania-m2-sessoes-v1"', ler('cidadania/m2/sessoes/01/index.html'))
        self.assertEqual(lista_js(js, 'PRIVADAS'), ['^cd\\d?-nome$', '^terra-firme-'])

    def test_totais_embutidos_conferem_com_as_pastas(self):
        js = ler('assets/resultados-turma.js')
        apoios = sorted(p.name for p in (R / 'cidadania/m1/fichas').iterdir() if re.fullmatch(r'f\d\d', p.name))
        self.assertIn('var APOIOS_M1 = %d;' % len(apoios), js)
        self.assertIn("'{n} de ' + APOIOS_M1 + ' apoios do M1", js)
        for m, de, ate in (('m1', 3, 10), ('m2', 1, 10)):
            pastas = sorted(int(p.parent.name) for p in (R / 'cidadania' / m / 'sessoes').glob('[0-9][0-9]/index.html') if 'data-session-done' in p.read_text('utf-8'))
            self.assertEqual(pastas, list(range(de, ate + 1)), m)
            self.assertIn("'%s': {de: %d, ate: %d}" % (m[1], de, ate), js)
            # 28/10/2026: «com registo», e no M1 diz que o total começa na sessão 03
            self.assertIn("'%s: {n} de %d sessões com registo%s'" % (m.upper(), ate - de + 1, ' (da %02d à %02d)' % (de, ate) if de > 1 else ''), js)


class Documento(unittest.TestCase):
    def test_nota_pedagogica(self):
        s = ler(DOC)
        for t in ('# Resultados da turma', 'código', 'pseudónimo', 'não para avaliar', 'docente/resultados/', 'tests/test_resultados_turma.py', 'tests/browser_resultados_turma.cjs', 'tests/resultados_turma.test.cjs'):
            self.assertIn(t, s)


if __name__ == '__main__':
    unittest.main()
