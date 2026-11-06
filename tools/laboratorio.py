"""30/10/2026: páginas de entrada e percursos; dados em assets/laboratorio/percursos.json.
O gerador só escreve navegação, nunca os exercícios nem as suas chaves.
31/10/2026: escreve também a continuação de cada peça (percurso, seguinte, menu e fim dos treinos)
a partir da ordem dos percursos, para que a lista e a peça digam o mesmo.
31/10/2026 (segunda correção): <title> e rótulo dos treinos também a partir dos percursos; uma peça
fora dos percursos (decisão 34: «Três cartas») continua no endereço e volta ao seu bloco.
31/10/2026 (terceira correção): a dobra diz «Mostrar» ou «Esconder» conforme o estado; a casca de todas as
peças apresenta-se como «Laboratório» (marca, cabeçalho do menu e «LAB»).
05/11/2026: decisão 163 (menus do Laboratório). Todas as páginas do gerador passam ao mesmo molde (data-lab="3",
assets/laboratorio/lab3.css): uma só barra «Lente › Laboratório» (tools/lab_nav.py), o fio do método (Ideias, Observar,
Treinar, Criar, com os passos), a entrada com uma só ligação por porta, as portas e os percursos com linhas sempre
abertas e «Daqui segues para» no fim. Sai a barra preta e saem as dobras. Os ids, as âncoras, os destinos, lab-dados,
lab-retiradas e as chaves de progresso ficam todos. No fim de um percurso há sempre um «a seguir» (percurso seguinte, porta
seguinte ou o Ideias) e o menu ≡ das peças vem de tools/menu_casca.py.
"""
from pathlib import Path
import json,html,posixpath,re,importlib.util,sys
R=Path(__file__).resolve().parents[1]
# 02/11/2026: decisão 115, apresentação sem pontos nas peças incorporadas.
_sp=importlib.util.spec_from_file_location('laboratorio_sem_pontos',R/'tools/laboratorio_sem_pontos.py')
SP=importlib.util.module_from_spec(_sp);_sp.loader.exec_module(SP)
sys.path.insert(0,str(R/'tools'))
import lab_nav as LN, menu_casca as MC
D=json.loads((R/'assets/laboratorio/percursos.json').read_text('utf-8'))
IM={x['id']:x for x in json.loads((R/'assets/laboratorio/imagens.json').read_text('utf-8'))}
P={p['id']:p for p in D['pieces']}
ALIAS=D['aliases']
INROUTE={id for r in D['routes'] for id in r['pieces']}
ABS='https://pedrohfernandes-klk.github.io/lente/'
# 05/11/2026: decisão 147. Ids das peças retiradas, para a reposição de um ficheiro antigo as ignorar.
RETIDS=json.dumps([x['peca'] for x in json.loads((R/'assets/laboratorio/retiradas.json').read_text('utf-8'))['retiradas'] if x.get('peca')])
NUM={2:'dois',3:'três',4:'quatro',5:'cinco',6:'seis',7:'sete',8:'oito'}
e=html.escape
def it(s):return re.sub(r'_(.+?)_',r'<i>\1</i>',e(s))
link=LN.link
def a(base,path,label,cur=''):return '<a href="'+e(link(base,path))+'"'+(' aria-current="'+cur+'"' if cur else '')+'>'+label+'</a>'
def credito(m):
    # Tabela de museu: autor, obra (itálico com _…_), data, técnica, instituição, Commons e licença.
    return (e(m['author'])+', '+it(m['title'])+(', '+e(m['date']) if m.get('date') else '')+'. '+(e(m['technique'])+'. ' if m.get('technique') else '')
            +(e(m['institution'])+'. ' if m.get('institution') else '')+'<a data-external aria-label="Wikimedia Commons, sítio externo" href="'+e(m['source'])+'">Wikimedia Commons</a>. '+e(m['license'])+'.')
def figura(base,b):
    # 05/11/2026: decisão 163, com a peça comum do «i» (decisão 153): imagem no tratamento das portas do Cartaz, legenda à vista
    # (diz o que se vê) e o crédito por extenso dentro do «i»; na impressão o «i» abre-se.
    m=IM[b]
    return ('<figure class="lab-figura"><div class="moldura com-i" style="--foco:'+e(m['foco'])+'"><img src="'+link(base,m['file'])+'" width="'+str(m['width'])+'" height="'+str(m['height'])+'" alt="'+e(m['alt'])+'" loading="lazy">'
            '<details class="info-i"><summary aria-label="Créditos da imagem"><span aria-hidden="true">i</span></summary><p class="info-i-texto">'+credito(m)+'</p></details></div>'
            '<figcaption class="legenda">'+e(m['reason'])+'</figcaption></figure>')
