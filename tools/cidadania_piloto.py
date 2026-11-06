"""31/10/2026: Cidadania refeita, M1 em piloto (decisões do docente de 30/10, segunda ronda, 5, 8, 17, 18 e 38).

Escreve três páginas escondidas dos motores de busca, a partir das lições em tools/licoes/cidadania-m1-sNN.json:
- cidadania/piloto/m1/index.html: a página do módulo, só com as 10 sessões, numeradas, com o título, a pergunta, o
  estado de cada uma («Feita dd/mm» ou «A seguir»; 31/10: «por fazer» não se escreve) e «Começar» ou «Continuar». O estado lê-se das chaves epi-cid-m1-s01 a s10,
  no formato que o motor grava (assets/licoes/jogo.js, função fim(): «lida» fica true no fim da lição e «versao» é a
  da lição; com outra versão, o motor recomeça, por isso a página também não a conta como feita);
- cidadania/piloto/m1/docente/index.html: o guia do docente, uma secção por sessão, a partir do plano da coordenação
  (scratchpad cid-m1/plano.md, 31/10) e do que as lições dizem (o «Na aula», a imagem, o vídeo, as fontes);
- cidadania/piloto/m1/ponto/index.html: o Ponto de partida e de chegada, as mesmas 10 perguntas, para imprimir.

O texto vem das lições; o que é só do docente (passos, tempos, materiais, grelhas) está em GUIA, abaixo.
Uso: python3 tools/cidadania_piloto.py              (escreve as três páginas)
     python3 tools/cidadania_piloto.py --verificar  (confirma que estão atualizadas e que cumprem as regras da casa)"""
import html, importlib.util, json, pathlib, posixpath, re, sys
from urllib.parse import urljoin

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('licoes_lente', ROOT / 'tools/licoes_lente.py')
LL = importlib.util.module_from_spec(spec); spec.loader.exec_module(LL)
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
MODULO = 'cidadania/piloto/m1/'
NOMES = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
e = html.escape


def sessoes():
    out = []
    for n in NOMES:
        d = json.loads((ROOT / f'tools/licoes/cidadania-m1-s{n}.json').read_text('utf-8'))
        abre = d['cartoes'][0]['html']
        # 05/11/2026 (plano do molde, pedido 2): uma sessão no molde cidadania-2026-11 não tem «Na aula», imagem com pergunta nem
        # vídeo (decisões 154 e 155); a pergunta da sessão está no Abre (.pergunta-sessao) e a página pode viver fora do piloto
        # (a s01 está em cidadania/m1/sessoes/01/). Antes, sessoes() exigia img, data-yt e pergunta-c e dava StopIteration.
        if d.get('molde'):
            out.append({'n': n, 'd': d, 'chave': d['chave'], 'versao': d['versao'], 'molde': True,
                        'titulo': d['titulo'].split(': ', 1)[1],
                        'pergunta': re.search(r'<p class="pergunta-sessao"[^>]*>(.*?)</p>', abre).group(1),
                        'pasta': d['saida'].rsplit('/', 1)[0] + '/'})
            continue
        cart = {c.get('rot'): c for c in d['cartoes'] if c['t'] == 'ler' and c.get('rot') in ('Na aula', 'Para levar')}
        img = next(c for c in d['cartoes'] if '<img' in c.get('html', ''))
        vid = next(c for c in d['cartoes'] if 'data-yt=' in c.get('html', ''))
        h = vid['html']
        out.append({
            'n': n, 'd': d, 'chave': d['chave'], 'versao': d['versao'],
            'titulo': d['titulo'].split(': ', 1)[1],
            'pergunta': re.search(r'<p class="pergunta-c">(.*?)</p>', abre).group(1),
            'pasta': d['saida'].rsplit('/', 1)[0] + '/',
            'aula': cart['Na aula'], 'levar': cart['Para levar'],
            'figcaption': re.search(r'<figcaption>(.*?)</figcaption>', img['html']).group(1),
            'img_pergunta': re.search(r'<p class="pergunta-c">(.*?)</p>', img['html']).group(1),
            'yt': re.search(r'data-yt="([^"]+)"', h).group(1),
            'yt_ini': (re.search(r'data-ini="(\d+)"', h) or [None, None])[1],
            'yt_fim': (re.search(r'data-fim="(\d+)"', h) or [None, None])[1],
            'yt_botao': re.search(r'data-yt-abrir>(.*?)</button>', h).group(1).replace('Ver: ', '', 1),
            'yt_cred': re.search(r'<p class="yt-cred">(.*?)</p>', h).group(1).replace(' O vídeo só se liga ao YouTube quando tocas no botão.', ''),
            'yt_tarefa': re.search(r'<p class="pergunta-c">(.*?)</p>', h).group(1),
        })
    return out


