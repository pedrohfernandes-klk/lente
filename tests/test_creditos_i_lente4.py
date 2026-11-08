"""08/11/2026: decisões 153 e 176 (pedido lente-4 do plano plano-creditos-i-20261105.md, secção 1, a peça «i»). Confere-se contra
o main de partida (e0c55de):

- a camada (tools/trocas/creditos-i-lente4-20261108.json) é fechada e reversível, como a do pedido lente-3, e a do lente-3 continua
  certa por baixo dela;
- na peça comum (assets/info-i.css) só muda a regra da projeção: o «i» aberto e o do canto guardam o fundo e o halo, só o «i»
  «linha» fechado os perde, e o foco leva um anel na cor da tinta e outro na cor do papel por dentro do alvo; fora da projeção, nada
  muda (o resto da folha é igual, letra a letra);
- em «Ler a cidade» (cidade/index.html), os dez créditos das missões (span.cr, a 11 px, dentro da ligação de cada cartão) estão
  inteiros dentro do «i», com as mesmas palavras, a ligação para a fonte (data-external e aria-label, como no pedido lente-1) e a da
  licença (rel="license"), as mesmas que o pedido lente-3 já pôs no «i» da mesma imagem; não fica span.cr nenhum; o «i» vive fora da
  ligação, num div.missao-i com o cartão; os quatro cartões sem crédito não mudam;
- a gaveta de cada lugar copia o cartão com o seu «i», fechado, e o filtro das portas esconde o conjunto; o Escape fecha primeiro o
  «i» e depois a gaveta (como no pedido lente-3);
- nada do que entrou traz «·», «—», «professor», «jogo», «jogar», «ficha» nem «folha», e o título da obra vai em itálico;
- o CI corre a verificação da camada e o teste de navegador novo."""
import json
import re
import subprocess
import sys
import unittest
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools'))
import creditos_i  # noqa: E402
import creditos_i_lente3  # noqa: E402
import creditos_i_lente4  # noqa: E402

BASE = 'e0c55dec56c9926c89da4382b519b7a4123f3f90'
MANIFESTO = 'tools/trocas/creditos-i-lente4-20261108.json'
PROJ = ':is(.em-projecao,.epi-projection,[data-cz-projection]) '
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a[sm]?|o|os|ou|uei|ámos)|fichas?|folhas?)(?![\wÀ-ÿ])|—|·', re.I)
CARTAO = re.compile(r'<a class="missao p-cartao" href="(m\d\d)/"[^>]*>.*?</a>', re.S)
COM_I = re.compile(r'<div class="missao-i com-i">(<a class="missao p-cartao" href="(m\d\d)/"[^>]*>.*?</a>)'
                   r'<details class="info-i" name="info-i"><summary aria-label="([^"]+)"><span aria-hidden="true">i</span></summary>'
                   r'<p class="info-i-texto">(.*?)</p></details></div>', re.S)


def ler(f):
    return (R / f).read_text('utf-8')


def antigo(f):
    return subprocess.check_output(['git', 'show', f'{BASE}:{f}'], cwd=R).decode('utf-8')


def texto(h):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', h))).strip()


def ligacoes(h):
    return re.findall(r'<a ([^>]*)>(.*?)</a>', h)


def attrs(s):
    return dict((k, v if v is not None else '') for k, v in re.findall(r'([\w-]+)(?:="([^"]*)")?', s))


class Ancestrais(HTMLParser):
    """Onde vive cada details.info-i: as etiquetas abertas por cima dele."""
    VAZIAS = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'wbr', 'col', 'area'}

    def __init__(self):
        super().__init__()
        self.pilha, self.achados = [], []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == 'details' and 'info-i' in (a.get('class') or '').split():
            self.achados.append(list(self.pilha))
        if tag not in self.VAZIAS:
            self.pilha.append((tag, a))

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                del self.pilha[i:]
                break