def routes_of(b):return [r for r in D['routes'] if r['block']==b['id']]
def block_of(r):return next(b for b in D['blocks'] if b['id']==r['block'])
def passos_de(r):return r.get('passos') or block_of(r)['passos']
def start(base,ids):
    # 02/11/2026: decisão 134 (docente). Sem a caixa «A seguir»: a ligação de continuar fica escondida, só para o progresso
    # marcar a peça seguinte nas linhas.
    p=P[ids[0]]
    return '<a class="continuar" hidden data-continuar="'+e(json.dumps(ids))+'" href="'+link(base,p['url'])+'">Começar: '+e(p['title'])+' →</a>'
def linhas(base,ids):
    # 05/11/2026: decisão 163. Linhas do sistema (Cartaz 6.5): alvo inteiro, número, título, descrição inteira, tempo e estado.
    out='<ol class="linhas">'
    for n,id in enumerate(ids,1):
        p=P[id]
        out+=('<li data-peca="'+id+'"><a class="linha" href="'+link(base,p['url'])+'"><span class="n" aria-hidden="true">'+str(n)+'</span>'
              '<span class="t"><strong>'+e(p['title'])+'</strong><span class="apoio">'+it(p['description'])+'</span>'
              +('<small>'+e(p['time'])+'</small>' if p['time'] else '')+'</span><span class="etq" data-estado="'+id+'"></span><span class="seta" aria-hidden="true">→</span></a></li>')
    return out+'</ol>'
def count(ids,hidden=True):return '<p class="contagem" data-contagem="'+e(json.dumps(ids))+'"'+(' hidden' if hidden else '')+'>0 de '+str(len(ids))+' peças feitas</p>'
def extras(base,treinar=False):
    # 31/10/2026: o guia do docente só fala de treinos; «Tudo» diz o que é; sem « / » entre ligações.
    links=[a(base,'narrativas/treinar/caderno/','O caderno de treino'),a(base,'narrativas/treinar/docente/','Como conduzir um treino (docente)')] if treinar else []
    return '<footer class="mais">'+''.join(links+[a(base,'narrativas/tudo/','Tudo o que há no Laboratório →')])+'</footer>'
def depois(base,itens):
    # 05/11/2026: decisão 163. «Daqui segues para»: o passo seguinte (ou o Ideias) e o regresso, nunca um beco.
    return ('<nav class="depois" aria-label="Daqui segues para">'+''.join('<a href="'+e(link(base,h))+'"><span><small>'+k+'</small><b>'+t+'</b></span><span class="seta" aria-hidden="true">→</span></a>' for k,h,t in itens)+'</nav>')
def passo_seguinte(b):
    i=D['blocks'].index(b)
    if i+1<len(D['blocks']):
        nb=D['blocks'][i+1];pl,n=LN.extenso(nb['passos'])
        return ('Passo seguinte','narrativas/'+nb['id']+'/',nb['title']+': '+pl.strip().lower()+' '+n)
    return ('No Ideias','narrativas/ideias/','As sessões')
def fim_percurso(r):
    """05/11/2026: decisão 163. Depois da última peça de um percurso: o percurso seguinte da mesma porta, a porta seguinte ou,
    no fim de Criar, as sessões do Ideias. Devolve (caminho, rótulo do botão, título)."""
    b=block_of(r);rs=routes_of(b);i=rs.index(r)
    if i+1<len(rs):nr=rs[i+1];return ('narrativas/percursos/'+nr['id']+'/','Percurso seguinte: '+nr['title'],nr['title'])
    j=D['blocks'].index(b)
    if j+1<len(D['blocks']):nb=D['blocks'][j+1];return ('narrativas/'+nb['id']+'/','Passo seguinte: '+nb['title'],nb['title'])
    return ('narrativas/ideias/','As sessões do Ideias','As sessões do Ideias')

