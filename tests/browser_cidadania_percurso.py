from pathlib import Path
import json,threading,mimetypes
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R.parents[1]/'outputs/lente-cidadania-percurso';O.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(R.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}';results=[]
def local(route):
 path=R.parent/urlsplit(route.request.url).path.lstrip('/')
 if path.is_dir():path=path/'index.html'
 route.fulfill(status=200 if path.exists() else 404,body=path.read_bytes() if path.exists() else b'',content_type=mimetypes.guess_type(str(path))[0] or 'application/octet-stream')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True)
 for width in [320,1440]:
  ctx=b.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce')
  ctx.route('https://pedrohfernandes-klk.github.io/lente/**',local)
  ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
  for path in ['cidadania/','cidadania/m1/','cidadania/projeto/','cidadania/m2/','cidadania/contra-feed/']:
   p=ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));assert p.goto(host+'/lente/'+path).status==200;p.wait_for_timeout(300)
   assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,path)
   assert not errors,(path,errors)
   assert not p.locator('a[href*="/guia-docente/"]').count()
   if path in ['cidadania/m1/','cidadania/m2/']:
    assert p.locator('.cid-route-step').count() in [4,5]
    p.locator('.cid-route').screenshot(path=str(O/f'rota-{path.split("/")[1]}-{width}.png'))
    for link in p.locator('.cid-route a').all():
     href=link.get_attribute('href');u=urlsplit(href);response=ctx.request.get(host+u.path);assert response.status==200,href
     if u.fragment:assert 'id="'+u.fragment+'"' in response.text(),href
   results.append({'page':path,'width':width,'overflow':False,'errors':errors});p.close()
  ctx.close()
 # Native projection route and largest font.
 p=b.new_page(viewport={'width':1440,'height':1000});ctx=p.context
 ctx.route('https://pedrohfernandes-klk.github.io/lente/**',local)
 p.goto(host+'/lente/projetar/?pagina=/lente/cidadania/m2/');p.locator('[data-projection-size="large"]').click();f=p.frame_locator('#lesson-frame');f.locator('#projeto-filosofico').wait_for();assert f.locator('html').evaluate('(e)=>e.scrollWidth<=e.clientWidth');p.screenshot(path=str(O/'projecao-m2.png'));results.append({'projection':'m2','largest_font':True,'overflow':False});b.close()
server.shutdown();(O/'qa-interface.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(results,ensure_ascii=False))