def regras(css):
    """As regras de topo de uma folha (sem comentários): [(seletores, corpo)]; as @media contam como uma regra."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, i, n = [], 0, len(css)
    while i < n:
        a = css.find('{', i)
        if a < 0:
            break
        sel, d, j = css[i:a].strip(), 1, a + 1
        while d:
            d += {'{': 1, '}': -1}.get(css[j], 0)
            j += 1
        out.append((sel, css[a + 1:j - 1]))
        i = j
    return out


class CreditosLente4(unittest.TestCase):
    def test_camada_fechada_e_reversivel(self):
        # tools/creditos_i.py --verificar, com o manifesto deste pedido e com o do pedido lente-3 (por omissão): as duas camadas
        # estão aplicadas, com as contagens exatas, e voltam atrás sem perdas; a do lente-4 não toca em nenhum «novo» do lente-3.
        for args in (['--manifesto', str(R / MANIFESTO)], []):
            r = subprocess.run([sys.executable, str(R / 'tools/creditos_i.py'), '--verificar'] + args, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(sorted(creditos_i_lente4.TROCAS), ['assets/info-i.css', 'cidade/index.html'])
        for f in creditos_i_lente4.TROCAS:
            with self.subTest(ficheiro=f):
                agora = ler(f)
                partida = creditos_i_lente4.desfazer(agora, f)
                self.assertEqual(partida, antigo(f))
                self.assertEqual(creditos_i_lente4.aplicar(partida, f), agora)
                self.assertEqual(creditos_i_lente4.alinhar(agora, f), agora)
                self.assertEqual(creditos_i_lente4.alinhar(partida, f), agora)
                for _, novo3, _ in creditos_i_lente3.TROCAS.get(f, []):
                    for antigo4, _, _ in creditos_i_lente4.TROCAS[f]:
                        self.assertNotIn(antigo4, novo3)
                        self.assertNotIn(novo3, antigo4)

    def test_peca_so_muda_na_projecao(self):
        # A peça comum muda numa só troca: a regra da projeção. Tudo o que entra está debaixo do seletor da projeção (fora dela, a
        # folha é a mesma, letra a letra: ver test_camada_fechada_e_reversivel).
        (velha, nova, n), = creditos_i_lente4.TROCAS['assets/info-i.css']
        self.assertEqual(n, 1)
        self.assertEqual(regras(velha), [(PROJ + '.info-i>summary>span',
                                          'background:transparent;border-width:1px;box-shadow:none;inline-size:32px;block-size:32px;font-size:1.25rem')])
        rs = regras(nova)
        self.assertEqual(len(rs), 3)
        for sel, _ in rs:
            self.assertTrue(sel.startswith(PROJ), sel)
            self.assertNotIn(',', sel[len(PROJ):], sel)
        corpo = dict(rs)
        # o círculo: o tamanho e a borda da projeção ficam; o fundo e o halo da regra de base também (o aberto fica cheio, na cor da
        # tinta, e o do canto guarda o papel e o halo sobre a fotografia)
        self.assertEqual(corpo[PROJ + '.info-i>summary>span'], 'border-width:1px;inline-size:32px;block-size:32px;font-size:1.25rem')
        # só o «i» «linha» fechado, sobre o papel da página, fica sem fundo nem halo
        self.assertEqual(corpo[PROJ + '.info-i--linha:not([open])>summary>span'], 'background:transparent;box-shadow:none')
        # o foco: um anel na cor da tinta e outro na cor do papel, por dentro do alvo de 44 px, colados ao contorno
        self.assertEqual(corpo[PROJ + '.info-i>summary:focus-visible'],
                         'outline-offset:0;box-shadow:inset 0 0 0 2px var(--ii-papel),inset 0 0 0 4px var(--ii-tinta)')
        css = ler('assets/info-i.css')
        self.assertNotIn('background:transparent;border-width:1px;box-shadow:none', css)
        # a regra de base do «i» aberto continua a encher o círculo e a do canto a pôr o halo
        self.assertIn('.info-i[open]>summary>span{background:var(--ii-tinta);color:var(--ii-papel)}', css)
        self.assertIn('box-shadow:0 0 0 2px var(--ii-papel)', css)
        self.assertIn('/* 08/11/2026: decisões 153 e 176 (pedido lente-4).', nova)

    def test_dez_creditos_no_i(self):
        velho, s = antigo('cidade/index.html'), ler('cidade/index.html')
        crs = re.findall(r'<a class="missao p-cartao" href="(m\d\d)/"[^>]*>(?:(?!</a>).)*?<span class="cr">([^<]*)</span></a>', velho)
        self.assertEqual(len(crs), 10)
        self.assertNotIn('class="cr"', s)
        self.assertNotIn('.missao .cr{', s)
        cartoes_velhos = {m.group(1): m.group(0) for m in CARTAO.finditer(velho)}
        self.assertEqual(len(cartoes_velhos), 14)
        self.assertEqual(len(CARTAO.findall(s)), 14)
        com_i = {m.group(2): m for m in COM_I.finditer(s)}
        self.assertEqual(sorted(com_i), sorted(mid for mid, _ in crs))
        self.assertEqual(s.count('<div class="missao-i com-i">'), 10)
        self.assertEqual(s.count('</a><details class="info-i" name="info-i"><summary aria-label="Créditos da '), 10)
        # os créditos que o pedido lente-3 já pôs no «i» das mesmas imagens (gaveta e páginas das missões): daí vêm as ligações
        conhecidos = {}
        for f in ['cidade/index.html'] + sorted(p.relative_to(R).as_posix() for p in (R / 'cidade').glob('m*/index.html')):
            t = ler(f).replace('\\"', '"').replace('<\\/', '</')
            for fig in re.findall(r'<figure\b.*?</figure>', t, re.S):
                im, cr = re.search(r'<img src="[^"]*/([\w-]+\.jpg)"', fig), re.search(r'<p class="info-i-texto">(.*?)</p>', fig)
                if im and cr:
                    conhecidos.setdefault(im.group(1), set()).update(h for _, h in re.findall(r'<a ([^>]*)href="([^"]+)"', cr.group(1)))
        for mid, cr in crs:
            with self.subTest(missao=mid):
                m = com_i[mid]
                cartao, rotulo, cred = m.group(1), m.group(3), m.group(4)
                # o cartão fica igual, sem o span.cr; o «i» vem logo a seguir, fora da ligação
                self.assertEqual(cartao, cartoes_velhos[mid].replace(f'<span class="cr">{cr}</span></a>', '</a>'))
                self.assertNotIn('info-i', cartao)
                numero = re.search(r'<span class="r">Missão (\d\d)', cartao).group(1)
                self.assertEqual(numero, mid[1:])
                tipo = 'gravura' if cr.startswith('Gravura:') else 'fotografia'
                self.assertEqual(rotulo, f'Créditos da {tipo}: Missão {numero}')
                # o mesmo texto, letra a letra (autor, obra, data, licença e fonte, conforme o crédito de antes)
                self.assertEqual(texto(cred), cr)
                img = re.search(r'<img src="[^"]*/([\w-]+\.jpg)"', cartao).group(1)
                for a, txt in ligacoes(cred):
                    at = attrs(a)
                    if 'creativecommons.org' in at['href']:
                        self.assertEqual(at.get('rel'), 'license')
                        self.assertRegex(txt, r'^CC BY(-SA)? \d\.\d$')
                        self.assertIn(txt, cr)
                    else:
                        self.assertIn('data-external', at)
                        self.assertEqual(at.get('aria-label'), txt + ', sítio externo')
                        self.assertTrue(at['href'].startswith('https://'))
                    # nada inventado: cada ligação já estava no «i» da mesma imagem, noutro sítio de «Ler a cidade»
                    self.assertIn(at['href'], conhecidos.get(img, set()), (img, at['href']))
                for lic in re.findall(r'CC BY(?:-SA)? \d\.\d', cr):
                    self.assertIn(f'">{lic}</a>', cred)
                if mid != 'm16':  # o Arquivo da EPI não tem página de fonte externa
                    self.assertTrue(any('data-external' in a for a, _ in ligacoes(cred)), mid)
        # os quatro cartões sem crédito não mudam
        for mid in set(cartoes_velhos) - set(com_i):
            self.assertIn(cartoes_velhos[mid], s)
            self.assertNotIn(f'<div class="missao-i com-i">{cartoes_velhos[mid]}', s)
        self.assertIn('para <i>Alice no País das Maravilhas</i>, de Lewis Carroll.', com_i['m08'].group(4))

    def test_i_fora_da_ligacao(self):
        p = Ancestrais()
        p.feed(ler('cidade/index.html'))
        self.assertEqual(len(p.achados), 11)  # o da fotografia nas letras (pedido lente-1) e os dez das missões
        missoes = [pilha for pilha in p.achados if pilha and 'missao-i' in (pilha[-1][1].get('class') or '').split()]
        self.assertEqual(len(missoes), 10)
        for pilha in p.achados:
            for tag, a in pilha:
                self.assertNotIn(tag, ('a', 'button', 'label', 'figcaption', 'summary'))
                self.assertNotEqual(a.get('aria-hidden'), 'true')
        for pilha in missoes:
            self.assertEqual(pilha[-1][0], 'div')
            self.assertEqual(pilha[-2][1].get('class'), 'missoes')

    def test_gaveta_e_filtro(self):
        s = ler('cidade/index.html')
        # a gaveta copia o cartão com o seu «i», fechado
        self.assertIn('if(a&&!a.hidden){var k=(a.closest(".missao-i")||a).cloneNode(true);$$("details[open]",k).forEach(function(x)'
                      '{x.removeAttribute("open")});cx.appendChild(k)}', s)
        self.assertNotIn('cx.appendChild(a.cloneNode(true))', s)
        # o filtro das portas e das áreas esconde o cartão e o seu «i»
        self.assertIn('var c=a.closest(".missao-i");a.hidden=!((p==="todas"||a.dataset.porta===p)&&(ar==="todas"||a.dataset.area===ar));'
                      'if(c)c.hidden=a.hidden', s)
        self.assertIn('.missao-i[hidden]{display:none}', s)
        # com um «i» aberto, o Escape fecha só o «i»; o seguinte fecha a gaveta (pedido lente-3)
        self.assertIn('if(ev.key==="Escape"&&aberto&&!document.querySelector("details.info-i[open]"))fecha()', s)
        # a página continua a carregar a peça comum uma vez
        self.assertEqual(s.count('<link rel="stylesheet" href="../assets/info-i.css?v=20261106-3">'), 1)
        self.assertEqual(s.count('<script defer src="../assets/info-i.js?v=20261106-3"></script>'), 1)
        # o estilo do cartão com «i»: o «i» numa faixa só sua, no fundo do cartão, só no ecrã (na impressão, o crédito sai por baixo)
        self.assertIn('.missao-i{display:grid;margin:0 0 var(--d1)}', s)
        self.assertIn('@media screen{.missao-i>.missao{padding-bottom:50px}.missao-i>.info-i>summary{inset-block-end:6px}}', s)

    def test_texto_do_que_entrou(self):
        # o que entrou: nos cartões, o nome do «i» e o crédito (o resto do cartão já lá estava); nas outras trocas, tudo
        entrou = []
        for trocas in creditos_i_lente4.MANIFESTO.values():
            for _, novo, _ in trocas:
                m = COM_I.fullmatch(novo)
                entrou += [m.group(3), m.group(4)] if m else [novo]
        self.assertEqual(len(entrou), 2 * 10 + 4)
        for t in entrou:
            self.assertIsNone(PROIBIDAS.search(texto(t)), texto(t)[:120])

    def test_workflow(self):
        wf = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn('- run: python tools/creditos_i.py --verificar --manifesto ' + MANIFESTO, wf)
        self.assertIn('- run: python tools/creditos_i.py --verificar\n', wf)
        self.assertIn('- run: node tests/browser_creditos_i_lente4.cjs', wf)
        for linha in re.findall(r"paths: \[(.*?)\]", wf):
            self.assertIn("'" + MANIFESTO + "'", linha)
            self.assertIn("'cidade/**'", linha)
            self.assertIn("'assets/info-i.*'", linha)
            self.assertIn("'tests/*creditos_i*'", linha)
        self.assertLess(wf.index('node tests/browser_creditos_i_lente3.cjs'), wf.index('node tests/browser_creditos_i_lente4.cjs'))
        self.assertTrue(json.loads(ler(MANIFESTO)))


if __name__ == '__main__':
    unittest.main()