def page(base,title,body,desc,foot=True,treinar=False,fio=None,abre=''):
    """fio: None na entrada; (atual, modo) nas outras páginas."""
    rel=lambda x:link(base,x)
    # 31/10/2026: só as peças que estão num percurso (uma peça fora dos percursos não conta nem se guarda aqui).
    data=[{k:p[k] for k in ['id','url','title','progress']} for p in D['pieces'] if p['id'] in INROUTE]
    data=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    s=('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>'+(e(title)+' | ' if title!='Laboratório' else '')+'Laboratório | Lente</title><meta name="description" content="'+e(desc)+'">'+LN.PROJ+
       '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;display=swap" media="print" onload="this.media=\'all\'">'
       '<link rel="stylesheet" href="'+rel('assets/appearance.css')+'?v=20261101-1"><link rel="stylesheet" href="'+rel('assets/cartaz-components.css')+'?v=20261101-1">'+LN.css(base)
       +'<script src="'+rel('assets/appearance.js')+'"></script><script defer src="'+rel('assets/laboratorio/percursos.js')+'?v='+LN.V+'"></script>'+abre+'</head>'
       '<body data-site="lente" data-lab="3"><a class="salta" href="#conteudo">Saltar para o conteúdo</a>'+LN.barra(base,entrada=fio is None)
       +('<div class="pg lab-fio-pg">'+LN.fio(base,*fio)+'</div>' if fio else '')
       +'<main data-cartaz="2" data-cartaz-laboratorio id="conteudo" class="pg" data-raiz="'+rel('')+'">'+body+(extras(base,treinar) if foot else '')+'</main>'
       '<script type="application/json" id="lab-dados">'+data+'</script><script type="application/json" id="lab-retiradas">'+RETIDS+'</script></body></html>\n')
    p=R/base/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.encode())

# Entrada
allids=[p for r in D['routes'] for p in r['pieces']]
SESS=LN.sessoes_publicadas()
def entrada():
    base='narrativas'
    # 05/11/2026: decisão 163. A região do Ideias: o botão «Abrir Ideias →» passa a «Continuar na sessão N →» quando há progresso
    # (assets/laboratorio/ideias/entrada.js, o mesmo da página Ideias) e as sessões publicadas, uma linha cada, com o estado
    # (decisão 141: a entrada liga a cada sessão pública; crescem sozinhas). Sem JavaScript, o botão abre o Ideias.
    linhas_s=''.join('<li data-chave="'+e(s['chave'])+'" data-versao="'+e(s['versao'])+'" data-n="'+str(s['n'])+'" data-titulo="'+e(s['titulo'])+'" data-href="'+link(base,s['url'])+'">'
                     '<a href="'+link(base,s['url'])+'"><span class="n" aria-hidden="true">'+str(s['n'])+'</span><span class="t"><span class="c-sr">Sessão '+str(s['n'])+': </span>'+e(s['titulo'])+'</span>'
                     '<span class="etq" data-estado></span></a></li>' for s in SESS)
    body=('<header class="lab-abre"><div class="abre-t"><h1>Laboratório</h1><div class="lab-saiu"><p class="lead">Observa uma escolha, experimenta uma regra e cria uma peça tua.</p></div></div>'
          '<section class="lab-ideias ideias-publico" id="ideias" aria-labelledby="ideias-publico-t"><p class="rotulo">Começa aqui</p><h2 id="ideias-publico-t">Ideias</h2>'
          '<p>Junta material, trabalha-o e põe uma ideia tua à prova, passo a passo.</p>'
          '<div data-proximo><a class="botao" data-p-botao href="ideias/">Abrir Ideias\u00a0→</a>'
          # o título da sessão seguinte e a última feita só aparecem com progresso (entrada.js)
          '<p class="estado-p" data-p-t></p><p class="estado-p" data-p-feito></p></div>'
          '<ol class="sessoes ideias-sessoes" data-seguir-com-feitas aria-label="Sessões publicadas">'+linhas_s+'</ol></section></header>')
    body+='<section class="lab-portas" aria-labelledby="portas-t"><p class="lab-sec-t" id="portas-t">Três portas para os cinco passos</p><ol class="portas3">'
    for b in D['blocks']:
        rs=routes_of(b);ids=[id for r in rs for id in r['pieces']]
        body+=('<li id="'+b['anchor']+'"><a class="porta3" href="'+b['id']+'/" data-cz-ids="'+e(json.dumps(ids))+'"><span class="nums" aria-hidden="true">'+LN.cartaz(b['passos'])+'</span>'
               '<div class="nome"><h2>'+b['title']+'</h2></div><span class="passo">'+e(b['passoTexto'])+'</span>'
               '<span class="conta">'+str(len(rs))+(' percurso, ' if len(rs)==1 else ' percursos, ')+str(len(ids))+' peças<span class="cz-state" data-contagem="'+e(json.dumps(ids))+'" data-curto hidden></span></span>'
               '<span class="seta" aria-hidden="true">→</span></a></li>')
    body+='</ol></section>'+start(base,allids)
    # Pé: o progresso, sem caixa; o índice dos percursos (as mesmas ligações de antes, numa linha por percurso) e os créditos das
    # imagens das portas, que se veem dentro de cada porta.
    indice=''
    for b in D['blocks']:
        indice+='<div class="ind-g"><h3>'+b['title']+'</h3><ul>'+''.join('<li><a class="ind" data-cz-route="'+e(json.dumps(r['pieces']))+'" href="percursos/'+r['id']+'/"><span>'+e(r['title'])+'</span><span class="cz-state"></span></a></li>' for r in routes_of(b))+'</ul></div>'
    creditos=' '.join('<span>'+b['title']+': '+credito(IM[b['id']])+'</span>' for b in D['blocks'])
    body+=('<footer class="lab-pe"><div class="lab-progresso"><h2>O teu progresso: <span data-contagem="'+e(json.dumps(allids))+'">0 de '+str(len(allids))+' peças feitas</span></h2>'
           '<p>O que fizeste fica só neste aparelho. Abrir uma peça não a marca como feita.</p>'
           '<div class="registos"><button type="button" data-guardar>Guardar num ficheiro</button><label class="repor"><input type="file" accept="application/json,.json" data-repor>Repor de um ficheiro</label></div>'
           '<p data-registos-aviso role="status">O ficheiro guarda só os estados, sem respostas nem textos.</p></div>'
           '<div class="lab-mais"><nav class="lab-indice" aria-labelledby="indice-t"><h2 id="indice-t">Os '+str(len(D['routes']))+' percursos</h2>'+indice+'</nav>'
           '<p class="lab-tudo"><a class="sec" href="tudo/">Tudo o que há no Laboratório →</a></p>'
           '<p class="lab-creditos">Créditos das imagens das portas Observar, Treinar e Criar: '+creditos+'</p></div></footer>')
    # 31/10/2026: uma âncora antiga que já não existe aqui leva ao catálogo, onde aponta para o percurso certo.
    body+='<script>(function(){function f(){var h=decodeURIComponent(location.hash.slice(1));if(h&&!document.getElementById(h))location.replace("tudo/"+location.search+location.hash)}addEventListener("hashchange",f);f()})()</script>'
    abre=('<script src="'+link(base,'assets/licoes/progresso-laboratorio.js')+'?v=20261102-1"></script>'
          '<script defer src="'+link(base,'assets/laboratorio/ideias/entrada.js')+'?v='+LN.V+'"></script>')
    page(base,'Laboratório',body,'Observa uma escolha, experimenta uma regra e cria uma peça tua: '+str(len(D['routes']))+' percursos em três portas (Observar, Treinar e Criar), depois do Ideias.',foot=False,abre=abre)
