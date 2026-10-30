"""Mede escolhas sem executar JavaScript nem alterar páginas.
30/10/2026: opções equilibradas (pedido do docente).
"""
from pathlib import Path
from html import unescape
import argparse,json,re,sys
PASTAS=('gigantes','sidequests','cidade','investigar','projetos','fachada','vozes','apresentar','estetica','etica','ler','direitos','olhar-e-decidir')
def visivel(texto):
 return re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]*>','',texto)).replace('_','').replace('*','')).strip()
def perguntas(raiz):
 decoder=json.JSONDecoder()
 for pasta in PASTAS:
  for p in sorted((raiz/pasta).rglob('*.html')):
   texto=p.read_text('utf-8-sig');numero=0
   for m in re.finditer(r'\{',texto):
    try:d,_=decoder.raw_decode(texto,m.start())
    except json.JSONDecodeError:continue
    if not isinstance(d,dict) or not isinstance(d.get('o'),list) or not isinstance(d.get('c'),int):continue
    op=d['o'];c=d['c']
    if not all(isinstance(x,str) for x in op) or not 0<=c<len(op) or len(op)<2:raise ValueError(str(p)+': opções inválidas')
    numero+=1
    n=list(map(lambda s:len(visivel(s)),op));err=max(v for i,v in enumerate(n) if i!=c)
    yield {'numero':numero,'pagina':p.relative_to(raiz).as_posix(),'pasta':pasta,'pergunta':d.get('p',''),'linha':texto.count('\n',0,m.start())+1,'opcoes':op,'certa':c,'comprimentos':n,'denunciadora':n[c]>=1.25*err and n[c]-err>=5,'fora20':max(n)>1.2*min(n) and max(n)-min(n)>=8,'certaMaisLonga':n[c]>err,'certaMaisCurta':n[c]<min(v for i,v in enumerate(n) if i!=c),'k':len(op)}
def resumir(rows,chave):
 out={}
 for q in rows:
  r=out.setdefault(q[chave],dict(perguntas=0,denunciadoras=0,fora20=0,certaMaisLonga=0,certaMaisCurta=0,esperadoMaisLonga=0))
  for k,inc in [('perguntas',1),('denunciadoras',q['denunciadora']),('fora20',q['fora20']),('certaMaisLonga',q['certaMaisLonga']),('certaMaisCurta',q['certaMaisCurta']),('esperadoMaisLonga',1/q['k'])]:r[k]+=inc
 return out
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--raiz',type=Path,default=Path(__file__).resolve().parents[1]);a.add_argument('--json',action='store_true');a.add_argument('--verificar',action='store_true');args=a.parse_args()
 rows=list(perguntas(args.raiz));res={'pastas':resumir(rows,'pasta'),'paginas':resumir(rows,'pagina'),'perguntas':rows}
 if args.json:print(json.dumps(res,ensure_ascii=False,indent=2))
 else:
  print('pasta | perguntas | denunciadoras | fora20 | certaMaisLonga | certaMaisCurta')
  for p,r in res['pastas'].items():print(p+' | '+' | '.join(str(r[k]) for k in ['perguntas','denunciadoras','fora20','certaMaisLonga','certaMaisCurta']))
 if args.verificar and any(q['denunciadora'] for q in rows):sys.exit(1)
