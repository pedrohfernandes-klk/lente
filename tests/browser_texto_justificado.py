"""30/10/2026: texto corrido justificado e hifenizado em pt-PT (decisão do docente), no navegador.

Abre uma página de cada família a 320, 390 e 1366 px e confere pelo estilo calculado:
- texto corrido com text-align justify, text-align-last auto, hyphens auto, word-spacing normal e
  overflow-wrap break-word, nunca abaixo de 22 caracteres por linha e sem <br>;
- versos, opções, botões, listas, tabelas, legendas, créditos curtos e formulários não justificados;
- nenhum deslocamento horizontal;
- língua efetiva pt-PT no texto justificado (ou o lang próprio de um texto noutra língua).
Nas lições de cartões avança pelos cartões com cliques, como o aluno, até ao cartão pedido.
Serve a cópia de trabalho em /lente/, seja qual for o nome da pasta."""
from pathlib import Path
import ast,json,mimetypes,sys,threading
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright,TimeoutError as PlaywrightTimeout

R=Path(__file__).resolve().parents[1];O=R.parents[1]/'outputs/lente-texto-justificado';O.mkdir(parents=True,exist_ok=True)
# Reutiliza a ação já testada do Butler/Singer para avançar nos cartões (como browser_lab_treinos.py).
src=(R/'tests/browser_cidadania_butler_singer.py').read_text('utf-8');node=next(x for x in ast.parse(src).body if isinstance(x,ast.FunctionDef) and x.name=='act');exec(compile(ast.Module(body=[node],type_ignores=[]),'<shared-act>','exec'))