entrada()

# Portas
for b in D['blocks']:
    base='narrativas/'+b['id'];rs=routes_of(b);ids=[p for r in rs for p in r['pieces']]
    frase=b['subtitle'][0].upper()+b['subtitle'][1:]+': '+b['question'][0].lower()+b['question'][1:]
    body=('<header class="lab-abre lab-abre-porta"><div class="abre-t"><p class="rotulo">'+e(b['passoTexto'].rstrip('.'))+'</p><h1>'+b['title']+'</h1>'
          '<p class="lead">'+e(frase)+'</p>'+LN.liga_ideias(base,b['passos'])+'</div>'+figura(base,b['id'])+'</header>'+start(base,ids))
    for i,r in enumerate(rs,1):
        body+=('<section class="percurso" id="'+r['id']+'" aria-labelledby="'+r['id']+'-t"><p class="rotulo">Percurso '+str(i)+' de '+str(len(rs))+'</p>'
               '<h2 id="'+r['id']+'-t">'+a(base,'narrativas/percursos/'+r['id']+'/',e(r['title']))+'</h2><p class="q">'+e(r['question'])+'</p>'+count(r['pieces'])+linhas(base,r['pieces'])+'</section>')
    body+=depois(base,[passo_seguinte(b),('Voltar ao','narrativas/','Laboratório')])
    page(base,b['title'],body,b['title']+' '+b['subtitle']+'. '+b['question'],treinar=b['id']=='treinar',fio=(b['id'],'page'))

# Percursos
for r in D['routes']:
    base='narrativas/percursos/'+r['id'];b=block_of(r);rs=routes_of(b);i=rs.index(r)
    antes=''
    if r.get('antes'):q=P[r['antes']['piece']];antes='<p class="antes">'+e(r['antes']['text'])+' '+a(base,q['url'],'«'+e(q['title'])+'»')+'.</p>'
    body=('<header class="lab-abre lab-abre-percurso"><div class="abre-t"><p class="rotulo">'+e(LN.rotulo_porta(b))+'</p><h1>'+e(r['title'])+'</h1><p class="lead">'+e(r['question'])+'</p>'
          +('<p class="razao">'+e(r['reason'])+'</p>' if r.get('reason') else '')+LN.liga_ideias(base,passos_de(r),r.get('sessao'))+'</div></header>'
          +start(base,r['pieces'])+'<section class="percurso">'+antes+count(r['pieces'])+linhas(base,r['pieces'])+'</section>')
    seg=('Percurso seguinte','narrativas/percursos/'+rs[i+1]['id']+'/',e(rs[i+1]['title'])) if i+1<len(rs) else passo_seguinte(b)
    body+=depois(base,[seg,('Voltar a','narrativas/'+b['id']+'/',b['title'])])
    page(base,r['title'],body,r['question']+' '+NUM[len(r['pieces'])].capitalize()+' peças, por ordem.',treinar=b['id']=='treinar',fio=(b['id'],'true'))

