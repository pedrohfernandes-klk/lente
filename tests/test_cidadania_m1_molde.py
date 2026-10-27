"""Molde das sessões de Cidadania M1 (27/10/2026, decisões do docente).

Abertura com imagem, pergunta curta e «Começar»; cinco passos visíveis (Recupera, Vê,
Decide, Faz, Leva); Decide marcado «sem ecrã»; Leva com uma pergunta de saída em papel;
cartões de obra com acesso, razão, contexto até 100 palavras, pergunta aberta, duas
ligações e uma leitura discordante. A sessão 03 realiza a tarefa partilhada.
"""
from pathlib import Path
from html.parser import HTMLParser
import importlib.util,re,sys,unittest

R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
try:
 spec=importlib.util.spec_from_file_location('molde',R/'tools/cidadania_m1_molde.py');molde=importlib.util.module_from_spec(spec);spec.loader.exec_module(molde)
finally:sys.path.pop(0)

class Texto(HTMLParser):
 """o texto visível do corpo, sem scripts nem estilos"""
 def __init__(self,s):
  super().__init__();self.out=[];self.skip=0;self.feed(s[s.index('<body'):])
 def handle_starttag(self,t,a):
  if t in('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
 def __str__(self):return re.sub(r'\s+',' ',' '.join(self.out))

def pagina(n):return (R/f'cidadania/m1/sessoes/{n:02}/index.html').read_text('utf-8')

class Molde(unittest.TestCase):
 def test_abertura_imagem_pergunta_comecar(self):
  for n in range(1,11):
   s=pagina(n);capa=s[s.index('data-session-intro'):s.index('data-session-flow')]
   self.assertEqual(capa.count('<img '),1,n);self.assertIn('class="c10-deck"',capa);self.assertIn('data-start>Começar</a>',capa)
   self.assertNotIn('3 horas',capa,n);self.assertNotIn('momentos',capa,n)

 def test_cinco_passos_pela_ordem(self):
  for n in range(1,11):
   s=pagina(n);esperado=molde.PASSOS_TAREFA if n==3 else molde.PASSOS
   self.assertEqual(re.findall(r' data-stage data-label="([^"]+)"',s),esperado,n)
   self.assertEqual(re.findall(r'data-stage-link><b>\d\d</b><span>([^<]+)</span>',s),esperado,n)
   self.assertIn('data-prev hidden>← Anterior',s);self.assertIn('data-next hidden>Seguinte →',s)

 def test_decide_sem_ecra_e_leva_em_papel(self):
  for n in range(1,11):
   s=pagina(n);passos=re.split(r'<section class="c10-stage" id="momento-',s)[1:]
   self.assertEqual(len(passos),5)
   recall=passos[0].count('<li><p>');self.assertTrue(2<=recall<=3,(n,recall))
   if n==3:
    self.assertIn('href="../../../projeto/"',passos[1]);continue
   self.assertIn('data-mark="Sem ecrã"',passos[2],n)
   self.assertIn('Primeiro, em silêncio',passos[2]);self.assertIn('Depois, em grupo',passos[2])
   self.assertIn('data-mark="Em papel"',passos[3],n);self.assertIn('data-mark="Em papel"',passos[4],n)
   self.assertEqual(passos[4].count('class="c10-exit-q"'),1,n)

 def test_recupera_confirma_so_com_resposta_da_sessao_anterior(self):
  for n,m in molde.MOLDE.items():
   for q,a in m['recupera']:
    self.assertTrue(q.endswith('?'),q)
    if a:self.assertNotIn('?',a,q)

 def test_cartoes_de_obra(self):
  self.assertEqual(sorted(molde.OBRAS),[1,2,4,5,6,7,8,9])
  for n,o in molde.OBRAS.items():
   self.assertLessEqual(len(o['contexto'].split()),100,n)
   self.assertEqual(len(o['ligacoes']),2,n);self.assertTrue(o['acesso'],n)
   self.assertTrue(o['razao'] and o['discordante'],n);self.assertTrue(o['pergunta'].endswith('?'),n)
   # obras protegidas: descritas, nunca citadas
   if o.get('protegida'):self.assertNotIn('citacao',o,n)
   for _,alvo in o['ligacoes']:
    alvo=R/alvo;self.assertTrue((alvo/'index.html').exists(),(n,alvo))
   s=pagina(n);self.assertEqual(s.count('class="c10-obra"'),1,n);self.assertIn('Outra leitura',s)
  for n in (3,10):self.assertNotIn('class="c10-obra"',pagina(n))

 def test_tempos_somam_180_e_plano_da_tarefa(self):
  spec=importlib.util.spec_from_file_location('sessoes',R/'tools/cidadania_m1_sessoes.py');m=importlib.util.module_from_spec(spec)
  sys.path.insert(0,str(R/'tools'))
  try:spec.loader.exec_module(m)
  finally:sys.path.pop(0)
  self.assertEqual(m.SESSOES[2]['times'],[10,5,60,35,70])
  for n,s in enumerate(m.SESSOES,1):
   if not s.get('prior'):self.assertEqual(sum(s['times']),180,n)

 def test_escrita(self):
  # pt-PT AO90: sem travessão, sem «professor», sem «jogar», sem «ficha» nem «folha» no texto visível;
  # sem avisos ao aluno sobre o que já estudou (isso fica no guia do docente).
  paginas=[R/f'cidadania/m1/sessoes/{n:02}/index.html' for n in range(1,11)]+[R/p for p in ('cidadania/m1/index.html','cidadania/m1/biblioteca/index.html','cidadania/m1/oficina-guiao/index.html')]
  for p in paginas:
   t=str(Texto(p.read_text('utf-8')));baixo=t.lower()
   self.assertNotIn('—',t,p)
   for w in ('professor','jogar','joga ','ficha','folha','já estudámos','conhecimentos prévios'):self.assertNotIn(w,baixo,(p,w))

 def test_registo_so_nas_sessoes_que_contam(self):
  for n in range(1,11):
   s=pagina(n);self.assertEqual(s.count('data-session-done'),0 if n<=2 else 1,n)

if __name__=='__main__':unittest.main()
