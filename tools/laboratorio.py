"""30/10/2026: páginas de entrada e percursos; dados em assets/laboratorio/percursos.json.
O gerador só escreve navegação, nunca os exercícios nem as suas chaves.
31/10/2026: escreve também a continuação de cada peça (percurso, seguinte, menu e fim dos treinos)
a partir da ordem dos percursos, para que a lista e a peça digam o mesmo.
"""
from pathlib import Path
import json,html,posixpath,re
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'assets/laboratorio/percursos.json').read_text('utf-8'))
IM={x['id']:x for x in json.loads((R/'assets/laboratorio/imagens.json').read_text('utf-8'))}
P={x['id']:x for x in D['pieces']}
ALIAS=D['aliases']
ABS='https://pedrohfernandes-klk.github.io/lente/'
NUM={4:'quatro',5:'cinco',6:'seis',7:'sete',8:'oito'}
e=html.escape
def it(s):return re.sub(r'_(.+?)_',r'<i>\1</i>',e(s))
def link(base,path):return posixpath.relpath(path or '.',base)+('/' if not path or path.endswith('/') else '')
def a(base,path,label,cur=''):return '<a href="'+e(link(base,path))+'"'+(' aria-current="'+cur+'"' if cur else '')+'>'+label+'</a>'
def pic(base,b):
    m=IM[b]
    return ('<figure class="arquivo"><img src="'+link(base,m['file'])+'" width="'+str(m['width'])+'" height="'+str(m['height'])+'" alt="'+e(m['alt'])+'" style="--foco:'+e(m['foco'])+'" loading="lazy">'
            '<figcaption>'+e(m['author'])+', <i>'+e(m['title'])+'</i>, '+e(m['date'])+'. '+(e(m['institution'])+'. ' if m.get('institution') else '')
            +'<a href="'+e(m['source'])+'">Wikimedia Commons</a>, '+e(m['license'])+'.<span class="legenda">'+e(m['reason'])+'</span></figcaption></figure>')
def start(base,ids):
    p=P[ids[0]]
    return '<a class="continuar" data-continuar="'+e(json.dumps(ids))+'" href="'+link(base,p['url'])+'">Começar: '+e(p['title'])+' →</a>'
def steps(base,ids):
    out='<ol class="passos">'
    for n,id in enumerate(ids,1):
        p=P[id]
        out+=('<li data-peca="'+id+'"><a href="'+link(base,p['url'])+'"><span class="n">'+str(n)+'</span><span><strong>'+e(p['title'])+'</strong><span class="descricao">'+it(p['description'])+'</span>'
              +('<small>'+e(p['time'])+'</small>' if p['time'] else '')+'</span><span class="chip" data-estado="'+id+'">por fazer</span></a></li>')
    return out+'</ol>'
def count(ids):return '<p class="contagem" data-contagem="'+e(json.dumps(ids))+'">0 de '+str(len(ids))+' peças feitas</p>'
def extras(base,treinar=False):
    # 31/10/2026: o guia do docente só fala de treinos; «Tudo» diz o que é; sem « / » entre ligações.
    links=[a(base,'narrativas/treinar/caderno/','O caderno de treino'),a(base,'narrativas/treinar/docente/','Como conduzir um treino (docente)')] if treinar else []
    return '<footer class="mais">'+''.join(links+[a(base,'narrativas/tudo/','Tudo o que há no Laboratório')])+'</footer>'
def page(base,title,body,desc,foot=True,treinar=False,cur=None):
    rel=lambda x:link(base,x)
    data=[{k:p[k] for k in ['id','url','title','progress']} for p in D['pieces']]
    data=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    cur=cur or {}
    nav=(a(base,'','Lente')+a(base,'narrativas/','Laboratório',cur.get('lab',''))
         +''.join(a(base,'narrativas/'+b['id']+'/',b['title'],cur.get(b['id'],'')) for b in D['blocks'])+'<span data-appearance-control></span>')
    s=('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>'+(e(title)+' | ' if title!='Laboratório' else '')+'Laboratório | Lente</title><meta name="description" content="'+e(desc)+'">'
       '<link rel="stylesheet" href="'+rel('assets/laboratorio/percursos.css')+'"><link rel="stylesheet" href="'+rel('assets/appearance.css')+'"><script src="'+rel('assets/appearance.js')+'"></script><script defer src="'+rel('assets/laboratorio/percursos.js')+'"></script></head>'
       '<body data-site="lente"><a class="salta" href="#conteudo">Saltar para o conteúdo</a><nav class="barra-nav" aria-label="Navegação">'+nav+'</nav>'
       '<main id="conteudo" data-raiz="'+rel('')+'">'+body+(extras(base,treinar) if foot else '')+'</main><script type="application/json" id="lab-dados">'+data+'</script></body></html>\n')
    p=R/base/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.encode())