# O que só o docente lê. Tempos em minutos; o «Na aula» soma 60 a 75 minutos, com os 10 da pausa.
# A grelha /20 de cada sessão é a do plano (proposta da equipa na sessão 01, que o plano não tinha); diz-se sempre indicativa (decisão 17).
GUIA = {
 # 05/11/2026 (plano do molde, pedido 2): a sessão 01 já está no molde final (cidadania-2026-11). O que só o docente faz vive
 # aqui, nunca no texto do aluno (decisão 154): «Na aula» por cartão (a coluna do plano, secção 2), como conduzir o Decide e o
 # «Em turma», as duas charneiras com o erro esperado, o papel e a devolução, o passo do projeto com a grelha /20, «se só houver
 # 90 minutos» e o que imprimir. A tabela dos tempos e as respostas tiram-se dos cartões da lição.
 '01': {
  'molde': True,
  'dominio': 'Direitos Humanos: a Declaração Universal, a Constituição e a força de cada texto; vida privada, imagem e liberdade de expressão.',
  'ensina': 'Olhar antes de concluir, situar um caso em artigos concretos, ver quando dois direitos chocam e pesá-los no caso, sem ir além das provas.',
  'antes': ('Recomendação: fazer o Ponto de partida em papel logo no início, antes do cartão 1, com os 10 minutos da folga. Os cartões 8 a 14 '
            'ensinam as respostas das perguntas 1 e 2: feito depois, o Ponto de partida deixava de o ser. O tempo total não muda.'),
  'na_aula': {
   1: 'O docente lê o caso em voz alta; a ligação «Projetar» abre a sessão na projeção e cada aluno abre-a no telemóvel.',
   2: 'Ver «Como conduzir o Decide».',
   3: 'Quando todos acabam, projeta-se e toca-se em «Mostrar resposta». Na sessão 01 não há papel anterior para devolver.',
   5: 'Projetado grande. Os pormenores (o emblema, as mãos, o título) só se apontam depois dos cartões 6 e 7.',
   8: 'Ler em voz alta os três artigos, uma vez; o 12.º até «honra e reputação».',
   12: 'Charneira 1 (ver abaixo): dedos no ar, um para verdadeiro e dois para falso.',
   13: 'O docente explica com a projeção, passo a passo, no máximo 6 minutos.',
   15: 'O caso é real: vale a pena abrir o acórdão na projeção (ligação no retorno) e mostrar onde está a frase citada.',
   16: 'Projetado e lido em voz alta. Numa segunda aula de 90 minutos, recomeça-se aqui.',
   18: 'Ver «Como conduzir o “Em turma”».',
   21: 'Charneira 2 (ver abaixo).',
   22: 'Relógio projetado (12 minutos de escrita). O docente recolhe os papéis por código.',
   23: 'Volta oral à pergunta do Abre e aos números do quadro: quantos mudaram de posição, e porquê.',
  },
  'folga': 'Ponto de partida, se não se fez no início. Quem acaba relê o Lê ou abre os lados do Decide; o docente circula.',
  'projeto_aula': 'Lista do passo e relógio projetados; cerca de dez conversas de 3 minutos (em três sessões, o docente passa por toda a turma).',
  'entrega': 'Recolha do papel A6, por código.',
  'decide': [
   'Antes de abrir os lados: braço no ar, uma vez, sem justificar. No quadro: Sim, Não, Depende, com os três números.',
   'Só depois se abrem os três lados na projeção, um a um, lidos em voz alta. Ninguém tem de dizer porquê nesta altura.',
   'Não há resposta certa. O que importa é ficar um registo para comparar no «Em turma». Quem não quiser levantar o braço escolhe no telemóvel: a escolha fica só no aparelho.',
  ],
  'em_turma': [
   'Um minuto em silêncio: cada aluno decide outra vez no cartão.',
   'Nova contagem de braço no ar, escrita ao lado dos números do Decide: quem mudou, e porquê.',
   'Seis minutos: duas vozes por lado, cada uma com uma prova do material (uma expressão entre aspas, com o artigo).',
   'No quadro, três colunas: o que sabemos, o que falta saber, o que pesa mais neste caso.',
   'Regra: fala-se do que se viu, nunca de quem. Se a turma se dividir, não se fecha: a posição vai para o papel.',
   'No fim, «O direito que pesou»: quantos escolheram vida privada, imagem ou liberdade de expressão.',
   'O cartão acaba-se sozinho (decisão 154): quem faltou ou faz a sessão em casa compara com a escolha do início e abre os três lados.',
  ],
  'charneiras': [
   (12, 'Verdadeiro, por ler o 19.º sozinho: «se tenho liberdade de expressão, posso publicar».',
    'Se mais de um terço erra, voltar ao Lê na projeção e ler o 12.º e o 19.º lado a lado. Pergunta: «O que diz o 12.º sobre a Sara?»'),
   (21, '«A partilha atinge a imagem da Sara, e o colega quis humilhá-la» (toma uma suposição sobre o colega por prova: o que ele quis, nenhum texto da sessão mostra) ou «A partilha é aceitável, porque a Sara estava num sítio público» (deixa de fora o 26.º e o pedido da Sara).',
    'Se mais de um terço erra, projetar a cadeia do cartão 20 e perguntar, frase a frase, de onde vem a prova.'),
  ],
  'papel': ['A conclusão responde à pergunta sem ir além das provas.', 'A prova junta um facto do caso a uma expressão exata, entre aspas, com o artigo.',
            'A dúvida é verdadeira: se tivesse resposta, podia mudar a conclusão.'],
  'devolucao': ('O docente recolhe os papéis (código e data, nunca o nome) e devolve-os no início da sessão 02, com uma marca por critério: ✓ cumpre, '
                '~ em parte, ○ falta. O aluno guarda o papel no dossiê do projeto. A sessão 02 abre com o Recupera; é o momento de devolver.'),
  'projeto': ('Três perguntas candidatas', '#pergunta-resposta',
              'Dez minutos para apresentar a Pergunta Humana na versão individual: um teatro-documento individual, em que as falas vêm da '
              'investigação (entrevistas, documentos e dados). Mostrar «Uma boa pergunta» na página do projeto. Trinta minutos: cada aluno escreve, '
              'em papel, três perguntas candidatas e testa cada uma com os três critérios; o docente faz cerca de dez conversas de 3 minutos. '
              'Cinco minutos: cada aluno sublinha a pergunta de que mais gosta. A mostra da sessão 10 é de 3 minutos e 2 de defesa por aluno '
              '(decisão 159); a página do projeto ainda diz 5 a 8 minutos e muda no pedido 3.'),
  'produto': 'Três perguntas candidatas',
  'grelha': [('Três perguntas sobre o que é ser humano, cada uma numa frase', 4), ('Nenhuma se responde com «sim» ou «não»', 4),
             ('Nenhuma se resolve com cinco minutos de pesquisa', 4), ('Cada uma pode investigar-se na escola, no bairro ou na família', 4),
             ('Cada uma diz de quem ou de que situação fala, sem nomear colegas', 4)],
  'noventa': [
   'Primeira aula: cartões 1 a 15 (60 minutos), 10 de Ponto de partida e 20 de projeto (a apresentação da Pergunta Humana e a primeira pergunta candidata).',
   'Segunda aula: reentrada no cartão 16, a Volta ao caso, escrita para isso; cartões 16 a 23 (50 minutos), 35 de projeto e 5 de entrega.',
   'Durante oito dias, cada telemóvel volta ao cartão onde ficou: na segunda aula, cada aluno abre a sessão e continua no cartão 16. '
   'A projeção vai direta ao cartão 16 com a barra dos cartões.',
  ],
  'imprimir': ['O Ponto de partida, um por aluno (ligação no fim deste guia).', 'Papéis A6 para «Agora, em papel»: um A4 dá quatro.',
               'A versão para imprimir da sessão, para quem não tem telemóvel, bateria ou rede: os 14 exercícios sem as respostas e o papel.',
               'Nada mais: a lição projeta-se.'],
  'caso_real': ('O caso do cartão 15 é real: acórdão do Tribunal da Relação de Évora de 25/06/2015, processo 789/13.7TMSTB-B.E1, em dgsi.pt. '
                'Cita-se só o que o acórdão diz: a ordem aos pais (ponto 11 do regime provisório) e duas passagens da fundamentação. A filha tinha 12 '
                'anos à data do acórdão (nascida em 2003, segundo o relatório). O acórdão é anonimizado; não se procuram nomes.'),
  'notas': ['O caso da Sara, o das mensagens e o da voz gravada são inventados e assim se diz; ninguém escreve sobre um colega identificável.',
            'Sem vídeo: a decisão 155 deixa no máximo um, visto por inteiro, em «Para ir mais longe». O vídeo do TED-Ed de Benedetta Berti não foi visto por inteiro pela equipa e fica de fora.',
            'Recupera 1, _Rhythm 0_: os factos vêm do registo da obra na Moderna galerija de Ljubljana (MG+MSUM), que a tem na coleção, incluindo o objetivo da artista («testar os limites da relação entre a artista e o público»). Não se mostram imagens da performance: os relatos são fortes.',
            'Olha: o cargo de Eleanor Roosevelt (presidiu à Comissão dos Direitos Humanos da ONU) confere com a página «Drafters of the Declaration» das Nações Unidas (un.org, consultada a 6/11/2026).',
            'Cada exercício tem a sua pista (botão «Pista»), escrita para o cartão e conferida pelo validador: nunca dá a resposta.',
            'Recupera 2: a distinção entre observar e interpretar vem da Etapa 1, «O que vemos» («demora a pagar» observa-se; «está a fazer-me perder tempo» interpreta-se).',
            'Grelha do passo do projeto: proposta da equipa, para o docente rever (indicativa).'],
 },
 # 06/11/2026 (decisão 166): a sessão 02 passa ao molde final (cidadania-2026-11), como a 01. O que só o docente faz vive aqui,
 # nunca no texto do aluno (decisão 154). A tabela dos tempos e as respostas tiram-se dos cartões da lição.
 '02': {
  'molde': True,
  'dominio': 'Direitos Humanos: o direito à imagem (Código Civil, artigo 79.º), o consentimento para um uso, as exceções e o seu limite.',
  'ensina': 'Separar filmar, rever e publicar; ver que o sim vale para o uso que se explicou; reconhecer quando a lei dispensa o consentimento e o limite que fica, sem ir além das provas.',
  'antes': ('Devolver, no início, o papel da sessão 01 com a marca por critério. Ninguém é filmado nem fotografado na aula; nenhum vídeo '
            'real de alunos entra na sessão.'),
  'na_aula': {
   1: 'O docente lê o caso em voz alta; a ligação «Projetar» abre a sessão na projeção e cada aluno abre-a no telemóvel.',
   2: 'Ver «Como conduzir o Decide».',
   3: 'Quando todos acabam, projeta-se e toca-se em «Mostrar resposta». Devolve-se o papel da sessão 01.',
   4: 'O retorno nomeia a sessão 01: vale a pena lembrar, em voz alta, o artigo 12.º até «honra e reputação».',
   5: 'Projetado grande. Os pormenores (o rosto de frente, os pés descalços, as bobinas) só se apontam depois dos cartões 6 e 7.',
   8: 'Ler em voz alta os três números do artigo 79.º, uma vez; o n.º 3 começa a mudar a conversa com «porém».',
   12: 'Charneira 1 (ver abaixo): dedos no ar, um para verdadeiro e dois para falso.',
   13: 'O docente explica com a projeção, passo a passo, no máximo 6 minutos.',
   15: 'O caso é real: vale a pena abrir o acórdão na projeção (ligação no retorno) e mostrar o sumário IV e a passagem citada.',
   16: 'Projetado e lido em voz alta. Numa segunda aula de 90 minutos, recomeça-se aqui.',
   18: 'Ver «Como conduzir o “Em turma”».',
   21: 'Charneira 2 (ver abaixo).',
   22: 'Relógio projetado (12 minutos de escrita). O docente recolhe os papéis por código.',
   23: 'Volta oral à pergunta do Abre e aos números do quadro: quantos mudaram de posição, e porquê.',
  },
  'folga': 'Quem acaba relê o Lê ou abre os lados do Decide; o docente circula.',
  'projeto_aula': 'Lista do passo e relógio projetados; cerca de dez conversas de 3 minutos (em três sessões, o docente passa por toda a turma).',
  'entrega': 'Recolha do papel A6, por código.',
  'decide': [
   'Antes de abrir os lados: braço no ar, uma vez, sem justificar. No quadro: Sim, Não, Depende, com os três números.',
   'Só depois se abrem os três lados na projeção, um a um, lidos em voz alta. Ninguém tem de dizer porquê nesta altura.',
   'Não há resposta certa. O que importa é ficar um registo para comparar no «Em turma». Quem não quiser levantar o braço escolhe no telemóvel: a escolha fica só no aparelho.',
  ],
  'em_turma': [
   'Um minuto em silêncio: cada aluno decide outra vez no cartão.',
   'Nova contagem de braço no ar, escrita ao lado dos números do Decide: quem mudou, e porquê.',
   'Seis minutos: duas vozes por lado, cada uma com uma prova do material (uma expressão entre aspas, com o número do artigo 79.º).',
   'No quadro, três colunas: o que sabemos, o que falta saber, o que pesa mais neste caso.',
   'Regra: fala-se do que se viu, nunca de quem. Se a turma se dividir, não se fecha: a posição vai para o papel.',
   'No fim, «A razão que pesou»: quantos escolheram o uso aceite (n.º 1), os fins didáticos (n.º 2) ou o decoro (n.º 3).',
   'O cartão acaba-se sozinho (decisão 154): quem faltou ou faz a sessão em casa compara com a escolha do início e abre os três lados.',
  ],
  'charneiras': [
   (12, 'Verdadeiro, por ler o n.º 2 sozinho: «se foi num lugar público, posso publicar».',
    'Se mais de um terço erra, voltar ao Lê na projeção e ler o n.º 2 e o n.º 3 seguidos. Pergunta: «O que acrescenta o “porém” do n.º 3?»'),
   (21, '«A escola pode publicar, porque a Marta aceitou ser filmada» (toma a razão do Duarte por prova e esquece o uso aceite) ou «A escola não pode publicar, porque quer humilhar a Marta» (supõe uma intenção que nenhum material mostra).',
    'Se mais de um terço erra, projetar a cadeia do cartão 20 e perguntar, frase a frase, de onde vem a prova.'),
  ],
  'papel': ['A conclusão responde à pergunta sem ir além das provas.', 'A prova junta um facto do caso a uma expressão exata, entre aspas, com o artigo.',
            'A dúvida é verdadeira: se tivesse resposta, podia mudar a conclusão.'],
  'devolucao': ('O docente recolhe os papéis (código e data, nunca o nome) e devolve-os no início da sessão 03, com uma marca por critério: ✓ cumpre, '
                '~ em parte, ○ falta. O aluno guarda o papel no dossiê do projeto.'),
  'projeto': ('O teu pedido de consentimento', '#metodo',
              'Cinco minutos para ler, na página do projeto, «Ética: as pessoas que entrevistas». Trinta minutos: cada aluno escreve, em papel, '
              'o seu pedido de consentimento em quatro partes (para quê; que uso; onde fica e até quando; como se retira o sim), para uma '
              'entrevista que queira fazer; o docente faz cerca de dez conversas de 3 minutos. Dez minutos: cada aluno relê o pedido com «O que '
              'conta» e corrige uma parte. O pedido entra no dossiê da Pergunta Humana.'),
  'produto': 'Pedido de consentimento',
  'grelha': [('Para quê: a finalidade dita em palavras simples', 4), ('Que uso: voz, cara ou só as palavras', 4), ('Onde fica e até quando', 4),
             ('Como se retira o sim, e a quem se diz', 4), ('Cuidado com menores: o pedido vai também ao encarregado de educação', 4)],
  'noventa': [
   'Primeira aula: cartões 1 a 15 (60 minutos), 10 de folga e 20 de projeto (a leitura da ética das entrevistas e o início do pedido).',
   'Segunda aula: reentrada no cartão 16, a Volta ao caso, escrita para isso; cartões 16 a 23 (50 minutos), 35 de projeto e 5 de entrega.',
   'Durante oito dias, cada telemóvel volta ao cartão onde ficou: na segunda aula, cada aluno abre a sessão e continua no cartão 16. '
   'A projeção vai direta ao cartão 16 com a barra dos cartões.',
  ],
  'imprimir': ['Papéis A6 para «Agora, em papel»: um A4 dá quatro.',
               'A versão para imprimir da sessão, para quem não tem telemóvel, bateria ou rede: os 14 exercícios sem as respostas e o papel.',
               'Nada mais: a lição projeta-se.'],
  'caso_real': ('O caso do cartão 15 é real: acórdão do Supremo Tribunal de Justiça de 07/06/2011, processo 1581/07.3TVLSB.L1.S1, em dgsi.pt. '
                'Uma mãe e a filha, sócias de um clube de Lisboa, foram fotografadas na piscina numa sessão aberta a sócios e familiares e '
                'saíram na capa de uma revista distribuída com um jornal. O tribunal negou a revista: concluiu que a mãe consentira na captação '
                'e na publicação «numa publicação», porque lho tinham dito; que as fotografias seriam só para os sócios, ela não o provou. '
                'Cita-se só o que o acórdão diz: o sumário (IV) e a passagem da fundamentação sobre o que foi dito à mãe. O acórdão é '
                'anonimizado; não se procuram nomes.'),
  'notas': ['O caso da Marta, o da montagem, o da praça, o do rapaz na poça e o do cartão da biblioteca são inventados e assim se diz; a cena '
            'da Lia foi escrita para a sessão 05 do M1 publicado (que a turma não fez). Ninguém escreve sobre um colega identificável.',
            'Sem vídeo (decisão 155). O candidato do plano, «Be kind online: consent to share and cyberbullying», está no sítio oficial '
            'Bullying. No Way! (bullyingnoway.gov.au, State of Queensland, em nome das autoridades de educação australianas, aberto a 6/11/2026), '
            'mas trata de uma imagem íntima partilhada sem consentimento e a equipa não o viu por inteiro. Se o docente o vir e o quiser, '
            'entra em «Para ir mais longe», com a alternativa escrita.',
            'Recupera 1, _The Truman Show_ (Peter Weir, 1998): a turma já viu o filme no percurso anterior; não se volta a exibir. O cartão usa só '
            'a premissa (a vida de Truman passa na televisão e todos à volta são atores, menos ele).',
            'Olha: o registo da Library of Congress (loc.gov/item/2018675335, aberto a 6/11/2026) dá o título do cartão do National Child Labor '
            'Committee, «1910 February», North Pownal, Vermont, a atribuição a Lewis Hine «based on provenance» e «No known restrictions on '
            'publication». O cartão original diz ainda que as raparigas da fábrica diziam que ela tinha dez anos e que ela admitiu ao '
            'fotógrafo ter doze: bom para a conversa depois do cartão 6.',
            'Cartão 11 (a praça) e charneira 1 (o rapaz na poça): a leitura de «enquadrada na de lugares públicos» (as pessoas como parte do '
            'lugar, não como assunto) e a de «simples decoro» aplicada a uma queda são leituras nossas do artigo 79.º; o docente confirma.',
            'Conceito: «pode ser retirado» assenta no artigo 81.º, n.º 2, do Código Civil (a limitação voluntária dos direitos de personalidade '
            '«é sempre revogável», ainda que com obrigação de indemnizar); ligar esse artigo ao direito à imagem é leitura nossa.',
            'Lei n.º 58/2019, artigo 16.º: só aparece para separar os 13 anos dos serviços digitais do consentimento para publicar a imagem de alguém.',
            'Cada exercício tem a sua pista (botão «Pista»), escrita para o cartão e conferida pelo validador: nunca dá a resposta.',
            'Grelha do passo do projeto: proposta da equipa, para o docente rever (indicativa).'],
 },
 # 06/11/2026 (decisões 166 a 168): a sessão 03 passa ao molde final (cidadania-2026-11), como a 01 e a 02. O que só o docente faz
 # vive aqui, nunca no texto do aluno (decisão 154). A tabela dos tempos e as respostas tiram-se dos cartões da lição.
 '03': {
  'molde': True,
  'dominio': 'Direitos Humanos: igualdade e não discriminação (Constituição, artigo 13.º), os direitos da criança com deficiência (Convenção, artigo 23.º) e a discriminação indireta (Lei n.º 46/2006).',
  'ensina': 'Ver que uma regra igual para todos pode ter efeitos desiguais, encontrar a barreira (no espaço, na informação, na decisão, no horário), separar ver de participar e pesar uma solução com orçamento sem ir além das provas.',
  'antes': ('Devolver, no início, o papel da sessão 02 com a marca por critério. Antes de projetar a fotografia do cartão 5, uma frase de '
            'enquadramento (decisão 30): a placa é de um tempo em que, em vários estados do sul dos Estados Unidos, a segregação racial '
            'era imposta por lei. Se houver na turma alguém com deficiência, não se usa como exemplo: o Rui e a Joana são personagens.'),
  'na_aula': {
   1: 'O docente lê o caso em voz alta; a ligação «Projetar» abre a sessão na projeção e cada aluno abre-a no telemóvel.',
   2: 'Ver «Como conduzir o Decide».',
   3: 'Quando todos acabam, projeta-se e toca-se em «Mostrar resposta». Devolve-se o papel da sessão 02.',
   4: 'O retorno nomeia a sessão 01: vale a pena lembrar, em voz alta, a força de cada texto (declaração, tratado, Constituição).',
   5: 'Projetado grande, depois da frase de enquadramento. Os pormenores (a seta, a palavra «COLORED») só se apontam depois dos cartões 6 e 7.',
   8: 'Ler em voz alta o artigo 13.º, n.º 2, e o artigo 23.º, n.º 1, uma vez cada; perguntar quem protege cada um.',
   12: 'Charneira 1 (ver abaixo): dedos no ar, um para verdadeiro e dois para falso.',
   13: 'O docente explica com a projeção, passo a passo, no máximo 6 minutos.',
   15: 'O caso é real: vale a pena abrir o acórdão na projeção (ligação no retorno, em inglês) e mostrar o § 10 (a oferta do acompanhante) e o § 72 (a razão do Tribunal).',
   16: 'Projetado e lido em voz alta. Numa segunda aula de 90 minutos, recomeça-se aqui.',
   18: 'Ver «Como conduzir o “Em turma”».',
   21: 'Charneira 2 (ver abaixo).',
   22: 'Relógio projetado (12 minutos de escrita). O docente recolhe os papéis por código.',
   23: 'Volta oral à pergunta do Abre e aos números do quadro: quantos mudaram de posição, e porquê.',
  },
  'folga': 'Quem acaba relê o Lê ou abre os lados do Decide; o docente circula.',
  'projeto_aula': 'Lista do passo e relógio projetados; cerca de dez conversas de 3 minutos (em três sessões, o docente passa por toda a turma).',
  'entrega': 'Recolha do papel A6, por código.',
  'decide': [
   'Antes de abrir os lados: braço no ar, uma vez, sem justificar. No quadro: Sim, Não, Depende, com os três números.',
   'Só depois se abrem os três lados na projeção, um a um, lidos em voz alta. Ninguém tem de dizer porquê nesta altura.',
   'Não há resposta certa. O que importa é ficar um registo para comparar no «Em turma». Quem não quiser levantar o braço escolhe no telemóvel: a escolha fica só no aparelho.',
  ],
  'em_turma': [
   'Um minuto em silêncio: cada aluno decide outra vez no cartão e gasta, sozinho, as cinco unidades (a escolha «Como gastas as cinco unidades?»).',
   'Nova contagem de braço no ar, escrita ao lado dos números do Decide: quem mudou, e porquê. Depois, a contagem por opção das cinco unidades: mudar e legendar, mudar e transmitir, legendar e transmitir.',
   'Seis minutos: duas vozes por opção, cada uma com uma prova do material (uma expressão entre aspas, com o artigo) e a dizer quem fica de fora com essa escolha.',
   'No quadro, três colunas: o que sabemos, o que falta saber, o que pesa mais neste caso.',
   'Regra: fala-se do que se viu, nunca de quem. Se a turma se dividir, não se fecha: a posição vai para o papel.',
   'O cartão acaba-se sozinho (decisão 154): quem faltou ou faz a sessão em casa compara com a escolha do início e abre os três lados.',
  ],
  'charneiras': [
   (12, 'Verdadeiro, por pensar que ver tudo pelo vídeo é estar na mostra («ele vê tudo»).',
    'Se mais de um terço erra, voltar ao Lê na projeção e ler o artigo 23.º até «participação activa». Pergunta: «O que fazem na mostra os colegas que estão na sala?»'),
   (21, '«A mostra fica em cima, porque a maioria perderia os seus lugares» (toma a razão dos pais por prova; ninguém contou os convidados) ou «A organização quer afastar o Rui e, por isso, tem de ser castigada» (supõe uma intenção que nenhum material mostra).',
    'Se mais de um terço erra, projetar a cadeia do cartão 20 e perguntar, frase a frase, de onde vem a prova.'),
  ],
  'papel': ['A conclusão responde à pergunta sem ir além das provas.', 'A prova junta um facto do caso a uma expressão exata, entre aspas, com o artigo.',
            'A dúvida é verdadeira: se tivesse resposta, podia mudar a conclusão.'],
  'devolucao': ('O docente recolhe os papéis (código e data, nunca o nome) e devolve-os no início da sessão 04, com uma marca por critério: ✓ cumpre, '
                '~ em parte, ○ falta. O aluno guarda o papel no dossiê do projeto.'),
  'projeto': ('A tua pergunta', '#pergunta-resposta',
              'Cinco minutos para ler, na página do projeto, «Uma boa pergunta». Trinta minutos: cada aluno escreve, em papel, a sua pergunta em '
              'três versões (a primeira, uma mais delimitada, com que pessoas, que lugar e que tempo, e a final); o docente faz cerca de dez '
              'conversas de 3 minutos. Dez minutos: cada aluno relê a versão final com «O que conta» e corrige-a. A pergunta entra no dossiê da '
              'Pergunta Humana.'),
  'produto': 'A pergunta da Pergunta Humana',
  'grelha': [('Não se responde com «sim» ou «não»', 4), ('Delimitada: que pessoas, que lugar, que tempo', 4), ('Investigável com fontes a que o aluno tem acesso', 4),
             ('As três versões mostram o caminho até à final', 4), ('A versão final é clara e cabe numa frase', 4)],
  'noventa': [
   'Primeira aula: cartões 1 a 15 (60 minutos), 10 de folga e 20 de projeto (a leitura de «Uma boa pergunta» e a primeira versão).',
   'Segunda aula: reentrada no cartão 16, a Volta ao caso, escrita para isso; cartões 16 a 23 (50 minutos), 35 de projeto e 5 de entrega.',
   'Durante oito dias, cada telemóvel volta ao cartão onde ficou: na segunda aula, cada aluno abre a sessão e continua no cartão 16. '
   'A projeção vai direta ao cartão 16 com a barra dos cartões.',
  ],
  'imprimir': ['Papéis A6 para «Agora, em papel»: um A4 dá quatro.',
               'A versão para imprimir da sessão, para quem não tem telemóvel, bateria ou rede: os 14 exercícios sem as respostas e o papel.',
               'Nada mais: a lição projeta-se.'],
  'caso_real': ('O caso do cartão 15 é real: Tribunal Europeu dos Direitos Humanos, Enver Şahin c. Turquia, queixa n.º 23065/12, acórdão de 30 de '
                'janeiro de 2018 (HUDOC, em inglês e em francês; sem tradução portuguesa). Um estudante de mecânica ficou paraplégico num acidente em '
                '2005 e pediu à faculdade que adaptasse o edifício para voltar às aulas (§§ 6 e 7). A faculdade respondeu que o edifício, com vários '
                'pisos, não se podia adaptar; a administração disse que as aulas teóricas, num edifício de três pisos, se podiam resolver com a ajuda '
                'de um acompanhante, e que o orçamento era limitado (§§ 8 e 10). O Tribunal disse que essa oferta, feita sem avaliar a situação '
                'concreta dele, não era razoável, porque ignorava a necessidade de viver da forma mais independente e autónoma possível (§§ 69 a 72), '
                'e concluiu, por seis votos contra um, que houve violação do artigo 14.º da Convenção Europeia dos Direitos Humanos, com o artigo 2.º '
                'do Protocolo n.º 1 (dispositivo, ponto 3). O cartão não cita o acórdão (não há texto português): conta-o por palavras nossas.'),
  'notas': ['O caso do Rui, o da direção e da Declaração, o das barreiras na escola, o da visita de estudo e o da reunião com os pais são '
            'inventados e assim se diz. Ninguém escreve sobre um colega identificável.',
            'Sem vídeo (decisão 155). O plano não propõe candidato para esta sessão; o vídeo do piloto (TED-Ed, «What does this symbol actually '
            'mean?», lição de Adrian Treharne) não foi visto por inteiro pela equipa e fica de fora.',
            'Recupera 1, _The Egg_, de Andy Weir (#84, s03): o cartão usa só a premissa do conto, como o #84. A confirmar no sítio do autor '
            '(galactanet.com), que não abriu nesta passagem.',
            'Olha: o ficheiro é o do piloto, a versão do Wikimedia Commons com as margens cortadas (aberta a 6/11/2026: Esther Bubley, setembro de '
            '1943, estação Greyhound de Rome, Geórgia; Library of Congress, cph.3b22541; domínio público). O registo da Library of Congress '
            '(loc.gov/item/2017862110) foi lido pelo piloto a 31/10; a 6/11 não abriu (verificação contra robôs): a confirmar.',
            'A legenda traduz «colored waiting room» por «sala de espera para “pessoas de cor”», a palavra da época, entre aspas.',
            'Cartão 10 (fora da lista): o artigo 13.º, n.º 2, não diz «deficiência»; a resposta assenta no que os textos dizem (a Convenção, '
            'artigo 23.º; a Constituição, artigo 71.º, no «Ler mais»), sem dizer se a lista do n.º 2 é ou não fechada. A Convenção vale para o Rui '
            'porque tem 16 anos (artigo 1.º: «criança é todo o ser humano menor de 18 anos»).',
            'A Convenção cita-se na tradução portuguesa anexa à Resolução da Assembleia da República n.º 20/90, com a grafia e as palavras da fonte '
            '(«criança mental e fisicamente deficiente», «activa»); hoje, a Lei n.º 46/2006 diz «pessoas com deficiência».',
            'Conceito: o nome e a definição assentam na Lei n.º 46/2006, artigo 3.º, alínea b) («Discriminação indirecta»), que a lei define para a '
            'deficiência; aplicá-lo à religião (cartão 14) é alargamento nosso, para o docente confirmar.',
            'Volta ao caso: as cinco unidades vêm do guia do piloto (mudar de sala custa três); as legendas e a transmissão para o átrio custam duas '
            'cada, para que as três medidas não caibam juntas no orçamento.',
            'Cada exercício tem a sua pista (botão «Pista»), escrita para o cartão e conferida pelo validador: nunca dá a resposta.',
            'Grelha do passo do projeto: proposta da equipa, para o docente rever (indicativa).'],
 },
 '04': {
  'dominio': 'Direitos Humanos (liberdade de expressão, bom nome); Democracia (discurso de ódio); Media (fontes, verificação).',
  'ensina': 'Separar opinião, sátira e acusação de facto, e verificar antes de repetir.',
  'passos': [
   (5, 'Cada aluno recebe as três afirmações reais e as três publicações inventadas sobre a escola.'),
   (25, 'Verificar cada afirmação: origem (quem, onde, quando), duas fontes independentes e veredicto (verdadeiro, falso, enganador ou sem prova). Leitura lateral: abrir outros separadores antes de ler a página até ao fim.'),
   (10, 'Pausa.'),
   (15, 'As três publicações: manter, corrigir ou retirar, com o artigo (Constituição, 37.º e 26.º; Convenção, 13.º).'),
   (10, 'O registo de fontes de cada aluno para a Pergunta Humana: duas fontes da sua pergunta, com o que é preciso para as reencontrar.'),
  ],
  'materiais': ['As três afirmações reais: o docente escolhe-as e confirma-as num verificador de factos antes da aula (não vêm prontas aqui).', 'Três publicações inventadas sobre a escola: uma crítica, uma sátira e uma acusação sem prova.', 'O registo de verificação: origem, fonte 1, fonte 2, porque são independentes, veredicto.', 'Um computador ou telemóvel por aluno.'],
  'escrito': 'O registo de verificação das três afirmações (é o laboratório de verificação do módulo) e o registo de fontes de cada aluno.',
  'projeto': ('As fontes', '#metodo', 'O registo de fontes, localizável, e a leitura lateral; o laboratório de verificação do módulo faz-se nesta sessão.'),
  'produto': 'Laboratório de verificação',
  'grelha': [('Origem identificada (quem, onde, quando)', 4), ('Duas fontes independentes e porque o são', 5), ('Veredicto proporcional à prova', 4), ('Decisão sobre as três publicações, com o artigo', 4), ('Registo localizável', 3)],
  'notas': ['Casos reais só os que o docente escolhe e confirma (decisão 12).', 'Na imagem, o cartão diz só o que está impresso na página de 1834; a atribuição a Daumier e a história do julgamento de Philipon ficam por confirmar na Gallica.', 'A Convenção Europeia dos Direitos Humanos (artigo 10.º) e o Código Penal (artigo 240.º) ficam fora dos cartões até se confirmarem.'],
 },
 '05': {
  'dominio': 'Direitos Humanos (reserva da vida privada, proteção de dados); Democracia (limites a quem vigia); Media.',
  'ensina': 'Pesar segurança e privacidade e saber o que a lei deixa fazer numa escola.',
  'passos': [
   (5, 'Cada aluno recebe o formulário inventado da visita de estudo.'),
   (15, 'Riscar o que não é preciso para a visita; ao lado de cada dado que fica, quem o vê e quando se apaga.'),
   (5, 'As regras da volta: em aula, com o docente, sem fotografar pessoas nem matrículas; anota-se só o que o aviso diz.'),
   (20, 'A volta ao quarteirão da escola, a contar câmaras e avisos de videovigilância: onde estão, quem é o responsável, que finalidade dizem.'),
   (10, 'Pausa.'),
   (10, 'Na sala, a nota de privacidade em cinco linhas e o plano de recolha das entrevistas: o que se guarda, onde, até quando, com que anonimato.'),
  ],
  'materiais': ['O formulário inventado da visita de estudo (por exemplo: nome, turma, data de nascimento, morada, número do documento de identificação, alergias, contacto de emergência, profissão dos pais, religião, fotografia).', 'O registo dos avisos, em papel, e pranchetas.'],
  'escrito': 'O formulário revisto, a nota de privacidade, o registo dos avisos e o plano de recolha das entrevistas.',
  'projeto': ('A recolha', '#fases', 'O plano de entrevistas e de dados (anonimato, onde se guarda, quando se apaga) entra no dossiê.'),
  'produto': 'Formulário revisto e registo',
  'grelha': [('Dados riscados com razão', 4), ('Finalidade e quem vê', 4), ('Prazo e forma de apagar', 4), ('Registo dos avisos, factual e sem rostos', 4), ('Plano de recolha do projeto, com anonimato', 4)],
  'notas': ['Saída só à volta da escola, em aula, sem autorização especial (decisão 10). Quem não pode sair regista as câmaras e os avisos visíveis do portão.', 'Imagem: a planta do panóptico desenhada pelo arquiteto Willey Reveley não se descarregou (o servidor recusou os pedidos três vezes e não se insistiu); entrou a página de título da edição de 1791.', 'O Regulamento Geral sobre a Proteção de Dados (artigos 5.º e 8.º) fica fora dos cartões até se confirmar no EUR-Lex.'],
 },
 '06': {
  'dominio': 'Democracia e Instituições Políticas (regras coletivas, ética e integridade, conflito de interesses); Direitos Humanos (igualdade).',
  'ensina': 'Comparar critérios de repartir, separar o resultado dos limites e ver o que muda quando quem decide ganha com a decisão.',
  'passos': [
   (5, 'O problema no quadro: seis turnos de filmagem para três grupos. Listar os critérios: igualdade, necessidade, ordem de inscrição, sorteio, outro.'),
   (10, 'Cada aluno escolhe a regra e escreve-a numa frase, sem saber o lugar que lhe vai calhar.'),
   (5, 'Cada aluno tira uma carta com o lugar (A, B ou C) e a situação desse lugar (por exemplo: o grupo C perdeu um turno porque o material não chegou).'),
   (10, 'Aplicar a regra. Quem perde apresenta a objeção em dois minutos, em turma; quem escreveu a regra responde ou revê.'),
   (10, 'Pausa.'),
   (25, 'A mesma pergunta para o teatro-documento: como se repartem as falas e o tempo de cena. A regra de cada aluno e o primeiro esboço do guião (quem fala, quanto tempo, com que fonte).'),
  ],
  'materiais': ['Cartas A, B e C, com a situação de cada lugar.', 'O quadro dos seis turnos.', 'Papel para o esboço do guião.'],
  'escrito': 'A regra final, quem perde com ela e porque a aceitaria mesmo assim; a regra de cada aluno para as falas, com o primeiro esboço do guião.',
  'projeto': ('O guião, em esboço', '#metodo', 'A regra de cada aluno para repartir falas e tempo de cena e o primeiro esboço do guião entram no dossiê.'),
  'produto': 'Regra e esboço',
  'grelha': [('Regra clara e aplicável', 4), ('Quem perde e porquê, dito do ponto de vista de quem perde', 4), ('Objeção respondida', 4), ('Conflito de interesses reconhecido', 4), ('Regra das falas', 4)],
  'notas': ['Enquadramento da imagem, antes de a projetar (decisão 30): à volta da Justiça, a gravura mostra castigos corporais do século XVI.', 'O problema do elétrico (Foot, Thomson) e a escolha de regras sem saber o lugar (Rawls) ficam como linha de fonte; a lição 1 da Justiça pode servir como leitura a mais, sem obrigatoriedade.'],
 },
 '07': {
  'dominio': 'Democracia e Instituições Políticas (deliberar e votar, tribunais); Direitos Humanos (presunção de inocência, direito a ser ouvido). Mecânica do M1: o Tribunal de turma.',
  'ensina': 'Separar prova de inferência, ouvir a defesa e ver o voto mudar, ou não mudar, com as provas.',
  'passos': [
   (5, 'Distribuir as cartas de papéis (acusação, defesa, três testemunhas, júri, relator, quem guarda o tempo) e o dossiê do caso.'),
   (10, 'Preparação por papel: a acusação e a defesa escolhem duas provas cada; as testemunhas leem o seu depoimento.'),
   (5, 'Primeiro voto do júri, em boletim, com uma razão obrigatória.'),
   (20, 'A audiência: acusação, defesa, três testemunhas e alegações finais, dois minutos por intervenção, com o relógio à vista.'),
   (10, 'Pausa.'),
   (10, 'Deliberação do júri e segundo voto, com razão; o relator conta quantos votos citam uma prova.'),
   (10, 'O acórdão da turma: a decisão, duas provas citadas, uma dúvida razoável e um voto vencido.'),
  ],
  'materiais': ['Cartas de papéis; numa turma grande, o júri tem as pessoas que sobram.', 'O dossiê do caso inventado: a captura de ecrã, três depoimentos curtos e a cronologia.', 'Boletins, dois por jurado, e um relógio visível.', 'O modelo do acórdão.'],
  'escrito': 'O acórdão da turma e as notas de cada papel, com o nome de quem as escreveu.',
  'projeto': ('Nenhum passo novo em aula', '#fases', 'Cinco minutos de ponto de situação do guião, que continua fora da aula.'),
  'produto': 'Acórdão',
  'grelha': [('Decisão clara', 3), ('Duas provas citadas, sem confundir prova com inferência', 5), ('Uma dúvida razoável', 4), ('Voto vencido com razão', 4), ('Papel cumprido, com notas próprias', 4)],
  'notas': ['Nenhum aluno faz de vítima: a colega do caso não entra em cena.', 'Imagem: a fotografia dos óstracos com o nome do general ateniense Temístocles não se descarregou (o servidor e o Flickr recusaram os pedidos, e não se insistiu); entrou uma litografia de Daumier do Metropolitan Museum of Art (CC0).', 'A Lei n.º 51/2012 (Estatuto do Aluno e Ética Escolar) fica fora dos cartões até se confirmar no Diário da República.'],
 },
 '08': {
  'dominio': 'Democracia e Instituições Políticas (órgãos de soberania, autarquias, União Europeia, eleições, petição, Provedor de Justiça).',
  'ensina': 'Distinguir quem faz as leis, quem governa, quem julga e quem decide o que se faz na rua, e escrever um pedido com destinatário e fundamento.',
  'passos': [
   (5, 'As regras da volta (em aula, com o docente, sem fotografar pessoas nem matrículas) e a grelha das seis coisas.'),
   (30, 'A volta ao quarteirão: passadeira, semáforo, contentor, banco, sinal, paragem; ao lado de cada uma, quem acham que decide.'),
   (10, 'Pausa.'),
   (10, 'Na sala, confirmar nos sítios da junta de freguesia e da câmara municipal quem decide cada coisa.'),
   (15, 'O pedido de uma página à entidade certa: destinatário, o que se pede, porquê (um facto observado e o artigo 52.º da Constituição), quem assina.'),
  ],
  'materiais': ['A grelha das seis coisas e pranchetas.', 'Os endereços dos sítios da junta de freguesia e da câmara municipal (o docente confirma-os antes).', 'O modelo do pedido.'],
  'escrito': 'O mapa de quem decide e o pedido de uma página.',
  'projeto': ('Nenhum passo novo em aula', '#fases', 'O guião completo, com a fonte de cada fala, fica pronto para o ensaio da sessão 09.'),
  'produto': 'Pedido à entidade certa',
  'grelha': [('Entidade certa, com a razão', 4), ('Pedido claro e possível', 4), ('Fundamento com artigo e factos observados', 4), ('Mapa de quem decide, factual', 4), ('Forma: destinatário, data, assinaturas, linguagem', 4)],
  'notas': ['Saída só à volta da escola, em aula, sem autorização especial (decisão 10). Quem não pode sair confirma no sítio da câmara.', 'Quem decide cada coisa da rua depende do concelho: as respostas do cartão de emparelhar confirmam-se no sítio da câmara da escola.', 'Alternativa ao vídeo, em português: «Como podes contactar o Parlamento Europeu?», no Centro Multimédia do Parlamento Europeu (leitor próprio, não YouTube; o motor só tem o do YouTube).'],
 },
 '09': {
  'dominio': 'Pluralismo e Diversidade Cultural; Direitos Humanos (igualdade, liberdade religiosa, minorias).',
  'ensina': 'Ver como uma regra igual pode calar alguém e como um estereótipo diz o mesmo de todos; no ensaio, procurar a voz que falta.',
  'passos': [
   (10, 'Aquecimento «O outro lado»: cada pessoa tira uma posição e defende-a durante um minuto, mesmo sem concordar; depois troca.'),
   (5, 'Entregar a cada aluno a grelha de três colunas.'),
   (15, 'Metade dos alunos mostra o ensaio (5 a 8 minutos) a um colega e recebe as notas dele: o que se ouviu, de quem é a voz, de que fonte vem, que voz falta.'),
   (10, 'Pausa.'),
   (15, 'Trocam-se os papéis: quem observou mostra o ensaio e recebe as notas.'),
   (10, 'Cada aluno decide duas mudanças, uma delas para incluir uma voz que ainda não estava. Cada aluno prepara também uma objeção para um colega, para a sessão 10.'),
  ],
  'materiais': ['Cartões de posição para «O outro lado» (a regra do português nos intervalos e outras posições do módulo).', 'A grelha de observação em três colunas.', 'Um relógio visível.'],
  'escrito': 'As notas dadas aos colegas e duas mudanças decididas por cada aluno.',
  'projeto': ('O ensaio', '#av-teatro', 'O ensaio cruzado do teatro-documento, com a voz de quem discorda e a fonte de cada fala.'),
  'produto': 'Ensaio',
  'grelha': [('Voz que discorda presente e com fonte', 4), ('Ligação reconhecível às fontes', 4), ('Duração dentro dos 5 a 8 minutos', 3), ('Notas concretas aos colegas', 4), ('Duas mudanças decididas e justificadas', 5)],
  # 31/10/2026 (verificação final, decisão 39): a fotografia da Library of Congress saiu e a nota «Para rever» também.
  'notas': ['No exemplo de estereótipo, ninguém nomeia colegas.', 'Imagem: a fotografia prevista no plano, _Pipers_, tirada na ilha de Ellis por Augustus Sherman, não se descarregou (o servidor recusou os pedidos e a Biblioteca Pública de Nova Iorque bloqueia robôs). A da Library of Congress (LC-D6-87) também saiu: a biblioteca não diz quem a tirou nem a declara em domínio público.', 'A fotografia nova é de Lewis Hine, _Immigrant Family in the Baggage Room of Ellis Island_ (1905), do Museum of Fine Arts, Houston, e está em domínio público segundo o Wikimedia Commons. O título do museu não diz de onde vem a família: o cartão fala de imigrantes, não de um país.', 'A Declaração Universal (artigos 2.º e 18.º) e a Resolução do Conselho de Ministros n.º 127/2025 ficam fora dos cartões até se confirmarem.'],
 },
 '10': {
  'dominio': 'Direitos Humanos e Democracia e Instituições Políticas (síntese do módulo); Media (fontes). Ponto de chegada.',
  'ensina': 'Defender uma resposta com fontes e responder a uma objeção.',
  'antes': 'Antes de abrir a lição: o Ponto de chegada, em papel, sem ajuda e sem consulta (10 a 15 minutos), com as mesmas 10 perguntas do Ponto de partida. Os cartões de recuperação vêm depois, para não ensinarem as respostas antes.',
  'passos': [
   (5, 'A ordem das apresentações e as regras da defesa: uma pergunta do público e a objeção preparada por um colega na sessão 09.'),
   (30, 'As primeiras apresentações: 5 a 8 minutos cada, seguidos de três minutos de defesa.'),
   (10, 'Pausa.'),
   (25, 'As restantes apresentações. O docente decide o que fazer com as que não couberem nestes 25 minutos.'),
   (5, 'A autoavaliação «Vi, Situei, Fiz», em três linhas, e o mapa de direitos da sessão 01 revisto: o que mudou.'),
  ],
  'materiais': ['O Ponto de chegada impresso, um por aluno (ligação abaixo).', 'A ordem das apresentações e as objeções preparadas na sessão 09.', 'Um relógio visível.', 'A fotografia do mapa de direitos da sessão 01.'],
  'escrito': 'O Ponto de chegada, a autoavaliação «Vi, Situei, Fiz» e o mapa de direitos revisto.',
  'projeto': ('A apresentação e a defesa', '#av-teatro', 'A apresentação pública do teatro-documento e a defesa das escolhas de cada aluno.'),
  'produto': 'Apresentação e defesa',
  'grelha': [('Guião e cena fundamentados na investigação', 5), ('Ligação reconhecível às fontes', 4), ('Duração de 5 a 8 minutos e clareza', 3), ('Defesa: resposta à objeção com fonte e limite', 5), ('Contributo próprio identificado', 3)],
  'notas': ['Ganho de cada aluno: Ponto de chegada menos Ponto de partida, por código, numa tabela fora do sítio.'],
 },
}

