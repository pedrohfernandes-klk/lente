"""02/11/2026: contratos opcionais do Laboratório, sem mudar as lições da Cidadania."""
import html, json, re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Citacao(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pilha = []
        self.texto = []
        self.erros = []
        self.palavras = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        literal = tag == 'blockquote' and 'literal' in a.get('class', '').split()
        if literal:
            if not re.match(r'^https://[^\s]+$', a.get('data-fonte', '')):
                self.erros.append('citação literal sem data-fonte https')
            self.palavras.append([])
        if tag not in ('br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'wbr'):
            self.pilha.append((tag, literal))

    def handle_endtag(self, tag):
        if self.pilha and self.pilha[-1][0] == tag:
            _, literal = self.pilha.pop()
            if literal and len(' '.join(self.palavras.pop()).split()) > 120:
                self.erros.append('citação literal com mais de 120 palavras')
        elif tag == 'blockquote':
            self.erros.append('citação literal mal formada')

    def handle_data(self, data):
        literal = any(v for _,v in self.pilha)
        if literal:
            if self.palavras:self.palavras[-1].append(data)
            data = data.replace('—', ' ').replace('·', ' ')
        self.texto.append(data)


def texto_literal(s):
    p = Citacao();p.feed(s);p.close()
    if any(v for _,v in p.pilha):p.erros.append('citação literal não fechada')
    return ' '.join(p.texto), p.erros


def aula_html(a):
    obrigatorios = ('faz','tempo','escrito','sozinho','imprimir')
    if not isinstance(a,dict) or any(not isinstance(a.get(k),str) or not a[k].strip() for k in obrigatorios):
        raise ValueError('aula: faltam faz, tempo, escrito, sozinho ou imprimir')
    destino = a['imprimir']
    alvo = (ROOT / destino.split('#')[0]).resolve()
    if not alvo.is_relative_to(ROOT) or not alvo.is_file() or not destino.startswith('narrativas/'):
        raise ValueError('aula: destino para imprimir inexistente ou fora do Laboratório')
    campos = [('O que se faz.',a['faz']),('Quanto tempo.',a['tempo']),('O que fica escrito.',a['escrito']),('Se estás sozinho.',a['sozinho'])]
    return ''.join('<p><b>'+rot+'</b> '+html.escape(t)+'</p>' for rot,t in campos) + '<p><a href="https://pedrohfernandes-klk.github.io/lente/'+html.escape(destino,quote=True)+'">Versão para imprimir</a></p>'


def cartoes(d):
    out=[]
    for c in d.get('cartoes',[]):
        c=dict(c)
        if d.get('familia')=='laboratorio' and c.get('rot')=='Na aula' and c.get('aula'):
            if c.get('html'):raise ValueError('aula: não misturar HTML livre e campos estruturados')
            c['html']=aula_html(c.pop('aula'))
        out.append(c)
    return out


def regras63(d, C, tipos):
    erros=[];regra=d.get('regras63',False)
    if regra not in (False,True,'contagem'):erros.append('regras63: usa true ou contagem')
    if d.get('medida')=='curta' and not d.get('saida','').startswith('narrativas/treinar/'):
        erros.append('medida curta só se aplica a treinos, nunca a sessões')
    if not regra:return erros
    fazer=[c for c in C if c.get('t') in tipos and c.get('prod')!='escrita']
    if len(fazer)<14:erros.append('regras63: pelo menos 14 atividades sem escrita')
    if len({c['t'] for c in fazer})<5:erros.append('regras63: pelo menos cinco tipos sem escrita')
    if sum(c.get('prod')=='escrita' for c in C)>2:erros.append('regras63: máximo de duas produções escritas')
    if any(C[i].get('t')==C[i+1].get('t')==C[i+2].get('t') for i in range(len(C)-2)):
        erros.append('regras63: não pode haver três cartões seguidos do mesmo tipo')
    if regra is True and (len(C)<2 or C[1].get('rot')!='Decide'):
        erros.append('regras63: o segundo cartão tem de ser Decide')
    return erros


def registo(d):
    r=d.get('registo')
    if r is None:return None
    if d.get('familia')!='laboratorio' or not isinstance(r,dict):raise ValueError('registo só se aplica ao Laboratório')
    mapa=json.loads((ROOT/'assets/laboratorio/percursos.json').read_text('utf-8'))
    p=next((p for p in mapa['pieces'] if p['url']+'index.html'==d.get('saida')),None)
    if not p or p.get('progress',{}).get('kind')!='feitas':raise ValueError('registo: peça sem registo conhecido em percursos.json')
    pr=p['progress']
    if r.get('chave')!=pr['key'] or r.get('id')!=pr['id']:raise ValueError('registo não coincide com a chave e o id antigos')
    if d.get('chave')!=r['chave']+'-'+r['id']:raise ValueError('chave do baralho não coincide com o registo antigo')
    if not isinstance(r.get('vezes',False),bool):raise ValueError('registo.vezes tem de ser booleano')
    return p,mapa


def continuacao(d):
    resultado=registo(d)
    if not resultado:return {},''
    p,mapa=resultado;r=next((r for r in mapa['routes'] if r['id']==p.get('route')),None)
    b=next(b for b in mapa['blocks'] if b['id']==p['block']) if not r else None
    url='https://pedrohfernandes-klk.github.io/lente/narrativas/'
    cfg={'titulo':p['title'],'percurso':url+('percursos/'+r['id'] if r else b['id'])+'/',
         'percursoRotulo':'Voltar ao percurso' if r else 'Voltar a '+b['title']}
    if r:
        i=r['pieces'].index(p['id'])
        if i+1<len(r['pieces']):
            seguinte=next(x for x in mapa['pieces'] if x['id']==r['pieces'][i+1])
            cfg.update(seguinte='https://pedrohfernandes-klk.github.io/lente/'+seguinte['url'],seguinteRotulo='Seguinte: '+seguinte['title'])
    link='<p class="tr-liga-lab"><a href="'+html.escape(cfg['percurso'],quote=True)+'">'+html.escape(cfg['percursoRotulo'])+'</a></p>' if p['id'].startswith('treinar/') else ''
    return cfg,link


def fim_registo(d):
    if not registo(d):return ''
    r=d['registo'];key=json.dumps(r['chave']);ident=json.dumps(r['id'])
    vezes=('S.vezes=S.vezes||{};S.vezes['+ident+']=(S.vezes['+ident+']||0)+1;') if r.get('vezes') else ''
    return ('CFG.fim=function(){if(/[?&]projetar=1(&|$)/.test(location.search)||window.self!==window.top)return;'
            'try{var K='+key+';var S=JSON.parse(localStorage.getItem(K)||"null")||{};S.feitas=S.feitas||{};'
            'S.feitas['+ident+']=Date.now();'+vezes+'localStorage.setItem(K,JSON.stringify(S))}catch(e){}};')
