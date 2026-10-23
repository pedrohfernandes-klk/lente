from pathlib import Path
import ast,json,threading
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R.parents[1]/'outputs/lente-lab-treinos';O.mkdir(parents=True,exist_ok=True)
# Reutiliza a ação já testada do Butler/Singer para avançar nos cartões.
src=(R/'tests/browser_cidadania_butler_singer.py').read_text('utf-8');node=next(x for x in ast.parse(src).body if isinstance(x,ast.FunctionDef) and x.name=='act');exec(compile(ast.Module(body=[node],type_ignores=[]),'<shared-act>','exec'))
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(R.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}';results=[]
AMOSTRA=['sem-olhos','sem-disse','tres-em-cinco','copia-lenta','pelo-meio','rascunho-mau']
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True)
 for width in [320,1440]:
  ctx=b.new_context(viewport={'width':width,'height':900},reduced_motion='reduce');ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
  for tid in AMOSTRA:
   p=ctx.new_page();p.set_default_timeout(10000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   assert p.goto(f'{host}/lente/narrativas/treinar/{tid}/').status==200
   p.evaluate('localStorage.setItem("epi-treinos",JSON.stringify({feitas:{outro:1},nota:"preservar"}))')
   viu_relogio=viu_lista=False
   for _ in range(60):
    if p.locator('#baralho .cartao.fim').count():break
    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),(width,tid)
    w=p.locator('#baralho .tr-relogio').first
    if not viu_relogio and w.count() and w.is_visible():
     ini=w.locator('.tr-tempo').inner_text();w.locator('[data-rl="ir"]').click();p.wait_for_timeout(2300)
     depois=w.locator('.tr-tempo').inner_text();assert depois!=ini,(tid,ini,depois)
     w.locator('[data-rl="parar"]').click();parado=w.locator('.tr-tempo').inner_text();p.wait_for_timeout(1200);assert w.locator('.tr-tempo').inner_text()==parado
     w.locator('[data-rl="zero"]').click();assert w.locator('.tr-tempo').inner_text()==ini
     b2=w.locator('[data-rl="ir"]');assert b2.bounding_box()['height']>=44
     if width==320:p.screenshot(path=str(O/f'{tid}-relogio-{width}.png'))
     viu_relogio=True
    caixas=p.locator('#baralho .tr-verifica input[type=checkbox]')
    if not viu_lista and caixas.count() and caixas.first.is_visible():
     assert caixas.count()==3
     for i in range(3):caixas.nth(i).click()
     assert p.locator('#baralho .tr-verifica input:checked').count()==3
     viu_lista=True
    act(p)
   else:raise AssertionError('Treino sem fim: '+tid)
   assert viu_relogio and viu_lista,(tid,viu_relogio,viu_lista)
   s=p.evaluate('JSON.parse(localStorage.getItem("epi-treinos"))');assert s['vezes'][tid]==1 and s['feitas']['outro']==1 and s['nota']=='preservar',s
   assert not errors,(tid,errors);results.append({'treino':tid,'width':width});p.close()
  ctx.close()
 # Projeção: o relógio continua legível e funcional em letra grande.
 ctx=b.new_context(viewport={'width':1280,'height':800});p=ctx.new_page();p.goto(f'{host}/lente/narrativas/treinar/sem-olhos/?projetar=1')
 for _ in range(10):
  if p.locator('#baralho .tr-relogio').count() and p.locator('#baralho .tr-relogio').first.is_visible():break
  act(p)
 assert p.locator('#baralho .tr-relogio').first.is_visible();p.screenshot(path=str(O/'projecao.png'));ctx.close()
 b.close()
server.shutdown();(O/'qa.json').write_text(json.dumps(results,indent=1),'utf-8');print('PASS treinos:',len(results),'percursos completos com relógio e verificação, 320/1440 e projeção')
