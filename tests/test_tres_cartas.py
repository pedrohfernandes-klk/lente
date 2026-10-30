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
  self.assertNotIn('tres-cartas',(R/'narrativas/index.html').read_text('utf-8'))
 def test_curated_crops(self):
  d=data();origin=json.loads((R/'assets/formas/baralho/origem.json').read_text('utf-8'))
  self.assertEqual({c['id'] for c in origin['cards']},{'11-01','13-02','20-03'})
  for c in origin['cards']:self.assertTrue(c['kept'])
  for im in d['imagens']:
   self.assertGreater(len(im['alt']),35)
   b=(R/('assets/formas/baralho/'+im['id']+'.webp')).read_bytes()
   self.assertEqual(b[:4],b'RIFF');self.assertEqual(b[12:16],b'VP8L')
   n=int.from_bytes(b[21:25],'little');self.assertEqual(((n&0x3fff)+1,((n>>14)&0x3fff)+1),(512,512))
  self.assertEqual(d['credito'],'Baralho improvável, obra do Lente feita com assistência de IA, CC BY-SA 4.0')
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
