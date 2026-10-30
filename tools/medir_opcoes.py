"""Mede escolhas sem executar JavaScript nem alterar páginas.
30/10/2026: opções equilibradas (pedido do docente).
"""
from pathlib import Path
from html import unescape
import argparse,json,re,sys
PASTAS=('cidade','investigar','projetos','fachada','apresentar','estetica','etica','ler','direitos','olhar-e-decidir')
EXCECOES = {'cidade/m01/index.html#1': 'Rótulos de locais no mapa: conservar os nomes e a sigla EPI.',
 'cidade/m01/index.html#3': 'Rótulos de locais no mapa: conservar os nomes e a sigla EPI.',
 'cidade/m02/index.html#1': 'Rótulos ligados às zonas do mapa; preservar a correspondência com os locais e '
                            'erros assinalados.',
 'cidade/m02/index.html#2': 'Rótulos ligados às zonas do mapa; preservar a correspondência com os locais e '
                            'erros assinalados.',
 'cidade/m02/index.html#4': 'Conectores de lacuna: não acrescentar palavras que mudem a função ou a sintaxe.',
 'cidade/m02/index.html#5': 'Conectores de lacuna: não acrescentar palavras que mudem a função ou a sintaxe.',
 'cidade/m03/index.html#3': 'Nomes de locais numa lacuna: jardim, mercado e ascensor.',
 'cidade/m04/index.html#2': 'Termos gramaticais de modalidade; manter as designações técnicas.',
 'cidade/m04/index.html#3': 'Termos gramaticais de modalidade; manter as designações técnicas.',
 'cidade/m04/index.html#4': 'Termos gramaticais de modalidade; manter as designações técnicas.',
 'cidade/m05/index.html#2': 'Topónimos: preservar os nomes próprios que se distinguem pela origem.',
 'cidade/m05/index.html#5': 'Topónimos: preservar os nomes próprios que se distinguem pela origem.',
 'cidade/m05/index.html#3': 'Numerais numa lacuna; não alterar o número nem acrescentar conteúdo.',
 'cidade/m06/index.html#1': 'Conectores de lacuna com funções distintas.',
 'cidade/m08/index.html#3': 'Marcadores de tempo numa lacuna; conservar a construção temporal.',
 'cidade/m08/index.html#4': 'Marcadores de tempo numa lacuna; conservar a construção temporal.',
 'cidade/m11/index.html#2': 'Categorias gramaticais usadas como termos numa lacuna.',
 'cidade/m11/index.html#3': 'Categorias gramaticais usadas como termos numa lacuna.',
 'cidade/m12/index.html#1': 'Contraste entre metáfora, comparação e verbos literais numa lacuna; preservar '
                            'as construções.',
 'cidade/m15/index.html#3': 'Contraste entre numeral e expressões deíticas numa lacuna.',
 'cidade/m16/index.html#5': 'Citações literais de imperativos da fachada; não reescrever a citação.',
 'cidade/m17/index.html#3': 'Verbos e nomes que completam lacunas sobre a imagem; não alongar a construção.',
 'cidade/m17/index.html#4': 'Verbos e nomes que completam lacunas sobre a imagem; não alongar a construção.',
 'cidade/m18/index.html#2': 'Palavras que completam lacunas sobre o som; manter a forma pedida.',
 'cidade/m18/index.html#3': 'Palavras que completam lacunas sobre o som; manter a forma pedida.',
 'cidade/m18/index.html#4': 'Palavras que completam lacunas sobre o som; manter a forma pedida.',
 'apresentar/passo-03/index.html#2': 'Palavras literais do apoio de apresentação descrito no texto.',
 'ler/passo-02/index.html#2': 'Vocábulos citados do poema, identificados pelo contexto.',
 'ler/passo-02/index.html#3': 'Inícios de estrofe citados literalmente.',
 'ler/passo-02/index.html#4': 'Inícios de estrofe citados literalmente.',
 'ler/passo-06/index.html#2': 'Versos citados literalmente; não cortar nem parafrasear.',
 'ler/passo-06/index.html#3': 'Conjuntos de nomes próprios; não substituir pessoas para acertar o '
                              'comprimento.'}

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
    yield {'excecao':EXCECOES.get(p.relative_to(raiz).as_posix()+'#'+str(numero)), 'amplitude20':max(n)>1.2*min(n),'numero':numero,'pagina':p.relative_to(raiz).as_posix(),'pasta':pasta,'pergunta':d.get('p',''),'linha':texto.count('\n',0,m.start())+1,'opcoes':op,'certa':c,'comprimentos':n,'denunciadora':n[c]>=1.25*err and n[c]-err>=5,'fora20':max(n)>1.2*min(n) and max(n)-min(n)>=8,'certaMaisLonga':n[c]>err,'certaMaisCurta':n[c]<min(v for i,v in enumerate(n) if i!=c),'k':len(op)}
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
