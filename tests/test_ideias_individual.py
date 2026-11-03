"""02/11/2026: L104-01, decisão 138. Autoria individual com verificação independente."""
from pathlib import Path
import importlib.util,json,re,subprocess,unittest
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ideias',R/'tools/ideias_piloto.py')
I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
class ModalidadeIndividual(unittest.TestCase):
    def test_sessao_um_individual_e_verificavel(self):
        d=json.loads((R/'tools/licoes/ideias-s01.json').read_text('utf-8'))
        aula=next(c['html'] for c in d['cartoes'] if c.get('rot')=='Na aula')
        for text in ['Com o docente','Regista dez factos','três inferências e uma pergunta','Verifica individualmente','factos de um colega','O teu auto de observação','outra pessoa confere os degraus']:
            self.assertIn(text,aula)
        self.assertNotRegex(aula,r'(?i)grupos?')
        self.assertEqual(I.SESSOES[0]['papel'],'o teu auto de observação.')
    def test_guiao_e_guia_concordam(self):
        guia=I.GUIA[1]
        self.assertEqual(guia['produto'],'o auto de observação, individual')
        # 02/11/2026: grelha /20 substituída por três critérios iguais no cartão, guia e guião.
        self.assertNotIn('grelha', guia)
        self.assertEqual(len(I.M.CRITERIOS[1]), 3)
        for n in (1,2):
            criterios = I.esta_bom(n)
            for rel in ('guiao/index.html','docente/index.html'):
                self.assertIn(I.LL.nq(criterios),(R/'narrativas/ideias'/rel).read_text('utf-8'))
            d=json.loads((R/f'tools/licoes/ideias-s{n:02d}.json').read_text('utf-8'))
            aula=next(c['html'] for c in d['cartoes'] if c.get('rot')=='Na aula')
            self.assertIn(I.LL.nq(criterios),aula)
            self.assertIn('Para a tua caixa',d['cartoes'][-1]['html'])
        self.assertNotRegex(json.dumps([guia,I.GUIAO[1]],ensure_ascii=False),r'(?i)\bgrupos?\b')
        guiao=(R/'narrativas/ideias/guiao/index.html').read_text('utf-8')
        self.assertIn('Nome: <i class="b"></i>',guiao)
        self.assertIn('Verificado por',guiao)
        self.assertIn('Facto (um que outra pessoa possa confirmar)',guiao)
    def test_sessao_dois_preserva_seguranca(self):
        d=json.loads((R/'tools/licoes/ideias-s02.json').read_text('utf-8'))
        aula=next(c['html'] for c in d['cartoes'] if c.get('rot')=='Na aula')
        self.assertIn('com o docente',aula)
        self.assertIn('aos pares por segurança',aula)
        self.assertIn('Trabalhas individualmente',aula)
        self.assertIn('aos pares por segurança',I.GUIA[2]['antes'])
    def test_cartoes_respostas_versoes_e_chaves_conservados(self):
        # 02/11/2026: base anterior ao pedido; a modalidade não reinicia o trabalho guardado.
        base='57e92c7517f69d3d7773ba74de8375e63ac5dfc2'
        for n in [1,2]:
            rel=f'tools/licoes/ideias-s{n:02d}.json'
            old=json.loads(subprocess.check_output(['git','show',base+':'+rel],cwd=R))
            now=json.loads((R/rel).read_text('utf-8'))
            for key in ['chave','versao','saida','titulo']:self.assertEqual(old[key],now[key])
            self.assertEqual(len(old['cartoes']),len(now['cartoes']))
            for a,b in zip(old['cartoes'],now['cartoes']):
                for key in ['t','g','rot','c','v','certas','pares','passos','lacunas']:
                    self.assertEqual(a.get(key),b.get(key),(n,key))
                if 'c' in a:self.assertEqual(a['o'][a['c']],b['o'][b['c']])
