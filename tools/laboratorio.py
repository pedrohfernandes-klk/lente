"""30/10/2026: páginas de entrada e percursos; dados em assets/laboratorio/percursos.json.
O gerador só escreve navegação, nunca os exercícios nem as suas chaves.
"""
from pathlib import Path
import json,html,posixpath
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'assets/laboratorio/percursos.json').read_text('utf-8'))
IM={x['id']:x for x in json.loads((R/'assets/laboratorio/imagens.json').read_text('utf-8'))}
P={x['id']:x for x in D['pieces']}
e=html.escape
def link(base,path):return posixpath.relpath(path or '.',base)+('/' if not path or path.endswith('/') else '')
def a(base,path,label):return '<a href="'+e(link(base,path))+'">'+label+'</a>'
def pic(base,b):
    m=IM[b]
    return '<figure class="arquivo"><img src="'+link(base,m['file'])+'" width="'+str(m['width'])+'" height="'+str(m['height'])+'" alt="'+e(m['alt'])+'" loading="lazy"><figcaption>'+e(m['author']+', '+m['title']+', '+m['date']+'. '+m['license']+'. ')+'<a href="'+e(m['source'])+'">Fonte</a><span>'+e(m['reason'])+'</span></figcaption></figure>'
def start(base,ids):
    p=P[ids[0]]
    return '<a class="continuar" data-continuar="'+e(json.dumps(ids))+'" href="'+link(base,p['url'])+'">Começar: '+e(p['title'])+' →</a>'
def steps(base,ids):
    out='<ol class="passos">'
    for n,id in enumerate(ids,1):
        p=P[id]
        out+='<li data-peca="'+id+'"><a href="'+link(base,p['url'])+'"><span class="n">'+str(n)+'</span><span><strong>'+e(p['title'])+'</strong><span class="descricao">'+e(p['description'])+'</span><small>'+e(p['time'])+'</small></span><span class="chip" data-estado="'+id+'">por fazer</span></a></li>'
    return out+'</ol>'
def count(ids):return '<p class="contagem" data-contagem="'+e(json.dumps(ids))+'">0 de '+str(len(ids))+' peças feitas</p>'
def extras(base):return '<footer class="mais">'+a(base,'narrativas/treinar/caderno/','Caderno de treino')+' / '+a(base,'narrativas/treinar/docente/','Guia do docente')+' / '+a(base,'narrativas/tudo/','Tudo')+'</footer>'
def page(base,title,body,scope=''):
    rel=lambda x:link(base,x)
    data=[{k:p[k] for k in ['id','url','title','progress']} for p in D['pieces']]
    data=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    s='<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+' | Laboratório | Lente</title><link rel="stylesheet" href="'+rel('assets/laboratorio/percursos.css')+'"><link rel="stylesheet" href="'+rel('assets/appearance.css')+'"><script src="'+rel('assets/appearance.js')+'"></script><script defer src="'+rel('assets/laboratorio/percursos.js')+'"></script></head><body data-site="lente"><a class="salta" href="#conteudo">Saltar para o conteúdo</a><nav class="barra-nav" aria-label="Navegação">'+a(base,'','Lente')+a(base,'narrativas/','Laboratório')+''.join(a(base,'narrativas/'+b['id']+'/',b['title']) for b in D['blocks'])+'</nav><main id="conteudo" data-raiz="'+rel('')+'">'+body+extras(base)+'</main><script type="application/json" id="lab-dados">'+data+'</script></body></html>\n'
    p=R/base/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.encode())
def routebox(base,r):
    return '<article class="modulo"><a href="'+link(base,'narrativas/percursos/'+r['id']+'/')+'"><h3>'+e(r['title'])+'</h3><p>'+e(r['question'])+'</p>'+count(r['pieces'])+'<span>Abrir →</span></a></article>'