# Ponto de partida e de chegada: as mesmas 10 perguntas, pela mesma ordem (proposta da equipa a partir do plano, para o docente rever).
# 8 de escolha (1 ponto cada) e 2 curtas escritas (0 a 2): máximo 12.
# 31/10/2026 (verificação final): as opções das perguntas 3, 5 e 6 foram acertadas para a regra das opções equilibradas (no
# máximo 20 % de amplitude e a certa a mais longa em 3 das 8, no máximo); tests/test_cidadania_piloto.py mede-as com a função
# de tools/medir_opcoes.py.
PONTO = [
 ('01', 'Uma fotografia tua, a dormir no autocarro, aparece no grupo da turma sem te perguntarem. Que direito está em causa em primeiro lugar?',
  ['a reserva da vida privada e a imagem', 'a liberdade de reunião no intervalo', 'o acesso gratuito ao ensino obrigatório'], 0),
 ('01', 'A Declaração Universal dos Direitos Humanos é…',
  ['uma lei aprovada pela Assembleia da República', 'uma declaração das Nações Unidas, não uma lei', 'um tratado que obriga só quem o assinou em 1948'], 1),
 ('02', 'A Marta aceitou ser filmada no ensaio para o grupo rever a cena. Para publicar o vídeo na conta da escola…',
  ['já não é preciso pedir outra autorização à Marta', 'é preciso pedir-lhe consentimento para esse uso', 'basta cortar do vídeo as partes em que ela cai'], 1),
 ('03', 'Que situação mostra uma regra igual para todos que deixa alguém de fora?',
  ['a mostra é aberta a todos, num primeiro andar sem elevador', 'a mostra só aceita os alunos do 10.º A, por ser deles', 'a mostra é gratuita para todas as turmas da escola'], 0),
 ('04', 'Que frase é uma acusação de facto, que tem de ser provada?',
  ['A comida da cantina é muito má.', 'O Diogo roubou dinheiro do bar.', 'O diretor parece mesmo uma pera.'], 1),
 ('05', 'Numa escola, onde podem estar câmaras de videovigilância?',
  ['no interior das salas de aula comuns', 'nos acessos e no perímetro exterior', 'em qualquer sítio, se houver furtos'], 1),
 ('07', 'Uma captura de ecrã mostra o nome do Tomás ao lado de um vídeo. O que se pode dizer com segurança?',
  ['que foi o Tomás que publicou o vídeo', 'que o nome do Tomás aparece na captura', 'que o Tomás está a mentir à turma'], 1),
 ('08', 'A passadeira em frente à escola vai desaparecer. Que forma de contestar obriga quem decide a examinar o pedido e a responder?',
  ['uma petição à câmara, com o pedido e a razão', 'um comentário anónimo numa rede social', 'esperar pelas próximas eleições autárquicas'], 0),
 ('06', 'Há seis turnos de filmagem para três grupos. Escreve uma regra para os repartir e diz quem perde com ela.', None, None),
 ('03 e 09', 'Nos intervalos, a escola quer que se fale só português. Quem fica de fora desta regra, e que pergunta farias antes de decidir?', None, None),
]
COTACAO_ESCRITA = {
 9: '0: sem regra; 1: uma regra, sem dizer quem perde; 2: uma regra aplicável e quem perde com ela, com a razão.',
 10: '0: sem resposta ou sem ninguém de fora; 1: quem fica de fora, sem pergunta; 2: quem fica de fora e uma pergunta a quem é afetado.',
}
LETRAS = 'ABC'

