"""01/11/2026: hierarquia dos títulos em todas as páginas (decisão 61), no navegador.

Abre todas as páginas do repositório a 390 e a 1366 px e corre as regras R1, R2, R3 e R5 da medição
(design/hierarquia/medir-hierarquia.js; a função MEASURE está copiada abaixo sem alterações):
- R1: um título mais pequeno do que um título de nível inferior que ele agrupa;
- R2: antetítulo (texto curto em maiúsculas ou espaçado logo antes de um título) com letra acima de 65 % da do título;
- R3: antetítulos da mesma classe com letra diferente na mesma página (família, tamanho ou peso);
- R5: título mais pequeno do que o texto corrido que o segue.
Os elementos decorativos com aria-hidden ficam fora de R2 e R3, como no script. R4 fica como relatório, fora daqui.

Falha com qualquer caso novo. Os casos ainda por corrigir estão em PENDENTES_20261101, com o número de vezes que
aparecem a cada largura; o teste falha também se um caso da lista já não aparecer tantas vezes (a lista só diminui:
quem corrige um caso tira-o da lista no mesmo pedido).

Páginas: os .html com </head> e sem meta refresh, fora de .git, tests, docs, _qa, node_modules e assets (como o script).
Serve a cópia de trabalho em /lente/, seja qual for o nome da pasta; os endereços absolutos do sítio
(https://pedrohfernandes-klk.github.io/lente/) vêm da mesma cópia e o resto da rede fica de fora.
Uso: python tests/browser_hierarquia_titulos.py [--json saida.json]"""
from pathlib import Path
from collections import Counter
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlsplit,unquote
import asyncio,json,mimetypes,re,sys,threading
from playwright.async_api import async_playwright

R=Path(__file__).resolve().parents[1]
LARGURAS=(390,1366)
FORA={'.git','tests','docs','_qa','node_modules','assets'}
SITIO='https://pedrohfernandes-klk.github.io/lente/'
TIPOS={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json',
 '.woff2':'font/woff2','.woff':'font/woff','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg',
 '.svg':'image/svg+xml','.gif':'image/gif','.ico':'image/x-icon','.vtt':'text/vtt','.txt':'text/plain','.pdf':'application/pdf'}

