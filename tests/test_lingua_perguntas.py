import json,pathlib,re,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
# 30/10/2026: pedido do docente («Qual citação identifica…» é muito mau em português). Em português europeu, a pergunta
# que escolhe entre opções diz «Qual das citações…», «Qual destas utilizações…», «Qual é a frase que…» ou «Que frase…»;
# nunca «Qual citação…». Vale também para a interrogativa indireta («decide que razão é mais forte»). «Qual» como
# pronome («Qual preferes?», «Qual é…», «Qual depende de qual?») e os textos literários citados ficam livres: a lista
# só tem nomes que aparecem em enunciados.
NOMES=r'''frases? citaç(?:ão|ões) afirmaç(?:ão|ões) perguntas? image(?:m|ns) vers(?:ão|ões) recortes? critérios?
conclus(?:ão|ões) formulaç(?:ão|ões) reformulaç(?:ão|ões) propostas? utilizaç(?:ão|ões) raz(?:ão|ões) créditos? obras?
detalhes? pormenor(?:es)? decis(?:ão|ões) opç(?:ão|ões) respostas? palavras? versos? estrofes? linhas? comparaç(?:ão|ões)
interpretaç(?:ão|ões) revis(?:ão|ões) sínteses? justificaç(?:ão|ões) desenvolvimentos? notas? registos? aç(?:ão|ões)
alteraç(?:ão|ões) inícios? par(?:es)? trios? procedimentos? promessas? exemplos? textos? parágrafos? títulos? legendas?
cenas? persona(?:gem|gens) argumentos? recursos? sentidos? efeitos? ideias? teses? provas? fontes? planos?
acontecimentos? hipóteses? nomes? leituras? testemunh(?:a|as|o|os)'''.split()
QUAL_NOME=re.compile(r'(?<![A-Za-zÀ-ÿ])(?:Qual|Quais|qual|quais)\s+(?:'+'|'.join(NOMES)+r')(?![A-Za-zÀ-ÿ])')
# 30/10/2026: pedido do docente (o problema é transversal). O aluno trata-se por «tu» e a turma por «vocês»: nada de
# imperativos de «você» a abrir uma instrução («Compare…», «Clique…»).
IMPERATIVO_VOCE=re.compile(r'(?:<li>|<p>|<dd>|"\s*:\s*")\s*(?:Clique|Toque|Arraste|Compare|Escreva|Leia|Observe|Repare|Responda|Escolha|Assinale|Sublinhe|Justifique|Explique|Indique)\s')
FORA=('tests','tools','docs','curadoria','node_modules','.git','biblioteca')
def paginas():
 for p in sorted(ROOT.rglob('*')):
  if p.suffix in ('.html','.js','.json') and not set(p.relative_to(ROOT).parts)&set(FORA):yield p
class LinguaDasPerguntas(unittest.TestCase):
 def test_padroes(self):
  for bom in ('Qual das citações identifica a testemunha?','Que critério deve decidir?','Qual preferes?','Qual é a frase que…','Qual depende de qual?'):
   self.assertIsNone(QUAL_NOME.search(bom),bom)
  for mau in ('Qual citação identifica a testemunha?','decide qual razão é mais forte','Quais frases mostram','Qual par cumpre?'):
   self.assertIsNotNone(QUAL_NOME.search(mau),mau)
  self.assertIsNotNone(IMPERATIVO_VOCE.search('<li>Compare duas apresentações'))
  self.assertIsNone(IMPERATIVO_VOCE.search('<li>Comparem duas apresentações'))
 def test_sem_qual_mais_nome(self):
  falhas=[]
  for p in paginas():
   s=p.read_text('utf-8',errors='replace')
   for m in QUAL_NOME.finditer(s):falhas.append(p.relative_to(ROOT).as_posix()+': …'+s[max(0,m.start()-30):m.end()+40].replace('\n',' ')+'…')
  self.assertEqual(falhas,[],'\n'.join(falhas))
 def test_sem_imperativo_de_voce(self):
  falhas=[]
  for p in paginas():
   s=p.read_text('utf-8',errors='replace')
   for m in IMPERATIVO_VOCE.finditer(s):falhas.append(p.relative_to(ROOT).as_posix()+': …'+s[m.start():m.end()+60].replace('\n',' ')+'…')
  self.assertEqual(falhas,[],'\n'.join(falhas))
 def test_trocas_registadas(self):
  # 30/10/2026: pedido do docente. As trocas desta passagem ficam num manifesto, que os testes de conservação da
  # Cidadania M1 usam para aceitar só estas diferenças; cada «novo» tem de estar no sítio o número de vezes registado e
  # nenhum «antigo» pode ter voltado.
  trocas=json.loads((ROOT/'tools/trocas/lingua-perguntas-20261030.json').read_text('utf-8'))
  self.assertTrue(trocas)
  for t in trocas:
   self.assertEqual(set(t),{'ficheiro','antigo','novo','ocorrencias'})
   s=(ROOT/t['ficheiro']).read_text('utf-8')
   self.assertEqual(s.count(t['novo']),t['ocorrencias'],t['ficheiro']+': '+t['novo'])
   self.assertNotIn(t['antigo'],s,t['ficheiro'])
if __name__=='__main__':unittest.main()
