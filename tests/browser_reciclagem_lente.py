"""Percursos reais, conservação da chave, projeção, revelação e destinos da reciclagem."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit,unquote
import threading,json,re,mimetypes,os
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('RECICLAGEM_OUT',str(R.parent/'capturas-reciclagem')));OUT.mkdir(parents=True,exist_ok=True)
KEY='epi-vozes-25-de-abril-v2'
class Servidor(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def translate_path(self,path):return str(R/unquote(urlsplit(path).path).removeprefix('/lente/'))
server=ThreadingHTTPServer(('127.0.0.1',0),Servidor);threading.Thread(target=server.serve_forever,daemon=True).start()
host=f'http://127.0.0.1:{server.server_port}/lente/'
def local(route):
 p=R/unquote(urlsplit(route.request.url).path).removeprefix('/lente/')
 if p.is_dir():p=p/'index.html'
 route.fulfill(status=200 if p.is_file() else 404,body=p.read_bytes() if p.is_file() else b'',content_type=mimetypes.guess_type(str(p))[0] or 'application/octet-stream')
def act(p):
 for sel in ('.casca [data-c-folha]:visible [data-seguinte]','.casca [data-c-acoes] [data-seguinte]'):
  if p.locator(sel).count():p.locator(sel).click();return
 if p.locator('#baralho .classes').count():
  for b in p.locator('#baralho [data-e]').all():
   b.click();p.locator('#baralho .classes .regiao .cab').first.click()
  return
 if p.locator('#baralho .pares .col.esq [data-e]').count():
  for i in range(p.locator('#baralho .pares .col.esq [data-e]').count()):
   p.locator(f'#baralho .pares [data-e="{i}"]').click();p.locator(f'#baralho .pares [data-d="{i}"]').click()
  return
 if p.locator('#baralho .ordem .soltos button.op').count():
  while p.locator('#baralho .ordem .soltos button.op').count():p.locator('#baralho .ordem .soltos button.op').first.click()
  return
 if p.locator('#baralho .ops button.op').count():p.locator('#baralho .ops button.op').first.click();return
 raise AssertionError(p.locator('#baralho').inner_text()[:250])
def finish(p):
 for _ in range(150):
  if p.locator('#baralho .cartao.fim').count():return
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
  act(p)
  p.wait_for_timeout(100)
 p.screenshot(path=str(OUT/'falha.png'))
 raise AssertionError('Percurso sem fim: '+p.locator('#baralho').inner_text()[:500])
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True)
  for width,theme in [(390,'light'),(1366,'dark')]:
   ctx=b.new_context(viewport={'width':width,'height':900},color_scheme=theme,reduced_motion='reduce')
   ctx.route('https://pedrohfernandes-klk.github.io/lente/**',local)
   ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
   p=ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   p.goto(host+'cidadania/25-de-abril/');p.locator('#baralho .cartao').wait_for()
   assert p.locator('#baralho figure:visible').count()==0
   p.screenshot(path=str(OUT/f'abril-{width}.png'))
   finish(p);saved=p.evaluate('k=>localStorage.getItem(k)',KEY);assert json.loads(saved)['lida']
   p.reload();p.locator('#baralho .cartao.fim').wait_for()
   p.goto(host+'cidadania/25-de-abril/?projetar=1');p.locator('#baralho .cartao').wait_for()
   if p.locator('[data-repetir]').count():p.locator('[data-repetir]').click()
   finish(p);assert p.evaluate('k=>localStorage.getItem(k)',KEY)==saved
   # Projeção nativa: a mesma página dentro do projetor.
   p.goto(host+'projetar/?pagina=/lente/cidadania/25-de-abril/')
   f=p.locator('#lesson-frame').element_handle().content_frame();f.locator('#baralho .cartao').wait_for()
   if f.locator('[data-repetir]').count():f.locator('[data-repetir]').click()
   finish(f);assert p.evaluate('k=>localStorage.getItem(k)',KEY)==saved
   for num in (1,3,4):
    p.goto(host+f'direitos/passo-{num:02}/');p.locator('#baralho .cartao').wait_for();finish(p)
   for num in (3,9):
    p.goto(host+f'cidadania/m2/sessoes/{num:02}/');p.locator('[data-start]').click()
    p.locator('[data-stage-link]').nth(1).click()
    caso=p.locator('#caso-reciclado');caso.wait_for(state='visible')
    assert caso.locator('details[open]').count()==0
    caso.locator('summary').first.click()
    for summary in caso.locator('.c10-feedback summary').all():
     summary.focus();summary.press('Enter');assert summary.locator('..').get_attribute('open') is not None
    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
    caso.screenshot(path=str(OUT/f'sessao-{num:02}-{width}.png'))
   p.goto(host+'cidadania/25-de-abril/guiao/');assert p.get_by_text('Para o docente: mediar sem escolher um lado').count()==1
   p.emulate_media(media='print');assert p.locator('table').is_visible()
   assert not errors,errors
   ctx.close();print('PASS',width,theme,'percurso, registo antigo, duas projeções, Direitos e sessões')
  b.close()
finally:server.shutdown()