def routebox(base,r):
    return '<article class="modulo"><a href="'+link(base,'narrativas/percursos/'+r['id']+'/')+'"><h3>'+e(r['title'])+'</h3><p>'+e(r['question'])+'</p>'+count(r['pieces'])+'<span>Abrir →</span></a></article>'
def routes_of(b):return [r for r in D['routes'] if r['block']==b['id']]
def block_of(r):return next(b for b in D['blocks'] if b['id']==r['block'])

# Entrada
allids=[p for r in D['routes'] for p in r['pieces']]
body='<header class="topo"><p class="marca">Lente</p><h1>Laboratório</h1><div class="lab-saiu"><p class="lead">Observa uma escolha, experimenta uma regra e cria uma peça tua.</p></div></header>'+start('narrativas',allids)+'<div class="blocos">'
for b in D['blocks']:
    rs=routes_of(b);n=NUM.get(len(rs),str(len(rs)))
    body+=('<section class="bloco" id="'+b['anchor']+'"><header><h2>'+b['title']+'</h2><p class="subtitulo">'+b['subtitle']+'</p><p class="pergunta">'+b['question']+'</p>'
           +a('narrativas','narrativas/'+b['id']+'/','Os '+n+' percursos de '+b['title']+' →')+'</header>'+pic('narrativas',b['id'])
           +'<details class="dobra"><summary>Os '+n+' percursos</summary><div class="modulos">'+''.join(routebox('narrativas',r) for r in rs)+'</div></details></section>')
body+=('</div><section class="progresso"><h2>O teu progresso</h2>'+count(allids)+'<p>O que fizeste fica só neste aparelho. Abrir uma peça não a marca como feita.</p>'
       '<div class="registos"><button type="button" data-guardar>Guardar num ficheiro</button><label class="repor"><input type="file" accept="application/json,.json" data-repor>Repor de um ficheiro</label></div>'
       '<p data-registos-aviso role="status">O ficheiro guarda só os estados, sem respostas nem textos.</p></section>')
# 31/10/2026: uma âncora antiga que já não existe aqui leva ao catálogo, onde aponta para o percurso certo.
body+='<script>(function(){function f(){var h=decodeURIComponent(location.hash.slice(1));if(h&&!document.getElementById(h))location.replace("tudo/"+location.search+location.hash)}addEventListener("hashchange",f);f()})()</script>'
page('narrativas','Laboratório',body,'Observa uma escolha, experimenta uma regra e cria uma peça tua: '+str(len(D['routes']))+' percursos em três blocos, Ver, Treinar e Criar.',cur={'lab':'page'})

# Blocos
for b in D['blocks']:
    base='narrativas/'+b['id'];rs=routes_of(b);ids=[p for r in rs for p in r['pieces']]
    body='<header class="topo"><h1>'+b['title']+'</h1><p class="subtitulo">'+b['subtitle']+'</p><p class="pergunta">'+b['question']+'</p></header>'+start(base,ids)+pic(base,b['id'])
    for r in rs:body+='<section class="unidade" id="'+r['id']+'"><h2>'+a(base,'narrativas/percursos/'+r['id']+'/',e(r['title']))+'</h2><p class="pergunta">'+e(r['question'])+'</p>'+count(r['pieces'])+steps(base,r['pieces'])+'</section>'
    page(base,b['title'],body,b['title']+' '+b['subtitle']+'. '+b['question'],treinar=b['id']=='treinar',cur={b['id']:'page'})

# Percursos
for r in D['routes']:
    base='narrativas/percursos/'+r['id'];b=block_of(r)
    antes=''
    if r.get('antes'):q=P[r['antes']['piece']];antes='<p class="antes">'+e(r['antes']['text'])+' '+a(base,q['url'],'«'+e(q['title'])+'»')+'.</p>'
    body='<header class="topo"><p class="marca">'+b['title']+'</p><h1>'+e(r['title'])+'</h1><p class="pergunta">'+e(r['question'])+'</p></header>'+start(base,r['pieces'])+'<section class="unidade">'+antes+count(r['pieces'])+steps(base,r['pieces'])+'</section>'
    page(base,r['title'],body,r['question']+' '+str(len(r['pieces']))+' peças, por ordem.',treinar=b['id']=='treinar',cur={b['id']:'true'})