# Tudo
base='narrativas/tudo';body='<header class="lab-abre"><div class="abre-t"><h1>Tudo o que há no Laboratório</h1><p class="lead">'+a(base,'narrativas/percursos/','Os '+str(len(D['routes']))+' percursos')+', com as peças de cada um, por porta.</p></div></header>'
used=set(ALIAS)
for b in D['blocks']:
    used.add(b['anchor'])
    body+='<section id="'+b['anchor']+'" class="cat">'+''.join('<span id="'+k+'"></span>' for k,v in ALIAS.items() if v==b['id'])+'<h2>'+a(base,'narrativas/'+b['id']+'/',b['title'])+'</h2><p>'+b['subtitle'][0].upper()+b['subtitle'][1:]+'.</p>'
    for r in routes_of(b):
        body+='<h3>'+''.join('<span id="'+k+'"></span>' for k,v in ALIAS.items() if v==r['id'])+a(base,'narrativas/percursos/'+r['id']+'/',e(r['title']))+'</h3><ol class="catalogo">'
        for id in r['pieces']:
            old=id.rsplit('/',1)[-1];attr='' if old in used else ' id="'+old+'"';used.add(old)
            body+='<li'+attr+'>'+a(base,P[id]['url'],e(P[id]['title']))+'</li>'
        body+='</ol>'
    body+='</section>'
body+=''.join('<span id="'+id+'" hidden></span>' for id in D['ancoras'] if id not in used)
body+='<nav class="mais" aria-label="Mais">'+a(base,'narrativas/fora-da-pagina/','Fora da página')+a(base,'narrativas/margens/','Margens')+a(base,'docente/','Área do docente')+'</nav>'
page(base,'Tudo',body,'Todas as peças do Laboratório, por porta e por percurso.',foot=False,fio=(None,'page'))

# Percursos (a lista): deixa de ser órfã (Tudo liga-lhe) e agrupa os dez por porta, em linhas.
base='narrativas/percursos';body='<header class="lab-abre"><div class="abre-t"><h1>Percursos</h1><p class="lead">Os '+str(len(D['routes']))+' percursos do Laboratório, por porta.</p></div></header>'
for b in D['blocks']:
    body+='<section class="percurso" aria-labelledby="g-'+b['id']+'"><p class="rotulo">'+e(b['passoTexto'].rstrip('.'))+'</p><h2 id="g-'+b['id']+'">'+a(base,'narrativas/'+b['id']+'/',b['title'])+'</h2><ol class="linhas">'
    for n,r in enumerate(routes_of(b),1):
        body+=('<li><a class="linha" href="'+link(base,'narrativas/percursos/'+r['id']+'/')+'"><span class="n" aria-hidden="true">'+str(n)+'</span><span class="t"><strong>'+e(r['title'])+'</strong><span class="apoio">'+e(r['question'])+'</span>'
               +count(r['pieces']).replace('<p ','<small ').replace('</p>','</small>')+'</span><span class="seta" aria-hidden="true">→</span></a></li>')
    body+='</ol></section>'
page(base,'Percursos',body,'Os '+str(len(D['routes']))+' percursos do Laboratório.',fio=(None,'page'))

