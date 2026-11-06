"""Molde das sessões de Cidadania M1 (27/10/2026, decisões do docente).

Abertura com imagem, pergunta curta e «Começar»; cinco passos visíveis (Recupera, Vê,
Decide, Faz, Leva); Decide marcado «sem ecrã»; Leva com uma pergunta de saída em papel;
cartões de obra com acesso, razão, contexto até 100 palavras, pergunta aberta, duas
ligações e uma leitura discordante. A sessão 03 realiza a tarefa partilhada.
"""
from pathlib import Path
from html.parser import HTMLParser
import importlib.util,json,re,sys,unittest

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
# 05/11/2026 (plano do molde da Cidadania, pedido 2; decisões 157 e 158): a sessão 01 deixa de ser a página publicada em cinco
# passos e passa a ser a lição no molde final, no mesmo endereço, escrita por tools/licoes_lente.py (test_sessao_01_no_molde,
# abaixo, e tests/test_molde_cidadania.py conferem-na). As regras deste molde antigo continuam a valer, iguais, para as sessões
# 02 a 10 publicadas, até ao pedido 3.
# 06/11/2026 (decisão 166): a sessão 02 também passa ao molde final, no mesmo endereço (test_sessao_02_no_molde, abaixo, e
# tests/test_molde_cidadania.py conferem-na); as regras do molde antigo continuam a valer, iguais, para as sessões 03 a 10.
# 06/11/2026 (decisões 166 a 168): a sessão 03 também passa ao molde final, no mesmo endereço (test_sessao_03_no_molde, abaixo, e
# tests/test_molde_cidadania.py conferem-na); as regras do molde antigo continuam a valer, iguais, para as sessões 04 a 10.
# 06/11/2026 (decisões 166 a 168): a sessão 04 também passa ao molde final, no mesmo endereço (test_sessao_04_no_molde, abaixo, e
# tests/test_molde_cidadania.py conferem-na); as regras do molde antigo continuam a valer, iguais, para as sessões 05 a 10.
# 06/11/2026 (fusão do main com as sessões 2 e 3 finais na sessão 4): a lista fica escrita, como a do main; que as sessões fora
# dela são as que têm o campo «molde» no .json (a regra que a s04 trazia) confere-se em test_sessao_04_no_molde.
# 06/11/2026 (decisões 166 a 168; fusão do main com as sessões 2 a 4 finais na sessão 5): a sessão 05 também passa ao molde final,
# no mesmo endereço (test_sessao_05_no_molde, abaixo, e tests/test_molde_cidadania.py conferem-na); a lista continua escrita, e as
# regras do molde antigo continuam a valer, iguais, para as sessões 06 a 10.
# 06/11/2026 (decisões 166 a 168; fusão do main com as sessões 2 a 5 finais na sessão 6): a sessão 06 também passa ao molde final,
# no mesmo endereço (test_sessao_06_no_molde, abaixo, e tests/test_molde_cidadania.py conferem-na); a lista continua escrita, e as
# regras do molde antigo continuam a valer, iguais, para as sessões 07 a 10.
PUBLICADAS=range(7,11)

