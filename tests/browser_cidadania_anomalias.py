from pathlib import Path
import ast,json,re,threading
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R.parents[1]/'outputs/lente-anomalias-exercicios';O.mkdir(parents=True,exist_ok=True)
# Reuse the tested action helper without running the Butler/Singer browser suite.
src=(R/'tests/browser_cidadania_butler_singer.py').read_text('utf-8');node=next(x for x in ast.parse(src).body if isinstance(x,ast.FunctionDef) and x.name=='act');exec(compile(ast.Module(body=[node],type_ignores=[]),'<shared-act>','exec'));base_act=act
def act(p):
 if p.locator('#baralho .cid-imgs button:enabled').count():p.evaluate('EPITipos.imagens.auto()');return
 if p.locator('#baralho .ordem .soltos button.op:enabled').count():
  ids=sorted(map(int,p.locator('#baralho .ordem .soltos button.op').evaluate_all('(a)=>a.map(b=>b.dataset.j)')))
  for j in ids:p.locator(f'#baralho .ordem .soltos button[data-j="{j}"]').click()
  return
 base_act(p)
def bank(path):
 s=(R/path).read_text('utf-8');m=re.search(r'itens:(\[)',s);return json.JSONDecoder().raw_decode(s[m.start(1):])[0]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(R.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}';results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True)
 for width in [320,1440]:
  for rel,total in [('m1/passo-00',4),('m2/passo-00',3),('m2/passo-01',2)]:
   print(width,rel,flush=True)
   ctx=b.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce');ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort());p=ctx.new_page();p.set_default_timeout(10000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(host+'/lente/cidadania/'+rel+'/',wait_until='domcontentloaded');cards=bank('cidadania/'+rel+'/index.html');key='epi-cidadania-'+rel.replace('/','-')
   seed={'feitas':{'passo-01':123},'nota':'preservar'};p.evaluate('(s)=>localStorage.setItem("epi-cidadania-m1",JSON.stringify(s))',seed)
   for attempt in range(2):
    for _ in range(100):
     if p.locator('#baralho .cartao.fim').count():break
     act(p)
    else:raise AssertionError('Lesson did not finish: '+rel)
    saved=p.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',key);assert saved['total']==total,(rel,saved);assert saved['certas']==total,(rel,saved)
    if attempt==0:p.locator('.casca [data-repetir]').click()
   progress=p.evaluate('JSON.parse(localStorage.getItem("epi-cidadania-m1"))');assert progress['nota']==seed['nota'] and progress['feitas']['passo-01']==123
   def mount(c):
    # Each isolated alternative gets a fresh document, without timers from a prior mount.
    p.reload(wait_until='domcontentloaded')
    p.evaluate("c=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:[c],chave:'qa-anomalia',variar:false,mostrarAnterior:false});document.querySelector('.jogo-alvo').id='baralho'}",c)
   pos=next(x for x in cards if x['t']=='posicao')
   for j in range(3):
    mount(pos);p.locator(f'#baralho [data-ops] button[data-j="{j}"]').press('Enter');sheet=p.locator('.casca [data-c-folha]:visible');assert 'Para discutir.' in sheet.inner_text();assert '+10' not in sheet.inner_text();act(p);saved=p.evaluate('JSON.parse(localStorage.getItem("qa-anomalia"))');assert saved['total']==0 and saved['certas']==0
   if rel=='m1/passo-00':
    for j in range(3):
     mount(cards[6]);p.locator('#baralho .cid-imgs img').last.wait_for();p.wait_for_timeout(150);assert p.locator('#baralho .cid-imgs figure').count()==3;assert not p.evaluate('document.documentElement.scrollWidth>innerWidth+2');p.screenshot(path=str(O/f'recortes-{width}.png'));p.locator(f'#baralho .cid-imgs button[data-j="{j}"]').press('Enter');assert cards[6]['feedback'][j] in p.locator('.casca [data-c-folha]:visible').inner_text()
   index=7 if rel=='m1/passo-00' else 5
   for j in range(1,len(cards[index]['o'])):
    # The engine presents the correct answer and two rotating distractors.
    # Isolate each distractor in a three-option bank so coverage is deterministic.
    c=dict(cards[index]);order=[0,j]+[k for k in range(len(c['o'])) if k not in [0,j]][:1];c['o']=[c['o'][k] for k in order];c['fe']=[c['fe'][k] for k in order];mount(c);p.locator('#baralho .ops button[data-j="1"]').press('Enter');assert cards[index]['fe'][j] in p.locator('.casca [data-c-folha]:visible').inner_text()
   assert not errors,errors;results.append({'lesson':rel,'width':width,'attempts':2,'objective_total':total,'neutral_choices':3,'errors':errors});ctx.close()
 b.close()
server.shutdown();(O/'qa.json').write_text(json.dumps(results,indent=2),'utf-8');print('PASS: three lessons, two attempts, all open positions and wrong-option feedback; 320/1440 px.')
