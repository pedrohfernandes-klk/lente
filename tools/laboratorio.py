"""30/10/2026: páginas de entrada e percursos; dados em assets/laboratorio/percursos.json.
O gerador só escreve navegação, nunca os exercícios nem as suas chaves.
31/10/2026: escreve também a continuação de cada peça (percurso, seguinte, menu e fim dos treinos)
a partir da ordem dos percursos, para que a lista e a peça digam o mesmo.
31/10/2026 (segunda correção): <title> e rótulo dos treinos também a partir dos percursos; uma peça
fora dos percursos (decisão 34: «Três cartas») continua no endereço e volta ao seu bloco.
31/10/2026 (terceira correção): a dobra diz «Mostrar» ou «Esconder» conforme o estado; a casca de todas as
peças apresenta-se como «Laboratório» (marca, cabeçalho do menu e «LAB»).
"""
from pathlib import Path
import json,html,posixpath,re
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'assets/laboratorio/percursos.json').read_text('utf-8'))
IM={x['id']:x for x in json.loads((R/'assets/laboratorio/imagens.json').read_text('utf-8'))}
P={x['id']:x for x in D['pieces']}
ALIAS=D['aliases']
INROUTE={id for r in D['routes'] for id in r['pieces']}
ABS='https://pedrohfernandes-klk.github.io/lente/'
NUM={4:'quatro',5:'cinco',6:'seis',7:'sete',8:'oito'}
e=html.escape
def it(s):return re.sub(r'_(.+?)_',r'<i>\1</i>',e(s))
def link(base,path):return posixpath.relpath(path or '.',base)+('/' if not path or path.endswith('/') else '')
def a(base,path,label,cur=''):return '<a href="'+e(link(base,path))+'"'+(' aria-current="'+cur+'"' if cur else '')+'>'+label+'</a>'
def credito(m):
    # Tabela de museu: autor, obra (itálico com _…_), data, técnica, instituição, Commons e licença.
    return (e(m['author'])+', '+it(m['title'])+(', '+e(m['date']) if m.get('date') else '')+'. '+(e(m['technique'])+'. ' if m.get('technique') else '')
            +(e(m['institution'])+'. ' if m.get('institution') else '')+'<a href="'+e(m['source'])+'">Wikimedia Commons</a>. '+e(m['license'])+'.')
def pic(base,b):
    m=IM[b]
    return ('<figure class="arquivo"><img src="'+link(base,m['file'])+'" width="'+str(m['width'])+'" height="'+str(m['height'])+'" alt="'+e(m['alt'])+'" style="--foco:'+e(m['foco'])+'" loading="lazy">'
            '<figcaption>'+credito(m)+'<span class="legenda">'+e(m['reason'])+'</span></figcaption></figure>')