# Casos por corrigir a 01/11/2026: chave -> (vezes a 390 px, vezes a 1366 px, nota). Só pode diminuir.
PENDENTES_20261101={
 # R5 no guia do docente do piloto do M1: h3 a 16 px antes de texto a 17 px. Corrige-se no #84 (tools/cidadania_piloto.py).
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «O que fica escrito» antes de p.pg':(8,8,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Imagem» antes de p.pg':(10,10,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Vídeo» antes de p.pg':(10,10,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Fontes da lição» antes de p.pg.fontes':(10,10,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: Apresentação» antes de p.pg':(1,1,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: Ética das entrevistas» antes de p.pg':(1,1,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: A pergunta» antes de p.pg':(1,1,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: As fontes» antes de p.pg':(1,1,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: A recolha» antes de p.pg':(1,1,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: O guião, em esboço» antes de p.pg':(1,1,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: Nenhum passo novo em aula» antes de p.pg':(2,2,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: O ensaio» antes de p.pg':(1,1,'corrige-se no #84'),
 'R5 | cidadania/piloto/m1/docente/index.html | h3 «Pergunta Humana: A apresentação e a defesa» antes de p.pg':(1,1,'corrige-se no #84'),
}

# Copiada sem alterações de medir-hierarquia.js (01/11/2026).
MEASURE=r"""const MEASURE=()=>{
  const vis=e=>{const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return false;for(let x=e;x&&x!==document.documentElement;x=x.parentElement){if(x.hidden)return false;const c=getComputedStyle(x);if(c.display==='none'||c.visibility==='hidden'||+c.opacity<.05)return false;if(x.matches&&x.matches('.sr-only,.c-sr,.p-sr,.visually-hidden,dialog:not([open]),details:not([open])>:not(summary)'))return false;}return true;};
  const fs=e=>parseFloat(getComputedStyle(e).fontSize);
  const txt=e=>e.textContent.replace(/\s+/g,' ').trim().slice(0,80);
  const desc=e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/).slice(0,3).join('.'):'');
  const sig=e=>{const parent=e.parentElement;const pc=parent&&typeof parent.className==='string'&&parent.className.trim()?'.'+parent.className.trim().split(/\s+/)[0]:'';return (parent?parent.tagName.toLowerCase()+pc+'>':'')+desc(e).replace(/#[^.]+/,'');};
  const level=e=>{const m=e.tagName.match(/^H([1-6])$/);if(m)return +m[1];const a=e.getAttribute('aria-level');return a?+a:2;};
  const heads=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role=heading]')].filter(e=>vis(e)&&txt(e));
  const out={r1:[],r2:[],r3:[],r5:[],roles:[]};
  heads.forEach((h,i)=>{const L=level(h),F=fs(h);out.roles.push({sig:sig(h),lvl:L,fs:F,txt:txt(h)});
    for(let j=i+1;j<heads.length;j++){const k=heads[j],Lk=level(k);if(Lk<=L)break;const Fk=fs(k);if(Fk>F+.5){out.r1.push({pai:desc(h),paiTxt:txt(h),paiFs:F,filho:desc(k),filhoTxt:txt(k),filhoFs:Fk});break;}}
    // R2 antetítulo
    const prev=h.previousElementSibling;if(prev&&vis(prev)&&!/^H[1-6]$/.test(prev.tagName)&&!prev.closest('[aria-hidden="true"]')){const t=txt(prev);const c=getComputedStyle(prev);const ls=parseFloat(c.letterSpacing)||0;if(t&&t.length<=60&&(c.textTransform==='uppercase'||ls>=.05*parseFloat(c.fontSize))){const Fp=fs(prev);out.r3.push({cls:desc(prev).replace(/#[^.]+/,''),desc:desc(prev),txt:t,fs:Fp,fam:c.fontFamily.split(',')[0].replace(/["']/g,''),w:c.fontWeight});if(Fp>.65*F)out.r2.push({ante:desc(prev),anteTxt:t,anteFs:Fp,titulo:desc(h),tituloTxt:txt(h),tituloFs:F});}}
    // R5 texto corrido a seguir
    const c=getComputedStyle(h);if(c.textTransform!=='uppercase'){let n=h.nextElementSibling;while(n&&!vis(n))n=n.nextElementSibling;if(n&&n.tagName==='P'&&txt(n).length>60){const Fn=fs(n);if(F<Fn-.5)out.r5.push({titulo:desc(h),tituloTxt:txt(h),tituloFs:F,texto:desc(n),textoFs:Fn});}}
  });
  const byCls={};for(const k of out.r3)(byCls[k.cls]=byCls[k.cls]||new Set()).add(k.fam+'|'+Math.round(k.fs)+'|'+k.w);out.r3=out.r3.filter(k=>byCls[k.cls].size>1);
  return out;};"""
MEDIR='()=>{'+MEASURE+'\nreturn MEASURE();}'

def paginas():
 out=[]
 def andar(d):
  for n in sorted(p.name for p in d.iterdir()):
   if n in FORA:continue
   f=d/n
   if f.is_dir():andar(f)
   elif n.endswith('.html'):
    s=f.read_text('utf-8',errors='replace')
    if re.search(r'</head\s*>',s,re.I) and not re.search(r'http-equiv=["\']?refresh',s,re.I):out.append(f.relative_to(R).as_posix())
 andar(R);return sorted(out)

def ficheiro(caminho):
 """O ficheiro da cópia de trabalho para um caminho /lente/...; nunca fora da cópia."""
 f=(R/unquote(caminho).removeprefix('/lente/').lstrip('/')).resolve()
 if f!=R and R not in f.parents:return None
 if f.is_dir():f=f/'index.html'
 return f if f.is_file() else None

def tipo(f):return TIPOS.get(f.suffix.lower()) or mimetypes.guess_type(str(f))[0] or 'application/octet-stream'

class Lente(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  p=urlsplit(self.path).path;f=ficheiro(p) if p.startswith('/lente/') else None
  if not f:self.send_response(404);self.end_headers();return
  dados=f.read_bytes();self.send_response(200);self.send_header('Content-Type',tipo(f))
  self.send_header('Content-Length',str(len(dados)));self.end_headers();self.wfile.write(dados)

def chaves(m):
 """Uma chave por caso, sem tamanhos (os tamanhos vão na mensagem)."""
 out=[]
 for c in m['r1']:out.append((f"R1 | {m['page']} | {c['pai']} «{c['paiTxt']}» < {c['filho']} «{c['filhoTxt']}»",f"{c['paiFs']} px < {c['filhoFs']} px"))
 for c in m['r2']:out.append((f"R2 | {m['page']} | {c['ante']} «{c['anteTxt']}» antes de {c['titulo']} «{c['tituloTxt']}»",f"{c['anteFs']} px antes de {c['tituloFs']} px"))
 for c in m['r3']:out.append((f"R3 | {m['page']} | {c['cls']} {c['fam']} {round(c['fs'])} px {c['w']}",f"«{c['txt']}»"))
 for c in m['r5']:out.append((f"R5 | {m['page']} | {c['titulo']} «{c['tituloTxt']}» antes de {c['texto']}",f"{c['tituloFs']} px, texto {c['textoFs']} px"))
 return out

async def medir(host,lista):
 trabalhos=[(p,w) for p in lista for w in LARGURAS];res=[]
 async with async_playwright() as pw:
  b=await pw.chromium.launch(headless=True)
  async def rota(route):
   u=route.request.url
   if u.startswith(host+'/'):return await route.continue_()
   if u.startswith(SITIO):
    f=ficheiro(urlsplit(u).path)
    if f:return await route.fulfill(status=200,body=f.read_bytes(),content_type=tipo(f))
    return await route.fulfill(status=404,body=b'')
   await route.abort()
  async def operario():
   ctx=await b.new_context(reduced_motion='reduce');await ctx.route('**/*',rota);pg=await ctx.new_page()
   while trabalhos:
    p,w=trabalhos.pop(0);erro=None
    for _ in range(2):  # uma segunda tentativa só se a página não abrir
     try:
      await pg.set_viewport_size({'width':w,'height':900})
      await pg.goto(f'{host}/lente/{p}',wait_until='load',timeout=30000);await pg.wait_for_timeout(250)
      res.append({'page':p,'w':w,**await pg.evaluate(MEDIR)});erro=None;break
     except Exception as e:
      erro=str(e)[:200]
      try:await pg.close()
      except Exception:pass
      pg=await ctx.new_page()
    if erro:res.append({'page':p,'w':w,'erro':erro})
   await ctx.close()
  await asyncio.gather(*[operario() for _ in range(6)])
  await b.close()
 return res

def avaliar(res,pendentes):
 """Compara as medições com a lista: devolve (erros, contagem por largura, casos novos, casos da lista que já não aparecem)."""
 erros=[f"{x['page']} a {x['w']} px: {x['erro']}" for x in res if 'erro' in x]
 contagem={w:Counter() for w in LARGURAS};exemplo={}
 for m in res:
  if 'erro' in m:continue
  for k,info in chaves(m):contagem[m['w']][k]+=1;exemplo.setdefault((k,m['w']),info)
 novos=[];resolvidos=[]
 for i,w in enumerate(LARGURAS):
  for k,n in sorted(contagem[w].items()):
   lista_n=pendentes.get(k,(0,0,''))[i]
   if n>lista_n:novos.append(f'{w} px, {n} vez(es), lista {lista_n}: {k} [{exemplo[(k,w)]}]')
  for k,v in pendentes.items():
   n=contagem[w].get(k,0)
   if n<v[i]:resolvidos.append(f'{w} px, agora {n} vez(es), lista {v[i]}: {k} ({v[2]})')
 return erros,contagem,novos,resolvidos

def main():
 server=ThreadingHTTPServer(('127.0.0.1',0),Lente);threading.Thread(target=server.serve_forever,daemon=True).start()
 host=f'http://127.0.0.1:{server.server_port}'
 lista=paginas();assert len(lista)>400,f'só {len(lista)} páginas: a lista de páginas falhou'
 try:res=asyncio.run(medir(host,lista))
 finally:server.shutdown()
 if '--json' in sys.argv:Path(sys.argv[sys.argv.index('--json')+1]).write_text(json.dumps(res,ensure_ascii=False),'utf-8')
 erros,contagem,novos,resolvidos=avaliar(res,PENDENTES_20261101)
 print(f'Hierarquia dos títulos: {len(lista)} páginas a {len(LARGURAS)} larguras, {len(res)} medições; '
       f'{sum(sum(c.values()) for c in contagem.values())} casos, {sum(v[0]+v[1] for v in PENDENTES_20261101.values())} na lista de pendentes.')
 falhas=[]
 if erros:falhas.append('Páginas que não abriram:\n  '+'\n  '.join(erros))
 if novos:falhas.append('Casos novos (corrige a página ou o gerador; a lista nunca cresce):\n  '+'\n  '.join(novos))
 if resolvidos:falhas.append('Casos da lista que já não aparecem (tira-os de PENDENTES_20261101):\n  '+'\n  '.join(resolvidos))
 if falhas:print('\n'.join(falhas));sys.exit(1)
 print('R1, R2, R3 e R5: nenhum caso novo; a lista de pendentes está certa.')

if __name__=='__main__':main()