class Lente(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def translate_path(self,path):
  p=unquote(urlsplit(path).path)
  return str(R/p[len('/lente/'):]) if p.startswith('/lente/') else str(R/'__fora__')
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Lente,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'

def local(route):
 f=R/unquote(urlsplit(route.request.url).path).removeprefix('/lente/')
 if f.is_dir():f=f/'index.html'
 if f.is_file():route.fulfill(status=200,body=f.read_bytes(),content_type=mimetypes.guess_type(str(f))[0] or 'application/octet-stream')
 else:route.fulfill(status=404,body=b'')

MEDIR="""(sel)=>{
 const cv=document.createElement('canvas').getContext('2d');
 const vis=e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&!e.closest('[hidden],details:not([open])>:not(summary)')};
 return [...document.querySelectorAll(sel)].filter(vis).map(e=>{
  const cs=getComputedStyle(e);const txt=(e.innerText||'').trim();cv.font=cs.font;
  const media=txt?cv.measureText(txt.slice(0,400)).width/Math.min(txt.length,400):1;
  const larg=e.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
  const lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.2;
  const L=e.closest('[lang]');
  return {sel:e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\\s+/).join('.'):''),
   ta:cs.textAlign,tal:cs.textAlignLast,hy:cs.hyphens||cs.webkitHyphens,ws:cs.wordSpacing,ow:cs.overflowWrap,disp:cs.display,
   lang:L?L.getAttribute('lang'):'',langDaPagina:L===document.documentElement,br:!!e.querySelector('br'),
   cpl:Math.round(larg/media),linhas:Math.round((e.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom))/lh),txt:txt.slice(0,60)}})}"""
# Todos os blocos justificados da página, para as regras gerais
JUSTIFICADOS="""()=>[...document.querySelectorAll('body *')].filter(e=>{const cs=getComputedStyle(e);return cs.textAlign==='justify'&&!['inline','contents','none'].includes(cs.display)&&(e.innerText||'').trim()})
 .map(e=>e.tagName.toLowerCase()+(typeof e.className==='string'&&e.className?'.'+e.className.trim().split(/\\s+/).join('.'):'')).slice(0,400)"""
NUNCA='button,li,td,th,label,figcaption,summary,legend,caption,h1,h2,h3,h4,h5,h6,dt,input,select,textarea,option,pre,code,cite,.versos,.poema p,.verso-q,.rot,.etq-m,p.q,.dica,p.fonte:not(.ae),.fonte-x,p.ap-fonte,p.fontes-p,p.quem'  # 30/10/2026: + p.fontes-p (listas de fontes)

# (família, página, passos). Passos: ('ate',seletor) avança nos cartões; ('J',seletor) justificado;
# ('E',seletor,mínimo) à esquerda; ('lang',seletor,lang) língua efetiva própria; ('centro',seletor);
# ('etapas',seletor) percorre os cinco passos de uma sessão de Cidadania; ('abrir',seletor) abre os details visíveis.
# 30/10/2026 (revisão adversarial): passos novos para as biografias de Vidas e vozes, Frei Luís (elenco e personagens),
# os Sete Mandamentos, as instruções curtas, a caixa de crédito das Sidequests, o guião em letra de máquina, a frase de
# Kafka com botões, os cartões de rotas do docente, as explicações em itens de lista e o texto corrido dentro de details.
# 30/10/2026 (verificação da revisão): a lista de fontes de Vidas e vozes (p.fontes-p) fica à esquerda.
PLANO=[
 ('L1a','narrativas/desenlace/',[('ate','.ler .excerto .trad:not(.poema) > p'),('J','.ler .excerto .trad > p')]),
 ('L1a','narrativas/corta/chuva/',[('ate','.ler .excerto .trad.poema'),('E','.ler .trad.poema > p',4),('ate','#baralho .ops button.op'),('E','#baralho .ops button.op',2),('ate','.casca-folha .c-expl'),('J','.casca-folha .c-expl')]),
 ('L1a','narrativas/margens/passo-02/',[('ate','.ler blockquote > p'),('J','.ler blockquote > p'),('E','.jogo .ler > p.ap-fonte',1)]),
 ('L1a','narrativas/corta/frei-luis/',[('ate','.ler .ap-texto > p.personagens'),('E','.ler .ap-texto > p.personagens',1),('J','.ler .ap-texto > p.fala')]),
 ('L1b','gigantes/triunfo-porcos/',[('ate','.ler details.orig-toque'),('abrir','.ler details.orig-toque'),('E','.ler .orig.lista > p',8),('J','.ler .relato')]),
 ('L1b','gigantes/diario-louco/',[('J','.jogo .ler > p:not([class])'),('ate','.ler .ap-texto > p:not([class])'),('J','.ler .ap-texto > p:not([class])'),('E','.jogo .ler > p.ap-fonte',1),('ate','.casca-folha .c-expl'),('J','.casca-folha .c-expl')]),
 ('L1c','vozes/prince/',[('ate','.ler dl.vz-vc > dd'),('E','.ler dl.vz-vc > dd',2),('E','.ler dl.vz-vc > dt',2),('ate','.ler .conceito > p:not([class])'),('J','.ler .conceito > p:not([class])'),
   ('ate','.ler p.fontes-p'),('E','.ler p.fontes-p',1),('ate','.ler ul.vz-lista > li'),('E','.ler ul.vz-lista > li',3)]),
 ('L1d','cidade/m10/',[('J','.jogo .ler > p:not([class])'),('E','.jogo .ler > p.porta-m',1),('ate','#baralho .palavras button.pal'),('E','#baralho .palavras button.pal',5),('E','#baralho p.q',1)]),
 ('L1e','sidequests/retorica/',[('E','.jogo .ler div.fonte',1),('ate','.ler .ap-texto > p.fala'),('J','.ler .ap-texto > p.fala')]),
 ('L1f','ler/passo-07/',[('ate','.ler .ap-texto > p.fala'),('J','.ler .ap-texto > p.fala'),('E','.ler .ap-texto > p.versos',1)]),
 ('L1g','cidadania/m1/passo-01/',[('ate','.ler .termo > dd'),('J','.ler .termo > dd')]),
 ('L1h','olhar-e-decidir/justica/licao-2/',[('ate','.jogo .ler > p.cita-en'),('J','.jogo .ler > p.cita-en'),('lang','.jogo .ler > p.cita-en i[lang]','en')]),
 ('L1h','olhar-e-decidir/estetica/licao-1/',[('ate','.jogo .ler > p.ex-antes'),('E','.jogo .ler > p.ex-antes',1)]),
 ('L2a','narrativas/fora-da-pagina/intervalo/',[('J','.jogo .ler > p:not([class])')]),
 ('L2b','narrativas/formas/certa-manha/',[('J','.formas-cartoes .lf-prosa > p'),('E','.formas-cartoes button',1)]),
 ('L3','narrativas/formas/',[('J','.lf-hero > p.lf-lead'),('J','.lf-level-body > p.lf-note'),('E','.lf-evidence-quote',1),('abrir','.lf-case details'),
   ('J','.lf-case > details.lf-pt > p:not([class])'),('E','.lf-case > details.lf-source > p',2)]),
 ('P1','ver-para-fazer/v01/',[('J','.vpf .vpf-porque'),('J','.vpf .vpf-fazer > p'),('E','.vpf button',1)]),
 ('P2','biblioteca/garrett-frei-luis-sousa/',[('J','.bib-texto > p:not([class])'),('lang','.bib-texto','pt-PT'),('E','.bib-texto > p.personagens',10),('E','.bib-texto > p.elenco',2)]),
 ('P2','biblioteca/cesario-sentimento-ocidental/',[('E','.bib-texto > p.versos',3)]),
 ('P2','biblioteca/brascubas-ao-leitor/',[('J','.bib-texto > p:not([class])'),('lang','.bib-texto','pt-PT')]),
 ('P3','narrativas/oficina-arco-imprimir/',[('J','main.pg > p:not([class])'),('E','main.pg li',3)]),
 ('P3b','dar-forma-as-palavras/',[('J','.comum > p:not([class])')]),
 ('E1','narrativas/',[('J','.p-cab > p.p-lead'),('J','.lab-saiu > p')]),
 ('E1','',[('E','a',5)]),
 ('E2','gigantes/',[('J','.p-cab p.p-lead'),('E','a.missao .s',5),('abrir','details.entrada-fontes'),('J','.entrada-fontes > p:not([class])')]),
 ('G1','narrativas/treinar/docente/',[('J','main.pg > p:not([class])')]),
 ('G1','narrativas/treinar/caderno/',[('J','main.pg > p:not([class])'),('E','th,td',2)]),
 ('J1','olhar-e-decidir/justica/guiao/',[('J','.lado > p:not([class])'),('J','.caso-im > p'),('E','th,td',2)]),
 ('J1','olhar-e-decidir/justica/docente/',[('E','.ex > dl > dd',10),('E','.ex > dl > dt',4)]),
 ('V1','vozes/25-de-abril/guiao/',[('J','.gu > p:not([class])')]),
 ('C1','cidadania/m1/fichas/f01/',[('J','.m1-v2 .m1-block > p:not([class])'),('E','.m1-v2 ol.m1-tasks li',2),('abrir','.m1-block details'),('J','.m1-v2 .m1-block > details > div > p:not([class])')]),
 ('C2','cidadania/m1/oficina-guiao/',[('E','.c10-document.c10-script',1)]),
 ('C2','cidadania/m1/sessoes/03/',[('etapas','.c10 :is(.c10-reading,.c10-instruction,.c10-document,.c10-obra-razao), .c10 details[open]:not(.c10-check) > div > p:not([class])')]),
 ('C3','cidadania/m2/sessoes/03/',[('etapas','.c10 :is(.c10-reading,.c10-instruction,.c10-document,.c10-obra-razao), .c10 details[open]:not(.c10-check) > div > p:not([class])')]),
 ('C4','cidadania/m2/aulas/03/',[('J','main > section > p:not([class])'),('E','main ol > li',2)]),
 ('C5','cidadania/ferramentas/m1-aula-01-ficha/',[('J','main > blockquote.citacao'),('E','main label',3),('E','blockquote.citacao cite',1)]),
 ('C6','cidadania/m2/',[('J','.p-cab > p.p-lead'),('J','.pg > p.rodape'),('abrir','details.cid-route'),('J','.cid-route-step > div > p:not([class])'),('J','.pg > details.cid-route > p:not([class])')]),
 ('C7','cidadania/aula-2/',[('J','main.pg > p:not([class])'),('abrir','details.extra-aula'),('J','.pg > details.extra-aula > p:not([class]):not(:has(> a:only-child))'),('E','.pg > details.extra-aula > p:has(> a:only-child)',1)]),
 ('C7','cidadania/m2/glossario/',[('J','.termo > dd')]),
 ('D1','docente/',[('J','.guide-block > p:not([class])'),('J','.guide-page > p.guide-lead'),('E','.guide-route > p',3)]),
 ('D1','docente/resultados/',[('J','.rt-antes')]),
 ('X','curadoria/',[('J','main section > p:not([class])')]),
 ('X','404.html',[('centro','main > p')]),
]

# 30/10/2026: páginas cuja tabela já transbordava a 320 px antes desta mudança (igual em origin/main)
TABELA_LARGA={(320,'vozes/25-de-abril/guiao/')}

def avancar(p):
 # O motor mostra só algumas das opções de cada escolha, e nem sempre a de data-j="0", que a ação partilhada
 # procura: nesse caso escolhe-se a primeira à vista; nos outros casos usa-se a ação partilhada.
 ops=p.locator('#baralho .ops:not(.soltos) button.op')
 livre=not p.locator('.casca [data-c-folha]:visible [data-seguinte], .casca [data-c-acoes] [data-seguinte], #baralho .pares, #baralho .ordem, #baralho [data-tipo-ext="posicao"]').count()
 if livre and ops.count() and not p.locator('#baralho .ops button.op[data-j="0"]').count():ops.first.click();return
 act(p)

def verifica_justificados(p,width,fam,pag,sel,res,minimo=1):
 m=p.evaluate(MEDIR,sel)
 assert len(m)>=minimo,(width,pag,'sem',sel)
 for x in m:
  assert x['ta']=='justify' and x['tal']=='auto',(width,pag,sel,x)
  assert x['hy']=='auto' and x['ws']=='0px' and x['ow']=='break-word',(width,pag,sel,x)
  assert not x['br'],(width,pag,sel,x)
  assert x['linhas']<2 or x['cpl']>=22,(width,pag,sel,'caixa estreita',x)
  # pt-PT (da página ou do próprio texto) ou uma língua estrangeira declarada no texto; nunca «pt» sem variedade nem pt-BR
  assert x['lang']=='pt-PT' or (not x['langDaPagina'] and x['lang'] and not x['lang'].startswith('pt')),(width,pag,sel,x)
 if m:res.append({'familia':fam,'pagina':pag or 'index.html','largura':width,'seletor':sel,'justificados':len(m),'car_linha_min':min(x['cpl'] for x in m),'linguas':sorted({x['lang'] for x in m})})
 return len(m)

def ver(p,width,fam,pag,passos,res):
 for passo in passos:
  tipo,sel=passo[0],passo[1]
  if tipo=='ate':
   p.set_default_timeout(2500)
   for _ in range(60):
    if p.locator(sel).first.is_visible():break
    try:avancar(p)
    except PlaywrightTimeout:pass  # o painel da explicação ainda a abrir: volta a olhar para o cartão
    try:p.locator(sel).first.wait_for(state='visible',timeout=1500)
    except PlaywrightTimeout:pass
   else:raise AssertionError((width,pag,'não chegou a',sel))
   p.set_default_timeout(10000)
   continue
  if tipo=='abrir':
   p.evaluate("(s)=>document.querySelectorAll(s).forEach(d=>{if(d.offsetParent||d.closest('details[open]'))d.open=true})",sel);p.wait_for_timeout(120)
   continue
  if tipo=='etapas':
   # sessões de Cidadania: «Começar» e depois cada um dos cinco passos, com as respostas abertas
   p.locator('[data-start]').click();n=p.locator('[data-stage-link]').count();vistos=0
   assert n>=5,(width,pag,n)
   for k in range(n):
    p.locator('[data-stage-link]').nth(k).click();p.wait_for_timeout(150)
    p.evaluate("document.querySelectorAll('[data-stage] details').forEach(d=>{if(d.offsetParent)d.open=true})")
    vistos+=verifica_justificados(p,width,fam,pag,sel,res,minimo=0)
    for x in p.evaluate(MEDIR,'[data-stage] li, [data-stage] li p'):assert x['ta']!='justify',(width,pag,x)
   assert vistos>=3,(width,pag,'poucos blocos justificados nas etapas',vistos)
   continue
  m=p.evaluate(MEDIR,sel)
  if tipo=='J':verifica_justificados(p,width,fam,pag,sel,res)
  elif tipo=='E':
   assert len(m)>=passo[2],(width,pag,sel,len(m))
   for x in m:assert x['ta']!='justify',(width,pag,sel,x)
  elif tipo=='lang':
   assert m and all(x['lang']==passo[2] for x in m),(width,pag,sel,m[:2])
  elif tipo=='centro':
   assert m and all(x['ta']=='center' for x in m),(width,pag,sel,m)
 # regras gerais da página no estado em que ficou
 nunca=p.evaluate(MEDIR,NUNCA)
 mal=[x for x in nunca if x['ta']=='justify']
 assert not mal,(width,pag,mal[:3])
 if (width,pag) in TABELA_LARGA:
  # 30/10/2026: a tabela do guião já passava a largura a 320 px em origin/main (não vem do texto justificado);
  # confirma-se que é a tabela que transborda e que nenhum bloco justificado sai do ecrã.
  quem=p.evaluate("()=>{let m='',mx=0;for(const e of document.querySelectorAll('body *')){const r=e.getBoundingClientRect();if(r.right>mx+0.5){mx=r.right;m=e.closest('table')?'TABLE':e.tagName}}return m}")
  assert quem=='TABLE',(width,pag,quem)
  assert p.evaluate("()=>[...document.querySelectorAll('body *')].every(e=>getComputedStyle(e).textAlign!=='justify'||e.getBoundingClientRect().right<=innerWidth+0.5)"),(width,pag,'bloco justificado fora do ecrã')
 else:
  assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,pag,'deslocamento horizontal')
 todos=p.evaluate(JUSTIFICADOS)
 assert all(not t.startswith(('li','td','th','button','label','figcaption','summary','h1','h2','h3','h4','h5','h6')) for t in todos),(width,pag,todos[:5])