def start(base,ids):
    p=P[ids[0]]
    return '<a class="continuar" data-continuar="'+e(json.dumps(ids))+'" href="'+link(base,p['url'])+'">Começar: '+e(p['title'])+'\u00a0→</a>'
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
# 01/11/2026: decisão 57. Migração limitada às quatro entradas; restantes moldes intactos.
CARTAZ_ENTRADAS={'narrativas','narrativas/ver','narrativas/treinar','narrativas/criar'}
def cartaz_body(base,body):
    body=re.sub(r'\bVer\b','Observar',body)
    # 01/11/2026: a mesma peça de continuação tem título, estado e uma ação.
    def next_region(m):
        ids=json.loads(html.unescape(re.search(r'data-continuar="([^"]+)"',m[0])[1]))
        return '<section class="cz-next" aria-labelledby="cz-prox"><p class="cz-label">A seguir</p><h2 id="cz-prox">'+e(P[ids[0]]['title'])+'</h2><p data-cz-estado></p>'+m[0]+'</section>'
    body=re.sub(r'<a class="continuar".*?</a>',next_region,body,count=1,flags=re.S)
    body=body.replace('class="continuar"','class="continuar cz-button primary"')
    body=body.replace('class="arquivo"','class="arquivo cz-museum"').replace('<figcaption>','<figcaption class="cz-credit">')
    body=re.sub(r'<a href="(https://commons.wikimedia.org/[^"]+)"',r'<a data-external aria-label="Wikimedia Commons, sítio externo" href="\1"',body)
    body=body.replace('class="dobra"','class="dobra cz-fold" open')
    body=body.replace('class="chip"','class="chip cz-state"').replace('>por fazer</span>','></span>')
    body=re.sub(r'(<li data-peca="[^"]+"><a)( href=)',r'\1 class="cz-row"\2',body)
    body=body.replace(' data-estado=', ' data-estado=')
    body=re.sub(r'(<span class="chip cz-state"[^>]*>.*?</span>)(</a>)',r'\1<span class="arrow" aria-hidden="true">→</span>\2',body)
    if base=='narrativas':
        groups=iter(D['blocks'])
        def group(m):
            b=next(groups);ids=[id for r in routes_of(b) for id in r['pieces']]
            return '<details class="dobra cz-fold" open data-cz-ids="'+e(json.dumps(ids))+'">'
        body=re.sub(r'<details class="dobra cz-fold" open>',group,body)
    if base!='narrativas':
        def fold(m):
            ident,title,rest=m.groups()
            label=re.sub('<[^>]*>','',title)
            href=re.search(r'href="([^"]+)"',title)[1]
            return '<details class="unidade cz-fold" id="'+ident+'" open><summary><h2>'+label+'</h2></summary><div class="cz-fold-body"><a class="cz-button" href="'+href+'">Abrir o percurso →</a>'+rest+'</div></details>'
        body=re.sub(r'<section class="unidade" id="([^"]+)"><h2>(.*?)</h2>(.*?)</section>',fold,body,flags=re.S)
    return body

def page(base,title,body,desc,foot=True,treinar=False,cur=None):
    if '--cartaz-entradas' in __import__('sys').argv and base not in CARTAZ_ENTRADAS:return
    rel=lambda x:link(base,x)
    migrated=base in CARTAZ_ENTRADAS
    if migrated:
        body=cartaz_body(base,body)
        title=re.sub(r'\bVer\b','Observar',title)
        desc=re.sub(r'\bVer\b','Observar',desc)
    # 31/10/2026: só as peças que estão num percurso (uma peça fora dos percursos não conta nem se guarda aqui).
    data=[{k:p[k] for k in ['id','url','title','progress']} for p in D['pieces'] if p['id'] in INROUTE]
    data=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    cur=cur or {}
    nav=(a(base,'','Lente')+a(base,'narrativas/','Laboratório',cur.get('lab',''))
         +''.join(a(base,'narrativas/'+b['id']+'/',b['title'],cur.get(b['id'],'')) for b in D['blocks'])+'<span data-appearance-control></span>')
    s=('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>'+(e(title)+' | ' if title!='Laboratório' else '')+'Laboratório | Lente</title><meta name="description" content="'+e(desc)+'">'
       '<link rel="stylesheet" href="'+rel('assets/laboratorio/percursos.css')+'"><link rel="stylesheet" href="'+rel('assets/appearance.css')+'"><script src="'+rel('assets/appearance.js')+'"></script><script defer src="'+rel('assets/laboratorio/percursos.js')+'"></script></head>'
       '<body data-site="lente"><a class="salta" href="#conteudo">Saltar para o conteúdo</a><nav class="barra-nav" aria-label="Navegação">'+nav+'</nav>'
       '<main id="conteudo" data-raiz="'+rel('')+'">'+body+(extras(base,treinar) if foot else '')+'</main><script type="application/json" id="lab-dados">'+data+'</script></body></html>\n')
    if migrated:
        s=s.replace('<main id="conteudo"','<main data-cartaz="2" data-cartaz-laboratorio id="conteudo"')
        s=s.replace('class="mais"','class="mais cz-footer"')
        s=s.replace(rel('assets/appearance.css')+'"',rel('assets/appearance.css')+'?v=20261101-1"')
        s=s.replace('</head>','<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;display=swap" media="print" onload="this.media=\'all\'"><link rel="stylesheet" href="'+rel('assets/cartaz-components.css')+'?v=20261101-1"><link rel="stylesheet" href="'+rel('assets/laboratorio/cartaz.css')+'?v=20261101-1"><script defer src="'+rel('assets/laboratorio/cartaz.js')+'?v=20261101-1"></script><script defer src="'+rel('assets/cartaz-components.js')+'?v=20261101-1"></script></head>')
    p=R/base/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.encode())