TOKENS = (':root{--tinta:#000;--papel:#fff;--fundo:#f3f2ee;--suave:#444;--mostarda:#d9a520;--vermelho:#c8232c}'
          'body.cid-piloto{--acento:#e0b23a}')
CSS = (TOKENS +
 'body.cid-piloto{margin:0;background:var(--fundo);color:var(--tinta);font:17px/1.5 Arial,Helvetica,sans-serif}'
 '.cid-piloto main{max-width:720px;margin:0 auto;padding:16px 16px 48px}'
 '.cid-piloto .migalhas{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:center;font-size:.9rem;margin:0 0 20px}'
 # 31/10/2026 (terceira correção, diretor de arte): as migalhas são alvos de 44 px (tinham 22); abaixo de 360 px ficam compactas,
 # numa só linha com o botão do tema (antes, duas linhas e 70 px, que empurravam a primeira ação para fora do primeiro ecrã).
 '.cid-piloto .migalhas a{color:inherit;display:inline-flex;align-items:center;min-height:44px}'
 '@media (max-width:359px){.cid-piloto .migalhas{gap:4px 10px;font-size:.8125rem}}'
 # 31/10/2026 (quarta correção, diretor de arte): no guia e no Ponto, abaixo de 400 px, as migalhas ficam numa só linha de 44 px
 # (tinham duas, 92 px, com o botão do tema sozinho na segunda); o nível atual sai da vista, mas fica para o leitor de ecrã, e o
 # h1 por baixo repete-o. A página do módulo, só com duas ligações, não muda. O botão do tema vai à direita da barra (sistema,
 # 6.1). «Lente» (33 a 36 px de largura) ganha uma área de toque de 44 px.
 '@media (max-width:399px){.cid-piloto .migalhas:has(>a+a+a){flex-wrap:nowrap;gap:4px 10px;font-size:.8125rem}.cid-piloto .migalhas:has(>a+a+a) a{white-space:nowrap}.cid-piloto .migalhas>a+a+a+[aria-current]{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}'
 '.cid-piloto .migalhas [data-appearance-control]{margin-left:auto}'
 '.cid-piloto .migalhas a:first-child{position:relative}.cid-piloto .migalhas a:first-child::after{content:"";position:absolute;top:0;bottom:0;left:-6px;width:44px}'
 '.cid-piloto .marca{font:400 1rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;letter-spacing:.06em;margin:0 0 4px}'
 '.cid-piloto h1{font:700 clamp(2.4rem,9vw,3.6rem)/.95 Arial,Helvetica,sans-serif;margin:0 0 10px;letter-spacing:-.05em}'
 '.cid-piloto h1,.cid-piloto h2,.cid-piloto h3{text-wrap:balance}'
 '.cid-piloto a{color:inherit;text-underline-offset:.15em}'
 '.cid-piloto h2{font:700 1.25rem/1.25 Arial,Helvetica,sans-serif;margin:32px 0 10px}'
 # 05/11/2026: os h3 passam de 16 para 18 px, acima do texto corrido (17 px); era o R5 da hierarquia dos títulos no guia.
 '.cid-piloto h3{font:700 1.125rem/1.3 Arial,Helvetica,sans-serif;margin:20px 0 6px}'
 '.cid-piloto .lead{font-size:1.05rem;margin:0 0 18px;max-width:38em}'
 '.cid-piloto .aviso-piloto{font-size:.9rem;color:var(--suave);margin:0 0 18px}'
 # 31/10/2026 (terceira correção, diretor de arte): na página do módulo, a linha do piloto passa para o rodapé (sistema, 6.10).
 '.cid-piloto ol.sessoes+.aviso-piloto{margin:24px 0 0}.cid-piloto .aviso-piloto+footer.mais{margin-top:16px}'
 '.cid-piloto section.proximo{background:var(--tinta);color:var(--papel);padding:14px 16px 16px;margin:4px 0 12px}'
 '.cid-piloto .proximo .kicker{font:700 .8125rem/1.2 Arial,Helvetica,sans-serif;letter-spacing:.12em;text-transform:uppercase;margin:0 0 6px}'
 '.cid-piloto .proximo .prox-n{font:400 2.6rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;margin:0}'
 '.cid-piloto .proximo .prox-t{font:700 1.15rem/1.25 Arial,Helvetica,sans-serif;margin:2px 0 12px}'
 '.cid-piloto a.continuar{display:inline-block;background:var(--papel);color:var(--tinta);text-decoration:none;font-weight:700;padding:12px 18px;border:3px solid var(--papel);margin:0}'
 '.cid-piloto :is(a,button):focus-visible{outline:3px solid var(--tinta);outline-offset:3px}'
 '.cid-piloto .proximo a.continuar:focus-visible{outline-color:var(--papel)}'
 '.cid-piloto .contagem{margin:0 0 16px;font-size:.95rem}'
 '.cid-piloto ol.sessoes{list-style:none;margin:0;padding:0;border-top:0}'
 '.cid-piloto ol.sessoes li{border-bottom:2px solid var(--fundo);background:var(--papel)}'
 # 31/10/2026 (verificação final, decisão da equipa; decisão 39: não se pergunta ao docente): linhas de 56 a 64 px. O estado
 # vai na linha do título; acima de 600 px a pergunta fica numa só linha, com reticências; abaixo, sai da linha e a da próxima
 # sessão aparece na região «A seguir» (.prox-q).
 '.cid-piloto ol.sessoes a{display:grid;grid-template-columns:2.6rem minmax(0,1fr) auto;column-gap:12px;align-items:center;min-height:56px;box-sizing:border-box;padding:8px 12px;color:inherit;text-decoration:none}'
 '.cid-piloto ol.sessoes a::after{content:"→";grid-column:3;grid-row:1/span 2;align-self:center;font-weight:700}'
 '.cid-piloto li.seguir a{box-shadow:inset 4px 0 0 var(--vermelho)}'
 '.cid-piloto ol.sessoes .n{font:400 2.2rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;grid-row:1/span 2;align-self:center}'
 '.cid-piloto ol.sessoes .tit{grid-column:2;line-height:1.25}'
 '.cid-piloto ol.sessoes strong{font-size:1.05rem;line-height:1.25}'
 '.cid-piloto ol.sessoes .perg{grid-column:2;color:var(--suave);font-size:.875rem;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}'
 # 31/10/2026 (quinta correção, diretor de arte): de 600 a 767 px a pergunta cortava-se; abaixo de 768 px sai da linha e fica
 # só na região «A seguir».
 '.cid-piloto ol.sessoes a{column-gap:10px;grid-template-columns:2.4rem minmax(0,1fr) auto}'
 '@media (max-width:767px){.cid-piloto ol.sessoes .perg{display:none}}'
 # 31/10/2026 (quarta correção, diretor de arte): sem a pergunta, o número e a seta ficam só na primeira linha da grelha, a do
 # título e do estado (ocupavam duas e o texto ficava 7 a 11 px acima do centro deles).
 '@media (max-width:767px){.cid-piloto ol.sessoes .n,.cid-piloto ol.sessoes a::after{grid-row:1}}'
 '.cid-piloto .proximo .prox-q{font:400 1rem/1.4 Georgia,"Times New Roman",serif;margin:-6px 0 14px;max-width:34em}'
 # 31/10/2026 (terceira correção, diretor de arte): o estado é a peça .etq do sistema (6.5 e 6.9): palavra em caixa alta; «Feita»
 # com o quadrado mostarda e contorno de 1,5 px a tinta; «A seguir» com o quadrado cheio a vermelho do token (no escuro, #e4555c);
 # até 499 px, sempre por baixo do título, para a mesma lista não ter o estado umas vezes ao lado e outras por baixo (o sistema
 # diz 420 px, mas entre 430 e 480 px, com as 10 sessões feitas, «FEITA dd/mm» em caixa alta ainda descia em 2 a 4 linhas).
 '.cid-piloto .estado{display:inline-flex;align-items:center;gap:6px;font-size:.8125rem;line-height:1;font-weight:700;text-transform:uppercase;letter-spacing:.06em;white-space:nowrap;vertical-align:baseline;margin-left:2px;border:0;padding:0}'
 '.cid-piloto .estado:empty{display:none}'
 '.cid-piloto li.feita .estado::before,.cid-piloto li.seguir .estado::before{content:"";width:11px;height:11px;box-sizing:border-box;flex:none}'
 '.cid-piloto li.feita .estado::before{background:var(--mostarda);border:0;box-shadow:inset 0 0 0 1.5px var(--tinta)}'
 '.cid-piloto li.seguir .estado::before{background:var(--vermelho);border:0}'
 '@media (max-width:499px){.cid-piloto ol.sessoes .estado:not(:empty){display:flex;margin:4px 0 0}}'
 # 31/10/2026 (quarta correção, diretor de arte): o traço sob o número da sessão feita usa a mostarda do quadrado «Feita» (no
 # claro eram dois amarelos, #d9a520 e #e0b23a, para o mesmo significado).
 '.cid-piloto li.feita .n::after{content:"";display:block;width:1.6rem;height:4px;background:var(--mostarda);margin-top:4px}'
 '.cid-piloto footer.mais{margin-top:28px;display:flex;flex-wrap:wrap;gap:8px 20px}'
 # 31/10/2026 (quarta correção, diretor de arte): as ligações do rodapé são alvos de 44 px de altura (tinham 26).
 '.cid-piloto footer.mais a{color:inherit;font-weight:700;display:inline-flex;align-items:center;min-height:44px}'
 '.cid-piloto .pg{overflow-wrap:break-word}.cid-piloto .fontes{overflow-wrap:anywhere}'
 # 31/10/2026 (verificação final): 28em (476 px a 1366) para a linha não passar dos 75 carateres na Georgia (com 34em chegava aos 91).
 '.cid-piloto .pg,.cid-piloto section.sessao p:not(.marca),.cid-piloto section.sessao li{font-family:Georgia,"Times New Roman",serif;max-width:28em;text-align:justify;hyphens:auto}'
 '.cid-piloto p.abrir{text-align:start}'
 '.cid-piloto a.botao{display:inline-flex;align-items:center;min-height:44px;padding:0 12px;border:2px solid var(--tinta);font:700 1rem/1.2 Arial,Helvetica,sans-serif;text-decoration:none;margin:0 8px 8px 0}'
 '.cid-piloto ul.indice a{display:inline-block;padding:12px 0}'
 '.cid-piloto .tabela{overflow-x:auto;max-width:100%}'
 '.cid-piloto section.sessao{border-top:3px solid var(--tinta);margin-top:36px;padding-top:4px}'
 '.cid-piloto section.sessao>h2{font:400 2rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;margin:16px 0 6px}'
 '.cid-piloto .caixa{background:var(--papel);border:2px solid var(--tinta);padding:4px 16px;margin:12px 0}'
 # 31/10/2026 (quarta correção, diretor de arte): no ecrã, a caixa fecha sobre o texto (com a medida de 28em, ficavam 208 px
 # vazios dentro dela, de 1024 a 1440 px); no papel fica como estava.
 '@media screen{.cid-piloto .caixa{width:fit-content;max-width:100%;box-sizing:border-box}}'
 # 31/10/2026 (quinta correção, diretor de arte): no guia, caixa, grelha, lead e aviso acabam onde acaba o texto (28em); a ligação
 # que é o único conteúdo da célula é um alvo de 44 px.
 '@media screen and (min-width:600px){.cid-piloto section.sessao:not(#ponto) .tabela,.cid-piloto .caixa{max-width:28em}}'
 '.cid-piloto.guia header .lead{max-width:28.3em;text-wrap:pretty}.cid-piloto.guia header .aviso-piloto{max-width:33em}'
 '.cid-piloto td>a:only-child{display:inline-flex;align-items:center;min-height:44px}'
 '.cid-piloto table{border-collapse:collapse;width:100%;background:var(--papel);margin:8px 0 4px}'
 '.cid-piloto th,.cid-piloto td{border:1px solid var(--tinta);padding:6px 8px;text-align:left;vertical-align:top}'
 '.cid-piloto td.num,.cid-piloto th.num{text-align:right;white-space:nowrap;width:4.5rem}'
 '@media (max-width:599px){.cid-piloto td.num,.cid-piloto th.num{width:auto;white-space:normal}}'
 # 31/10/2026 (verificação final): abaixo de 600 px, as tabelas do guia cabem na caixa (letra .875rem, células mais estreitas,
 # hifenização); na chave do Ponto sai a coluna «Sessão», que o docente encontra em cada secção.
 '@media (max-width:599px){.cid-piloto .tabela table{font-size:.875rem}.cid-piloto .tabela th,.cid-piloto .tabela td{padding:5px 6px;hyphens:auto;overflow-wrap:break-word}.cid-piloto #ponto th:last-child,.cid-piloto #ponto td:last-child{display:none}}'
 # Abaixo de 360 px, a chave do Ponto ainda passava 21 px (309 em 288): as células podem partir uma palavra longa
 # («videovigilância?», «consentimento»), que a hifenização do aparelho marca com hífen.
 '@media (max-width:359px){.cid-piloto #ponto td{overflow-wrap:anywhere}}'
 '.cid-piloto ol.passos li{margin:0 0 6px}'
 '.cid-piloto ol.passos .min{font-weight:700;white-space:nowrap}'
 '.cid-piloto .indicativa{font-weight:700;border-left:6px solid var(--tinta);padding-left:10px}'
 '.cid-piloto ul.indice{columns:2 14rem;padding-left:1.2em}'
 '.cid-piloto .q{break-inside:avoid;margin:0 0 18px}'
 '.cid-piloto .q ol{list-style:none;padding-left:0;margin:6px 0 0}'
 '.cid-piloto .q ol li{margin:2px 0}'
 '.cid-piloto .linhas{border-bottom:1px solid var(--tinta);height:1.8em}'
 '.cid-piloto .campos{display:flex;flex-wrap:wrap;gap:8px 24px;margin:0 0 20px;padding:10px 12px;border:2px solid var(--tinta);background:var(--papel)}'
 '.cid-piloto button.imprimir{font:700 1rem Arial,Helvetica,sans-serif;background:var(--papel);color:var(--tinta);border:3px solid var(--tinta);padding:8px 14px;min-height:48px;cursor:pointer}'
 '@media print{.cid-piloto .migalhas,.cid-piloto button.imprimir,.cid-piloto footer.mais,[data-appearance-control]{display:none}'
 'body.cid-piloto{background:#fff;color:#000;font-size:12pt}.cid-piloto main{max-width:none;padding:0}'
 '.cid-piloto section.sessao{break-before:page}.cid-piloto section.sessao:first-of-type{break-before:auto}'
 '.cid-piloto table,.cid-piloto .caixa{break-inside:avoid}'
 'body.cid-piloto{font-size:11pt;line-height:1.35}.cid-piloto .q{margin:0 0 10px}.cid-piloto .q ol{margin-top:4px}'
 '.cid-piloto .q ol li{margin:0}.cid-piloto .q p{margin:0 0 4px}.cid-piloto .linhas{height:1.6em}'
 # 31/10/2026 (verificação final): cada sessão do guia em duas páginas A4. A página leva margens reais (10 e 12 mm, como as do
 # navegador; sem elas o PDF saía sem margens). Cada sessão imprime-se em duas colunas de cerca de 9 cm (55 carateres por
 # linha a 11 pt, entrelinha 1,4), com o número, o título e a pergunta por cima das duas; as fontes vão a 8,5 pt e a chave do
 # Ponto a 9,5 pt, numa página. Medido com page.pdf e pdftotext: 23 páginas, duas por sessão.
 '@page{size:A4;margin:10mm 12mm}'
 '.cid-piloto .fontes{font-size:8.5pt;line-height:1.25}'
 'body.cid-piloto.guia{font-size:11pt;line-height:1.4}.cid-piloto.guia h3{margin:12px 0 4px;break-after:avoid}'
 '.cid-piloto.guia section.sessao:not(#ponto){column-count:2;column-gap:8mm}.cid-piloto.guia section.sessao>:is(.marca,h2,.lead){column-span:all}'
 '.cid-piloto.guia .pg,.cid-piloto.guia section.sessao p:not(.marca),.cid-piloto.guia section.sessao li{max-width:none}.cid-piloto.guia #ponto{font-size:9.5pt}'
 # 31/10/2026 (terceira correção, diretor de arte): no papel, os botões «Abrir a sessão» e «Projetar» não servem e não se imprimem;
 # nenhum item de lista se parte entre colunas; entrelinha de 1,45 no texto corrido.
 '.cid-piloto p.abrir{display:none}.cid-piloto.guia section.sessao li{break-inside:avoid}body.cid-piloto.guia{line-height:1.45}}'
 # 31/10/2026 (verificação final): as fontes, com endereços longos, alinham à esquerda (justificadas abriam rios).
 '.cid-piloto section.sessao p.fontes{text-align:start}')