# Tudo
base='narrativas/tudo';body='<header class="topo"><h1>Tudo o que há no Laboratório</h1></header>'
used=set(ALIAS)
for b in D['blocks']:
    used.add(b['anchor'])
    body+='<section id="'+b['anchor']+'">'+''.join('<span id="'+k+'"></span>' for k,v in ALIAS.items() if v==b['id'])+'<h2>'+b['title']+'</h2><p>'+b['subtitle']+'</p>'
    for r in routes_of(b):
        body+='<h3>'+''.join('<span id="'+k+'"></span>' for k,v in ALIAS.items() if v==r['id'])+a(base,'narrativas/percursos/'+r['id']+'/',e(r['title']))+'</h3><ol class="catalogo">'
        for id in r['pieces']:
            old=id.rsplit('/',1)[-1];attr='' if old in used else ' id="'+old+'"';used.add(old)
            body+='<li'+attr+'>'+a(base,P[id]['url'],e(P[id]['title']))+'</li>'
        body+='</ol>'
    body+='</section>'
body+=''.join('<span id="'+id+'" hidden></span>' for id in D['ancoras'] if id not in used)
body+='<nav class="mais" aria-label="Mais">'+a(base,'narrativas/fora-da-pagina/','Fora da página')+a(base,'narrativas/margens/','Margens')+a(base,'narrativas/formas/?mesa=pt','Pontes para Português')+a(base,'docente/','Área do docente')+'</nav>'
page(base,'Tudo',body,'Todas as peças do Laboratório, por bloco e por percurso.',foot=False,cur={'lab':'true'})

page('narrativas/percursos','Percursos','<header class="topo"><h1>Percursos</h1></header>'+''.join(routebox('narrativas/percursos',r) for r in D['routes']),'Os '+str(len(D['routes']))+' percursos do Laboratório.',cur={'lab':'true'})

# Continuação nas peças (31/10/2026): a ordem vem de percursos.json.
def continuacao():
    route={id:r for r in D['routes'] for id in r['pieces']}
    changed=0
    for p in D['pieces']:
        r=route[p['id']];ids=r['pieces'];i=ids.index(p['id']);nxt=P[ids[i+1]] if i+1<len(ids) else None
        f=R/p['url']/'index.html';s=f.read_text('utf-8');o=s
        rurl=ABS+'narrativas/percursos/'+r['id']+'/'
        # menu da casca: uma só saída, para o percurso
        s=re.sub(r'</ol><a href="[^"]*">(?:Voltar ao ginásio|Voltar ao Laboratório|Voltar ao percurso|Voltar a Treinar)</a>','</ol><a href="'+rurl+'">Voltar ao percurso</a>',s)
        # configuração do motor
        if 'EPIJogo.montar(' in s and 'percurso:"' in s:
            s=re.sub(r'percurso:"'+re.escape(ABS)+r'narrativas/percursos/[^"/]+/"','percurso:"'+rurl+'"',s)
            s=re.sub(r',seguinte:"[^"]*",seguinteRotulo:"[^"]*"','',s)
            if nxt:s=s.replace('voltarRotulo:"Voltar ao percurso"','voltarRotulo:"Voltar ao percurso",seguinte:"'+ABS+nxt['url']+'",seguinteRotulo:"Seguinte"',1)
            # fim dos treinos: o texto aponta para o mesmo sítio que o botão
            fim=('Seguinte: <a href=\\"'+ABS+nxt['url']+'\\">'+e(nxt['title'],quote=False)+'</a>') if nxt else '<a href=\\"'+rurl+'\\">Voltar ao percurso</a>'
            s=re.sub(r'(<p class=\\"sub\\">)(?:Treino seguinte: |Seguinte: )?<a href=\\"[^"\\]*\\">[^<]*</a>(\. Ou volta a este noutro dia: repetir é treinar\.)',lambda m:m.group(1)+fim+m.group(2),s)
        # páginas sem motor: nav.lab-fim-percurso
        def nav(m):
            rel=lambda u:posixpath.relpath(u.rstrip('/'),p['url'].rstrip('/'))+'/'
            return m.group(1)+'<a href="'+rel('narrativas/percursos/'+r['id']+'/')+'">Voltar ao percurso</a>'+(' <a href="'+rel(nxt['url'])+'">Seguinte: '+e(nxt['title'])+' →</a>' if nxt else '')+'</nav>'
        s=re.sub(r'(<nav class="lab-fim-percurso"[^>]*>).*?</nav>',nav,s,flags=re.S)
        if s!=o:f.write_text(s,'utf-8');changed+=1
    return changed
continuacao()
print('23 páginas geradas; 93 peças preservadas.')
