from pathlib import Path
import json,re,threading
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT.parents[1]/'outputs/lente-cidadania-cinco-quartas';OUT.mkdir(parents=True,exist_ok=True);key='cid-m1-butler-singer';s=(ROOT/'cidadania/m1'/key/'index.html').read_text('utf-8');m=re.search(r'itens:(\[)',s);cards=json.JSONDecoder().raw_decode(s[m.start(1):])[0]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}';results=[]
def act(p):
 if p.locator('.casca [data-c-folha]:visible [data-seguinte]').count():p.locator('.casca [data-c-folha]:visible [data-seguinte]').click();return
 if p.locator('.casca [data-c-acoes] [data-seguinte]').count():p.locator('.casca [data-c-acoes] [data-seguinte]').click();return
 if p.locator('#baralho [data-tipo-ext="posicao"] [data-ops] button').count():p.locator('#baralho [data-tipo-ext="posicao"] [data-ops] button').first.click();return
 if p.locator('#baralho .pares .col.esq [data-e]').count():
  n=p.locator('#baralho .pares .col.esq [data-e]').count()
  for i in range(n):p.locator(f'#baralho .pares .col.esq [data-e="{i}"]').click();p.locator(f'#baralho .pares .col.dir [data-d="{i}"]').click()
  return
 if p.locator('#baralho .ordem .soltos button.op').count():
  n=p.locator('#baralho .ordem .soltos button.op').count()
  for i in range(n):p.locator('#baralho .ordem .soltos button.op').first.click()
  return
 if p.locator('#baralho .ops button.op').count():p.locator('#baralho .ops button.op[data-j="0"]').click();return
 raise AssertionError(p.locator('#baralho').inner_text()[:250])
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True)
  for width in [320,1440]:
   ctx=b.new_context(viewport={'width':width,'height':900},reduced_motion='reduce');ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort());p=ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(host+'/lente/cidadania/m1/'+key+'/',wait_until='networkidle');seed={'feitas':{'passo-00':1,'passo-01':1},'nota':'manter'};p.evaluate('s=>localStorage.setItem("epi-cidadania-m1",JSON.stringify(s))',seed)
   def finish():
    for _ in range(100):
     if p.locator('#baralho .cartao.fim').count():return
     assert not p.evaluate('document.documentElement.scrollWidth>innerWidth+2')
     if p.locator('.cid-duas-perguntas').count():p.screenshot(path=str(OUT/f'comparacao-percurso-{width}.png'))
     act(p)
    raise AssertionError('stalled')
   finish();saved=p.evaluate('JSON.parse(localStorage.getItem("epi-cidadania-m1-butler-singer"))');assert saved['lida'] and saved['total']==4,saved;assert p.evaluate('JSON.parse(localStorage.getItem("epi-cidadania-m1"))')==seed;p.reload(wait_until='networkidle');p.locator('#baralho .cartao.fim').wait_for();p.locator('.casca [data-repetir]').click();finish();repeat=p.evaluate('JSON.parse(localStorage.getItem("epi-cidadania-m1-butler-singer"))');assert repeat['tentativas']==2 and repeat['total']==4
   def mount(items):p.evaluate("items=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:items,chave:'qa-butler-singer',variar:false,mostrarAnterior:false});document.querySelector('.jogo-alvo').id='baralho'}",items)
   mount(cards);finish()
   for i in [4,11]:
    for j in range(3):
     mount([cards[i]]);choice=p.locator(f'#baralho [data-ops] button[data-j="{j}"]');choice.focus();choice.press('Enter');sheet=p.locator('.casca [data-c-folha]:visible');assert 'Para discutir.' in sheet.inner_text();assert 'Certo.' not in sheet.inner_text();assert '+10' not in sheet.inner_text();assert cards[i]['opcoes'][j]['comentario'] in sheet.inner_text();assert p.locator('#baralho .f-rev.reflexao').count()==1;act(p);neutral=p.evaluate('JSON.parse(localStorage.getItem("qa-butler-singer"))');assert neutral['total']==0 and neutral['certas']==0,neutral
   for i in [6,8]:
    for j in [1,2]:
     mount([cards[i]]);choice=p.locator(f'#baralho .ops [data-j="{j}"]');choice.focus();choice.press('Enter');assert cards[i]['fe'][j] in p.locator('.casca [data-c-folha]:visible').inner_text()
   mount([cards[10]]);assert p.locator('.cid-duas-perguntas section').count()==2;assert not p.evaluate('document.documentElement.scrollWidth>innerWidth+2');p.screenshot(path=str(OUT/f'comparar-{width}.png'));mount([cards[5]]);p.screenshot(path=str(OUT/f'butler-{width}.png'));assert p.locator('#baralho textarea,input[type=text]').count()==0;assert not errors;results.append({'width':width,'full_bank':15,'normal_attempt_and_reload':True,'second_normal_attempt':True,'objective_total':4,'neutral_positions':6,'wrong_choices':4,'progress_unchanged':True,'errors':errors});ctx.close()
  ctx=b.new_context(viewport={'width':1440,'height':900});ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort());p=ctx.new_page();p.goto(host+'/lente/projetar/?pagina=/lente/cidadania/m1/'+key+'/',wait_until='networkidle');f=p.frame_locator('#lesson-frame');f.locator('#baralho .cartao').wait_for();p.locator('[data-projection-size="large"]').click();assert not f.locator('html').evaluate('e=>e.scrollWidth>e.clientWidth+2');p.screenshot(path=str(OUT/'projecao-licao.png'));real_frame=p.locator('#lesson-frame').element_handle().content_frame()
  for _ in range(35):
   if real_frame.locator('.cid-duas-perguntas').count():break
   act(real_frame)
  else:raise AssertionError('comparison not reached in projection')
  assert not real_frame.evaluate('document.documentElement.scrollWidth>innerWidth+2');assert real_frame.locator('.cid-duas-perguntas section').first.bounding_box()['width']>=200;p.screenshot(path=str(OUT/'projecao-comparacao.png'));results.append({'mode':'native_projection','largest_text':True,'comparison_reached_in_real_path':True,'overflow':False});ctx.close();b.close()
finally:server.shutdown()
(OUT/'qa-licao.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('PASS Butler/Singer: full lesson, 6 neutral choices, 4 errors, progress, mobile and projection')