def it(s):
    return re.sub(r'_(.+?)_', r'<i>\1</i>', e(s))


def cabeca(base, titulo, desc):
    return ('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(titulo)}</title><meta name="robots" content="noindex, nofollow"><meta name="description" content="{e(desc)}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style><link rel="stylesheet" href="{base}assets/appearance.css"><script src="{base}assets/appearance.js"></script></head>')


def migalhas(base, itens):
    out = '<nav class="migalhas" aria-label="Onde estás">'
    for rot, href in itens:
        out += f'<a href="{e(href)}">{rot}</a>' if href else f'<span aria-current="page">{rot}</span>'
    return out + '<span data-appearance-control></span></nav>'


def rel(de, para):
    """A ligação relativa de uma pasta para outra (ambas com «/» no fim), como no sítio publicado."""
    return posixpath.relpath(para, de) + '/'


def pagina_modulo(S):
    base = '../../../'
    linhas = ''
    for s in S:
        linhas += (f'<li data-chave="{e(s["chave"])}" data-versao="{e(s["versao"])}" data-n="{s["n"]}" data-titulo="{e(s["titulo"])}" data-pergunta="{e(LL.visivel(s["pergunta"]))}">'
                   f'<a href="{rel(MODULO, s["pasta"])}"><span class="n" aria-hidden="true">{s["n"]}</span>'
                   # 31/10/2026 (verificação final, decisão da equipa): o estado vai na linha do título; a pergunta só aparece
                   # na linha acima de 600 px, numa linha com reticências (abaixo, só a da próxima sessão, na região «A seguir»).
                   f'<span class="tit"><strong><span class="c-sr">Sessão {s["n"]}: </span>{e(s["titulo"])}</strong> <span class="estado" data-estado></span></span>'
                   f'<span class="perg">{s["pergunta"]}</span></a></li>')
    # 05/11/2026 (plano do molde da Cidadania, pedido 1): «Feita» conta com feita(st) do progresso comum
    # (assets/licoes/progresso-licoes.js): a sessão concluída nesta versão ou numa anterior (st.antes, que o motor preenche ao
    # subir a versão com preservarAnterior). Antes contava só st.lida com a versão igual à da página, e subir a versão apagava
    # o «feita» de todos. A data é a da primeira conclusão. Na projeção, nada se lê.
    js = ('(function(){"use strict";var L=[].slice.call(document.querySelectorAll("[data-chave]")),feitas=0,prox=null;'
          'var P=window.EPILicoesProgresso,proj=/[?&]projetar=1(&|$)/.test(location.search)||window.self!==window.top;'
          'L.forEach(function(li){var st=null;try{st=proj?null:JSON.parse(localStorage.getItem(li.getAttribute("data-chave"))||"null")}catch(x){st=null}'
          'var ok=!!(st&&P&&P.feita(st));var el=li.querySelector("[data-estado]");'
          # 31/10/2026 (revisão do diretor de arte): a sessão feita diz «Feita dd/mm» (o motor grava t=Date.now() no fim); a
          # próxima por fazer leva «A seguir» e o filete vermelho; «por fazer» não se escreve.
          'var dd=function(n){return(n<10?"0":"")+n};'
          'if(ok){feitas++;li.classList.add("feita");var t=P.data(st),d=t===null?null:new Date(t);el.textContent="Feita"+(d&&!isNaN(d)?" "+dd(d.getDate())+"/"+dd(d.getMonth()+1):"")}'
          'else if(!prox){prox=li;li.classList.add("seguir");el.textContent="A seguir"}});'
          'var b=document.querySelector("[data-continuar]"),c=document.querySelector("[data-contagem]"),pn=document.querySelector("[data-prox-n]"),pt=document.querySelector("[data-prox-t]"),pk=document.querySelector("[data-prox-k]"),pq=document.querySelector("[data-prox-q]");'
          'if(c)c.textContent=feitas+" de "+L.length+" sessões feitas";'
          'if(b&&feitas){if(prox){b.href=prox.querySelector("a").getAttribute("href");b.textContent="Continuar: Sessão "+prox.getAttribute("data-n")+", "+prox.getAttribute("data-titulo")+"\\u00a0→";if(pn)pn.textContent=prox.getAttribute("data-n");if(pt)pt.textContent=prox.getAttribute("data-titulo");if(pq)pq.textContent=prox.getAttribute("data-pergunta")}'
          'else{b.textContent="As 10 sessões estão feitas. Rever a sessão 01\\u00a0→";if(pk)pk.textContent="Módulo feito"}}})();')
    corpo = (migalhas(base, [('Lente', LENTE), ('Cidadania', LENTE + 'cidadania/'), ('Módulo 1 (piloto)', '')])
             + '<header><p class="marca">Cidadania, módulo 1</p><h1>Humanos</h1>'
             '<p class="lead">Direitos humanos, democracia e instituições políticas, em 10 sessões de 180 minutos. Cada sessão é uma lição em cartões, com uma parte na aula.</p>'
             '</header>'
             f'<section class="proximo" aria-label="A seguir"><p class="kicker" data-prox-k>A seguir</p>'
             f'<p class="prox-n" data-prox-n>01</p><p class="prox-t" data-prox-t>{e(S[0]["titulo"])}</p><p class="prox-q" data-prox-q>{S[0]["pergunta"]}</p>'
             f'<a class="continuar" data-continuar href="{rel(MODULO, S[0]["pasta"])}">Começar: Sessão 01, {e(S[0]["titulo"])} →</a></section>'
             f'<p class="contagem" data-contagem>0 de {len(S)} sessões feitas</p>'
             f'<ol class="sessoes">{linhas}</ol>'
             # 31/10/2026 (terceira correção, diretor de arte): a linha do piloto vai para o rodapé (sistema, 6.10); no cabeçalho,
             # empurrava a primeira ação para fora do primeiro ecrã a 320 px.
             '<p class="aviso-piloto">Piloto em revisão. O que fazes fica só neste aparelho.</p>'
             '<footer class="mais"><a href="docente/">Guia do docente</a></footer>')
    return (cabeca(base, 'Módulo 1 (piloto) · Cidadania · Lente', 'Cidadania, módulo 1, Humanos: as 10 sessões em piloto.')
            + '<body class="cid-piloto"><style>.c-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}</style>'
            + f'<main id="conteudo">{corpo}</main><script src="{base}assets/licoes/{LL.PROGRESSO}"></script><script>{js}</script></body></html>\n')