def routebox(base,r):
    if base=='narrativas':
        number=next(i for i,x in enumerate(routes_of(block_of(r)),1) if x['id']==r['id'])
        return '<article class="modulo"><a class="cz-row" data-cz-route="'+e(json.dumps(r['pieces']))+'" href="'+link(base,'narrativas/percursos/'+r['id']+'/')+'"><b>'+str(number)+'</b><div><h3>'+e(r['title'])+'</h3><small>'+e(r['question'])+'</small>'+count(r['pieces'])+'</div><span class="cz-state"></span><span class="arrow" aria-hidden="true">→</span></a></article>'
    return '<article class="modulo"><a href="'+link(base,'narrativas/percursos/'+r['id']+'/')+'"><h3>'+e(r['title'])+'</h3><p>'+e(r['question'])+'</p>'+count(r['pieces'])+'<span>Abrir →</span></a></article>'
def routes_of(b):return [r for r in D['routes'] if r['block']==b['id']]
def block_of(r):return next(b for b in D['blocks'] if b['id']==r['block'])

# Entrada
allids=[p for r in D['routes'] for p in r['pieces']]
body='<header class="topo"><p class="marca">Lente</p><h1>Laboratório</h1><div class="lab-saiu"><p class="lead">Observa uma escolha, experimenta uma regra e cria uma peça tua.</p></div></header>'+start('narrativas',allids)+'<div class="blocos">'
for b in D['blocks']:
    rs=routes_of(b);n=NUM.get(len(rs),str(len(rs)))
    body+=('<section class="bloco" id="'+b['anchor']+'"><header><h2>'+b['title']+'</h2><p class="subtitulo">'+b['subtitle']+'</p><p class="pergunta">'+b['question']+'</p>'
           +a('narrativas','narrativas/'+b['id']+'/','Os '+n+' percursos do bloco '+b['title']+'\u00a0→')+'</header>'+pic('narrativas',b['id'])
           +'<details class="dobra"><summary><span class="abrir">Mostrar os '+n+' percursos</span><span class="fechar">Esconder os '+n+' percursos</span></summary><div class="modulos">'+''.join(routebox('narrativas',r) for r in rs)+'</div></details></section>')
body+=('</div><section class="progresso"><h2>O teu progresso</h2>'+count(allids)+'<p>O que fizeste fica só neste aparelho. Abrir uma peça não a marca como feita.</p>'
       '<div class="registos"><button type="button" data-guardar>Guardar num ficheiro</button><label class="repor"><input type="file" accept="application/json,.json" data-repor>Repor de um ficheiro</label></div>'
       '<p data-registos-aviso role="status">O ficheiro guarda só os estados, sem respostas nem textos.</p></section>')
