from pathlib import Path
import json,re,unittest,struct
R=Path(__file__).resolve().parents[1]
def data():return json.loads((R/'assets/formas/tres-cartas-dados.js').read_text('utf-8').split('=',1)[1].rstrip(';\n'))
class TresCartas(unittest.TestCase):
 def test_assets_and_isolation(self):
  s=(R/'narrativas/formas/tres-cartas/index.html').read_text('utf-8')
  self.assertIn('content="noindex"',s);self.assertNotIn('/cartoes.js',s)
  for dep in re.findall(r'(?:src|href)="([^"?#]+)',s):
   if dep.startswith(('http','?')):continue
   self.assertTrue((R/'narrativas/formas/tres-cartas'/dep).exists(),dep)
  # 30/10/2026: o protótipo fica fora do percurso até ter imagens reais ou desenho próprio (decisão 34)
  self.assertNotIn('tres-cartas',(R/'narrativas/index.html').read_text('utf-8'))
  for rel in ['narrativas/tudo/index.html','narrativas/criar/index.html','narrativas/percursos/experimentar/index.html']:
   self.assertNotIn('tres-cartas',(R/rel).read_text('utf-8'),rel)
 def test_curated_crops(self):
  # 30/10/2026: metadados das pranchas de IA retirados; ficam as três situações descritas, com os mesmos ids.
  d=data();self.assertFalse((R/'assets/formas/baralho/origem.json').exists())
  self.assertEqual({im['id'] for im in d['imagens']},{'11-01','13-02','20-03'})
  for im in d['imagens']:
   self.assertGreater(len(im['alt']),35)
   # 30/10/2026: descrições das três situações substituem os recortes de IA.
   self.assertFalse((R/('assets/formas/baralho/'+im['id']+'.webp')).exists())
  self.assertIn('CC BY-SA 4.0',d['credito'])
  self.assertNotIn('assistência de IA',d['credito'])
 def test_plano_em_blocos(self):
  for c in data()['cartoes']:
   if c['tipo']!='composicao':continue
   self.assertEqual(list(dict.fromkeys(p['bloco'] for p in c['partes'])),['O conto','A notícia'])
   for p in c['partes']:
    self.assertEqual(p['conector'],'')
    if p['fonte']=='conector':self.assertEqual(p['se'],{'fonte':'ligacao','valor':'a'})
    if p['fonte']=='ordem':self.assertEqual(p['sequencia'],['Primeiro','depois','por fim'])
 def test_course_and_language(self):
  d=data();cs=d['cartoes'];first=next(i for i,c in enumerate(cs) if c['tipo']=='escrita')
  self.assertGreaterEqual(sum(c['tipo'] in ['escolher','ordenar','completar','classificar'] for c in cs[:first]),10)
  self.assertLess(max(i for i,c in enumerate(cs) if c['tipo']=='autoavaliacao'),min(i for i,c in enumerate(cs) if c['tipo']=='exemplo'))
  for c in cs:
   self.assertLessEqual(len(c['pergunta'].split()),25,c['id']);self.assertLessEqual(len(c.get('apoio','').split()),40,c['id'])
   for o in c.get('opcoes',[]):self.assertLessEqual(len(re.findall(r'[.!?](?: |$)',o['feedback'])),2)
  text=json.dumps(d,ensure_ascii=False)
  self.assertIsNone(re.search(r'\b(professor|ficha|folha|jogar)\b|[·—]',text,re.I))
  for c in cs:
   if c['tipo']=='composicao':
    for p in c['partes']:self.assertIn(p['fonte'],[x['id'] for x in cs])
if __name__=='__main__':unittest.main()