def tabela_grelha(g):
    soma = sum(p for _, p in g['grelha'])
    assert soma == 20, (g['produto'], soma)
    linhas = ''.join(f'<tr><td>{e(c)}</td><td class="num">{p}</td></tr>' for c, p in g['grelha'])
    return (f'<div class="tabela"><table><caption class="c-sr">Grelha indicativa: {e(g["produto"])}</caption><thead><tr><th scope="col">Critério</th><th scope="col" class="num">Pontos</th></tr></thead>'
            f'<tbody>{linhas}</tbody><tfoot><tr><th scope="row">Total (indicativo)</th><td class="num">20</td></tr></tfoot></table></div>')


def yt_link(s):
    u = 'https://www.youtube.com/watch?v=' + s['yt']
    return u + (f'&t={s["yt_ini"]}s' if s['yt_ini'] and s['yt_ini'] != '0' else '')


# 05/11/2026 (revisão da decisão 154): o cartão «Na aula» pode ligar a outra página do Lente, com o endereço relativo à página
# da lição (a sessão 07 liga ao caso «O júri»). O guia está noutra pasta: a ligação resolve-se a partir da lição e volta a
# escrever-se relativa ao guia, para levar ao mesmo sítio. As ligações absolutas e as âncoras ficam como estão.
def ligacoes_no_guia(h, saida, pasta=MODULO + 'docente/'):
    def troca(m):
        u = html.unescape(m.group(1))
        if u.startswith(('http:', 'https:', '//', 'mailto:', '#')):
            return m.group(0)
        alvo = urljoin(LENTE + saida, u)
        assert alvo.startswith(LENTE), (saida, u)
        caminho, _, resto = alvo[len(LENTE):].partition('#')
        rel = posixpath.relpath(caminho or '.', pasta) + ('/' if caminho.endswith('/') else '')
        return 'href="' + e(rel + ('#' + resto if resto else ''), quote=True) + '"'
    return re.sub(r'href="([^"]+)"', troca, h)