# 31/10/2026: uma âncora antiga que já não existe aqui leva ao catálogo, onde aponta para o percurso certo.
body+='<script>(function(){function f(){var h=decodeURIComponent(location.hash.slice(1));if(h&&!document.getElementById(h))location.replace("tudo/"+location.search+location.hash)}addEventListener("hashchange",f);f()})()</script>'
page('narrativas','Laboratório',body,'Observa uma escolha, experimenta uma regra e cria uma peça tua: '+str(len(D['routes']))+' percursos em três blocos (Observar, Treinar e Criar).',cur={'lab':'page'})

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
    page(base,r['title'],body,r['question']+' '+NUM[len(r['pieces'])].capitalize()+' peças, por ordem.',treinar=b['id']=='treinar',cur={b['id']:'true'})

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
    blocks={b['id']:b for b in D['blocks']}
    changed=0
    for p in D['pieces']:
        r=route.get(p['id'])
        f=R/p['url']/'index.html';s=f.read_text('utf-8');o=s
        if r:
            ids=r['pieces'];i=ids.index(p['id']);nxt=P[ids[i+1]] if i+1<len(ids) else None
            b=blocks[r['block']];rurl=ABS+'narrativas/percursos/'+r['id']+'/';rpath='narrativas/percursos/'+r['id']+'/';back='Voltar ao percurso'
        else:
            # fora dos percursos (decisão 34): volta ao bloco, sem «Seguinte»
            nxt=None;b=blocks[p['block']];rurl=ABS+'narrativas/'+b['id']+'/';rpath='narrativas/'+b['id']+'/';back='Voltar a '+b['title']
        # <title> igual em todas as peças: título | bloco | Laboratório | Lente
        s=re.sub(r'<title>[^<]*</title>','<title>'+e(p['title'],quote=False)+' | '+b['title']+' | Laboratório | Lente</title>',s,count=1)
        # 31/10/2026 (terceira correção): a casca apresenta-se como «Laboratório» em todas as peças (decisão 15):
        # marca do motor, ligação da marca na casca, cabeçalho do menu (sem tocar nas migalhas «Estás em:») e «LAB».
        s=re.sub(r'marca:"[^"]*"','marca:"Laboratório"',s)
        s=re.sub(r'(class="c-menu-cab"><p>)(?!Estás em:)[^<]*(</p>)',r'\1Laboratório\2',s)
        s=re.sub(r'(<a class="c-marca"[^>]*>)LAB(</a>)',r'\1Laboratório\2',s)
        s=re.sub(r'(<a class="c-marca" href="[^"]*" aria-label="Página inicial \()[^)"]*(\)">(?:<svg[^>]*>.*?</svg>)?)[^<]*(</a>)',r'\1Laboratório\2Laboratório\3',s)
        # 31/10/2026 (releitura): a marca «Laboratório» leva ao Laboratório e o nome acessível é o texto visível
        s=re.sub(r'(<a class="c-marca" href=")[^"]*(" aria-label=")[^"]*(")',r'\g<1>'+ABS+r'narrativas/\g<2>Laboratório\g<3>',s)
        # rótulo dos treinos com o nome do percurso
        if r and p['id'].startswith('treinar/'):
            s=re.sub(r'(<p class=\\"etq-m\\">Treino · )[^·<]+?( · )',lambda m:m.group(1)+e(r['title'],quote=False)+m.group(2),s)
        # menu da casca: uma só saída, para o percurso
        s=re.sub(r'</ol><a href="[^"]*">(?:Voltar ao ginásio|Voltar ao Laboratório|Voltar ao percurso|Voltar a Treinar|Voltar a Ver|Voltar a Criar)</a>','</ol><a href="'+rurl+'">'+back+'</a>',s)
        # configuração do motor
        if 'EPIJogo.montar(' in s and 'percurso:"' in s:
            s=re.sub(r'percurso:"'+re.escape(ABS)+r'narrativas/percursos/[^"/]+/"','percurso:"'+rurl+'"',s)
            s=re.sub(r',seguinte:"[^"]*",seguinteRotulo:"[^"]*"','',s)
            if nxt:s=s.replace('voltarRotulo:"Voltar ao percurso"','voltarRotulo:"Voltar ao percurso",seguinte:"'+ABS+nxt['url']+'",seguinteRotulo:"Seguinte"',1)
            # fim dos treinos: o texto aponta para o mesmo sítio que o botão
            fim=('Seguinte: <a href=\\"'+ABS+nxt['url']+'\\">'+e(nxt['title'],quote=False)+'</a>') if nxt else 'É o último treino deste percurso: <a href=\\"'+rurl+'\\">regressa à lista</a>'
            s=re.sub(r'(<p class=\\"sub\\">)(?:Treino seguinte: |Seguinte: |É o último treino deste percurso: )?<a href=\\"[^"\\]*\\">[^<]*</a>(\. Ou volta a este noutro dia: repetir é treinar\.)',lambda m:m.group(1)+fim+m.group(2),s)
        # páginas sem motor: nav.lab-fim-percurso
        def nav(m):
            rel=lambda u:posixpath.relpath(u.rstrip('/'),p['url'].rstrip('/'))+'/'
            return m.group(1)+'<a href="'+rel(rpath)+'">'+back+'</a>'+(' <a href="'+rel(nxt['url'])+'">Seguinte: '+e(nxt['title'])+'\u00a0→</a>' if nxt else '')+'</nav>'
        s=re.sub(r'(<nav class="lab-fim-percurso"[^>]*>).*?</nav>',nav,s,flags=re.S)
        if s!=o:f.write_text(s,'utf-8');changed+=1
    return changed
