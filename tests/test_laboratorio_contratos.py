"""02/11/2026: pedido 2, contratos opcionais e conservação dos motores antigos."""
import importlib.util,json,re,subprocess,unittest
from renomeacoes_cidadania import renomear
import lab147
import grupos146  # 05/11/2026: decisões 146 e 154
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def mod(nome):
 s=importlib.util.spec_from_file_location(nome,R/'tools'/f'{nome}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
L=mod('licoes_lente');SP=mod('laboratorio_sem_pontos')
class Contratos(unittest.TestCase):
 def base(self):return json.loads((R/'tools/licoes/ideias-s01.json').read_text('utf-8'))
 def test_literal_so_pontuacao_na_citacao_com_fonte(self):
  d=self.base();c=d['cartoes'][1]
  for texto in ['<p>— fala</p>','<p>texto · texto</p>','<blockquote class="literal">— fala</blockquote>','<blockquote class="literal" data-fonte="https://example.org/">— fala','<blockquote class="literal" data-fonte="https://example.org/">professor</blockquote>']:
   c['html']=texto;self.assertTrue(L.validar(d),texto)
  c['html']='<blockquote class="literal" data-fonte="https://example.org/">— Uma fala · citada.</blockquote>'
  self.assertEqual(L.validar(d),[])
  c['html']='<blockquote class="literal" data-fonte="https://example.org/">'+'palavra '*121+'</blockquote>'
  self.assertTrue(any('120 palavras' in e for e in L.validar(d)))
 def test_contagem_e_molde_sao_distintos(self):
  tipos=['escolha','vf','emparelhar','sublinhar','ordenar']
  c=[{'t':tipos[i%5]} for i in range(14)]
  self.assertEqual(L.LC.regras63({'regras63':'contagem'},c,set(tipos)),[])
  self.assertTrue(L.LC.regras63({'regras63':True},c,set(tipos)))
  c[1]['rot']='Decide';self.assertEqual(L.LC.regras63({'regras63':True},c,set(tipos)),[])
  for ruim in [c[:13],[{'t':'vf'}]*14,[dict(x,prod='escrita') if i<3 else x for i,x in enumerate(c)]]:
   self.assertTrue(L.LC.regras63({'regras63':'contagem'},ruim,set(tipos)))
  self.assertTrue(L.LC.regras63({'medida':'curta','saida':'narrativas/ideias/sessao-03/index.html'},c,set(tipos)))
 def test_aula_estruturada_e_destino(self):
  d=self.base();c=next(c for c in d['cartoes'] if c.get('rot')=='Na aula');c.pop('html')
  c['aula']={'faz':'Observa um lugar.','tempo':'70 minutos.','escrito':'O teu registo.','sozinho':'Observa da janela.','imprimir':'narrativas/ideias/guiao/index.html'}
  self.assertEqual(L.validar(d),[]);self.assertIn('Versão para imprimir',L.pagina(d));self.assertIn('Se estás sozinho.',L.pagina(d))
  for destino in ['narrativas/inexistente/index.html','../../fora.html','https://example.org/']:
   c['aula']['imprimir']=destino;self.assertTrue(L.validar(d))
 def test_registo_so_aceita_chaves_e_destinos_antigos(self):
  d=self.base();d.update(chave='epi-treinos-lista-substantivos',saida='narrativas/treinar/lista-substantivos/index.html',registo={'chave':'epi-treinos','id':'lista-substantivos','vezes':True})
  self.assertEqual(L.validar(d),[])
  pag=L.pagina(d)
  for frase in ['var K="epi-treinos"','S.feitas["lista-substantivos"]','S.vezes["lista-substantivos"]','tr-liga-lab','Voltar ao percurso','Seguinte:']:
   self.assertIn(frase,pag)
  d['registo']['id']='outro';self.assertTrue(L.validar(d))
 def test_imagens_opcionais_exigem_correspondencia_e_credito(self):
  d=self.base();c=next(c for c in d['cartoes'] if c['t']=='escolha')
  c['imagens']=[{'src':'../../../assets/laboratorio/ideias/atget-quiosque-fiacres.webp','alt':'Fotografia de uma rua.','credito':'Eugène Atget, CC0.'} for _ in c['o']]
  self.assertEqual(L.validar(d),[])
  c['imagens'].pop();self.assertTrue(L.validar(d))
  c['imagens']=[{'src':'javascript:alert(1)','alt':'Rua.','credito':'Atget.'} for _ in c['o']];self.assertTrue(L.validar(d))
  c['imagens']=[{'src':'imagem.webp','alt':'Rua.'} for _ in c['o']];self.assertTrue(L.validar(d))
 def test_relogio_so_e_carregado_quando_existe(self):
  d=self.base();self.assertNotIn('assets/licoes/relogio.js',L.pagina(d))
  d['cartoes'][1]['html']='<div data-relogio="60">Um minuto.</div>'
  self.assertIn('assets/licoes/relogio.js',L.pagina(d))
 def test_motores_antigos_so_recebem_transformacao_autorizada(self):
  base='e71ebf4600a11b3d2bd73abce68fa92f6be22076';n=0
  for p in (R/'narrativas').rglob('*.html'):
   atual=p.read_text('utf-8')
   if 'EPIJogo.montar(' not in atual or 'assets/licoes/jogo.js' in atual:continue
   rel=p.relative_to(R).as_posix();antes=subprocess.check_output(['git','show',base+':'+rel],cwd=R).decode('utf-8').replace('\r\n','\n')
   with self.subTest(pagina=rel):
    # 03/11/2026 (#107; data posta a 05/11/2026): títulos Humanos, Algoritmos e Decisões pelo manifesto tests/fixtures/cidadania-nomes-20261103.json; a exigência é a mesma.
    # 05/11/2026: decisão 147 (Laboratório sem o Português): navegação e limpezas pelo manifesto fechado
    # tests/fixtures/lab-147-20261105.json, com contagem exata; a comparação continua integral.
    # 05/11/2026: decisões 146 e 154 (os exercícios fazem-se sozinho). Por cima da 147, só as trocas dos manifestos fechados
    # tools/trocas/grupos-146-20261105.json e tools/trocas/autonomia-154-20261105.json (tests/grupos146.py), com contagem
    # exata e por esta ordem; a comparação continua integral.
    self.assertEqual(grupos146.aplicar(lab147.aplicar(renomear(SP.aplicar(antes),rel),rel),rel),atual)
    self.assertEqual(SP.aplicar(atual),atual)
    self.assertIn('EPIJogo.montar({semPontos:true,',atual)
    self.assertIn('if(cfg.fim&&!soErrados&&!PROJ)',atual)
   n+=1
  # 05/11/2026: decisão 147. As peças retiradas passam a redirecionamento; as 86 contam-se entre as que ficam e as retiradas.
  ret=sum(1 for u in lab147.RETIRADAS if 'EPIJogo.montar(' in subprocess.check_output(['git','show',base+':'+u+'index.html'],cwd=R).decode('utf-8'))
  self.assertEqual(n+ret,86)
if __name__=='__main__':unittest.main()
