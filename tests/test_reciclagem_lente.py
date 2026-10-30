"""30/10/2026: destinos da reciclagem, sem retirar as secções de origem."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys,json,re,math,unittest
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
import medir_opcoes as medir
from cidadania_m2_molde import CASOS_RECICLADOS
from test_opcoes_equilibradas import ordinal,PROIBIDAS

ABRIL='cidadania/25-de-abril/index.html'
DESTINOS=[ABRIL,'cidadania/25-de-abril/guiao/index.html']+[f'direitos/passo-{n:02}/index.html' for n in (1,3,4)]+[f'cidadania/m2/sessoes/{n:02}/index.html' for n in (3,5,9)]
def ler(p):return (R/p).read_text('utf-8')
def cards(p):
 s=ler(p);m=re.search(r'itens\s*:\s*',s)
 return json.JSONDecoder().raw_decode(s[m.end():])[0]
def grupos():
 yield ABRIL,[c for c in cards(ABRIL) if 'o' in c]
 for n,c in CASOS_RECICLADOS.items():yield f'sessao-{n:02}',c['perguntas']
 for n in (1,3,4):
  p=f'direitos/passo-{n:02}/index.html'
  yield p,[c for c in cards(p) if c.get('rot')=='De quem é a imagem?' and 'o' in c]

class Refs(HTMLParser):
 def __init__(self,s):self.refs=[];super().__init__();self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  for k in ('href','src'):
   if k in a:self.refs.append(a[k])

class Reciclagem(unittest.TestCase):
 def test_opcoes_estritas_e_distribuicao(self):
  for p,qs in grupos():
   self.assertTrue(qs,p);longas=curtas=0
   for q in qs:
    ns=[len(medir.visivel(o)) for o in q['o']];c=q['c'];err=[v for i,v in enumerate(ns) if i!=c]
    self.assertLessEqual(max(ns),1.2*min(ns),(p,ns,q['p']))
    self.assertLess(ns[c],1.25*max(err),(p,ns))
    longas+=ns[c]>max(err);curtas+=ns[c]<min(err)
    self.assertEqual(len(q['fe']),len(q['o']))
    for f in [q['f']]+q['fe']:self.assertIsNone(ordinal(q['p']).search(f),(p,f))
   esperado=math.ceil(sum(1/len(q['o']) for q in qs))
   self.assertLessEqual(longas,esperado,p);self.assertLessEqual(curtas,esperado,p)
 def test_registo_e_conteudo_preservado(self):
  s=ler(ABRIL);antigos=cards('vozes/25-de-abril/index.html');novos=cards(ABRIL)
  self.assertIn('chave:"epi-vozes-25-de-abril-v2"',s)
  self.assertEqual([c['t'] for c in antigos],[c['t'] for c in novos])
  for som in ('S10638','S10639','S10662'):self.assertIn('https://www.cd25a.uc.pt/storage/media/Sons/'+som+'.mp3',s)
  for texto in ('Sophia','48 artistas','Vasco Lourenço','Paulo Núncio','Pedro Pinto','Hugo Soares','CC0','Domínio público'):self.assertIn(texto,s)
  self.assertNotIn('fim:function()',s)
  self.assertNotIn('<figure',novos[0]['html'].split('<details')[0])
  self.assertNotIn('vozes/',s)
 def test_casos_e_fontes(self):
  for n in (3,9):
   s=ler(f'cidadania/m2/sessoes/{n:02}/index.html')
   self.assertIn('Ler o relato em português',s);self.assertIn('não é uma tradução editorial',s)
   self.assertNotIn('Cartão da obra',s);self.assertNotIn('gigantes/',s)
   self.assertEqual(s.count('data-opcoes-reciclagem'),2)
  self.assertNotIn('gigantes/lovelace/',ler('cidadania/m2/sessoes/05/index.html'))
  self.assertIn('investigar/passo-04/',ler('cidadania/m2/sessoes/05/index.html'))
  for n in (1,3,4):self.assertIn('https://pedrohfernandes-klk.github.io/pt/m9/licao-m9-f10/',ler(f'direitos/passo-{n:02}/index.html'))
  self.assertNotRegex(ler('direitos/passo-03/index.html'),r'<img[^>]+(?:Goldsmith|goldsmith|orange-prince)')
 def test_ligacoes_locais(self):
  for p in DESTINOS:
   s=ler(p);blocos=[s]+([c.get('html','') for c in cards(p)] if 'itens:' in s else [])
   for bloco in blocos:
    for ref in Refs(bloco).refs:
     u=urlsplit(ref)
     if u.scheme and not ref.startswith('https://pedrohfernandes-klk.github.io/lente/'):continue
     if not u.path:continue
     alvo=R/unquote(u.path[len('/lente/'):]) if u.path.startswith('/lente/') else (R/p).parent/unquote(u.path)
     if alvo.is_dir():alvo=alvo/'index.html'
     self.assertTrue(alvo.is_file(),(p,ref))
 def test_escrita_nova(self):
  for p,qs in grupos():
   for q in qs:
    for texto in [q['p'],q['f']]+q['o']+q['fe']:self.assertIsNone(PROIBIDAS.search(texto),(p,texto))

if __name__=='__main__':
 if '--medir' in sys.argv:
  for p,qs in grupos():
   ns=[[len(medir.visivel(o)) for o in q['o']] for q in qs]
   print(p, 'perguntas',len(qs),'máximo %',round(max((max(n)/min(n)-1)*100 for n in ns),2),'certa mais longa',sum(n[q['c']]>max(v for i,v in enumerate(n) if i!=q['c']) for q,n in zip(qs,ns)),ns)
 else:unittest.main()
