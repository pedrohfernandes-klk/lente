"""31/10/2026: verifica a entrega documental; não substitui os testes dos sítios."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
O=Path(__file__).resolve().parents[1]
class Doc(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.text=[];self.skip=0
 def handle_starttag(self,t,attrs):
  if t in ['script','style','code']:self.skip+=1
  for k,v in attrs:
   if k in ['href','src'] and v:self.refs.append(v)
 def handle_endtag(self,t):
  if t in ['script','style','code']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.text.append(d)
pages=json.loads((O/'paginas.json').read_text(encoding='utf8'));missing=[];broken=[];language=[]
for p in pages:
 for w in [320,390,1024,1366,1440]:
  for t in ['light','dark']:
   for q in [O/'medidas'/f'{p["id"]}-{w}-{t}.json',O/'capturas'/f'{p["id"]}-{w}-{t}.jpg']:
    if not q.exists():missing.append(str(q.relative_to(O)))
for f in O.rglob('*.html'):
 d=Doc();d.feed(f.read_text(encoding='utf8'))
 for ref in d.refs:
  u=urlsplit(ref)
  if u.scheme or not u.path or u.path.startswith('/'):continue
  q=(f.parent/unquote(u.path)).resolve()
  if not q.exists():broken.append({'file':str(f.relative_to(O)),'target':ref})
 txt=' '.join(d.text)
 for m in re.finditer(r'\b(?:jogar|jogo|ficha|folha|professor)\b|[—·]',txt,re.I):language.append({'file':str(f.relative_to(O)),'text':txt[max(0,m.start()-30):m.end()+30]})
base=[json.loads(f.read_text(encoding='utf8')) for f in (O/'medidas').glob('*.json') if not f.name.endswith('-ERROR.json')]
studies=[json.loads(f.read_text(encoding='utf8')) for f in (O/'provas').glob('depois-*.json') if not f.name.endswith('-ERROR.json')]
library=[json.loads(f.read_text(encoding='utf8')) for f in (O/'provas').glob('biblioteca-pecas-*.json')]
result={'baseCases':len(base),'proposalCases':len(studies),'libraryCases':len(library),'missing':missing,'brokenLocalLinks':broken,'authoredLanguageFindings':language,'baseOverflow':max(x['overflow'] for x in base),'proposalOverflow':max(x['overflow'] for x in studies),'proposalContrastFindings':sum(len(x['contrastFailures']) for x in studies),'libraryContrastFindings':sum(len(x['contrastFailures']) for x in library),'baseJavascriptErrors':sum(len(x['errors']) for x in base),'proposalJavascriptErrors':sum(len(x['errors']) for x in studies),'baseReducedMotionRunning':sum(x['reducedMotion']['running'] for x in base),'files':len(list(O.rglob('*'))),'note':'Contraste calculado apenas em fundos sólidos. As capturas de páginas antigas preservam o texto original como prova. Não há certificação WCAG integral.'}
(O/'provas/validacao-documental.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
try:
 from PIL import Image,ImageDraw
 for theme in ['light','dark']:
  canvas=Image.new('RGB',(1200,1840),'white');draw=ImageDraw.Draw(canvas)
  for i,p in enumerate(pages):
   img=Image.open(O/'capturas'/f'{p["id"]}-390-{theme}.jpg').crop((0,0,390,844)).resize((195,422))
   x,y=(i%6)*200,(i//6)*460;canvas.paste(img,(x,y+25));draw.text((x+4,y+5),p['id'],fill='black')
  canvas.save(O/'provas'/f'contacto-{theme}.jpg')
except ImportError:pass
if missing or broken or language or len(base)!=240 or len(studies)!=96 or result['proposalOverflow'] or result['proposalContrastFindings']:raise SystemExit(1)