class Molde(unittest.TestCase):
 def test_abertura_imagem_pergunta_comecar(self):
  for n in PUBLICADAS:
   s=pagina(n);capa=s[s.index('data-session-intro'):s.index('data-session-flow')]
   self.assertEqual(capa.count('<img '),1,n);self.assertIn('class="c10-deck"',capa);self.assertIn('data-start>Começar</a>',capa)
   self.assertNotIn('3 horas',capa,n);self.assertNotIn('momentos',capa,n)

 def test_cinco_passos_pela_ordem(self):
  for n in PUBLICADAS:
   s=pagina(n);esperado=molde.PASSOS_TAREFA if n==3 else molde.PASSOS
   self.assertEqual(re.findall(r' data-stage data-label="([^"]+)"',s),esperado,n)
   self.assertEqual(re.findall(r'data-stage-link><b>\d\d</b><span>([^<]+)</span>',s),esperado,n)
   self.assertIn('data-prev hidden>← Anterior',s);self.assertIn('data-next hidden>Seguinte →',s)

 def test_decide_sem_ecra_e_leva_em_papel(self):
  for n in PUBLICADAS:
   s=pagina(n);passos=re.split(r'<section class="c10-stage" id="momento-',s)[1:]
   self.assertEqual(len(passos),5)
   recall=passos[0].count('<li><p>');self.assertTrue(2<=recall<=3,(n,recall))
   if n==3:
    self.assertIn('href="../../../projeto/"',passos[1]);continue
   self.assertIn('data-mark="Sem ecrã"',passos[2],n)
   # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): a conversa do Decide passa a ser em turma.
   self.assertIn('Primeiro, em silêncio',passos[2]);self.assertIn('Depois, em turma',passos[2])
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
   if n not in PUBLICADAS:continue
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
  # 28/10/2026: os dezoito apoios (f01 a f18) também são texto para o aluno.
  paginas+=[R/f'cidadania/m1/fichas/f{n:02}/index.html' for n in range(1,19)]
  for p in paginas:
   t=str(Texto(p.read_text('utf-8')));baixo=t.lower()
   self.assertNotIn('—',t,p)
   for w in ('professor','jogar','joga ','ficha','folha','já estudámos','conhecimentos prévios'):self.assertNotIn(w,baixo,(p,w))

 def test_oficina_de_argumento_e_guiao(self):
  # o caminho das sessões 04 a 10, o argumento em cinco partes e a mesma cena em três formatos
  s=(R/'cidadania/m1/oficina-guiao/index.html').read_text('utf-8')
  self.assertEqual(re.findall(r'href="\.\./sessoes/(\d\d)/"',s),[f'{n:02}' for n in range(4,11)])
  self.assertEqual(s.count('<dt>'),5);self.assertEqual(s.count('c10-script'),3)
  for nome in ('Teatro','Cinema','Áudio'):self.assertIn('<b>'+nome+'</b>',s)
  self.assertIn('Não é preciso encenar, filmar ou gravar.',s)

 def test_registo_so_nas_sessoes_que_contam(self):
  # 06/11/2026 (decisões 166 a 168): a sessão 03 passou ao molde final, que não tem registo de sessão (como a 01 e a 02); as 04 a
  # 10 publicadas continuam com um registo cada.
  for n in range(1,11):
   # 06/11/2026 (decisões 166 a 168): a sessão 04 também passou ao molde final, sem registo de sessão; as 05 a 10 publicadas
   # continuam com um registo cada.
   # 06/11/2026 (fusão do main com as sessões 2 a 4 finais na sessão 5): a sessão 05 também passou ao molde final, sem registo de
   # sessão; as 06 a 10 publicadas continuam com um registo cada.
   # 06/11/2026 (fusão do main com as sessões 2 a 5 finais na sessão 6): a sessão 06 também passou ao molde final, sem registo de
   # sessão; as 07 a 10 publicadas continuam com um registo cada.
   s=pagina(n);self.assertEqual(s.count('data-session-done'),0 if n<=6 else 1,n)


 def test_sessao_01_no_molde(self):
  # 05/11/2026 (pedido 2): no endereço da sessão 01 está a lição no molde final, com a chave do piloto e sem os cinco passos.
  s=pagina(1)
  self.assertIn('molde-cidadania',s);self.assertIn('"chave": "epi-cid-m1-s01"',s);self.assertIn('"preservarAnterior": true',s)
  self.assertNotIn('data-stage',s);self.assertNotIn('data-session-done',s)
  sys.path.insert(0,str(R/'tests'))
  try:
   import molde_pedido2
  finally:sys.path.pop(0)
  self.assertTrue(molde_pedido2.inteiro_ok('cidadania/m1/sessoes/01/index.html'))

 def test_sessao_02_no_molde(self):
  # 06/11/2026 (decisão 166): no endereço da sessão 02 está a lição no molde final, com a chave do piloto e sem os cinco passos.
  s=pagina(2)
  self.assertIn('molde-cidadania',s);self.assertIn('"chave": "epi-cid-m1-s02"',s);self.assertIn('"preservarAnterior": true',s)
  self.assertNotIn('data-stage',s);self.assertNotIn('data-session-done',s)
  sys.path.insert(0,str(R/'tests'))
  try:
   import molde_s02
  finally:sys.path.pop(0)
  self.assertTrue(molde_s02.inteiro_ok('cidadania/m1/sessoes/02/index.html'))

 def test_sessao_03_no_molde(self):
  # 06/11/2026 (decisões 166 a 168): no endereço da sessão 03 está a lição no molde final, com a chave do piloto e sem os cinco passos.
  s=pagina(3)
  self.assertIn('molde-cidadania',s);self.assertIn('"chave": "epi-cid-m1-s03"',s);self.assertIn('"preservarAnterior": true',s)
  self.assertNotIn('data-stage',s);self.assertNotIn('data-session-done',s)
  sys.path.insert(0,str(R/'tests'))
  try:
   import molde_s03
  finally:sys.path.pop(0)
  self.assertTrue(molde_s03.inteiro_ok('cidadania/m1/sessoes/03/index.html'))

 def test_sessao_04_no_molde(self):
  # 06/11/2026 (decisões 166 a 168): no endereço da sessão 04 está a lição no molde final, com a chave do piloto e sem os cinco
  # passos; as outras sessões publicadas (PUBLICADAS) continuam no molde antigo.
  # 06/11/2026 (fusão do main com as sessões 2 a 4 finais na sessão 5): a 05 também saiu de PUBLICADAS (test_sessao_05_no_molde);
  # a primeira sessão publicada no molde antigo, a seguir à 04, é agora a 06.
  # 06/11/2026 (fusão do main com as sessões 2 a 5 finais na sessão 6): a 06 também saiu de PUBLICADAS (test_sessao_06_no_molde);
  # a primeira sessão publicada no molde antigo, a seguir à 04, é agora a 07.
  self.assertNotIn(4,PUBLICADAS);self.assertIn(7,PUBLICADAS)
  # 06/11/2026 (fusão do main com as sessões 2 e 3 finais): as sessões 03 a 10 fora de PUBLICADAS são exatamente as que têm o campo
  # «molde» no seu .json (hoje, a 03 e a 04). 06/11/2026 (fusão na sessão 5): hoje, a 03, a 04 e a 05.
  # 06/11/2026 (fusão na sessão 6): hoje, as 03 a 06.
  self.assertEqual([n for n in range(3,11) if json.loads((R/f'tools/licoes/cidadania-m1-s{n:02}.json').read_text('utf-8')).get('molde')],
                   [n for n in range(3,11) if n not in PUBLICADAS])
  s=pagina(4)
  self.assertIn('molde-cidadania',s);self.assertIn('"chave": "epi-cid-m1-s04"',s);self.assertIn('"preservarAnterior": true',s)
  self.assertNotIn('data-stage',s);self.assertNotIn('data-session-done',s)
  sys.path.insert(0,str(R/'tests'))
  try:
   import molde_s04
  finally:sys.path.pop(0)
  self.assertTrue(molde_s04.inteiro_ok('cidadania/m1/sessoes/04/index.html'))

 def test_sessao_05_no_molde(self):
  # 06/11/2026 (decisões 166 a 168): no endereço da sessão 05 está a lição no molde final, com a chave do piloto e sem os cinco
  # passos; as outras sessões publicadas (PUBLICADAS) continuam no molde antigo.
  # 06/11/2026 (fusão do main com as sessões 2 a 5 finais na sessão 6): a 06 também saiu de PUBLICADAS; a primeira sessão publicada
  # no molde antigo, a seguir à 05, é agora a 07.
  self.assertNotIn(5,PUBLICADAS);self.assertIn(7,PUBLICADAS)
  # 06/11/2026 (fusão do main com as sessões 2 a 4 finais): a regra que a s05 trazia (fora de PUBLICADAS só as sessões com o campo
  # «molde» no .json) confere-se, para a 05 também, em test_sessao_04_no_molde; aqui, que o .json da 05 o tem.
  self.assertTrue(json.loads((R/'tools/licoes/cidadania-m1-s05.json').read_text('utf-8')).get('molde'))
  s=pagina(5)
  self.assertIn('molde-cidadania',s);self.assertIn('"chave": "epi-cid-m1-s05"',s);self.assertIn('"preservarAnterior": true',s)
  self.assertNotIn('data-stage',s);self.assertNotIn('data-session-done',s)
  sys.path.insert(0,str(R/'tests'))
  try:
   import molde_s05
  finally:sys.path.pop(0)
  self.assertTrue(molde_s05.inteiro_ok('cidadania/m1/sessoes/05/index.html'))

 def test_sessao_06_no_molde(self):
  # 06/11/2026 (decisões 166 a 168): no endereço da sessão 06 está a lição no molde final, com a chave do piloto e sem os cinco
  # passos; as outras sessões publicadas (PUBLICADAS) continuam no molde antigo.
  self.assertNotIn(6,PUBLICADAS);self.assertIn(7,PUBLICADAS)
  # 06/11/2026 (fusão do main com as sessões 2 a 5 finais na sessão 6): como na 05, a regra (fora de PUBLICADAS só as sessões com o
  # campo «molde» no .json) confere-se, para a 06 também, em test_sessao_04_no_molde; aqui, que o .json da 06 o tem.
  self.assertTrue(json.loads((R/'tools/licoes/cidadania-m1-s06.json').read_text('utf-8')).get('molde'))
  s=pagina(6)
  self.assertIn('molde-cidadania',s);self.assertIn('"chave": "epi-cid-m1-s06"',s);self.assertIn('"preservarAnterior": true',s)
  self.assertNotIn('data-stage',s);self.assertNotIn('data-session-done',s)
  sys.path.insert(0,str(R/'tests'))
  try:
   import molde_s06
  finally:sys.path.pop(0)
  self.assertTrue(molde_s06.inteiro_ok('cidadania/m1/sessoes/06/index.html'))

if __name__=='__main__':unittest.main()