# Continuação nas peças (31/10/2026): a ordem vem de percursos.json.
def menu_peca(p,s,r,b,nxt):
    """05/11/2026: decisão 163. O contexto do menu ≡ de uma peça (tools/menu_casca.py). As ligações do menu antigo que o menu
    novo não tem (o caderno de treino, as das experiências de Fora da página e das Formas) ficam como itens próprios; os botões
    dos motores próprios (Formas) ficam como estão, dentro do menu."""
    i=s.find('<div class="casca-menu');velho=s[i:MC.fim_div(s,i)]
    porta=ABS+'narrativas/'+b['id']+'/'
    if r:
        ids=r['pieces'];k=ids.index(p['id'])
        voltar=(ABS+'narrativas/percursos/'+r['id']+'/','Voltar ao percurso',r['title']);onde=r['title']+', peça '+str(k+1)+' de '+str(len(ids))+'.'
        if nxt:seguinte=(ABS+nxt['url'],'Seguinte',nxt['title'])
        else:
            dest,rot,tit=fim_percurso(r);seguinte=(ABS+dest,rot.split(':')[0] if ':' in rot else 'No Ideias',tit if ':' in rot else 'As sessões')
    else:
        voltar=(porta,'Voltar a '+b['title'],b['title']);onde='Fora dos percursos.';seguinte=None
    imp=p['url'].rstrip('/')+'-imprimir/'
    papel=(ABS+imp,'Versão para imprimir') if (R/imp/'index.html').exists() else None
    caminho=[('Lente',ABS),('Laboratório',ABS+'narrativas/'),(b['title'],porta)]
    # o texto da c-menu-extra (ou, na segunda volta, das fontes ou da nota) passa para o sítio certo do menu novo
    fontes=nota=None
    m=re.search(r'<p class="c-menu-extra">(.*?)</p>',velho,re.S)
    if m:
        if 'Fontes' in m[1]:fontes=m[1]
        else:nota=m[1]
    m=re.search(r'<details class="m-fontes"><summary>Fontes e créditos</summary><p>(.*?)</p></details>',velho,re.S)
    if m:fontes=m[1]
    m=re.search(r'<p class="m-nota">(.*?)</p>',velho,re.S)
    if m and m[1]!='O que fazes fica só neste aparelho.':nota=m[1]
    # ligações e botões do menu antigo que não cabem no menu novo
    orig=re.search(r'<nav class="m-orig"[^>]*>.*?</nav>',velho,re.S)
    if orig:orig=orig[0]
    elif 'class="casca-menu m2"' in velho:orig=''  # menu novo sem ligações próprias: nada a guardar
    else:
        nv=re.search(r'<nav([^>]*)>(.*?)</nav>',velho,re.S)
        corpo=re.sub(r'<ol class="c-migalhas".*?</ol>','',nv[2],flags=re.S) if nv else ''
        base_url=ABS+p['url']
        tem={posixpath.normpath(x) for x in [voltar[0],ABS,ABS+'narrativas/',porta,MC.COMO]+([seguinte[0]] if seguinte else [])+([papel[0]] if papel else [])}
        itens=[]
        for el in re.findall(r'<a\b[^>]*>.*?</a>|<button\b[^>]*>.*?</button>',corpo,re.S):
            h=re.search(r'href="([^"]*)"',el)
            if h and (h[1].startswith('?') or posixpath.normpath(__import__('urllib.parse').parse.urljoin(base_url,h[1])) in tem):continue
            itens.append(el)
        lab=re.search(r'aria-label="([^"]*)"',nv[1]) if nv else None
        orig='<nav class="m-orig" aria-label="'+(lab[1] if lab else 'Mais')+'">'+''.join(itens)+'</nav>' if itens else ''
    ctx={'cab':'Laboratório, '+b['title'],'titulo':p['title'],'onde':onde,'voltar':voltar,'seguinte':seguinte,'papel':papel,
         'projecao':'?projetar=1' in velho or 'class="casca-menu m2"' in velho and 'so-normal' in velho,'caminho':caminho,'fontes':fontes,'nota':nota,'mais':orig}
    return ctx
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
            # 05/11/2026: decisão 163. Na última peça de um percurso, o «a seguir» é o percurso seguinte, a porta seguinte ou o Ideias.
            fim=None if nxt else fim_percurso(r)
        else:
            # fora dos percursos (decisão 34): volta ao bloco, sem «Seguinte»
            nxt=None;fim=None;b=blocks[p['block']];rurl=ABS+'narrativas/'+b['id']+'/';rpath='narrativas/'+b['id']+'/';back='Voltar a '+b['title']
        # <title> igual em todas as peças: título | bloco | Laboratório | Lente
        s=re.sub(r'<title>[^<]*</title>','<title>'+e(p['title'],quote=False)+' | '+b['title']+' | Laboratório | Lente</title>',s,count=1)
        # 31/10/2026 (terceira correção): a casca apresenta-se como «Laboratório» em todas as peças (decisão 15):
        # marca do motor, ligação da marca na casca, cabeçalho do menu (sem tocar nas migalhas «Estás em:») e «LAB».
        s=re.sub(r'marca:"[^"]*"','marca:"Laboratório"',s)
        s=re.sub(r'(<a class="c-marca"[^>]*>)LAB(</a>)',r'\1Laboratório\2',s)
        s=re.sub(r'(<a class="c-marca" href="[^"]*" aria-label="Página inicial \()[^)"]*(\)">(?:<svg[^>]*>.*?</svg>)?)[^<]*(</a>)',r'\1Laboratório\2Laboratório\3',s)
        # 31/10/2026 (releitura): a marca «Laboratório» leva ao Laboratório e o nome acessível é o texto visível
        s=re.sub(r'(<a class="c-marca" href=")[^"]*(" aria-label=")[^"]*(")',r'\g<1>'+ABS+r'narrativas/\g<2>Laboratório\g<3>',s)
        # 05/11/2026 (revisão): o nome da marca num <span class="c-marca-t">, como no Ideias e no piloto, para a barra ficar numa
        # linha em todas as famílias (assets/licoes/menu.css esconde-o abaixo de 400 px; o nome acessível continua a dizê-lo)
        s=re.sub(r'(<a class="c-marca" href="[^"]*" aria-label="Laboratório">(?:<svg[^>]*>.*?</svg>)?)Laboratório(</a>)',r'\1<span class="c-marca-t">Laboratório</span>\2',s)
        # rótulo dos treinos com o nome do percurso
        if r and p['id'].startswith('treinar/'):
            s=re.sub(r'(<p class=\\"etq-m\\">Treino · )[^·<]+?( · )',lambda m:m.group(1)+e(r['title'],quote=False)+m.group(2),s)
        # configuração do motor
        if 'EPIJogo.montar(' in s and 'percurso:"' in s:
            s=re.sub(r'percurso:"'+re.escape(ABS)+r'narrativas/percursos/[^"/]+/"','percurso:"'+rurl+'"',s)
            s=re.sub(r',seguinte:"[^"]*",seguinteRotulo:"[^"]*"','',s)
            if nxt:s=s.replace('voltarRotulo:"Voltar ao percurso"','voltarRotulo:"Voltar ao percurso",seguinte:"'+ABS+nxt['url']+'",seguinteRotulo:"Seguinte"',1)
            elif fim:s=s.replace('voltarRotulo:"Voltar ao percurso"','voltarRotulo:"Voltar ao percurso",seguinte:"'+ABS+fim[0]+'",seguinteRotulo:"'+e(fim[1],quote=False)+'"',1)
            # fim dos treinos: o texto aponta para o mesmo sítio que o botão
            txt=('Seguinte: <a href=\\"'+ABS+nxt['url']+'\\">'+e(nxt['title'],quote=False)+'</a>') if nxt else ('É o último treino deste percurso. A seguir: <a href=\\"'+ABS+fim[0]+'\\">'+e(fim[2],quote=False)+'</a>') if fim else 'É o último treino deste percurso: <a href=\\"'+rurl+'\\">regressa à lista</a>'
            s=re.sub(r'(<p class=\\"sub\\">)(?:Treino seguinte: |Seguinte: |É o último treino deste percurso: |É o último treino deste percurso\. A seguir: )?<a href=\\"[^"\\]*\\">[^<]*</a>(\. Ou volta a este noutro dia: repetir é treinar\.)',lambda m:m.group(1)+txt+m.group(2),s)
        # páginas sem motor: nav.lab-fim-percurso
        def nav(m):
            rel=lambda u:posixpath.relpath(u.rstrip('/'),p['url'].rstrip('/'))+'/'
            seg=(' <a href="'+rel(nxt['url'])+'">Seguinte: '+e(nxt['title'])+'\u00a0→</a>') if nxt else (' <a href="'+rel(fim[0])+'">'+e(fim[1])+'\u00a0→</a>') if fim else ''
            return m.group(1)+'<a href="'+rel(rpath)+'">'+back+'</a>'+seg+'</nav>'
        s=re.sub(r'(<nav class="lab-fim-percurso"[^>]*>).*?</nav>',nav,s,flags=re.S)
        # 05/11/2026: decisão 163. O menu ≡ inteiro vem de tools/menu_casca.py (o mesmo das sessões e da Cidadania).
        if '<div class="casca-menu' in s:
            ctx=menu_peca(p,s,r,b,nxt)
            s=MC.trocar_menu(s,MC.menu(ctx))
            s=MC.com_controls(s)
            s=re.sub(r'<style id="mg-css">.*?</style>','',s,count=1,flags=re.S)
            if '<main class="casca-corpo" id="casca-corpo" tabindex="-1">' in s:s=MC.com_semjs(s,ctx,'peça')
            s=MC.ativos(s,posixpath.relpath('.',p['url'].rstrip('/'))+'/')
        s=SP.aplicar(s)
        if s!=o:f.write_bytes(s.encode('utf-8'));changed+=1
    # 02/11/2026: três versões para imprimir incluem também o motor incorporado.
    for nome in ('oficina-ficcao-comecar-imprimir', 'oficina-ficcao-personagem-imprimir', 'oficina-matriz-imprimir'):
        f=R/'narrativas'/nome/'index.html'
        antes=f.read_text('utf-8');depois=SP.aplicar(antes)
        if depois!=antes:f.write_bytes(depois.encode('utf-8'));changed+=1
    return changed