def pagina_guia(S):
    base = '../../../../'
    indice = ''.join(f'<li><a href="#s{s["n"]}">Sessão {s["n"]}: {e(s["titulo"])}</a></li>' for s in S)
    tempos = ('<div class="tabela"><table><thead><tr><th scope="col">Parte</th><th scope="col">Tempo</th><th scope="col">O que acontece</th></tr></thead><tbody>'
              '<tr><td>Ponto de partida ou de chegada</td><td>10 a 15 min</td><td>Só nas sessões 01 e 10, em papel, antes de abrir a lição.</td></tr>'
              '<tr><td>Cartões até ao «Na aula»</td><td>cerca de 50 min</td><td>Abre, Decide, recuperar, ver a imagem e o vídeo, decidir.</td></tr>'
              '<tr><td>«Na aula»</td><td>60 a 75 min</td><td>A atividade de turma, com a pausa de 10 minutos.</td></tr>'
              '<tr><td>Cartões depois do «Na aula»</td><td>cerca de 25 min</td><td>Aplicar a um caso novo.</td></tr>'
              '<tr><td>«Para levar»</td><td>5 min</td><td>A frase da sessão e a fotografia do que ficou escrito, com o código e a data.</td></tr>'
              '</tbody></table></div>')
    instr = ('<div class="tabela"><table><thead><tr><th scope="col">Instrumento do projeto</th><th scope="col" class="num">Peso</th><th scope="col">Produtos das sessões</th></tr></thead><tbody>'
             '<tr><td><a href="../../../projeto/#av-diario">Diário de investigação</a></td><td class="num">20 %</td><td>«Para levar» de cada sessão, acórdão (07), pedido (08)</td></tr>'
             '<tr><td><a href="../../../projeto/#av-laboratorio">Laboratório de verificação</a></td><td class="num">20 %</td><td>Registo de verificação (04)</td></tr>'
             '<tr><td><a href="../../../projeto/#av-dossie">Dossiê de investigação</a></td><td class="num">30 %</td><td>Consentimento (02), pergunta (03), fontes (04), plano de recolha (05), esboço do guião (06)</td></tr>'
             '<tr><td><a href="../../../projeto/#av-teatro">Teatro-documento e defesa</a></td><td class="num">30 %</td><td>Ensaio (09), apresentação e defesa (10)</td></tr>'
             '</tbody></table></div>')
    corpo = (migalhas(base, [('Lente', LENTE), ('Cidadania', LENTE + 'cidadania/'), ('Módulo 1 (piloto)', '../'), ('Guia do docente', '')])
             + '<header><p class="marca">Cidadania, módulo 1, piloto</p><h1>Guia do docente</h1>'
             '<p class="lead">Uma secção por sessão: o «Na aula» em pormenor, a imagem, o vídeo, o passo da Pergunta Humana e a grelha do produto da sessão.</p>'
             '<p class="aviso-piloto">Piloto escondido dos motores de busca. O módulo 1 atual mantém-se até 25/11. Os casos das lições são inventados; um caso real só entra depois de o docente o confirmar.</p></header>'
             # 31/10/2026 (quinta correção, diretor de arte): a primeira ação do guia (ir à sessão do dia) logo no primeiro ecrã
             f'<nav aria-label="Sessões"><h2>As 10 sessões</h2><ul class="indice">{indice}</ul></nav>'
             '<section><h2>Antes de começar</h2>'
             '<p class="pg">Cada sessão tem 180 minutos, com uma pausa. A lição em cartões abre-se no ecrã de cada aluno ou projeta-se para a turma (ligação «Projetar» em cada sessão: a projeção começa no primeiro cartão e não grava nada neste aparelho).</p>'
             + tempos +
             '<p class="pg">As sessões 01, 02 e 03 já estão no molde final das vinte sessões: 23 cartões com o tempo de cada um, um momento «Em turma» e três linhas em papel A6. As secções dessas sessões, mais abaixo, têm a tabela dos 180 minutos, cartão a cartão; as outras sete seguem o quadro acima até passarem ao molde.</p>'
             '<p class="pg">O <a href="../ponto/">Ponto de partida e de chegada</a> tem as mesmas 10 perguntas, para imprimir. Faz-se no início da sessão 01 e no início da sessão 10; a chave e a cotação estão no fim deste guia, e não nas páginas dos alunos.</p>'
             '<p class="pg">As saídas das sessões 05 e 08 são só à volta da escola, em aula, com o docente e sem autorização especial. Não se fotografam pessoas nem matrículas.</p>'
             '<h2>Avaliação</h2>'
             '<p class="indicativa">Avaliação indicativa: orienta o trabalho e não é para usar a sério (decisão 17; Portaria n.º 235-A/2018, artigo 27.º, n.º 8).</p>'
             '<p class="pg">Cada sessão tem uma grelha /20 do produto da sessão. Em cada critério há três níveis: 0 pontos (não aparece), metade dos pontos (aparece, mas incompleto ou sem razão) e todos os pontos (como está descrito). A correspondência com os quatro instrumentos da <a href="../../../projeto/">Pergunta Humana</a> também é indicativa:</p>'
             + instr + '</section>')
    for s in S:
        g = GUIA[s['n']]
        if s.get('molde'):
            corpo += secao_molde(s, g)
            continue
        passos = ''.join(f'<li><span class="min">{m} min.</span> {e(t)}</li>' for m, t in g['passos'])
        total = sum(m for m, _ in g['passos'])
        assert 60 <= total <= 75, (s['n'], total)
        proj_href = '../../../projeto/' + g['projeto'][1]
        # 31/10/2026: o texto do botão já traz «Título» (duração); não se volta a pôr entre «».
        yt = (f'<p class="pg">{it(s["yt_botao"])}. {s["yt_cred"]} <a href="{e(yt_link(s))}">Abrir no YouTube</a>'
              + (f' (excerto de {s["yt_ini"]} a {s["yt_fim"]} s)' if s['yt_fim'] else '') + '.</p>'
              f'<p class="pg"><b>Tarefa.</b> {s["yt_tarefa"]}</p>'
              '<p class="pg"><b>Sem vídeo.</b> O docente conta o essencial em duas frases e a turma responde à mesma tarefa.</p>')
        corpo += (f'<section class="sessao" id="s{s["n"]}"><p class="marca">Sessão {s["n"]}</p><h2>{e(s["titulo"])}</h2>'
                  f'<p class="lead">{s["pergunta"]}</p>'
                  f'<p class="pg"><b>Domínio.</b> {e(g["dominio"])} <b>O que ensina.</b> {e(g["ensina"])}</p>'
                  f'<p class="abrir"><a class="botao" href="../../m1-s{s["n"]}/">Abrir a sessão</a><a class="botao" href="../../m1-s{s["n"]}/?projetar=1">Projetar</a></p>'
                  + (f'<p class="pg"><b>Antes.</b> {e(g["antes"])}</p>' if g.get('antes') else '')
                  + '<h3>O que o aluno lê no cartão «Na aula»</h3>'
                  f'<div class="caixa">{ligacoes_no_guia(s["aula"]["html"], s["d"]["saida"])}</div>'
                  f'<h3>O «Na aula» em pormenor ({total} minutos, com a pausa)</h3><ol class="passos">{passos}</ol>'
                  '<h3>Materiais</h3><ul>' + ''.join(f'<li>{e(m)}</li>' for m in g['materiais']) + '</ul>'
                  f'<h3>O que fica escrito</h3><p class="pg">{e(g["escrito"])}</p>'
                  f'<h3>Pergunta Humana: {e(g["projeto"][0])}</h3><p class="pg">{e(g["projeto"][2])} <a href="{e(proj_href)}">Ver na página do projeto</a>.</p>'
                  f'<h3>Imagem</h3><p class="pg">{s["figcaption"]}</p><p class="pg"><b>Pergunta do cartão.</b> {s["img_pergunta"]}</p>'
                  f'<h3>Vídeo</h3>{yt}'
                  f'<h3>Grelha: {e(g["produto"])} (/20, indicativa)</h3>' + tabela_grelha(g)
                  + '<p class="indicativa">Avaliação indicativa: orienta o trabalho e não é para usar a sério.</p>'
                  # 31/10/2026 (verificação final): as notas também levam os títulos de obras em itálico (_…_, LL.esc_it).
                  '<h3>Notas</h3><ul>' + ''.join(f'<li>{LL.esc_it(x)}</li>' for x in g['notas']) + '</ul>'
                  # 31/10/2026: títulos de obras em itálico (_…_), com a guarda do motor (LL.esc_it), não com it(), que não a tem.
                  f'<h3>Fontes da lição</h3><p class="pg fontes">{LL.esc_it(s["d"]["fontes"])}</p></section>')
    chave = ''
    for i, (ses, q, ops, c) in enumerate(PONTO, 1):
        if ops:
            chave += f'<tr><td class="num">{i}</td><td>{e(q)}</td><td>{LETRAS[c]}: {e(ops[c])}</td><td class="num">1</td><td>{e(ses)}</td></tr>'
        else:
            chave += f'<tr><td class="num">{i}</td><td>{e(q)}</td><td>{e(COTACAO_ESCRITA[i])}</td><td class="num">2</td><td>{e(ses)}</td></tr>'
    corpo += ('<section class="sessao" id="ponto"><p class="marca">Sessões 01 e 10</p><h2>Ponto de partida e de chegada: chave e cotação</h2>'
              '<p class="pg">Em papel, sem ajuda e sem consulta, 10 a 15 minutos. Cada aluno escreve o seu código, nunca o nome. As mesmas 10 perguntas, pela mesma ordem, na sessão 10. Máximo 12 pontos: 8 de escolha (1 ponto cada) e 2 escritas (0 a 2). O ganho de cada aluno (chegada menos partida, por código) calcula-se numa tabela fora do sítio. Perguntas propostas pela equipa a partir do plano, para o docente rever.</p>'
              # 31/10/2026 (quarta correção, diretor de arte): a ligação ao Ponto é um botão como «Abrir a sessão» e «Projetar»
              # (48 px de altura, como eles; tinha 19 px); como eles, não se imprime.
              '<p class="abrir"><a class="botao" href="../ponto/">Abrir o Ponto para imprimir</a></p>'
              '<div class="tabela"><table><thead><tr><th scope="col" class="num">N.º</th><th scope="col">Pergunta</th><th scope="col">Chave ou cotação</th><th scope="col" class="num">Pontos</th><th scope="col">Sessão</th></tr></thead>'
              f'<tbody>{chave}</tbody></table></div></section>'
              '<footer class="mais"><a href="../">Voltar ao módulo</a><a href="../../../projeto/">Pergunta Humana</a></footer>')
    return (cabeca(base, 'Guia do docente, módulo 1 (piloto) · Cidadania · Lente', 'Guia do docente das 10 sessões do módulo 1 de Cidadania em piloto.')
            + '<body class="cid-piloto guia"><style>.c-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
            + (CSS_GUIA_MOLDE if any(x.get('molde') for x in S) else '') + '</style>'
            + f'<main id="conteudo">{corpo}</main></body></html>\n')


# 05/11/2026 (plano do molde da Cidadania, pedido 2): o guia, a versão para imprimir e o redirecionamento das sessões no molde
# cidadania-2026-11 (por agora, só a s01 do M1; 06/11/2026: e a s02 e a s03). Tudo sai dos cartões da lição e de GUIA; nada se escreve à mão nas páginas.
GUIA_PASTA = MODULO + 'docente/'


def _txt(s):
    return LL.visivel(s)


def _resposta(c):
    """A resposta de um cartão de fazer, em texto simples, para a chave do guia."""
    t = c['t']
    if t == 'escolha':
        return _txt(c['o'][c['c']])
    if t == 'vf':
        return 'Verdadeiro.' if c['v'] else 'Falso.'
    if t == 'emparelhar':
        return '; '.join(f'{_txt(a)} → {_txt(b)}' for a, b in c['pares']) + '.'
    if t == 'sublinhar':
        w = c['frase'].split()
        return '«' + ' '.join(w[j] for j in c['certas']).strip(',.') + '»'
    if t == 'ordenar':
        return ' '.join(f'{k}. {_txt(x)}' for k, x in enumerate(c['passos'], 1))
    return ''


def _tipo_aluno(c):
    nomes = {'escolha': 'escolha', 'vf': 'verdadeiro ou falso', 'emparelhar': 'emparelhar', 'sublinhar': 'tocar nas palavras', 'ordenar': 'ordenar'}
    return 'ler' if c['t'] == 'ler' else nomes.get(c['t'], c['t'])


def tabela_tempos(s, g):
    d, C = s['d'], s['d']['cartoes']
    T = d['tempos']
    volta = next(i for i, c in enumerate(C) if c.get('rot') == 'Volta ao caso')
    linhas, total = '', 0

    def linha(n, nome, m, aluno, aula, cls=''):
        return (f'<tr{cls}><td class="num">{n}</td><td>{nome}</td><td class="num">{m}</td><td>{aluno}</td><td>{aula}</td></tr>')

    def parte(t):
        return f'<tr class="parte"><th scope="rowgroup" colspan="5">{t}</th></tr>'
    linhas += parte(f'Parte 1, ver antes de concluir ({sum(c["min"] for c in C[:volta])} minutos)')
    for i, c in enumerate(C):
        if i == volta:
            linhas += linha('', 'Folga', T['folga'], 'Nada novo no ecrã.', e(g['folga']), ' class="pausa"')
            linhas += linha('', 'Pausa', T['pausa'], '', '', ' class="pausa"')
            linhas += parte(f'Parte 2, pesar e escrever ({sum(c["min"] for c in C[volta:])} minutos)')
        nome = (f'<b>{e(c.get("rot") or "")}</b>' + (f'<br>{e(c["titulo"])}' if c['t'] == 'ler' and c.get('titulo') and c['titulo'] != c.get('rot') else ''))
        linhas += linha(i + 1, nome, c['min'], _tipo_aluno(c), e(g['na_aula'].get(i + 1, '')))
        total += c['min']
    linhas += linha('', 'O passo do projeto', T['projeto'], e(GUIA[s['n']]['projeto'][0]), e(g['projeto_aula']), ' class="pausa"')
    linhas += linha('', 'Entrega e arrumar', T['entrega'], '', e(g['entrega']), ' class="pausa"')
    total += sum(T.values())
    assert 175 <= total <= 185, total
    return (f'<div class="tabela"><table class="tempos"><caption class="c-sr">Os tempos da sessão {s["n"]}, cartão a cartão</caption>'
            '<thead><tr><th scope="col" class="num">N.º</th><th scope="col">Cartão</th><th scope="col" class="num">Min</th>'
            '<th scope="col">O aluno</th><th scope="col">Na aula (só aqui)</th></tr></thead>'
            f'<tbody>{linhas}</tbody><tfoot><tr><th scope="row" colspan="2">Total</th><td class="num">{total}</td><td colspan="2"></td></tr></tfoot></table></div>')


def secao_molde(s, g):
    d, C = s['d'], s['d']['cartoes']
    sessao = rel(GUIA_PASTA, s['pasta'])
    fazer = [(i, c) for i, c in enumerate(C) if c['t'] != 'ler']
    charn = ''
    for n, erro, fazer_se in g['charneiras']:
        c = C[n - 1]
        charn += (f'<tr><td class="num">{n}</td><td>{e(_txt(c["p"]))}</td><td>{e(_resposta(c))}</td><td>{e(erro)}</td><td>{e(fazer_se)}</td></tr>')
    chave = ''.join(f'<tr><td class="num">{i + 1}</td><td>{e(c["rot"])}</td><td>{e(_resposta(c))}</td><td>{e(c.get("tipo", ""))}</td></tr>' for i, c in fazer)
    img = next(c for c in C if c.get('rot') == 'Olha')
    credito = re.search(r'<p class="info-i-texto">(.*?)</p>', img['html'], re.S).group(1)
    return (f'<section class="sessao" id="s{s["n"]}"><p class="marca">Sessão {s["n"]}, no molde final</p><h2>{e(s["titulo"])}</h2>'
            f'<p class="lead">{s["pergunta"]}</p>'
            f'<p class="pg"><b>Domínio.</b> {e(g["dominio"])} <b>O que ensina.</b> {e(g["ensina"])}</p>'
            f'<p class="abrir"><a class="botao" href="{sessao}">Abrir a sessão</a><a class="botao" href="{sessao}?projetar=1">Projetar</a>'
            f'<a class="botao" href="{sessao}imprimir/">Versão para imprimir</a></p>'
            f'<p class="pg"><b>Antes.</b> {e(g["antes"])}</p>'
            '<h3>Os 180 minutos, cartão a cartão</h3>'
            '<p class="pg">A ordem dos cartões e das opções é fixa e igual na projeção e em todos os telemóveis; não há pontos. Tudo o que o aluno lê faz-se sozinho; o que depende do docente está só nesta coluna.</p>'
            + tabela_tempos(s, g)
            + '<h3>Como conduzir o Decide (cartão 2)</h3><ol class="passos">' + ''.join(f'<li>{e(x)}</li>' for x in g['decide']) + '</ol>'
            + '<h3>Como conduzir o «Em turma» (cartão 18, 13 minutos)</h3><ol class="passos">' + ''.join(f'<li>{e(x)}</li>' for x in g['em_turma']) + '</ol>'
            + '<h3>As duas charneiras</h3><div class="tabela"><table><thead><tr><th scope="col" class="num">Cartão</th><th scope="col">Pergunta</th>'
              '<th scope="col">Certa</th><th scope="col">Erro esperado</th><th scope="col">Se a turma errar</th></tr></thead>'
            f'<tbody>{charn}</tbody></table></div>'
            + '<h3>Agora, em papel (cartão 22): o que conta e a devolução</h3><ol class="passos">' + ''.join(f'<li>{e(x)}</li>' for x in g['papel']) + '</ol>'
            + f'<p class="pg">{e(g["devolucao"])}</p>'
            + f'<h3>Pergunta Humana: {e(g["projeto"][0])} (o passo do projeto, 45 minutos)</h3>'
            f'<p class="pg">{e(g["projeto"][2])} <a href="../../../projeto/{g["projeto"][1]}">Ver na página do projeto</a>.</p>'
            f'<h3>Grelha: {e(g["produto"])} (/20, indicativa)</h3>' + tabela_grelha(g)
            + '<p class="indicativa">Avaliação indicativa: orienta o trabalho e não é para usar a sério.</p>'
            + '<h3>Se só houver 90 minutos</h3><ul>' + ''.join(f'<li>{e(x)}</li>' for x in g['noventa']) + '</ul>'
            + '<h3>O que imprimir</h3><ul>' + ''.join(f'<li>{e(x)}</li>' for x in g['imprimir']) + '</ul>'
            + '<h3>Respostas dos 14 exercícios</h3><div class="tabela"><table><thead><tr><th scope="col" class="num">Cartão</th><th scope="col">Exercício</th>'
              f'<th scope="col">Resposta</th><th scope="col">Tipo</th></tr></thead><tbody>{chave}</tbody></table></div>'
            + f'<h3>O caso real</h3><p class="pg">{e(g["caso_real"])}</p>'
            + f'<h3>Imagem</h3><p class="pg">{credito}</p>'
            + '<h3>Notas</h3><ul>' + ''.join(f'<li>{LL.esc_it(x)}</li>' for x in g['notas']) + '</ul>'
            + f'<h3>Fontes da lição</h3><p class="pg fontes">{LL.esc_it(d["fontes"])}</p></section>')