res=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True)
 # 30/10/2026 (revisão adversarial): também a 320 px, onde as caixas estreitas se notam
 for width in [320,390,1366]:
  for fam,pag,passos in PLANO:
   # contexto novo por página: o progresso guardado de uma lição não muda o cartão de partida de outra
   ctx=b.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
   ctx.route('https://pedrohfernandes-klk.github.io/lente/**',local)
   ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());ctx.route('https://fonts.gstatic.com/**',lambda r:r.abort())
   print(width,pag or 'index.html',file=sys.stderr,flush=True)
   p=ctx.new_page();p.set_default_timeout(10000);erros=[];p.on('pageerror',lambda e:erros.append(str(e)))
   assert p.goto(f'{host}/lente/{pag}').status==200,pag
   p.wait_for_timeout(300)
   ver(p,width,fam,pag,passos,res)
   assert not erros,(width,pag,erros)
   if width==390 and pag in ('narrativas/corta/chuva/','narrativas/desenlace/','biblioteca/garrett-frei-luis-sousa/'):
    p.screenshot(path=str(O/(pag.strip('/').replace('/','_')+f'-{width}.png')))
   ctx.close()
 b.close()
server.shutdown()
familias=sorted({r['familia'] for r in res}|{'X','E1'})
(O/'resultado.json').write_text(json.dumps(res,ensure_ascii=False,indent=1),'utf-8')
print(f'PASS texto justificado: {len(PLANO)} páginas de {len(familias)} famílias a 320, 390 e 1366 px; {sum(r["justificados"] for r in res)} blocos justificados verificados')