if '--cartaz-entradas' not in __import__('sys').argv:continuacao()

# Mapa do Lente (31/10/2026, terceira correção): a secção do Laboratório sai de percursos.json, como narrativas/tudo/:
# Ver, Treinar e Criar, com os 17 percursos e as peças de cada um, pela ordem do Laboratório.
def mapa():
    f=R/'mapa/index.html';s=f.read_text('utf-8')
    ini='<section class="map-section"><h2><a href="'+ABS+'narrativas/">';i=s.index(ini);j=s.index('</section>',i)+len('</section>')
    seta=' <span aria-hidden="true">→</span>'
    def ramo(nome,abrir,dentro,extra=''):
        return ('<li><details class="map-branch"><summary><span>'+nome+'</span><b aria-hidden="true">+</b></summary><div class="map-branch-body">'
                '<p class="map-open"><a href="'+abrir+'">Abrir '+nome+seta+'</a></p>'+extra+'<ul class="map-tree">'+dentro+'</ul></div></details></li>')
    out=ini+'Laboratório</a></h2><p class="map-open"><a href="'+ABS+'narrativas/tudo/">Tudo o que há no Laboratório'+seta+'</a></p><ul class="map-tree">'
    for b in D['blocks']:
        extra=('<p class="map-open"><a href="'+ABS+'narrativas/treinar/caderno/">O caderno de treino</a></p><p class="map-open"><a href="'+ABS+'narrativas/treinar/docente/">Como conduzir um treino (docente)</a></p>') if b['id']=='treinar' else ''
        rs=''.join(ramo(e(r['title']),ABS+'narrativas/percursos/'+r['id']+'/',''.join('<li class="map-leaf"><a href="'+ABS+P[id]['url']+'">'+e(P[id]['title'])+'</a></li>' for id in r['pieces'])) for r in routes_of(b))
        out+=ramo(b['title'],ABS+'narrativas/'+b['id']+'/',rs,extra)
    mais=[('narrativas/fora-da-pagina/','Fora da página'),('narrativas/margens/','Margens'),('narrativas/formas/?mesa=pt','Pontes para Português'),('dar-forma-as-palavras/','Dar forma às palavras'),('projetos/','Projetos'),('docente/','Área do docente')]
    out+='</ul>'+''.join('<p class="map-open"><a href="'+ABS+u+'">'+t+'</a></p>' for u,t in mais)+'</section>'
    s2=s[:i]+out+s[j:]
    if s2!=s:f.write_text(s2,'utf-8')
if '--cartaz-entradas' not in __import__('sys').argv:mapa()
print(('4 entradas geradas; ' if '--cartaz-entradas' in __import__('sys').argv else '23 páginas geradas; ')+str(len(INROUTE))+' peças nos percursos; '+str(len(P))+' peças preservadas.')
