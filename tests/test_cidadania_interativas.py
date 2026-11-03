"""Integração real: quatro bancos, 80 cartões, sem reaplicar respostas antigas."""
from pathlib import Path
import json, hashlib, sys, unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import cidadania_interativas as G

class Interativas(unittest.TestCase):
 def test_bancos_paginas_e_ordem(self):
  dados=G.bancos();self.assertEqual(len(dados),4)
  for d in dados:
   self.assertEqual(G.L.validar(d),[])
   self.assertFalse(d['piloto']);self.assertFalse(d['modelo'])
   self.assertEqual(len(d['cartoes']),20)
   self.assertEqual(len([x for x in d['cartoes'] if x['t']!='ler']),14)
   self.assertEqual(len({x['g'] for x in d['cartoes']}),20)
   s=(ROOT/d['saida']).read_text('utf-8');self.assertEqual(s,G.L.pagina(d))
   self.assertIn('"chave": "'+d['chave']+'-20261103"',s)
   self.assertNotIn('noindex',s);self.assertNotIn('ensaio-',s)
 def test_mapa_nao_migra(self):
  mapa=json.loads((ROOT/'docs/qa/cidadania-m1-migracao-20261103.json').read_text('utf-8'))
  self.assertEqual(len(mapa['sessoes']),4)
  for d,m in zip(G.bancos(),mapa['sessoes']):
   antigo=json.loads((ROOT/m['original_main']).read_text('utf-8'))
   self.assertEqual(hashlib.sha256(json.dumps(antigo,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),m['sha256_main_json'])
   self.assertNotEqual(m['chave_anterior'],m['chave_atual'])
   self.assertEqual(len(m['cartoes']),20)
   for c,x in zip(d['cartoes'],m['cartoes']):
    self.assertEqual(x['acao'],'não migrar respostas')
    self.assertEqual(x['id'],c['id'])
    self.assertEqual(x['sha256_cartao'],hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode()).hexdigest())
 def test_indice_e_guias_reproduziveis(self):
  s=(ROOT/'cidadania/m1/index.html').read_text('utf-8');self.assertEqual(G.instalar_indice(s),s)
  for n in range(1,5):self.assertIn('href="licoes/'+f'{n:02}'+'/"',s)
  for n in range(5,11):self.assertIn('href="sessoes/'+f'{n:02}'+'/"',s)
  for flag,pasta in [(True,'docente'),(False,'guiao')]:self.assertEqual((ROOT/'cidadania/m1/licoes'/pasta/'index.html').read_text('utf-8'),G.pagina_guia(flag))
 def test_indice_nao_escreve(self):
  s=(ROOT/'assets/cidadania-interativas-indice.js').read_text('utf-8')
  self.assertNotRegex(s,r'localStorage\.(setItem|removeItem|clear)')
  self.assertIn('if(proj)return {}',s)

if __name__=='__main__':unittest.main()