continuacao()

# 05/11/2026: decisão 147. As peças que saíram por dependerem do Português ficam no endereço como redirecionamento
# para o Laboratório (nada se parte); a lista está em assets/laboratorio/retiradas.json.
RET=json.loads((R/'assets/laboratorio/retiradas.json').read_text('utf-8'))['retiradas']
def retiradas():
    nomes={'narrativas/':'Laboratório',**{'narrativas/'+b['id']+'/':b['title'] for b in D['blocks']}}
    for x in RET:
        assert x['url'] not in {p['url'] for p in D['pieces']},x['url']
        base=x['url'].rstrip('/');dest=ABS+x['destino'];rel=lambda u:link(base,u)
        s=('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<title>'+e(x['titulo'])+' | Laboratório | Lente</title><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url='+e(dest)+'"><link rel="canonical" href="'+e(dest)+'">'
           '<link rel="stylesheet" href="'+rel('assets/appearance.css')+'"><script src="'+rel('assets/appearance.js')+'"></script></head>'
           '<body data-site="lente"><main><p>«'+e(x['titulo'])+'» já não faz parte do Laboratório. Continua em <a href="'+e(dest)+'">'+e(nomes[x['destino']])+'</a>.</p></main></body></html>\n')
        f=R/x['url']/'index.html';f.parent.mkdir(parents=True,exist_ok=True)
        if not f.exists() or f.read_text('utf-8')!=s:f.write_bytes(s.encode('utf-8'))