allids=[p for r in D['routes'] for p in r['pieces']]
body='<header class="topo"><p class="marca">Lente</p><h1>Laboratório</h1><div class="lab-saiu"><p class="lead">Observa uma escolha, experimenta uma regra e cria uma peça tua.</p></div></header>'+start('narrativas',allids)+'<div class="blocos">'
for b in D['blocks']:
    routes=[r for r in D['routes'] if r['block']==b['id']]
    body+='<section class="bloco" id="'+b['anchor']+'"><header><h2>'+b['title']+'</h2><p class="subtitulo">'+b['subtitle']+'</p><p class="pergunta">'+b['question']+'</p>'+a('narrativas','narrativas/'+b['id']+'/','Abrir '+b['title']+' →')+'</header>'+pic('narrativas',b['id'])+'<div class="modulos">'+''.join(routebox('narrativas',r) for r in routes)+'</div></section>'
body+='</div><section class="progresso"><h2>O teu progresso</h2>'+count(allids)+'<p>O que fizeste fica só neste aparelho. Abrir uma peça não a marca como feita.</p>'+'<div class="registos"><button type="button" data-guardar>Guardar progresso</button><label>Repor progresso <input type="file" accept="application/json,.json" data-repor></label></div><p data-registos-aviso role="status">O ficheiro guarda só os estados, sem respostas nem textos.</p>'+'</section><details class="mais"><summary>Mais</summary>'+a('narrativas','narrativas/tudo/','Tudo o que há no Laboratório')+'</details>'
body+=''.join('<span id="'+id+'" hidden></span>' for id in json.loads((R/'tests/lab-manifesto.json').read_text('utf-8'))['ancoras']['narrativas/'] if id not in {b['anchor'] for b in D['blocks']})
page('narrativas','Laboratório',body)
for b in D['blocks']:
    base='narrativas/'+b['id'];routes=[r for r in D['routes'] if r['block']==b['id']];ids=[p for r in routes for p in r['pieces']]
    body='<header class="topo"><h1>'+b['title']+'</h1><p class="subtitulo">'+b['subtitle']+'</p><p class="pergunta">'+b['question']+'</p></header>'+start(base,ids)+pic(base,b['id'])
    for r in routes:body+='<section class="unidade" id="'+r['id']+'"><h2>'+a(base,'narrativas/percursos/'+r['id']+'/',e(r['title']))+'</h2><p class="pergunta">'+e(r['question'])+'</p>'+count(r['pieces'])+steps(base,r['pieces'])+'</section>'
    page(base,b['title'],body)
for r in D['routes']:
    base='narrativas/percursos/'+r['id'];b=next(b for b in D['blocks'] if b['id']==r['block'])
    body='<header class="topo"><p class="marca">'+b['title']+'</p><h1>'+e(r['title'])+'</h1><p class="pergunta">'+e(r['question'])+'</p></header>'+start(base,r['pieces'])+'<section class="unidade">'+count(r['pieces'])+steps(base,r['pieces'])+'</section>'
    page(base,r['title'],body)
base='narrativas/tudo';body='<header class="topo"><h1>Tudo o que há no Laboratório</h1></header>'
anchors=json.loads((R/'tests/lab-manifesto.json').read_text('utf-8'))['ancoras'].get('narrativas/',[])
used=set()
for b in D['blocks']:
    used.add(b['anchor']);body+='<section id="'+b['anchor']+'"><h2>'+b['title']+'</h2><p>'+b['subtitle']+'</p>'
    for r in [r for r in D['routes'] if r['block']==b['id']]:
        body+='<h3>'+a(base,'narrativas/percursos/'+r['id']+'/',e(r['title']))+'</h3><ol class="catalogo">'
        for id in r['pieces']:
            old=id.rsplit('/',1)[-1];attr='' if old in used else ' id="'+old+'"';used.add(old)
            body+='<li'+attr+'>'+a(base,P[id]['url'],e(P[id]['title']))+'</li>'
        body+='</ol>'
    body+='</section>'
body+=''.join('<span id="'+id+'" hidden></span>' for id in anchors if id not in used)
body+='<p>'+a(base,'narrativas/fora-da-pagina/','Fora da página')+' / '+a(base,'narrativas/margens/','Margens')+' / '+a(base,'narrativas/formas/?mesa=pt','Pontes para Português')+' / '+a(base,'docente/','Área do docente')+'</p>'
page(base,'Tudo',body)
print('22 páginas geradas; 93 peças preservadas.')

page('narrativas/percursos','Percursos','<header class="topo"><h1>Percursos</h1></header>'+''.join(routebox('narrativas/percursos',r) for r in D['routes']))
