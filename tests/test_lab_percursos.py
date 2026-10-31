"""30/10/2026: cobertura da reorganização, sem confundir catálogos com peças."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,unittest,subprocess,sys
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'assets/laboratorio/percursos.json').read_text('utf-8'))
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v:self.links.append(v)
class Percursos(unittest.TestCase):
 def test_inventario_completo_sem_duplicados(self):
  ids=[p['id'] for p in D['pieces']];assigned=[id for r in D['routes'] for id in r['pieces']]
  self.assertEqual(len(ids),93);self.assertEqual(len(set(ids)),len(ids));self.assertCountEqual(ids,assigned)
  for r in D['routes']:self.assertTrue(4<=len(r['pieces'])<=8,r['id'])
  support={'','tudo','ver','treinar','criar','percursos','corta','margens','fora-da-pagina','treinar/caderno','treinar/docente'}
  actual={p.parent.relative_to(R/'narrativas').as_posix().replace('.','') for p in (R/'narrativas').rglob('index.html') if '-imprimir' not in str(p) and 'percursos' not in p.parts}
  self.assertEqual(actual-set(ids),support-{'percursos'})
 def test_paginas_geradas_e_ligacoes(self):
  pages=[R/'narrativas/index.html',R/'narrativas/tudo/index.html']+[R/'narrativas'/b['id']/'index.html' for b in D['blocks']]+list((R/'narrativas/percursos').rglob('index.html'))
  before={p:p.read_bytes() for p in pages};subprocess.run([sys.executable,str(R/'tools/laboratorio.py')],check=True,capture_output=True)
  for p in pages:
   self.assertEqual(before[p],p.read_bytes(),p)
   l=Links();l.feed(p.read_text('utf-8'))
   for url in l.links:
    u=urlsplit(url)
    if u.scheme or u.netloc or not u.path:continue
    target=(p.parent/unquote(u.path)).resolve()
    if target.is_dir():target=target/'index.html'
    self.assertTrue(target.is_file(),(p,url))
    self.assertNotIn(target.relative_to(R).parts[0],('gigantes','sidequests','vozes'))
 def test_estados_assentam_em_chaves_reais(self):
  for p in D['pieces']:
   q=p['progress'];s=(R/p['url']/'index.html').read_text('utf-8')
   if q['kind']=='feitas' and not p['id'].startswith('fora-da-pagina/'):
    self.assertIn('var K="'+q['key']+'"',s);self.assertIn('S.feitas["'+q['id']+'"]',s)
   elif q['kind']=='manual':self.assertIn('data-registo="'+p['id']+'"',s)
  for p in D['pieces']:self.assertTrue(p['incoming'] or p['id']=='formas/tres-cartas',p['id'])
 def test_imagens_sem_ia(self):
  for p in list((R/'narrativas').rglob('*.html'))+list((R/'assets/formas').glob('*.js')):
   self.assertNotIn('assistência de IA',p.read_text('utf-8'),p)
  for rel in ['carteira-linha.png','carteira/perda.webp','carteira/bolso.svg','baralho/11-01.webp','baralho/13-02.webp','baralho/20-03.webp']:
   self.assertFalse((R/'assets/formas'/rel).exists())
  ims=json.loads((R/'assets/laboratorio/imagens.json').read_text('utf-8'))
  self.assertEqual(len(ims),3)
  for im in ims:
   self.assertTrue((R/im['file']).is_file());self.assertGreater(len(im['alt']),25);self.assertIn(im['license'],['Domínio público','CC0','CC BY','CC BY-SA']);self.assertTrue(im['source'].startswith('https://commons.wikimedia.org/wiki/File:'))
if __name__=='__main__':unittest.main()