retiradas()

# Mapa do Lente (31/10/2026, terceira correção): a secção do Laboratório sai de percursos.json, como narrativas/tudo/:
# Ver, Treinar e Criar, com os percursos de percursos.json (10 desde a decisão 147, 05/11/2026) e as peças de cada um, pela ordem do Laboratório.
def mapa():
    f=R/'mapa/index.html';s=f.read_text('utf-8')
    ini='<section class="map-section"><h2><a href="'+ABS+'narrativas/">';i=s.index(ini);j=s.index('</section>',i)+len('</section>')
    seta=' <span aria-hidden="true">→</span>'
    def ramo(nome,abrir,dentro,extra=''):
        return ('<li><details class="map-branch"><summary><span>'+nome+'</span><b aria-hidden="true">+</b></summary><div class="map-branch-body">'
                '<p class="map-open"><a href="'+abrir+'">Abrir '+nome+seta+'</a></p>'+extra+'<ul class="map-tree">'+dentro+'</ul></div></details></li>')
    out=ini+'Laboratório</a></h2><p class="map-open"><a href="'+ABS+'narrativas/tudo/">Tudo o que há no Laboratório'+seta+'</a></p><ul class="map-tree">'
    # 02/11/2026: decisão 141, acesso público antes das três portas.
    out+='<li class="map-leaf"><a href="'+ABS+'narrativas/ideias/">Ideias: o método em cinco passos</a></li>'
    for b in D['blocks']:
        extra=('<p class="map-open"><a href="'+ABS+'narrativas/treinar/caderno/">O caderno de treino</a></p><p class="map-open"><a href="'+ABS+'narrativas/treinar/docente/">Como conduzir um treino (docente)</a></p>') if b['id']=='treinar' else ''
        rs=''.join(ramo(e(r['title']),ABS+'narrativas/percursos/'+r['id']+'/',''.join('<li class="map-leaf"><a href="'+ABS+P[id]['url']+'">'+e(P[id]['title'])+'</a></li>' for id in r['pieces'])) for r in routes_of(b))
        out+=ramo(b['title'],ABS+'narrativas/'+b['id']+'/',rs,extra)
    mais=[('narrativas/fora-da-pagina/','Fora da página'),('narrativas/margens/','Margens'),('dar-forma-as-palavras/','Dar forma às palavras'),('projetos/','Projetos'),('docente/','Área do docente')]
    out+='</ul>'+''.join('<p class="map-open"><a href="'+ABS+u+'">'+t+'</a></p>' for u,t in mais)+'</section>'
    s2=s[:i]+out+s[j:]
    if s2!=s:f.write_text(s2,'utf-8')
mapa()
print('23 páginas geradas; '+str(len(INROUTE))+' peças nos percursos; '+str(len(P))+' peças preservadas.')
