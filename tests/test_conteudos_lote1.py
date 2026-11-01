"""01/11/2026: lote de conteúdos sem mudar chaves, ligações ou Cidadania."""
import json
import re
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from aplicar_conteudos import aplicar
from medir_opcoes import escolha


class Conteudos(unittest.TestCase):
    def test_trocas_aplicadas_e_ambito(self):
        aplicar(verificar=True)
        es=json.loads((ROOT/'tools/trocas/conteudos-lote1-20261101.json').read_text('utf-8'))
        self.assertEqual({e['ficheiro'] for e in es},{'narrativas/piramide/index.html','narrativas/oficina-ficcao-comecar/index.html','olhar-e-decidir/justica/licao-1/index.html'})
        links={}
        for e in es:
            before,after=json.loads(e['antigo']),json.loads(e['novo'])
            if after['t']=='escolha':
                m=escolha(after['o'],after['c'])
                self.assertIsNotNone(m)
                lengths=[len(s) for s in after['o']]
                self.assertLessEqual(max(lengths),1.2*min(lengths))
                self.assertEqual(len(after['fe']),len(after['o']))
                self.assertTrue(all(x for i,x in enumerate(after['fe']) if i!=after['c']))
            # Os materiais literários e as suas fontes continuam presentes.
            oldlinks=re.findall(r'href="([^"]+)"',before.get('html','')+before.get('ver',''))
            newlinks=re.findall(r'href="([^"]+)"',after.get('html','')+after.get('ver',''))
            bucket=links.setdefault(e['ficheiro'],[[],[]]);bucket[0].extend(oldlinks);bucket[1].extend(newlinks)
        for oldlinks,newlinks in links.values():
            self.assertEqual(sorted(oldlinks),sorted(newlinks))

    def test_piramide_variedade_e_limite(self):
        s=(ROOT/'narrativas/piramide/index.html').read_text('utf-8')
        cards=json.JSONDecoder().raw_decode(s.split('itens:',1)[1])[0]
        self.assertEqual(len(cards),11)
        for a,b,c in zip(cards,cards[1:],cards[2:]):
            self.assertFalse(a['t']==b['t']==c['t'])
        self.assertEqual(cards[6]['t'],'sublinhar')
        self.assertIn('não torna merecido',cards[6]['f'])
        self.assertIn('não uma regra',cards[10]['html'])
        self.assertIn('Kafka',cards[10]['html'])


if __name__=='__main__':unittest.main()