# as tabelas das secções no molde (tempos, charneiras, respostas) ocupam a largura da página; no papel, uma só coluna
CSS_GUIA_MOLDE = (
 '@media screen and (min-width:600px){.cid-piloto section.sessao:has(table.tempos) .tabela{max-width:54rem}}'
 '.cid-piloto table.tempos td:nth-child(2){width:9.5rem}.cid-piloto table.tempos td:nth-child(4){width:6.5rem}.cid-piloto table.tempos td.num{width:2.6rem}'
 '.cid-piloto table.tempos tr.parte th{background:var(--fundo);text-align:left;font-size:.95rem}'
 '.cid-piloto table.tempos tr.pausa td{background:var(--fundo);font-style:italic}'
 '@media print{.cid-piloto.guia section.sessao:has(table.tempos){column-count:1}.cid-piloto table.tempos{font-size:9.5pt}}')


CSS_IMPRIMIR = (
 '.cid-piloto.imprimir main{max-width:44rem}'
 '.cid-piloto.imprimir h2{font:400 1.7rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;margin:28px 0 8px;padding-top:6px;border-top:3px solid var(--tinta)}'
 '.cid-piloto.imprimir .material{background:var(--papel);border:1.5px solid var(--tinta);padding:10px 16px;margin:12px 0}'
 '.cid-piloto.imprimir .material p,.cid-piloto.imprimir .material li{font-family:Georgia,"Times New Roman",serif}'
 '.cid-piloto.imprimir blockquote{margin:8px 0;padding-left:12px;border-left:2px solid var(--tinta)}'
 '.cid-piloto.imprimir blockquote .art{display:block;font:700 .72rem/1.3 Arial,Helvetica,sans-serif;letter-spacing:.1em;text-transform:uppercase}'
 '.cid-piloto.imprimir figure{margin:10px 0}.cid-piloto.imprimir figure img{max-width:100%;height:auto;display:block}'
 '.cid-piloto.imprimir figcaption{font:italic .95rem/1.4 Georgia,serif;margin-top:6px}.cid-piloto.imprimir .credito{font-size:.82rem}'
 '.cid-piloto.imprimir .ex{break-inside:avoid;margin:14px 0 18px}.cid-piloto.imprimir .ex .rot{font:700 .72rem/1.3 Arial,Helvetica,sans-serif;letter-spacing:.12em;text-transform:uppercase;margin:0 0 2px}'
 '.cid-piloto.imprimir .ex ol{margin:6px 0 4px;padding-left:1.6em}.cid-piloto.imprimir .ex ol.letras{list-style:upper-latin}'
 '.cid-piloto.imprimir .cols{display:grid;grid-template-columns:1fr 1fr;gap:4px 24px}'
 '.cid-piloto.imprimir .resp{margin:4px 0 0;font-size:.95rem}'
 '.cid-piloto.imprimir .a6{border:1.5px solid var(--tinta);padding:10px 14px;max-width:30rem;background:var(--papel)}'
 '.cid-piloto.imprimir .a6 .linhas{height:3.4em}'
 '.cid-piloto.imprimir table{font-size:.95rem}'
 '@media (max-width:599px){.cid-piloto.imprimir .cols{grid-template-columns:1fr}}'
 '@media print{.cid-piloto.imprimir h2{break-after:avoid}.cid-piloto.imprimir .material,.cid-piloto.imprimir .a6{break-inside:avoid}}'
 # 06/11/2026 (revisor de pt-PT; decisão 153 e atribuição CC BY): o crédito impresso leva os endereços por extenso
 '.cid-piloto.imprimir .credito a[href]::after{content:" (" attr(href) ")";word-break:break-all}')


def _ex_imprimir(num, c, d, k):
    """Um exercício na versão para imprimir, sem a resposta. A ordem das opções é a do ecrã (a semente do motor)."""
    q = f'<div class="ex"><p class="rot">Exercício {num}: {e(c["rot"])}</p>'
    if c.get('cita'):
        q += f'<p class="cita"><i>«{e(_txt(c["cita"]))}»</i></p>'
    p = html.unescape(re.sub(r'<[^>]+>', '', c['p']))
    if c['t'] == 'sublinhar':  # 06/11/2026: em papel não se toca, sublinha-se
        p = re.sub(r'\b([Tt])oca nas palavras', lambda m: ('S' if m.group(1) == 'T' else 's') + 'ublinha as palavras', p)
    q += f'<p><b>{LL.esc_it(p)}</b></p>'
    t = c['t']
    if t == 'escolha':
        ordem = dict(LL.ordem_opcoes(d)).get(k) or list(range(len(c['o'])))
        q += '<ol class="letras">' + ''.join(f'<li>{e(_txt(c["o"][j]))}</li>' for j in ordem) + '</ol><p class="resp">Resposta: ______</p>'
    elif t == 'vf':
        q += '<p class="resp">☐ Verdadeiro &nbsp; ☐ Falso</p>'
    elif t == 'sublinhar':
        q += f'<p class="material"><span>{e(c["frase"])}</span></p>'
    elif t == 'emparelhar':
        sem = LL._semente(d['chave'], k)
        esq = LL._mist(sem, list(range(len(c['pares']))))
        vals = list(dict.fromkeys(b for _, b in c['pares']))
        dto = LL._mist(sem, list(range(len(vals))))
        if len(vals) == len(c['pares']) and all(c['pares'][esq[i]][1] == vals[dto[i]] for i in range(len(esq))):
            dto = dto[1:] + dto[:1]
        q += ('<div class="cols"><ol>' + ''.join(f'<li>{e(_txt(c["pares"][j][0]))}</li>' for j in esq) + '</ol>'
              '<ol class="letras">' + ''.join(f'<li>{e(_txt(vals[j]))}</li>' for j in dto) + '</ol></div>'
              '<p class="resp">Liga: ' + ' &nbsp; '.join(f'{i + 1} ___' for i in range(len(esq))) + '</p>')
    elif t == 'ordenar':
        ordem = LL.ordem_ordenar(d, k)  # 06/11/2026: a ordem do ecrã, sem nenhum passo no seu lugar
        q += ('<ol class="letras">' + ''.join(f'<li>{e(_txt(c["passos"][j]))}</li>' for j in ordem) + '</ol>'
              '<p class="resp">Ordem: ' + ' → '.join('___' for _ in ordem) + '</p>')
    return q + '</div>'


def _ler_imprimir(c):
    """O material de um cartão de ler, para o papel: sem botões, sem lados por abrir, com o crédito por extenso."""
    h = c['html']
    h = re.sub(r'<button\b.*?</button>', '', h, flags=re.S)
    h = re.sub(r'<div class="pos-lados".*?</div></details></div>', '', h, flags=re.S)
    h = re.sub(r'<div class="tr-relogio".*?</div>', '', h, flags=re.S)
    h = re.sub(r'<details class="info-i"[^>]*><summary[^>]*>.*?</summary><p class="info-i-texto">(.*?)</p></details>', r'<p class="credito">\1</p>', h, flags=re.S)
    # 06/11/2026: «Ler mais» é um botão e no papel não diz nada; os outros títulos («O que conta», «Um exemplo…») ficam
    h = re.sub(r'<details class="mais"><summary>(.*?)</summary><div>(.*?)</div></details>',
               lambda m: ('' if m.group(1) == 'Ler mais' else f'<p><b>{m.group(1)}</b></p>') + m.group(2), h, flags=re.S)
    h = re.sub(r'<div class="cc-passo[^"]*"( hidden)?', '<div class="cc-passo"', h)
    h = re.sub(r'<p class="pos-antes"[^>]*></p>', '', h)
    h = re.sub(r'\s(?:data-[\w-]+="[^"]*"|hidden|role="[^"]*"|aria-[\w-]+="[^"]*")', '', h)
    h = h.replace('src="../../../../img/', 'src="../../../../../img/')
    return f'<div class="material">{h}</div>'


def _opcoes_prova(c):
    """06/11/2026: as opções da escolha que pesou no «Em turma» (data-valor), tiradas do cartão em vez de escritas à mão."""
    m = re.search(r'<div class="posicao" data-artefacto="prova".*?</div></div>', c['html'], re.S)
    return ' '.join(f'☐ {e(html.unescape(v))}' for v in re.findall(r'data-valor="([^"]+)"', m.group(0))) if m else ''


def pagina_imprimir(s):
    """A versão para imprimir da sessão (plano, secção 5): o material, os 14 exercícios sem retorno e o papel, para quem não tem
    telemóvel, bateria ou rede. As respostas ficam no guia do docente."""
    d, C = s['d'], s['d']['cartoes']
    base = '../' * (s['pasta'].count('/') + 1)
    corpo = (f'<header><p class="marca">Cidadania, módulo 1, sessão {s["n"]}</p><h1>{e(s["titulo"])}</h1>'
             '<p class="lead">Versão para imprimir: o material, os 14 exercícios e o papel do fim. Fazes tudo sozinho, só com uma caneta.</p>'
             '<p><button type="button" class="imprimir" onclick="window.print()">Imprimir</button></p></header>'
             '<div class="campos"><span>O teu código: ____________</span><span>Data: ____ / ____</span></div>')
    num = 0
    volta = next(i for i, c in enumerate(C) if c.get('rot') == 'Volta ao caso')
    corpo += '<h2>Parte 1, ver antes de concluir</h2>'
    for k, c in enumerate(C):
        if k == volta:
            corpo += '<h2>Parte 2, pesar e escrever</h2>'
        if c['t'] != 'ler':
            num += 1
            corpo += _ex_imprimir(num, c, d, k)
            continue
        rot = c.get('rot')
        if rot == 'Para levar':
            continue
        if rot in ('Decide', 'Em turma'):
            perg = re.findall(r'<p class="pos-q">(.*?)</p>', c['html'])
            corpo += (f'<div class="ex"><p class="rot">{e(rot)}</p><p><b>{perg[0]}</b></p><p class="resp">☐ Sim &nbsp; ☐ Não &nbsp; ☐ Depende</p>'
                      + ('<p>Escreve, numa linha, a razão que pesa mais para ti.</p><div class="linhas"></div>' if rot == 'Decide' else
                         f'<p>Compara com a tua escolha do início. {perg[1] if len(perg) > 1 else ""} {_opcoes_prova(c)}</p>')
                      + '</div>')
            continue
        titulo = f'<p class="rot">{e(rot)}{": " + e(c["titulo"]) if c.get("titulo") and c["titulo"] != rot else ""}</p>'
        corpo += titulo + _ler_imprimir(c)
    corpo += f'<footer class="mais"><a href="{base}{s["pasta"]}">Voltar à sessão</a></footer>'
    return (cabeca(base, f'{s["titulo"]}, para imprimir · Cidadania · Lente', f'Sessão {s["n"]} do módulo 1 de Cidadania, para imprimir.')
            + f'<body class="cid-piloto imprimir"><style>{CSS_IMPRIMIR}.c-sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}</style>'
            + f'<main id="conteudo">{corpo}</main></body></html>\n')


def pagina_ponto():
    base = '../../../../'
    qs = ''
    for i, (ses, q, ops, c) in enumerate(PONTO, 1):
        if ops:
            qs += (f'<div class="q"><p><b>{i}.</b> {e(q)}</p><ol>'
                   + ''.join(f'<li>{LETRAS[k]}. {e(o)}</li>' for k, o in enumerate(ops)) + '</ol>'
                   '<p>Resposta: ______</p></div>')
        else:
            qs += f'<div class="q"><p><b>{i}.</b> {e(q)}</p>' + '<div class="linhas"></div>' * 4 + '</div>'
    corpo = (migalhas(base, [('Lente', LENTE), ('Cidadania', LENTE + 'cidadania/'), ('Módulo 1 (piloto)', '../'), ('Ponto de partida e de chegada', '')])
             + '<header><p class="marca">Cidadania, módulo 1</p><h1>Ponto de partida e de chegada</h1>'
             '<p class="lead">Dez perguntas, em papel, sem ajuda e sem consulta: 10 a 15 minutos. Na sessão 01 é o Ponto de partida; na sessão 10, as mesmas perguntas são o Ponto de chegada. Não conta para nota: serve para veres o que mudou.</p>'
             '<p><button type="button" class="imprimir" onclick="window.print()">Imprimir</button></p></header>'
             '<div class="campos"><span>O teu código: ____________</span><span>Data: ____ / ____</span><span>Partida ☐ Chegada ☐</span></div>'
             '<p>Nas perguntas 1 a 8, escreve a letra da resposta. Nas perguntas 9 e 10, responde em duas ou três linhas.</p>'
             + qs)
    return (cabeca(base, 'Ponto de partida e de chegada, módulo 1 · Cidadania · Lente', 'As mesmas 10 perguntas no início e no fim do módulo 1 de Cidadania, para imprimir.')
            + f'<body class="cid-piloto"><main id="conteudo">{corpo}</main></body></html>\n')


def regras(nome, s):
    """As regras da casa no texto visível (a <title> leva «·» como as lições; fica de fora)."""
    corpo = re.sub(r'<(script|style|title)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    txt = LL.visivel(corpo)
    erros = [f'{nome}: «{m.group(0)}» em …{txt[max(0, m.start() - 40):m.end() + 40]}…' for m in LL.PROIBIDAS.finditer(txt)]
    erros += [f'{nome}: «{m.group(0)}» (usa «Qual das…» ou «Que…»)' for m in LL.QUAL_NOME.finditer(txt)]
    return erros


def paginas():
    S = sessoes()
    out = {MODULO + 'index.html': pagina_modulo(S), MODULO + 'docente/index.html': pagina_guia(S), MODULO + 'ponto/index.html': pagina_ponto()}
    # 05/11/2026 (plano do molde, pedido 2): cada sessão no molde tem a versão para imprimir. O endereço antigo do piloto
    # (cidadania/piloto/m1-s01/) fica como está até ao pedido 3, que faz os redirecionamentos do piloto todos de uma vez.
    for s in S:
        if s.get('molde'):
            out[s['pasta'] + 'imprimir/index.html'] = pagina_imprimir(s)
    return out


def main(argv):
    verificar = '--verificar' in argv
    falhou = False
    for rel, s in paginas().items():
        erros = regras(rel, s)
        if erros:
            falhou = True
            print('\n'.join(erros))
            continue
        alvo = ROOT / rel
        if verificar:
            ok = alvo.exists() and alvo.read_text('utf-8') == s
            print(f'{rel}: ' + ('ok' if ok else 'desatualizada (corre o gerador)'))
            falhou |= not ok
        else:
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_text(s, 'utf-8')
            print(f'{rel}: escrita')
    return 1 if falhou else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
