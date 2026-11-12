"""Percorrer os cartões novos, incluindo todos os tipos e os leitores por toque."""
import json, threading, re, os
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'justica-novas-qa';OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
def clean(s):return re.sub(r'\s+',' ',re.sub(r'[_*]','',s)).strip()
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    total=0
    for width,mode,project in [(390,'light',False),(1280,'dark',True)]:
      for n in range(4,14):
        ctx=browser.new_context(viewport={'width':width,'height':900},color_scheme=mode,reduced_motion='reduce')
        page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('https://www.youtube-nocookie.com/**',lambda r:r.fulfill(body='Vídeo externo não reproduzido neste teste.'))
        page.goto(f'http://127.0.0.1:{server.server_port}/olhar-e-decidir/justica/licao-{n}/'+('?projetar=1' if project else ''),wait_until='domcontentloaded')
        bank=json.loads((ROOT/f'tools/justica/bancos/licao-{n}.json').read_text('utf-8'))
        assert page.locator('iframe').count()==0
        for k,c in enumerate(bank):
            page.locator('#baralho .cartao').first.wait_for()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(n,k,width)
            if k in [0,1,3,len(bank)-1]:page.screenshot(path=str(OUT/f'l{n}-c{k+1}-{width}.png'))
            if c['t']=='ler':
                if page.locator('.ju-video').count():
                    box=page.locator('.ju-video');data=box.evaluate('(e)=>({...e.dataset})');box.locator('button').click()
                    src=box.locator('iframe').get_attribute('src')
                    assert f'/embed/{data["yt"]}?' in src and '&start='+data['ini'] in src and '&end='+data['fim'] in src
                page.locator('[data-c-acoes] [data-seguinte]').click()
            elif project:
                page.locator('[data-mostrar]').click()
                page.locator('[data-c-folha] [data-seguinte]').click()
            else:
                t=c['t']
                if t in ['escolha','pistas']:
                    page.locator(f'#baralho button.op[data-j="{c["c"]}"]').click()
                elif t=='vf':page.locator(f'#baralho button.op[data-j="{1 if c["v"] else 0}"]').click()
                elif t=='mapa':
                    page.locator(f'.op-m[data-j="{c["c"]}"]').focus();page.keyboard.press('Enter')
                    page.locator('[data-confirmar]').click()
                elif t=='sublinhar':
                    for j in c['certas']:page.locator(f'#baralho button.pal[data-j="{j}"]').click()
                    page.locator('[data-confirmar]').click()
                elif t in ['frase','ordenar']:
                    items=c['palavras'] if t=='frase' else c['passos']
                    for j in range(len(items)):page.locator(f'#baralho .soltos button[data-j="{j}"]').click()
                elif t=='completar':
                    for j,l in enumerate(c['lacunas']):page.locator(f'select[data-k="{j}"]').select_option(str(l['c']))
                elif t=='emparelhar':
                    vals=list(dict.fromkeys(p[1] for p in c['pares']))
                    for j,pair in enumerate(c['pares']):
                        page.locator(f'[data-e="{j}"]').click()
                        page.locator(f'[data-d="{vals.index(pair[1])}"]').click()
                else:raise ValueError(t)
                page.locator('[data-c-folha]:not([hidden]) [data-seguinte]').click()
            total+=1
        page.locator('.cartao.fim').wait_for()
        assert errors==[],(n,errors)
        if project:assert page.evaluate(f'localStorage.getItem("lente-justica-licao-{n}")') is None
        print('PASS',n,width,mode,'projecao',project,flush=True)
        ctx.close()
    browser.close()
server.shutdown()
print(total,'cartões percorridos')
