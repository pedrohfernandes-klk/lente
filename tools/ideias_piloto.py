"""31/10/2026: «Ideias», o coração do Laboratório, em piloto escondido (decisões do docente 31 a 34 e 39; plano final em
coracao/plano.md, no caderno de bordo).

Escreve, a partir das lições em tools/licoes/ideias-sNN.json (as que já existem) e do quadro SESSOES abaixo:
- narrativas/ideias/index.html: a entrada da secção no sistema «Cartaz» (barra, abertura com a imagem do atol, uma só
  região preta «A seguir», o gesto de decisão das escadas, as sete sessões em três portas, saídas e rodapé). Lê o progresso
  das chaves epi-lab-ideias-sNN (o formato que o motor grava no fim de uma lição: «lida», «versao» e «t»); na projeção
  (?projetar=1) não lê nada e mostra sempre «Começa aqui: 1»;
- narrativas/ideias/guiao/index.html: o guião em papel, frente e verso por sessão, para imprimir em A4;
- narrativas/ideias/docente/index.html: o guia do docente, com o quadro da sequência e, por sessão pronta, os tempos, os
  materiais, o que fica escrito, a imagem, o vídeo, a grelha /20 indicativa e as notas;
- biblioteca/young-tecnica-1940/index.html: a página do Young na Biblioteca, no molde das outras (biblioteca/orta-benjui/),
  só com o excerto aprovado (decisão 31: até 120 palavras, «tradução nossa», crédito e ligação ao registo do livro). É
  pública, entra na lista da Biblioteca (biblioteca/index.html, «Em português») e não liga ao coração enquanto ele for piloto.

As três páginas do coração levam noindex, nofollow e nenhuma página do mapa, das portas, da entrada do Laboratório ou de
assets/laboratorio/percursos.json liga para elas (tests/test_ideias.py confirma).

Porquê um gerador próprio e não uma extensão de tools/cidadania_piloto.py: aquele está preso às dez sessões do M1, ao Ponto
de partida e à Pergunta Humana, e as suas páginas são comparadas byte a byte; a entrada de «Ideias» tem outra forma (a imagem
com a tabela de museu, o gesto, as sessões por porta, as sessões ainda em preparação) e o guião é em papel, frente e verso.
Partilham-se as regras de escrita e as funções de tools/licoes_lente.py (visivel, PROIBIDAS, QUAL_NOME, esc_it).

01/11/2026 (método, encargo do docente «assumir o método de Young, passo a passo»): a entrada abre com o bloco «O método»
(quem é Young, o livro de 1940, que as sete sessões seguem o método dele passo a passo, que há outros e porque seguimos este, e
os cinco passos numa lista numerada, PASSOS) e a frase de abertura nomeia o método; cada sessão diz «Passo N de 5» (ou
«Passos N e N+1 de 5») na lista e na região «A seguir»; o guião diz o passo no cabeçalho de cada sessão; o guia do docente abre
com «Porque seguimos um método» e deixa de repetir «Young» onde basta «o método» ou «o passo».

Uso: python3 tools/ideias_piloto.py              (escreve as páginas e acerta a linha da lista da Biblioteca)
     python3 tools/ideias_piloto.py --verificar  (confirma que estão atualizadas e que cumprem as regras da casa)"""
import html, importlib.util, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('licoes_lente', ROOT / 'tools/licoes_lente.py')
LL = importlib.util.module_from_spec(spec); spec.loader.exec_module(LL)
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
PASTA = 'narrativas/ideias/'
e = html.escape

# As sete sessões (plano final, secção 4.1). As que têm lição em tools/licoes/ideias-sNN.json ficam prontas e ligadas; as
# outras aparecem «Em preparação», sem ligação. «linha» e «papel» são o que a região «A seguir» mostra dessa sessão.
# 01/11/2026 (correção 2 do método, diretor de arte): o passo de cada porta é o das sessões que estão dentro dela (Ver, sessões
# 1 e 2: passo 1; Treinar, sessões 3 e 4: passos 1 a 3); antes, Ver dizia «Passos 1 e 2» e Treinar «Passos 2 e 3»
PORTAS = [
 ('ver', 'Ver', 'Passo 1: juntar material, com os olhos e até ao fundo.', '../ver/'),
 ('treinar', 'Treinar', 'Passos 1 a 3: o material geral, trabalhá-lo na cabeça e, depois, largá-lo.', '../treinar/'),
 ('criar', 'Criar', 'Passos 4 e 5: a ideia aparece, ganha forma e vai a quem a pode criticar.', '../criar/'),
]
SESSOES = [
 {'n': 1, 'porta': 'ver', 'titulo': 'Ver ou observar?', 'pergunta': 'Quantos degraus tem a escada que sobes todos os dias?',
  'passo': 'Passo 1 de 5: juntar material, com os olhos', 'peca': ('Observar para transformar', 'Galileu', 'galileu/'),
  'linha': 'O detetive Sherlock Holmes, a historiadora de arte Amy\u00a0E.\u00a0Herman, um quadro do pintor Georges de La Tour e a escada da escola.', 'papel': 'o auto de observação do grupo.'},
 {'n': 2, 'porta': 'ver', 'titulo': 'O cocheiro', 'pergunta': 'O que distingue uma coisa de todas as outras iguais a ela?',
  'passo': 'Passo 1 de 5: juntar material, até ao fundo', 'peca': ('Conhecer uma personagem', 'A personagem pelo que faz', 'personagem-faz/'),
  'linha': 'O escritor Guy de Maupassant e o seu mestre, Gustave Flaubert, uma fotografia de Paris e um lugar perto da escola.', 'papel': 'o teu «cocheiro», a linha que levaste à fila e o resultado.'},
 {'n': 3, 'porta': 'treinar', 'titulo': 'O caleidoscópio', 'pergunta': 'Uma ideia nova é feita de coisas velhas?',
  'passo': 'Passos 1 e 2 de 5: o material geral e as relações', 'peca': ('Escolher por onde começar', 'Lista de substantivos', 'treinar/lista-substantivos/')},
 {'n': 4, 'porta': 'treinar', 'titulo': 'Três cachimbos', 'pergunta': 'O que fazes com os factos quando ainda não fazem sentido?',
  'passo': 'Passos 2 e 3 de 5: trabalhar o material e largá-lo', 'peca': ('Escolher a palavra e o ritmo', 'Cópia lenta', 'treinar/copia-lenta/')},
 {'n': 5, 'porta': 'criar', 'titulo': 'O estribo', 'pergunta': 'Quando a ideia aparece, sabes de onde veio?',
  'passo': 'Passo 4 de 5: a ideia aparece', 'peca': ('Construir uma ficção', 'Do conceito ao argumento', 'oficina-argumento/')},
 {'n': 6, 'porta': 'criar', 'titulo': 'A manhã seguinte', 'pergunta': 'Quem pode tornar a tua ideia melhor?',
  'passo': 'Passo 5 de 5: dar forma e pôr à prova', 'peca': ('Construir com palavras e imagens', 'A matriz por meio', 'oficina-matriz/')},
 {'n': 7, 'porta': 'criar', 'titulo': 'As versões à mostra', 'pergunta': 'Como se mostra o caminho de uma ideia?',
  'passo': 'Os cinco passos juntos', 'peca': ('Criar para além da página', 'O espaço expandido', 'oficina-espaco/')},
]
# 01/11/2026 (método): os cinco passos do método, com nomes simples conferidos no resumo do próprio Young (texto de trabalho no
# caderno de bordo, biblioteca-young/texto.txt, capítulo «A Fase Final»: «a recolha de matérias-primas», «o tratamento mental
# destas matérias-primas», «a fase de incubação, em que deixamos algo para além da mente consciente fazer o trabalho de
# síntese», «o nascimento propriamente dito da ideia», «a moldagem e desenvolvimento final da ideia»; e «submetê-la à crítica de
# pessoas criteriosas»). Os mesmos nomes nos cartões (tools/licoes/ideias-sNN.py) e no guia.
PASSOS = ['Juntar material', 'Trabalhar o material', 'Largar', 'A ideia aparece', 'Dar forma e pôr à prova']
# 01/11/2026 (correção 3, diretor de arte): a imagem voltou a ser tratada, porque o recife mal se separava do oceano (2,06:1
# em claro e 1,80:1 em escuro). Em cinzento: a vinheta da fotografia original aplanada (fundo estimado pelo percentil 25 em
# blocos de 40 px, alisado), depois níveis de entrada 110 a 235 levados a 0 a 255, com gama 1,0; a multiplicação sobre
# --campo continua no CSS. Mediana 78 e percentil 99 239: 4,84:1 sobre #d9a520 e 3,32:1 sobre #9a7a22, e o canto inferior
# direito já não escurece (de 113 para 79 de média, como o resto do oceano).
ATOL = {
 'src': '../../assets/laboratorio/ideias/manihi-atol.webp', 'w': 1200, 'h': 789,
 'alt': 'Vista do espaço: um anel estreito de recife e ilhotas fecha uma lagoa no meio do oceano, com pequenas nuvens à volta.',
 'tabela': ('Tripulação da Expedição 6 da Estação Espacial Internacional, <i>Atol de Manihi, arquipélago das Tuamotu</i> (título nosso), '
            '9 de março de 2003. Fotografia <span class="id">ISS006-E-37110</span>. Imagem cedida pela Earth Science and Remote Sensing Unit, NASA Johnson Space Center '
            '(<a href="https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS006&amp;roll=E&amp;frame=37110">eol.jsc.nasa.gov</a>). '
            'Domínio público. Recorte e tratamento a duas cores: nossos.'),
}
# O guia do docente: o que só o docente lê, por sessão pronta (plano final, secção 8). Tempos em minutos.
GUIA = {
 1: {
  'ensina': 'Separar o que se vê do que se conclui; observar é ver com uma pergunta. É o passo 1 de 5: juntar material específico.',
  'antes': 'Ter a lista dos lugares da escola para os grupos (a escada, o portão, o bar, o pátio), um por grupo, para dois grupos não se cruzarem. Confirmar o som do projetor para o vídeo.',
  'tempos': [
   ('0 a 5', '«Abre»: cada um escreve o número de degraus, em silêncio. O docente anota três palpites no quadro, sem nomes.'),
   # 01/11/2026 (método): o cartão novo «O método» (cartão 2) leva 5 minutos, tirados da folga do fim; os cartões seguintes
   # passam um número para a frente
   ('5 a 10', '«O método» (cartão 2): os cinco passos no quadro, numerados, com o passo 1 marcado (ver «Porque seguimos um método», acima).'),
   ('10 a 20', '«Decide», de braço no ar. Não se fecha: a posição volta na sessão 7.'),
   # 01/11/2026 (correção 5, revisor de pt-PT): «no cartão 7», o único com o vídeo («a partir do» lia-se «daí em diante»)
   ('20 a 55', 'Cartões 4 a 14. O vídeo de Herman (4 min 50 s) projeta-se com legendas no cartão 8; diante do quadro de La Tour, dois minutos de silêncio antes de alguém falar.'),
   ('55 a 125', '«Na aula» (70 minutos): 5 para as regras e os grupos de três; 20 no lugar (um facto de cada vez; contam-se os degraus); 10 de pausa; 15 na troca, em que cada grupo vai ao lugar de outro e marca cada facto como confirmado ou desmentido; 15 na sala, a passar o auto para o guião; 5 para dois grupos dizerem o número de degraus.'),
   ('125 a 150', 'Cartões 16 a 20.'),
   ('150 a 170', '«Para levar»: palpites contra contagem (quantos acertaram, quantos erraram por mais de três). Cada um guarda os factos com o resto do seu material.'),
   ('170 a 180', 'Folga: as duas colunas do vídeo e as cinco coisas do quadro passam a limpo no guião; cada um escreve o lugar para a sessão 2.'),
  ],
  # 01/11/2026 (correção 2, revisor de pt-PT): no guia, o crédito do vídeo sem a instrução ao aluno («ativa as legendas»)
  'video_cred': 'TED-Ed, lição de Amy\u00a0E.\u00a0Herman, em inglês, com legendas no leitor.',
  'materiais': ['A forma escolhida por cada aluno para guardar o material; para quem quiser, cartões brancos de 12,5 por 7,5 centímetros.', 'O guião da sessão 1, impresso.', 'Projetor com som e um relógio visível.'],
  'escrito': 'O palpite e a contagem; as duas colunas do vídeo; as cinco coisas do quadro; o auto do grupo, com as marcas do grupo que verificou; os factos, na forma escolhida por cada um; o lugar para a sessão 2.',
  'produto': 'o auto de observação, por grupo',
  # 01/11/2026 (correção 6, revisor de pt-PT): «A pergunta a que o lugar não responde», como o campo do guião que avalia
  'grelha': [('Factos verificáveis, sem opinião nem «parece»', 6), ('Três inferências, cada uma apoiada em dois factos', 5), ('A pergunta a que o lugar não responde', 2), ('Factos confirmados pelo grupo que foi verificar', 4), ('Factos registados um a um, na forma escolhida', 3)],
  'notas': [
   'Se a escola não tiver uma escada com degraus contáveis, conta-se outra coisa que todos veem e ninguém contou (as janelas da fachada, os cacifos do corredor); o «Abre» diz «escada», e o docente troca a palavra em voz alta.',
   'No conto, Watson já está casado e só visita Baker Street: os cartões dizem que o visita, nunca que vive com Holmes.',
   'O quadro de Magritte (_Time Transfixed_) é o exemplo do resumo oficial da lição de Herman e não se reproduz no Lente: Magritte morreu em 1967 e a obra não está em domínio público.',
   'O título português do quadro de La Tour, _A leitora da sina_, é nosso, e o cartão di-lo. Nas lições, as imagens ficam a preto e branco e a cor volta no fim; para mostrar as cores à turma, o docente abre a página do Met.',
   'Os dois cartões «Toca no quadro» são novos no Lente: quando duas zonas ficam muito juntas, o primeiro toque amplia o quadro e o segundo escolhe. Se no aparelho de algum aluno não funcionar, faz-se a mesma pergunta em voz alta, com o quadro projetado.',
   'Para quem quiser ir mais longe: a enfermeira Florence Nightingale e a observação dos doentes, na Biblioteca; e Como se investiga, passo 2, «Olhar e registar».',
  ],
  'ligacoes': [('Florence Nightingale, _Notas sobre Enfermagem_ (Biblioteca)', '../../../biblioteca/nightingale-observacao/'), ('Como se investiga, passo 2', '../../../investigar/passo-02/'), ('_The Fortune-Teller_ no Met (cores)', 'https://www.metmuseum.org/art/collection/search/436838')],
 },
 2: {
  'ensina': 'Ir à fonte de uma citação sem cinismo (uma testemunha que erra num pormenor não mente) e pôr uma descrição à prova em quem não sabe o que se descreve. É o passo 1 de 5, até ao fundo.',
  'antes': 'Se a turma sair, escolher, entre os lugares que os alunos escreveram no guião da sessão 1, um só lugar a cinco minutos da escola, com um percurso sem travessias perigosas, onde os pares possam estar sempre à vista do docente.',
  'tempos': [
   ('0 a 5', '«Abre»: diz-se à turma o lugar da saída ou, se não houver saída, a alternativa (a janela ou uma fotografia de rua).'),
   ('5 a 15', '«Decide», de braço no ar.'),
   ('15 a 50', 'Cartões 3 a 12: as duas versões do conselho (a do livro, de 1940, e a de Maupassant, de 1888) lidas em voz alta, com a comparação no guião; a fotografia de Atget com dez minutos de «vejo, concluo, não sei».'),
   ('50 a 120', '«Na aula» (70 minutos): 5 para as regras (pares; ninguém fotografa caras; pessoas só de longe; quinze notas); 5 de caminho; 25 no lugar (cada um escolhe o seu «cocheiro», escreve-o no guião, regista as quinze notas e escreve a linha que só serve para ele); 5 de regresso; 10 de pausa; 15 para a fila de reconhecimento (cada um lê a sua linha sem dizer o que é; a turma diz qual é; o docente regista «reconhecido» ou «não»); 5 para cada um rever a linha.'),
   ('120 a 145', 'Cartões 14 a 18.'),
   ('145 a 165', 'Guião: cada um completa a tabela das duas versões do conselho; «Para levar».'),
   ('165 a 180', 'Folga: as três colunas da fotografia passam a limpo no guião; o docente explica as dez notas de material geral para a sessão 3.'),
  ],
  'materiais': ['O material de cada aluno, com espaço para quinze notas.', 'Cartão rígido ou pranchetas para escrever na rua.', 'O guião da sessão 2, impresso.', 'O percurso até ao lugar e o quadro da sala para a lista dos «cocheiros» (só o nome de cada um, sem a linha).'],
  'escrito': 'As quinze notas; a linha antes e depois da fila, com o resultado; as três colunas sobre a fotografia; as duas versões do conselho comparadas.',
  # 01/11/2026 (correção 5, revisor de pt-PT): sem «de cada aluno», que repetia «individual», e em paralelo com a sessão 1
  'produto': 'o «cocheiro», individual',
  'grelha': [('Quinze notas nas três categorias (vê; ouve, cheira ou toca; distingue)', 6), ('Nenhuma inferência escrita como observação', 4), ('A linha que só serve para aquele «cocheiro», testada na fila (reconhecida: 6 pontos; não reconhecida, mas revista: 4 pontos)', 6), ('As duas versões do conselho comparadas: o que mudou e o que ficou', 4)],
  'notas': [
   'A descoberta da sessão não é «o livro enganou-se»: é que a versão de 1940 muda três pormenores e guarda o essencial, que está em Maupassant quase com as mesmas palavras. Se a turma cair no cinismo, o docente lê esta frase do prefácio: Flaubert «obrigava-me a exprimir, em poucas frases, um ser ou um objeto de maneira a particularizá-lo nitidamente» (tradução nossa).',
   'O livro não diz onde foi buscar a história; os cartões não dizem mais do que isto.',
   'As traduções de Maupassant são nossas e curtas; o texto inteiro, em francês, está no Project Gutenberg.',
   'A saída é opcional (decisão do docente de 31/10): sem ela, cada aluno escolhe o seu «cocheiro» da janela, numa fotografia de rua ou no caminho de casa para a escola, com as mesmas regras.',
   # 01/11/2026 (correção 5, revisor de pt-PT): a pergunta já não dá por certo que o sítio prova alguma coisa (o retorno do
   # cartão 12 chama-lhe «uma pista mais forte do que uma capa», e a sessão ensina que uma inferência não é uma prova)
   'Na fotografia de Atget há um homem sentado no alto de um fiacre, na ponta esquerda. Boa pergunta para a turma: o sítio onde está é uma prova ou só uma pista mais forte?',
  ],
  'ligacoes': [('Maupassant, prefácio de _Pierre et Jean_ (Project Gutenberg, em francês)', 'https://www.gutenberg.org/ebooks/11131'), ('_Kiosque et fiacres, Paris_ na Paris Musées', 'https://www.parismuseescollections.paris.fr/fr/musee-carnavalet/oeuvres/kiosque-et-fiacres-paris')],
 },
}
# O guião em papel (plano final, 8.1): frente e verso por sessão pronta.
# 01/11/2026 (correção 2, diretor de arte): na sessão 2, mais linhas de escrita onde se pedem razões e versões (a tabela de
# Atget com sete filas, para as «pelo menos três linhas» de cada coluna), em vez de 113 e 143 mm de branco no fundo das páginas
# 3 e 4; continuam 4 páginas A4.
# 01/11/2026 (correção 3, diretor de arte): o mesmo na sessão 1, cujas páginas acabavam com 88,6 e 84,8 mm de branco (contra
# 63,5 e 65,3 na sessão 2): o vídeo de Herman com oito filas e a pergunta a que o lugar não responde com três linhas.
GUIAO = {
 1: {
  'frente': [
   # 01/11/2026 (correção 4, diretor de arte): no telemóvel, nenhum espaço para escrever sozinho numa linha
   ('p', 'O teu palpite: <i class="b"></i> degraus. <span class="nq">A contagem: <i class="b"></i></span> <span class="nq">(grupos <i class="b"></i> e <i class="b"></i>).</span>'),
   ('h2', 'O vídeo de Herman, em duas colunas'),
   ('tabela', ['Está no quadro', 'Não está no quadro, mas conta'], 8),
   ('h2', 'O quadro de La Tour: cinco coisas que se veem'),
   ('nota', 'Só o que se vê: nada de «parece» nem de «está a pensar».'),
   ('linhas', 5),
   ('h2', 'A tua posição: as ideias caem do céu?'),
   ('p', 'Sim, não ou depende: <i class="b"></i>'),
   ('p', 'A razão, numa linha: <i class="b l"></i>'),
  ],
  'verso_titulo': 'O auto de observação',
  'verso': [
   ('p', 'Lugar: <i class="b"></i> Grupo: <i class="b"></i> Hora: <i class="b"></i>'),
   ('tabela', ['Facto (um que outro grupo possa confirmar)', 'Confirmado ou desmentido pelo grupo\u00a0___'], 10),
   ('tabela', ['Inferência', 'Os dois factos que a apoiam'], 3),
   # 01/11/2026 (correção 6, revisor de pt-PT): «responder a» (a pergunta a que…), aqui e na grelha do guia
   ('p', 'A pergunta a que o lugar não responde: <i class="b l"></i>'),
   ('linhas', 2),
   ('nota', 'Os teus factos ficam onde guardas o material; este papel entrega-se ao docente.'),
   ('p', 'Para a sessão 2, um lugar a cinco minutos da escola por onde passas sem olhar: <i class="b l"></i>'),
  ],
 },
 2: {
  'frente': [
   ('h2', 'As duas versões do conselho, lado a lado'),
   # 01/11/2026 (método): as colunas com os nomes que as versões têm nos cartões («a versão de 1940», «em 1888»)
   ('tabela-linhas', ['', 'Versão de 1940', 'Versão de 1888', 'Mudou ou ficou?'], ['Quem dá o conselho', 'O que se olha', 'O que se pede', 'Com quantas palavras']),
   ('h2', 'A fotografia de Atget, em três colunas'),
   ('tabela', ['Vejo', 'Concluo', 'Não sei'], 7),
   ('h2', 'A tua posição: uma árvore da tua rua é só uma árvore?'),
   ('p', 'Sim, não ou depende, e porquê: <i class="b l"></i>'),
   ('linhas', 3),
  ],
  'verso_titulo': 'O teu «cocheiro»',
  'verso': [
   ('p', 'O que é e onde está: <i class="b l"></i>'),
   ('linhas', 3),
   ('h2', 'As quinze notas, resumidas em cinco linhas'),
   ('linhas', 5),
   ('p', 'A linha que só serve para ele, antes da fila: <i class="b l"></i>'),
   ('linhas', 3),
   ('p', 'Resultado da fila: reconhecido por <i class="b"></i> de <i class="b"></i> colegas.'),
   ('p', 'A linha revista: <i class="b l"></i>'),
   ('linhas', 3),
   ('nota', 'Para a sessão 3: dez notas de material geral (um desporto, uma receita, uma canção, um ofício da família), uma coisa por nota, com um pormenor que só tu sabes. Guarda-as onde guardas o material.'),
  ],
 },
}
# A página da Biblioteca (decisão 31): o excerto aprovado, conferido letra a letra com a tradução nossa (texto de trabalho no
# caderno de bordo, biblioteca-young/texto.txt, capítulo «Combinação de Elementos Antigos», parágrafos 96, 98 e 99, com um corte).
YOUNG_EXCERTO = [
 'O primeiro foi já referido na citação de Pareto: que uma ideia não é nada mais, nada menos, do que uma nova combinação de elementos antigos.',
 'O segundo princípio relevante aqui envolvido é que a capacidade de fazer novas combinações a partir de elementos existentes depende, em larga medida, da capacidade de ver relações.',
 'É aqui, suspeito, que as mentes mais diferem umas das outras no que se refere à produção de ideias propriamente dita. Para umas, cada facto é um pedaço de conhecimento autónomo. Para outras, é um elo numa cadeia de conhecimento: tem relações e semelhanças, e é menos um facto do que a ilustração de uma lei geral aplicável a toda uma série de factos.',
]
YOUNG_REGISTO = 'https://archive.org/details/techniqueforprod0000jame'
BIB_ID = 'young-tecnica-1940'


def it(s):
    return LL.esc_it(s)


def licoes():
    out = {}
    for p in sorted((ROOT / 'tools/licoes').glob('ideias-s*.json')):
        d = json.loads(p.read_text('utf-8'))
        out[int(d['id'][-2:])] = d
    return out


TOKENS = ':root{--tinta:#000;--papel:#fff;--fundo:#f3f2ee;--suave:#444;--mostarda:#d9a520;--vermelho:#c8232c;--campo:#d9a520}'
CSS = (TOKENS +
 '*{box-sizing:border-box}'
 'body.ideias{margin:0;background:var(--fundo);color:var(--tinta);font:17px/1.5 Arial,Helvetica,sans-serif}'
 '.ideias main{max-width:1200px;margin:0 auto;padding:0 16px 56px}'
 # 01/11/2026 (correção 5, diretor de arte; sistema 3): 24 px de margem lateral a partir de 768 px, como na Cidadania piloto
 # (eram 16 px a 768 e a 1024 px); a largura útil fica nos 1200 px do --larga do sistema
 '@media (min-width:768px){.ideias main{padding-left:24px;padding-right:24px;max-width:1248px}}'
 '.ideias a{color:inherit;text-underline-offset:.15em}'
 '.ideias :is(a,button,summary):focus-visible{outline:3px solid var(--tinta);outline-offset:3px}'
 '.ideias .c-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
 # 31/10/2026 (revisão do diretor de arte): «Saltar para o conteúdo» (sistema, secção 7), o primeiro alvo do teclado
 '.ideias a.salta:focus{position:fixed;left:8px;top:8px;z-index:10;width:auto;height:auto;overflow:visible;clip:auto;white-space:normal;padding:10px 14px;background:var(--papel);color:var(--tinta);font-weight:700}'
 # barra (sistema 6.1): migalhas com «›», o tema e o botão de projeção à direita, 12 px de folga mínima
 '.ideias .migalhas{display:flex;flex-wrap:wrap;align-items:center;gap:0 12px;min-height:56px;font-size:.9375rem;margin:0 0 12px}'
 '.ideias .migalhas a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px}'
 '.ideias .migalhas .sep{color:var(--suave)}'
 '.ideias .migalhas [aria-current]{font-weight:700}'
 '.ideias .migalhas [data-appearance-control]{margin-left:auto}'
 '@media (max-width:359px){.ideias .migalhas{gap:0 8px;font-size:.875rem}}'
 # 31/10/2026 (revisão do diretor de arte): abaixo de 400 px a barra cabe numa linha (sistema 6.1); o último elo, a página
 # onde estás, que o h1 logo abaixo repete, fica só para o leitor de ecrã, como no piloto da Cidadania
 '@media (max-width:399px){.ideias .migalhas [aria-current]{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}.ideias .migalhas .sep:has(+[aria-current]){display:none}}'
 '.ideias .rotulo{display:flex;align-items:center;gap:8px;font:700 .8125rem/1.2 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;margin:0 0 8px}'
 '.ideias .rotulo::before{content:"";width:11px;height:11px;background:var(--tinta);flex:none}'
 '.ideias h1,.ideias h2,.ideias h3{text-wrap:balance}'
 '.ideias p{text-wrap:pretty}'
 # abertura (sistema 6.2)
 '.ideias .abre h1{font:400 clamp(3.6rem,15vw,6rem)/.86 "Bebas Neue","Arial Narrow",Arial,sans-serif;letter-spacing:.01em;margin:0}'
 '.ideias .abre .sub{font:italic 1.25rem/1.3 Georgia,"Times New Roman",serif;margin:4px 0 14px}'
 '.ideias .abre .lead{font:1.125rem/1.5 Georgia,"Times New Roman",serif;margin:0 0 10px;max-width:32em}'
 '.ideias .abre .info{font-size:.9375rem;color:var(--suave);margin:0 0 20px;max-width:36em}'
 # 01/11/2026 (correção 4, diretor de arte): a linha de informação e a etiqueta de parede passavam os 75 carateres por linha
 # (77 e 78 a 1366 px): 34 em
 '.ideias .abre .info,.ideias .topo .atol figcaption{max-width:34em}'
 # 01/11/2026 (método): o bloco «O método» (sistema 6.2, abertura): um filete, o rótulo em caixa alta como os títulos de secção
 # do rodapé, o parágrafo a tinta e os cinco passos numa lista numerada que parte entre passos e nunca dentro de um, com os
 # números em cartaz, como os das sessões
 # 01/11/2026 (correção 2 do método, diretor de arte): o bloco fica com a largura da coluna (o título, a frase de abertura e a
 # imagem), para o filete acabar onde ela acaba; com 34 em (a 17 px, 578 px), acabava a meio da coluna a 1366 e 1440 px. A medida
 # do parágrafo continua nos 34 em da linha de informação (a 15 px, 510 px), pela regra de cima
 '.ideias .metodo{border-top:2px solid var(--tinta);padding-top:8px;margin:0 0 20px;max-width:none}'
 '.ideias .metodo h2{float:left;font:700 .8125rem/1.67 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;margin:0 10px 0 0}'
 '.ideias .abre .metodo .info{color:var(--tinta);margin:0 0 8px}'
 '.ideias ol.passos-m{clear:both;list-style:none;display:flex;flex-wrap:wrap;gap:0 18px;margin:0;padding:0}'
 '.ideias ol.passos-m li{display:inline-flex;align-items:baseline;gap:6px;font:700 .9375rem/1.4 Arial,Helvetica,sans-serif;white-space:nowrap}'
 '.ideias ol.passos-m b{font:400 1.3125rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif}'
 # 01/11/2026 (correção 1 do método, diretor de arte): em flex-wrap, a lista partia onde calhava e o passo 5 ficava sozinho na
 # última linha (a 360 e 390 px [[1, 2], [3, 4], [5]]; de 1024 a 1440 px e na moldura a 1024 px [[1, 2, 3, 4], [5]]). Em grelha:
 # um passo por linha abaixo de 600 px, mais juntos (entrelinha 1,2 e o número a 18 px, para a entrada a 390 px ficar abaixo dos
 # 2500 px), e três mais dois, em colunas, a partir de 600 px, como a linha dos passos no «Abre» das lições. Vem depois das regras
 # do li e do b, para a entrelinha e o número as vencerem
 '@media (max-width:599px){.ideias ol.passos-m{display:grid;grid-template-columns:max-content;row-gap:0}.ideias ol.passos-m li{line-height:1.2}.ideias ol.passos-m b{font-size:1.125rem}}'
 '@media (min-width:600px){.ideias ol.passos-m{display:grid;grid-template-columns:repeat(3,max-content);column-gap:16px}}'
 # região «A seguir» (sistema 6.3): a única preta; nunca anima
 '.ideias .proximo{background:var(--tinta);color:var(--papel);padding:16px 16px 18px;margin:0 0 20px}'
 '.ideias .proximo .kicker{font:700 .8125rem/1.2 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;margin:0 0 6px}'
 '.ideias .proximo .cab{display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 12px;margin:0 0 8px}'
 '.ideias .proximo .num{font:400 3.2rem/.9 "Bebas Neue","Arial Narrow",Arial,sans-serif;margin:0}'
 '.ideias .proximo h2{font:700 1.375rem/1.2 Arial,Helvetica,sans-serif;margin:0}'
 '.ideias .proximo .linha{font:1rem/1.45 Georgia,"Times New Roman",serif;margin:0 0 6px;max-width:30em}'
 '.ideias .proximo .papel,.ideias .proximo .feito{font-size:.9375rem;margin:0 0 14px;max-width:30em}'
 '.ideias .proximo .feito{font-weight:700}.ideias .proximo .feito:empty{display:none}'
 '.ideias .proximo .botao{display:inline-flex;align-items:center;min-height:48px;padding:0 18px;background:var(--papel);color:var(--tinta);font-weight:700;text-decoration:none;border:3px solid var(--papel)}'
 '.ideias .proximo .botao:focus-visible{outline-color:var(--papel)}'
 # 01/11/2026 (correção 2): abaixo de 400 px, a linha «No fim, em papel» passa para depois do botão. Com as pessoas
 # apresentadas (revisor de pt-PT), a linha da sessão 2 ganhou uma linha e, a 320 × 640 com progresso, «Continuar» saía do
 # primeiro ecrã (y = 612 a 660); assim fica a ação logo a seguir ao que se vai fazer, e nada se perde
 '@media (max-width:399px){.ideias .proximo{display:flex;flex-direction:column;align-items:flex-start}.ideias .proximo .papel{order:1;margin:14px 0 0}.ideias .proximo .papel:empty{display:none}}'
 # gesto de decisão (sistema 6.8): botões de contorno de 48 px, aria-pressed, resposta na mesma região
 '.ideias .gesto{background:var(--papel);padding:16px;margin:0 0 20px}'
 '.ideias .gesto .q{font:700 1.125rem/1.35 Georgia,"Times New Roman",serif;margin:0 0 12px}'
 # 01/11/2026 (correção 3, diretor de arte): a pergunta acabava em «os dias?» sozinho (a 320, 1366 e 1440 px e na projeção)
 '.ideias .gesto .q{text-wrap:balance}'
 # 31/10/2026 (revisão do diretor de arte): três colunas iguais, como a variante .gesto .opcoes.tres do sistema (nenhuma
 # opção sozinha numa linha)
 '.ideias .gesto .ops{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}'
 # 01/11/2026 (correção 2, diretor de arte): abaixo de 380 px, com 80 px por botão, os rótulos partiam-se palavra a palavra
 # («Não / faço / ideia»; premido, o visto sozinho na primeira linha): três botões numa coluna
 '@media (max-width:379px){.ideias .gesto .ops{grid-template-columns:minmax(0,1fr)}}'
 # 01/11/2026 (correção 6, diretor de arte): na projeção, de 380 a 469 px, os botões de 100 a 130 px partiam «Tenho um palpite» e
 # «Não faço ideia» palavra a palavra, em três linhas (premido, «✓ Tenho um palpite» ficava em três até 460 px): também numa
 # coluna. A partir de 470 px as etiquetas cabem em duas linhas, também premidas
 '@media (min-width:380px) and (max-width:469px){html.em-projecao .ideias .gesto .ops{grid-template-columns:minmax(0,1fr)}}'
 # 01/11/2026 (correção 4, diretor de arte): na projeção, entre 960 e 1099 px (o portátil ligado ao projetor), a coluna da
 # direita deixa 107 a 116 px por botão e «Tenho um palpite» partia-se em três linhas: os três botões numa coluna
 '@media (min-width:960px) and (max-width:1099px){html.em-projecao .ideias .gesto .ops{grid-template-columns:minmax(0,1fr)}}'
 # 01/11/2026 (correção 5, diretor de arte): no ecrã, a partir de 1080 px, a mesma coluna única: com três colunas de 141 px as
 # etiquetas partiam-se desiguais (a 1366 px, «Sei» numa linha, «Tenho um palpite» em duas, «Não faço ideia» numa) e a tabela
 # de museu ficava sozinha a meio de 132 a 159 px de vazio. Abaixo não, porque o pé da tabela desceria abaixo do da imagem: o
 # diretor propôs 1060 px com a margem de 16 px; com a de 24 px (acima), o pé descia 15 a 18 px de 1060 a 1071 px
 '@media (min-width:1080px){html:not(.em-projecao) .ideias .gesto .ops{grid-template-columns:minmax(0,1fr)}}'
 '.ideias .gesto button{min-height:48px;padding:6px 8px;border:2px solid var(--tinta);background:transparent;color:var(--tinta);font:700 1rem/1.15 Arial,Helvetica,sans-serif;text-align:center;cursor:pointer}'
 '.ideias .gesto button[aria-pressed="true"]{border-width:4px;padding:4px 6px}'
 '.ideias .gesto button[aria-pressed="true"]::before{content:"✓ "}'
 '.ideias .gesto .resposta{font:1rem/1.45 Georgia,"Times New Roman",serif;margin:12px 0 0;padding-left:10px;border-left:4px solid var(--tinta);max-width:32em}'
 '.ideias .gesto .resposta:empty{display:none}'
 '.ideias .gesto .sala{display:none;font-size:.9375rem;color:var(--suave);margin:10px 0 0}'
 'html.em-projecao .ideias .gesto .sala{display:block}'
 '@media (max-width:639px){.ideias .gesto.ja-feita{display:none}}'
 'html.em-projecao .ideias .gesto.ja-feita{display:block}'
 # imagem com a tabela de museu (sistema 6.4): cinzento em multiplicação sobre o campo
 '.ideias .atol{margin:0 0 24px}'
 '.ideias .atol .campo{display:block;background:var(--campo);aspect-ratio:1200/789;overflow:hidden}'
 '.ideias .atol img{display:block;width:100%;height:100%;object-fit:cover;filter:grayscale(1);mix-blend-mode:multiply}'
 '.ideias .atol figcaption{font:.8125rem/1.4 Arial,Helvetica,sans-serif;color:var(--suave);margin:8px 0 0}'
 '.ideias .atol figcaption a{overflow-wrap:anywhere}'
 # 01/11/2026 (correção 3): o número da fotografia não se parte no hífen (com a etiqueta de parede, partia em «ISS006- / E-37110»)
 '.ideias .atol figcaption .id{white-space:nowrap}'
 # as sessões em três portas (sistema 6.5): faixa de nós e linhas de 64 px com estado
 # 01/11/2026 (correção 3, medida da hierarquia, R1): o h2 «As sete sessões» (32 px) era mais pequeno do que os nomes das
 # portas que agrupa (h3, 38,4 px); passa a 44 px
 # 01/11/2026 (correção 4, diretor de arte): a 48 px (3 rem), 1,25 vezes os 38,4 px dos nomes das portas; a 44 px, os três
 # níveis em Bebas (44, 38,4 e 35,2 px) quase se confundiam (relações de 1,15 e 1,09)
 '.ideias h2.sessoes-t{font:400 3rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;margin:40px 0 8px}'
 '.ideias .faixa{display:grid;grid-template-columns:2fr 2fr 3fr;gap:6px;margin:0 0 20px}'
 # 31/10/2026 (revisão do diretor de arte): a faixa do sistema (6.6): transparente, nós em barra numa linha contínua e o
 # rótulo em Arial, para não repetir em cartaz o nome da porta que vem logo abaixo
 '.ideias .faixa a{display:flex;align-items:center;gap:3px;flex-wrap:wrap;min-height:56px;padding:10px 0 8px;background:none;text-decoration:none}'
 '.ideias .faixa .nome{font:700 .875rem/1.2 Arial,Helvetica,sans-serif;width:100%}'
 # 01/11/2026 (correção 2, diretor de arte): a partir de 1024 px a faixa fica por cima de cada porta, que repete o nome 82 px
 # abaixo; o rótulo fica só para o leitor de ecrã. Abaixo de 1024 px, a faixa vem numa linha à parte e o rótulo vê-se.
 '@media (min-width:1024px){.ideias .faixa .nome{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}'
 '.ideias .faixa .no{flex:1 1 0;width:auto;height:14px;border:1.5px solid var(--tinta)}'
 '.ideias .faixa .no.feita{background:var(--mostarda)}'
 '.ideias .faixa .no.seguir{border:3.5px solid var(--vermelho)}'
 '.ideias .faixa .no.prep{border-style:dashed}'
 '.ideias .porta{margin:0 0 24px;scroll-margin-top:16px}'
 '.ideias .porta h3{font:400 2.4rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;margin:0 0 4px}'
 # 01/11/2026 (correção 3, diretor de arte; sistema 3 e 6.4): abaixo de 640 px, as portas só com sessões em preparação dobram-se
 # numa banda de 88 px (nome em Bebas a 1,75 rem, uma linha e o botão + de 48 × 48) e abrem-se no sítio. Só com script
 # (html.cv, posto no <head>; sem script fica tudo aberto) e nunca na projeção. A 390 px, a entrada passa de 2912 para 2361 px.
 '.ideias .porta-linha,.ideias .porta-abre{display:none}'
 '@media (max-width:639px){html.cv .ideias .porta[data-dobra] .porta-cab{display:grid;grid-template-columns:minmax(0,1fr) 48px;grid-template-areas:"nome abre" "linha abre";column-gap:12px;align-items:center;min-height:88px;padding:10px 12px 10px 16px;background:var(--papel)}'
 'html.cv .ideias .porta[data-dobra] h3{grid-area:nome;align-self:end;font-size:1.75rem;margin:0}'
 'html.cv .ideias .porta[data-dobra] .porta-linha{display:block;grid-area:linha;align-self:start;margin:2px 0 0;font-size:.9375rem;line-height:1.3;color:var(--suave)}'
 'html.cv .ideias .porta[data-dobra] .porta-abre{display:inline-flex;align-items:center;justify-content:center;grid-area:abre;width:48px;height:48px;padding:0;border:2px solid var(--tinta);background:transparent;color:var(--tinta);font:700 1.625rem/1 Arial,Helvetica,sans-serif;cursor:pointer}'
 'html.cv .ideias .porta-abre::before{content:"+"}html.cv .ideias .porta-abre[aria-expanded="true"]::before{content:"\\2212"}'
 'html.cv .ideias .porta[data-dobra]:not(.aberta) .porta-corpo{display:none}html.cv .ideias .porta[data-dobra].aberta .porta-corpo{padding-top:10px}}'
 '.ideias .porta .apoio-porta{font:1rem/1.45 Georgia,"Times New Roman",serif;color:var(--suave);margin:0 0 10px;max-width:30em}'
 '.ideias ol.sessoes{list-style:none;margin:0;padding:0}'
 '.ideias ol.sessoes li{background:var(--papel);border-bottom:2px solid var(--fundo)}'
 '.ideias ol.sessoes .linha{display:grid;grid-template-columns:2.4rem minmax(0,1fr) auto;column-gap:12px;align-items:center;min-height:64px;padding:10px 12px;color:inherit;text-decoration:none}'
 '.ideias ol.sessoes a.linha::after{content:"→";grid-column:3;grid-row:1/span 2;align-self:center;font-weight:700}'
 '.ideias ol.sessoes .n{font:400 2.2rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;grid-row:1/span 2;align-self:center}'
 '.ideias ol.sessoes .tit{grid-column:2;line-height:1.25}'
 '.ideias ol.sessoes strong{font-size:1.0625rem}'
 '.ideias ol.sessoes .apoio{grid-column:2;color:var(--suave);font:.9375rem/1.4 Georgia,"Times New Roman",serif;margin-top:2px}'
 '.ideias li.seguir .linha{box-shadow:inset 4px 0 0 var(--vermelho)}'
 '.ideias li.prep .n,.ideias li.prep strong{color:var(--suave)}'
 '.ideias .estado{display:inline-flex;align-items:center;gap:6px;font-size:.8125rem;line-height:1;font-weight:700;text-transform:uppercase;letter-spacing:.06em;white-space:nowrap;margin-left:2px}'
 '.ideias .estado:empty{display:none}'
 '.ideias .estado::before{content:"";width:11px;height:11px;box-sizing:border-box;flex:none;border:1.5px solid currentColor}'
 '.ideias li.feita .estado::before{background:var(--mostarda);border-color:var(--tinta)}'
 '.ideias li.seguir .estado::before,.ideias li.comeca .estado::before{background:var(--vermelho);border-color:var(--vermelho)}'
 '.ideias li.prep .estado{color:var(--suave)}.ideias li.prep .estado::before{border-style:dashed}'
 # 31/10/2026 (revisão do diretor de arte): o estado vai sempre para a linha de baixo do título (antes, só abaixo de 500 px)
 '.ideias ol.sessoes .estado:not(:empty){display:flex;margin:4px 0 0}'
 # saídas e rodapé (sistema 6.10)
 '.ideias .saidas-sec{display:flex;flex-wrap:wrap;gap:4px 24px;margin:8px 0 32px}'
 '.ideias .saidas-sec a{display:inline-flex;align-items:center;min-height:44px;font-weight:700}'
 '.ideias .rodape{background:var(--papel);padding:16px;margin:0}'
 '.ideias .rodape h2{font:700 .8125rem/1.2 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;margin:0 0 10px}'
 '.ideias .saidas{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:0 0 12px}'
 # 31/10/2026 (revisão do diretor de arte): as saídas do sistema (6.10): caixas de 64 px com fundo, sem contorno
 '.ideias .saidas a{display:flex;align-items:center;min-height:64px;padding:10px 14px;border:0;background:var(--fundo);font-weight:700;text-decoration:none}'
 '.ideias .saidas a::after{content:"→";margin-left:auto;padding-left:8px}'
 '.ideias .rodape .nota{font-size:.875rem;color:var(--suave);margin:0}'
 '@media (min-width:900px){.ideias .saidas{grid-template-columns:repeat(4,minmax(0,1fr))}}'
 # 01/11/2026 (correção 3, diretor de arte): abaixo de 360 px, «Biblioteca:» empurrava a seta 2 px para fora da caixa
 '@media (max-width:359px){.ideias .saidas a{padding:10px 12px}.ideias .saidas a::after{padding-left:6px}}'
 # até 959 px, a linha de informação passa para cima da imagem, depois da região e do gesto: a primeira ação fica no primeiro
 # ecrã também a 320 × 640 (estava em y = 723)
 '@media (max-width:959px){.ideias .topo{display:flex;flex-direction:column}.ideias .topo .abre{display:contents}.ideias .topo .abre>*{order:1}'
 '.ideias .topo .proximo{order:2}.ideias .topo .gesto{order:3}.ideias .topo .abre>.metodo{order:4;margin:0 0 12px}.ideias .topo .atol{order:5}}'
 # a partir de 960 px (sistema 3): 7/12 para a abertura e a imagem, 5/12 para a região «A seguir» e o gesto
 # 31/10/2026 (revisão do diretor de arte): o gesto fica 20 px abaixo da região «A seguir» (proximidade), e não na linha da
 # imagem, 90 px abaixo
 # 01/11/2026 (correção 3, diretor de arte): a tabela de museu passa a etiqueta de parede, na coluna da direita, alinhada ao pé
 # da imagem (deixava 319 px de vazio à direita a 1366 px e corria a 109 carateres por linha); no DOM continua no <figure>
 '@media (min-width:960px){.ideias .topo{display:grid;grid-template-columns:7fr 5fr;column-gap:40px;grid-template-areas:"abre proximo" "abre gesto" "atol gesto" "atol cap";grid-template-rows:auto auto 1fr auto;align-items:start}'
 '.ideias .topo .abre{grid-area:abre}.ideias .topo .proximo{grid-area:proximo;margin-top:8px}.ideias .topo .gesto{grid-area:gesto;align-self:start}'
 '.ideias .topo .atol{display:contents}.ideias .topo .atol .campo{grid-area:atol}.ideias .topo .atol figcaption{grid-area:cap;align-self:end;margin:0}'
 '.ideias .abre .lead{font-size:1.3125rem}'
 # a imagem baixa para 16:9, para a coluna da esquerda não ficar muito mais alta do que a da direita
 # 01/11/2026 (correção 8, diretor de arte): o enquadramento escolhe-se à mão, pelo anel, e não pelo tamanho da caixa. Com
 # 50% 55%, a curva de baixo do anel saía 8 a 14 px pelo pé a 16:9 e, com o gesto premido (a imagem estica até 0,97:1), a ponta
 # nordeste saía até 47 px pela borda direita. Com 75% 83%, o anel (na fonte de 1200 × 789: x 368 a 1042, y 107 a 757) fica
 # inteiro de 0,90:1 a 16:9: 12 px de folga da fonte em cima e em baixo a 16:9, 42 e 49 px dos lados a 0,97:1
 '.ideias .atol .campo{aspect-ratio:16/9}.ideias .atol img{object-position:75% 83%}}'
 # 01/11/2026 (correção 7, diretor de arte): quando a coluna da direita é mais alta do que a abertura com a imagem a 16:9 (na
 # projeção de 1100 a 1239 px, na moldura /projetar/ a 1440 × 900 e 1400 × 1050, no ecrã com a sessão 1 feita de 1080 a 1199 px),
 # a tabela de museu descia até 81 px abaixo do pé da imagem e agrupava-se com o gesto. A imagem estica até ao pé da tabela e nunca
 # fica abaixo de 16:9 (o ::before guarda a altura mínima, a imagem enche o recorte): o pé da tabela fica no pé da imagem
 '@media (min-width:960px){.ideias .topo .atol .campo{position:relative;aspect-ratio:auto;align-self:stretch}.ideias .topo .atol .campo::before{content:"";display:block;padding-top:56.25%}.ideias .topo .atol img{position:absolute;inset:0}}'
 # 01/11/2026 (correção 6, diretor de arte): na projeção, de 960 a 1099 px (o portátil ligado ao projetor; a moldura a 1280 × 800
 # e 1366 × 768), a coluna da direita cresce com o gesto numa coluna e a tabela de museu descolava-se da imagem: ficava 20 px abaixo
 # do gesto, toda abaixo do pé da imagem, e lia-se como parte do gesto. Aqui a tabela volta para debaixo da imagem, 8 px abaixo e
 # alinhada à sua margem; o gesto ocupa a coluna da direita até ao fim. No ecrã e na projeção a partir de 1100 px não muda
 '@media (min-width:960px) and (max-width:1099px){html.em-projecao .ideias .topo{grid-template-areas:"abre proximo" "abre gesto" "atol gesto" "cap gesto";grid-template-rows:auto auto auto 1fr}'
 'html.em-projecao .ideias .topo .atol figcaption{align-self:start;margin:8px 0 0}}'
 # a faixa alinha pelas três colunas das portas (continuidade): cada grupo de nós por cima da sua porta
 '@media (min-width:1024px){.ideias .portas{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}.ideias .faixa{grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}}'
 # 31/10/2026 (revisão do diretor de arte): na projeção a letra cresce na raiz, para os tamanhos em rem crescerem também
 # (letra mínima de 13 para 17,9 px, sistema 8); o botão Projetar some; na moldura /projetar/, as migalhas a 17,9 px
 'html.em-projecao{font-size:137.5%}html.em-projecao body.ideias{font-size:1rem}html.em-projecao .epi-projection-launcher{display:none!important}'
 'html.epi-projection .ideias .migalhas{font-size:.8125rem!important}'
 # 01/11/2026 (correção 5, diretor de arte): na projeção abaixo de 600 px, «As sete sessões» (66 px) partia-se e deixava
 # «sessões» sozinha; os títulos a 55 e 44 px (a mesma relação de 1,25 entre o h2 e os nomes das portas). Na faixa, o rótulo
 # «Treinar» enchia a coluna e ficava a 6 px de «Criar»: os rótulos ficam só para o leitor de ecrã, como a partir de 1024 px
 # (os nomes das portas vêm logo abaixo), e as colunas com mínimo 0, para a proporção 2:2:3 dos nós não se perder
 '@media (max-width:599px){html.em-projecao .ideias h2.sessoes-t{font-size:2.5rem}html.em-projecao .ideias .porta h3{font-size:2rem}'
 'html.em-projecao .ideias .faixa{grid-template-columns:minmax(0,2fr) minmax(0,2fr) minmax(0,3fr)}'
 'html.em-projecao .ideias .faixa .nome{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}'
 '@media (prefers-reduced-motion:reduce){.ideias *{animation:none!important;transition:none!important}}'
 # guião e guia do docente: páginas de papel (A4), as mesmas peças
 # 01/11/2026 (correção 2, diretor de arte): 2 px de traço, como os outros botões de contorno (semelhança)
 '.ideias .imprimir{font:700 1rem Arial,Helvetica,sans-serif;background:var(--papel);color:var(--tinta);border:2px solid var(--tinta);padding:9px 15px;min-height:48px;cursor:pointer}'
 '.ideias .papel-cab{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin:0 0 20px}'
 '.ideias .papel-cab .pq{font-size:.875rem;color:var(--suave)}'
 '.ideias section.lado{background:var(--papel);padding:18px 16px 20px;margin:0 0 20px;max-width:860px}'
 '.ideias .lado h2{font:700 1.375rem/1.15 Arial,Helvetica,sans-serif;margin:0 0 8px}'
 '.ideias .lado h3{font:700 1rem/1.25 Arial,Helvetica,sans-serif;margin:16px 0 6px;padding:0 0 4px;border-bottom:1px solid var(--tinta)}'
 '.ideias .lado p{margin:0 0 8px}.ideias .lado p.campo{text-align:start;line-height:1.9}'
 '.ideias .nome{display:flex;gap:8px;align-items:flex-end;font:700 .8125rem/1.2 Arial,Helvetica,sans-serif;letter-spacing:.06em;text-transform:uppercase;margin:6px 0 12px}'
 '.ideias .nome i{flex:1;border-bottom:1px solid var(--tinta);height:1.2rem}'
 # 01/11/2026 (correção 3, medida da hierarquia, R2): «Nome e turma» é o rótulo de um campo, como «Lugar:» e «Grupo:», e não um
 # antetítulo; em maiúsculas espaçadas competia com o título que vem logo a seguir (13 px contra 16 px)
 '.ideias .lado p.nome{font-size:.875rem;letter-spacing:0;text-transform:none}'
 '.ideias i.b{display:inline-block;min-width:3.5em;border-bottom:1px solid var(--tinta);height:1.1em;vertical-align:baseline}'
 '.ideias i.b.l{display:block;width:100%;margin-top:4px}'
 '.ideias .escrever{border-bottom:1px solid var(--suave);height:1.9em}'
 '.ideias .lado .nota-p{font-size:.875rem;color:var(--suave)}'
 '.ideias table{border-collapse:collapse;width:100%;background:var(--papel);margin:8px 0 10px;table-layout:fixed}'
 '.ideias th,.ideias td{border:1px solid var(--tinta);padding:6px 8px;text-align:left;vertical-align:top;overflow-wrap:break-word}'
 '.ideias table.grelha-escrever td{height:2.1em}'
 '.ideias table.grelha-escrever th{font:700 .8125rem/1.25 Arial,Helvetica,sans-serif}'
 '.ideias .tabela{overflow-x:auto;max-width:100%}'
 # 31/10/2026 (revisão do diretor de arte): 6,5 rem, para «120 a 145» caber na coluna sem passar por cima da borda
 '.ideias td.num,.ideias th.num{text-align:right;white-space:nowrap;width:6.5rem}'
 # o n.º da sessão, no quadro da sequência, só tem um algarismo: coluna estreita, para a tabela de seis colunas caber melhor
 '.ideias table.seq td.num,.ideias table.seq th.num{width:3.5rem}'
 # 01/11/2026 (correção 3, diretor de arte, bloqueante): abaixo de 640 px o quadro da sequência deslizava para o lado dentro da
 # caixa (183 px escondidos a 320, a coluna «Estado» invisível). Passa a uma ficha por sessão: «Sessão N: título» em cabeça e,
 # por baixo, cada campo com o nome da coluna (data-r); os papéis ARIA guardam a tabela para o leitor de ecrã, que não ouve o
 # rótulo duas vezes (texto alternativo vazio no content, onde o navegador o aceita)
 '@media (max-width:639px){.ideias table.seq,.ideias table.seq tbody,.ideias table.seq tr,.ideias table.seq td{display:block;width:auto}'
 '.ideias table.seq thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}'
 '.ideias table.seq tr{border:1px solid var(--tinta);margin:0 0 8px;padding:8px 10px}.ideias table.seq td{border:0;padding:2px 0}'
 '.ideias table.seq td::before{content:attr(data-r) ": ";content:attr(data-r) ": "/"";font-weight:700}'
 '.ideias table.seq td.num,.ideias table.seq td.num+td{display:inline;font:700 1.0625rem/1.3 Arial,Helvetica,sans-serif;text-align:left;width:auto;padding:0}'
 '.ideias table.seq td.num::before{content:"Sessão ";content:"Sessão "/""}.ideias table.seq td.num+td::before{content:": ";content:": "/""}'
 '.ideias table.seq td:nth-child(3){margin-top:4px}}'
 '.ideias .guia section.sessao,.ideias.guia section.sessao{border-top:3px solid var(--tinta);margin-top:36px;padding-top:4px;max-width:860px}'
 '.ideias.guia section.sessao>h2{font:400 2.2rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;margin:16px 0 6px}'
 '.ideias.guia h3{font:700 1.0625rem/1.3 Arial,Helvetica,sans-serif;margin:22px 0 6px}'
 '.ideias.guia .pg,.ideias.guia section li{font-family:Georgia,"Times New Roman",serif;max-width:32em}'
 '.ideias.guia .pg{margin:0 0 10px}'
 # texto corrido do guia justificado e hifenizado, com o limiar da casa (à esquerda abaixo de 360 px: --epi-texto-corrido)
 # 01/11/2026 (correção 2, diretor de arte): só o texto corrido; as listas e a frase de abertura ficam à esquerda (são itens e
 # texto de cartaz: justificadas, abriam espaços até 12,4 vezes o normal a 360 px), e as listas ganham 21 px de medida
 '.ideias.guia .pg:not(.fontes){text-align:var(--epi-texto-corrido,justify);hyphens:auto;-webkit-hyphens:auto}'
 '.ideias.guia section ul{padding-left:1.2em}'
 # 31/10/2026 (revisão do diretor de arte): sem inline-flex, que partia em colunas as ligações com <i> e, a 320 px, fazia a
 # página deslizar 16 px
 # 01/11/2026 (correção 4, diretor de arte): em bloco e não em inline-block, que alinhava a marca da lista pela última linha das
 # ligações com duas ou três linhas; as alturas e os 44 px de alvo não mudam
 '.ideias.guia ul.ligacoes a{display:block;min-height:44px;padding:9px 0}'
 '.ideias.guia .caixa{background:var(--papel);border:2px solid var(--tinta);padding:4px 16px;margin:12px 0;max-width:34em}'
 '.ideias.guia .indicativa{font-weight:700;border-left:6px solid var(--tinta);padding-left:10px;max-width:34em}'
 '.ideias.guia .botao-s{display:inline-flex;align-items:center;min-height:48px;padding:0 14px;border:2px solid var(--tinta);font-weight:700;text-decoration:none;margin:0 8px 8px 0}'
 # 01/11/2026 (correção 4, diretor de arte): abaixo de 480 px, os três botões de cada sessão numa coluna, à largura do texto
 # («O guião» ficava sozinho numa segunda fila a 320, 360 e 390 px)
 '@media (max-width:479px){.ideias.guia .acoes-s{display:grid;grid-template-columns:minmax(0,1fr);gap:8px}.ideias.guia .acoes-s a.botao-s{margin:0}}'
 # 01/11/2026 (correção 4, diretor de arte): os rótulos a negro do texto corrido não se partem («O / passo.»)
 '.ideias.guia .pg b{white-space:nowrap}'
 '.ideias.guia ul.indice{padding-left:1.2em}.ideias.guia ul.indice a{display:inline-block;padding:10px 0}'
 '.ideias.guia .fontes{font-size:.875rem;color:var(--suave);overflow-wrap:anywhere}'
 '.ideias.guia .tabela{max-width:52em}'
 # 01/11/2026 (método): os cinco passos à cabeça do guia, numa lista numerada com a medida do texto
 '.ideias.guia ol.passos-g{font-family:Georgia,"Times New Roman",serif;max-width:32em;padding-left:1.4em;margin:4px 0 12px}.ideias.guia ol.passos-g li{margin:0 0 4px}'
 # 01/11/2026 (método): no guião, o passo do método logo abaixo do título de cada sessão
 '.ideias .lado p.passo-g{font:700 .9375rem/1.3 Arial,Helvetica,sans-serif;margin:-2px 0 6px}'
 # 01/11/2026 (correção 2, diretor de arte): duas margens direitas no mesmo fio, a do texto (32em, 544 px) e a das tabelas e
 # dos filetes; a caixa «Na aula», a nota da avaliação e as listas acabam onde acaba o texto
 '.ideias.guia .caixa,.ideias.guia .indicativa,.ideias.guia section ul{max-width:32em}.ideias.guia section li{max-width:none}'
 # e, a partir de 1100 px, o índice numa coluna à direita, sempre à vista durante a aula (ocupa o vazio de 308 px)
 '@media (min-width:1100px){.ideias.guia main{display:grid;grid-template-columns:minmax(0,860px) minmax(180px,1fr);column-gap:40px;align-items:start}'
 '.ideias.guia main>*{grid-column:1}.ideias.guia main>.migalhas{grid-column:1/-1}'
 '.ideias.guia main>nav.indice-nav{grid-column:2;grid-row:2/span 40;position:sticky;top:24px;align-self:start;padding-top:12px}'
 '.ideias.guia nav.indice-nav ul.indice{list-style:none;margin:0;padding:8px 0 0;border-top:3px solid var(--tinta);font-size:.9375rem}'
 '.ideias.guia nav.indice-nav ul.indice a{padding:12px 0;min-height:44px;box-sizing:border-box}}'
 # 01/11/2026 (correção 2, diretor de arte): uma forma verbal com pronome não se parte no hífen (AO90, base XX)
 '.ideias .nq{white-space:nowrap}'
 '@media (max-width:599px){.ideias .tabela table{font-size:.875rem}.ideias th,.ideias td{padding:5px 6px;hyphens:auto}}'
 # 31/10/2026 (revisão do diretor de arte): no telemóvel, nenhum cabeçalho partido a meio da palavra («Maupassa / nt») e
 # nenhum rótulo com a última palavra sozinha
 '.ideias .lado .rotulo{text-wrap:balance}'
 '@media (max-width:599px){.ideias table{table-layout:auto}.ideias th,.ideias td{overflow-wrap:normal}}'
 '@page{size:A4;margin:10mm 12mm}'
 '@media print{.ideias .migalhas,.ideias .imprimir,.ideias .papel-cab,.ideias .saidas-sec,[data-appearance-control],.epi-projection-launcher{display:none!important}'
 'body.ideias{background:#fff;color:#000;font-size:10.5pt;line-height:1.35}.ideias main{max-width:none;padding:0}'
 '.ideias section.lado{padding:0;margin:0;max-width:none;break-after:page}.ideias section.lado:last-of-type{break-after:auto}'
 '.ideias table,.ideias .caixa,.ideias li{break-inside:avoid}.ideias .lado h3,.ideias.guia h3{break-after:avoid}'
 '.ideias.guia section.sessao{max-width:none}.ideias.guia .botao-s{display:none}'
 # 31/10/2026 (revisão do diretor de arte): no guia, só as sessões prontas abrem página (de 9 para 8 páginas); no guião, sem
 # o cabeçalho de ecrã, e linhas de escrita de 9,5 mm (continuam 4 páginas)
 '.ideias.guia section.sessao.pronta{break-before:page}'
 '.ideias.guiao .abre{display:none}.ideias .escrever{height:9.5mm}.ideias table.grelha-escrever td{height:9.5mm}'
 # 01/11/2026 (correção 2, diretor de arte): o título de secção nunca fica sozinho no fundo da página («A sequência» abre
 # página); o índice de ligações não serve em papel; o texto corrido com 120 mm de medida (72 carateres medidos; com os 128 mm propostos eram 76 a 80; eram 97
 # a 114 a toda a largura); a caixa e a nota da avaliação acabam no mesmo fio, as tabelas e os filetes a toda a largura
 '.ideias.guia section.sessao>h2{break-after:avoid}.ideias.guia #sequencia{break-before:page}.ideias.guia ul.indice{display:none}'
 # 01/11/2026 (método): o guia abre com «Porque seguimos um método», na primeira página com o cabeçalho; «Antes de começar» abre
 # página, para não se partir entre duas (o guia passa de 8 para 9 páginas A4)
 '.ideias.guia #antes{break-before:page}'
 '.ideias.guia .pg,.ideias.guia section ul,.ideias.guia .caixa,.ideias.guia .indicativa{max-width:120mm}.ideias.guia section li{max-width:none}'
 # 01/11/2026 (correção 2): em papel, as ligações sem os 44 px de alvo de toque (com eles, as «Fontes da lição» da sessão 1
 # passavam duas linhas para uma página quase vazia),
 # e os títulos de grupo mais perto do texto (de 22 para 14 px por cima), para cada sessão caber nas suas três páginas
 '.ideias.guia ul.ligacoes a{min-height:0;padding:0}.ideias.guia h3{margin:14px 0 4px}.ideias.guia .pg{margin:0 0 6px}.ideias.guia section ul{margin:4px 0 6px}}')


def migalhas(base, itens):
    out = '<nav class="migalhas" aria-label="Onde estás">'
    for k, (rot, href) in enumerate(itens):
        if k:
            out += '<span class="sep" aria-hidden="true">›</span>'
        out += f'<a href="{e(href)}">{rot}</a>' if href else f'<span aria-current="page">{rot}</span>'
    return out + '<span data-appearance-control></span></nav>'


def cabeca(base, titulo, desc, robots=True):
    return ('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(titulo)}</title>' + ('<meta name="robots" content="noindex, nofollow">' if robots else '')
            + f'<meta name="description" content="{e(desc)}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style><link rel="stylesheet" href="{base}assets/appearance.css"><script src="{base}assets/appearance.js"></script></head>')


def passo_n(s):
    """01/11/2026 (método): o passo da sessão só com o número, para o rótulo da região «A seguir» («passo 1 de 5», «passos 1 e
    2 de 5», «os cinco passos»); a forma longa, com o que a sessão faz nesse passo, fica na lista, no guião e no guia."""
    t = s['passo'].split(':')[0]
    # 01/11/2026 (correção 1 do método, diretor de arte): inseparável (espaços duros), como «sessão N» no botão: o rótulo partia
    # dentro do passo e deixava um pedaço sozinho («… passos 1» / «e 2 de 5» a 390 px; «Começa aqui: passo» / «1 de 5» na projeção a
    # 320 px). Serve o data-passo, o rótulo inicial e a sessão em preparação no script
    return (t[0].lower() + t[1:]).replace(' ', '\u00a0')


def pergunta_abre(d):
    return re.search(r'<p class="pergunta-c">(.*?)</p>', d['cartoes'][0]['html']).group(1)


def pagina_entrada(L):
    base = '../../'
    prontas = [s for s in SESSOES if s['n'] in L]
    s1 = SESSOES[0]
    portas = ''
    faixa = ''
    for pid, nome, apoio, _url in PORTAS:
        ss = [s for s in SESSOES if s['porta'] == pid]
        nums = ', '.join(str(s['n']) for s in ss[:-1]) + ' e ' + str(ss[-1]['n'])
        faixa += (f'<a href="#porta-{pid}"><span class="nome">{nome}</span>'
                  + ''.join(f'<span class="no{"" if s["n"] in L else " prep"}" data-no="{s["n"]}" aria-hidden="true"></span>' for s in ss)
                  + f'<span class="c-sr">: sessões {nums}</span></a>')
        linhas = ''
        for s in ss:
            rota, peca, _u = s['peca']
            apoio_l = f'{e(s["passo"])}. Leva à peça <i>{e(peca)}</i>.'
            if s['n'] in L:
                d = L[s['n']]
                linhas += (f'<li data-chave="{e(d["chave"])}" data-versao="{e(d["versao"])}" data-n="{s["n"]}" data-titulo="{e(s["titulo"])}" '
                           f'data-passo="{e(passo_n(s))}" data-linha="{e(s["linha"])}" data-papel="{e(s["papel"])}" data-href="sessao-{s["n"]:02d}/">'
                           f'<a class="linha" href="sessao-{s["n"]:02d}/"><span class="n" aria-hidden="true">{s["n"]}</span>'
                           f'<span class="tit"><strong><span class="c-sr">Sessão {s["n"]}: </span>{e(s["titulo"])}</strong> <span class="estado" data-estado></span></span>'
                           f'<span class="apoio">{apoio_l}</span></a></li>')
            else:
                linhas += (f'<li class="prep" data-n="{s["n"]}" data-titulo="{e(s["titulo"])}"><div class="linha"><span class="n" aria-hidden="true">{s["n"]}</span>'
                           f'<span class="tit"><strong><span class="c-sr">Sessão {s["n"]}: </span>{e(s["titulo"])}</strong> <span class="estado">Em preparação</span></span>'
                           f'<span class="apoio">{apoio_l}</span></div></li>')
        # 01/11/2026 (correção 3, diretor de arte): uma porta sem nenhuma sessão pronta dobra-se no telemóvel (CSS e script abaixo)
        dobra = all(s['n'] not in L for s in ss)
        cab = f'<h3 id="pt-{pid}">{nome}</h3>'
        if dobra:
            nn = [s['n'] for s in ss]
            quais = f'Sessão {nn[0]}' if len(nn) == 1 else (f'Sessões {nn[0]} e {nn[1]}' if len(nn) == 2 else f'Sessões {nn[0]} a {nn[-1]}')
            cab += (f'<p class="porta-linha">{quais}, em preparação</p><button type="button" class="porta-abre" data-nome="{nome}" '
                    f'aria-expanded="false" aria-controls="pc-{pid}" aria-label="Abrir {nome}"></button>')
        portas += (f'<section class="porta" id="porta-{pid}" aria-labelledby="pt-{pid}"{" data-dobra" if dobra else ""}><div class="porta-cab">{cab}</div>'
                   f'<div class="porta-corpo" id="pc-{pid}"><p class="apoio-porta">{e(apoio)}</p><ol class="sessoes">{linhas}</ol></div></section>')
    proxima_prep = next((s for s in SESSOES if s['n'] not in L), None)
    js = ('(function(){"use strict";var proj=/[?&]projetar=1(&|$)/.test(location.search)||window.self!==window.top;'
          'if(proj)document.documentElement.classList.add("em-projecao");'
          'var dd=function(n){return(n<10?"0":"")+n};'
          'var L=[].slice.call(document.querySelectorAll("ol.sessoes li[data-chave]")),feitas=[],prox=null;'
          'L.forEach(function(li){var st=null;if(!proj){try{st=JSON.parse(localStorage.getItem(li.getAttribute("data-chave"))||"null")}catch(x){st=null}}'
          'var ok=!!(st&&st.lida&&st.versao===li.getAttribute("data-versao"));var el=li.querySelector("[data-estado]");'
          'var no=document.querySelector("[data-no=\\""+li.getAttribute("data-n")+"\\"]");'
          'if(ok){var d=typeof st.t==="number"?new Date(st.t):null,data=d&&!isNaN(d)?dd(d.getDate())+"/"+dd(d.getMonth()+1):"";'
          'feitas.push({li:li,data:data});li.classList.add("feita");el.textContent="Feita"+(data?" "+data:"");if(no)no.classList.add("feita")}'
          'else if(!prox){prox=li;li.classList.add("seguir");el.textContent="A seguir";if(no)no.classList.add("seguir")}});'
          # a região «A seguir»: «Continuar» na sessão a seguir à última feita; com as prontas todas feitas, a próxima em preparação
          'var R=document.querySelector("[data-proximo]");'
          'if(R&&feitas.length){var q=function(s){return R.querySelector(s)},u=feitas[feitas.length-1];'
          'q("[data-p-feito]").textContent="Feita: sessão "+u.li.getAttribute("data-n")+(u.data?", "+u.data:"")+".";'
          'if(prox){q("[data-p-k]").textContent="Continuar";q("[data-p-n]").textContent=q("[data-p-srn]").textContent=prox.getAttribute("data-n");q("[data-p-t]").textContent=prox.getAttribute("data-titulo");'
          'q("[data-p-passo]").textContent=": "+prox.getAttribute("data-passo");q("[data-p-linha]").textContent=prox.getAttribute("data-linha");q("[data-p-papel]").textContent="No fim, em papel: "+prox.getAttribute("data-papel");'
          # 01/11/2026 (correção 6, diretor de arte): «sessão N» inseparável no botão (na projeção a 320 px partia-se em «Começar a
          # sessão» / «1 →»; agora «Começar a» / «sessão 1 →»), no «Começar», no «Continuar» e no «Rever»
          'var b=q("[data-p-botao]");b.href=prox.getAttribute("data-href");b.textContent="Continuar na sessão\\u00a0"+prox.getAttribute("data-n")+"\\u00a0→"}'
          + (f'else{{q("[data-p-k]").textContent="A seguir, em preparação";q("[data-p-n]").textContent=q("[data-p-srn]").textContent="{proxima_prep["n"]}";q("[data-p-t]").textContent="{proxima_prep["titulo"]}";q("[data-p-passo]").textContent=": {passo_n(proxima_prep)}";'
             'q("[data-p-linha]").textContent="As sessões prontas estão feitas. A próxima ainda está a ser preparada.";q("[data-p-papel]").textContent="";'
             'var b2=q("[data-p-botao]");b2.href=u.li.getAttribute("data-href");b2.textContent="Rever a sessão\\u00a0"+u.li.getAttribute("data-n")+"\\u00a0→"}'
             if proxima_prep else 'else{q("[data-p-k]").textContent="Feitas";}')
          + '}'
          # o gesto: não grava nada; um segundo toque desfaz; a sessão 1 ganha «Começa aqui»
          'var G=document.querySelector("[data-gesto]");if(G){if(feitas.length&&!proj)G.classList.add("ja-feita");'
          'var res=G.querySelector("[data-resposta]"),bs=[].slice.call(G.querySelectorAll("button[data-op]")),l1=document.querySelector("li[data-n=\\"1\\"][data-chave]");'
          'bs.forEach(function(b){b.addEventListener("click",function(){var on=b.getAttribute("aria-pressed")==="true";'
          'bs.forEach(function(o){o.setAttribute("aria-pressed","false")});'
          'if(on){res.textContent="";if(l1&&!l1.classList.contains("feita")){l1.classList.remove("comeca");if(l1.classList.contains("seguir"))l1.querySelector("[data-estado]").textContent="A seguir"}return}'
          'b.setAttribute("aria-pressed","true");res.innerHTML=G.querySelector("template[data-resposta-html]").innerHTML;'
          # 31/10/2026 (revisão do diretor de arte, sistema 6.8): a página rola o necessário para a resposta ficar à vista
          'var rr=res.getBoundingClientRect();if(rr.bottom>innerHeight)scrollBy({top:rr.bottom-innerHeight+16,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});'
          'if(l1&&!l1.classList.contains("feita")){l1.classList.add("comeca");l1.querySelector("[data-estado]").textContent="Começa aqui"}})})}'
          # 01/11/2026 (correção 3): as portas dobradas (abaixo de 640 px, com html.cv) abrem e fecham no sítio; a faixa abre a sua
          'var abre=function(s,on){s.classList.toggle("aberta",on);var bt=s.querySelector(".porta-abre");bt.setAttribute("aria-expanded",on?"true":"false");bt.setAttribute("aria-label",(on?"Fechar ":"Abrir ")+bt.getAttribute("data-nome"))};'
          '[].slice.call(document.querySelectorAll(".porta[data-dobra]")).forEach(function(s){s.querySelector(".porta-abre").addEventListener("click",function(){abre(s,!s.classList.contains("aberta"))});'
          'var a=document.querySelector(".faixa a[href=\\"#"+s.id+"\\"]");if(a)a.addEventListener("click",function(){abre(s,true)});if(location.hash==="#"+s.id)abre(s,true)});'
          '})();')
    d1 = L[1]
    corpo = (migalhas(base, [('Lente', LENTE), ('Laboratório', '../'), ('Ideias', '')])
             + '<div class="topo">'
             '<header class="abre"><p class="rotulo">Laboratório, piloto</p><h1>Ideias</h1><p class="sub">Como nasce uma ideia</p>'
             '<p class="lead">Uma ideia é a parte que se vê de um trabalho que não se vê. Em sete sessões, levas uma ideia tua por um método de cinco passos.</p>'
             # 01/11/2026 (método): o bloco «O método», logo abaixo do título, no lugar da linha de informação (que dizia o livro
             # de Young e as sete sessões de 180 minutos): quem é Young, o livro, que as sessões o seguem passo a passo, que há
             # outros métodos e porque seguimos este, e os cinco passos numa lista numerada. O parágrafo guarda a classe «info»
             # (a medida de 34 em). No telemóvel vem depois do gesto, como vinha a linha de informação: a região «A seguir» e o
             # gesto continuam no primeiro ecrã, e a frase de abertura e a região já dizem o método e o passo de hoje
             '<section class="metodo" aria-labelledby="metodo-t"><h2 id="metodo-t">O método</h2>'
             '<p class="info">Seguimos, passo a passo, o método de James Webb Young, publicitário norte-americano, em <i>A Technique for Producing Ideas</i> (1940), um livro de poucas páginas. Há outros métodos; escolhemos este por ser simples, claro e útil.</p>'
             '<ol class="passos-m">' + ''.join(f'<li><b>{n}</b> {t}</li>' for n, t in enumerate(PASSOS, 1)) + '</ol></section></header>'
             '<section class="proximo inverso" aria-labelledby="prox-t" data-proximo>'
             # 01/11/2026 (método): o passo do método na linha do rótulo («Começa aqui: passo 1 de 5»), sem linha nova: a 390 px
             # cabe na mesma linha e a entrada fica abaixo dos 2500 px; a 320 px parte em duas e a primeira ação continua no
             # primeiro ecrã. O nome do passo está na linha da sessão, mais abaixo, e no bloco «O método»
             f'<p class="kicker"><span data-p-k>Começa aqui</span><span data-p-passo>: {e(passo_n(s1))}</span></p>'
             f'<div class="cab"><p class="num" data-p-n aria-hidden="true">{s1["n"]}</p><h2 id="prox-t"><span class="c-sr">Sessão <span data-p-srn>{s1["n"]}</span>: </span><span data-p-t>{e(s1["titulo"])}</span></h2></div>'
             f'<p class="linha" data-p-linha>{e(s1["linha"])}</p><p class="papel" data-p-papel>No fim, em papel: {e(s1["papel"])}</p><p class="feito" data-p-feito></p>'
             f'<a class="botao" data-p-botao href="sessao-01/">Começar a sessão 1 →</a></section>'
             # 01/11/2026 (correção 2, diretor de arte): a resposta vem de um <template>, já com «subiu-lhe» numa <span class="nq">
             '<section class="gesto" aria-labelledby="gesto-q" data-gesto>'
             f'<p class="q" id="gesto-q">{pergunta_abre(d1)}</p>'
             '<div class="ops" role="group" aria-labelledby="gesto-q"><button type="button" data-op aria-pressed="false">Sei</button><button type="button" data-op aria-pressed="false">Tenho um palpite</button><button type="button" data-op aria-pressed="false">Não faço ideia</button></div>'
             '<p class="resposta" data-resposta role="status" aria-live="polite"></p>'
             '<template data-resposta-html>Watson, o amigo médico de Holmes, subiu-lhe a escada centenas de vezes e não sabia quantos degraus tinha. Holmes sabia: dezassete. Na sessão 1, contas os da escola.</template>'
             '<p class="sala">Na sala: cada um escreve o seu número antes de alguém dizer o dele.</p></section>'
             f'<figure class="atol"><span class="campo"><img src="{ATOL["src"]}" width="{ATOL["w"]}" height="{ATOL["h"]}" alt="{e(ATOL["alt"])}" loading="lazy"></span>'
             f'<figcaption>{ATOL["tabela"]}</figcaption></figure>'
             '</div>'
             '<h2 class="sessoes-t" id="sessoes">As sete sessões</h2>'
             f'<nav class="faixa" aria-label="As sete sessões, por porta do Laboratório">{faixa}</nav>'
             f'<div class="portas">{portas}</div>'
             '<p class="saidas-sec"><a href="guiao/">Em papel: o guião →</a><a href="docente/">Para o docente →</a></p>'
             '<footer class="rodape"><h2>Daqui também se vai</h2><nav class="saidas" aria-label="Daqui também se vai">'
             + ''.join(f'<a href="{u}">{n}</a>' for _p, n, _a, u in PORTAS)
             + f'<a href="../../biblioteca/{BIB_ID}/">Biblioteca: Young</a></nav>'
             '<p class="nota">Piloto em revisão, escondido dos motores de busca. O que fazes fica só neste aparelho.</p></footer>')
    corpo = LL.nq(corpo)  # 01/11/2026 (correção 2, diretor de arte): formas verbais com pronome sem quebra no hífen
    cv = ('<script>(function(){if(!(/[?&]projetar=1(&|$)/.test(location.search)||window.self!==window.top))'
          'document.documentElement.classList.add("cv")})();</script></head>')
    return (cabeca(base, 'Ideias | Laboratório | Lente', 'Ideias, como nasce uma ideia: sete sessões do Laboratório que seguem, passo a passo, o método de James Webb Young (piloto).').replace('</head>', cv, 1)
            + f'<body class="ideias"><a class="c-sr salta" href="#conteudo">Saltar para o conteúdo</a><main id="conteudo">{corpo}</main><script>{js}</script>'
            f'<script defer src="{base}assets/projection-launcher.js" data-site="lente"></script></body></html>\n')


def bloco_guiao(itens):
    out = ''
    for it_ in itens:
        k = it_[0]
        if k == 'p':
            out += f'<p class="campo">{it_[1]}</p>'
        elif k == 'h2':
            out += f'<h3>{e(it_[1])}</h3>'
        elif k == 'nota':
            out += f'<p class="nota-p">{e(it_[1])}</p>'
        elif k == 'linhas':
            out += '<div class="escrever"></div>' * it_[1]
        elif k == 'tabela':
            cab, n = it_[1], it_[2]
            out += ('<table class="grelha-escrever"><thead><tr>' + ''.join(f'<th scope="col">{e(c)}</th>' for c in cab) + '</tr></thead><tbody>'
                    + ('<tr>' + '<td></td>' * len(cab) + '</tr>') * n + '</tbody></table>')
        elif k == 'tabela-linhas':
            cab, linhas = it_[1], it_[2]
            out += ('<table class="grelha-escrever"><thead><tr>' + ''.join(f'<th scope="col">{e(c)}</th>' if c else '<td></td>' for c in cab) + '</tr></thead><tbody>'
                    + ''.join(f'<tr><th scope="row">{e(l)}</th>' + '<td></td>' * (len(cab) - 1) + '</tr>' for l in linhas) + '</tbody></table>')
    return out


def pagina_guiao(L):
    base = '../../../'
    lados = ''
    for s in SESSOES:
        if s['n'] not in L:
            continue
        g = GUIAO[s['n']]
        lados += (f'<section class="lado" aria-labelledby="g{s["n"]}f"><p class="rotulo">Lente, Ideias, guião. Sessão {s["n"]}, frente</p>'
                  f'<h2 id="g{s["n"]}f">Sessão {s["n"]}: {e(s["titulo"])}</h2>'
                  # 01/11/2026 (método): o cabeçalho de cada sessão diz o passo do método e o nome dele
                  f'<p class="passo-g">{e(s["passo"])}</p><p class="nome">Nome e turma <i></i></p>'
                  + bloco_guiao(g['frente']) + '</section>'
                  f'<section class="lado" aria-labelledby="g{s["n"]}v"><p class="rotulo">Sessão {s["n"]}, verso</p>'
                  f'<h2 id="g{s["n"]}v">{e(g["verso_titulo"])}</h2>' + bloco_guiao(g['verso']) + '</section>')
    n = len([s for s in SESSOES if s['n'] in L])
    # 01/11/2026 (correção 5, revisor de pt-PT): «escreve-se no guião impresso» e não «aqui», que no ecrã apontava para a página
    # web, onde não se escreve
    corpo = (migalhas(base, [('Lente', LENTE), ('Laboratório', '../../'), ('Ideias', '../'), ('Guião', '')])
             + '<header class="abre"><p class="rotulo">Ideias, piloto</p><h1>O guião</h1>'
             f'<p class="lead">Para imprimir em A4: frente e verso de cada sessão pronta ({2 * n} páginas). No telemóvel só se toca; escreve-se no guião impresso e onde cada um guarda o material.</p></header>'
             '<p class="papel-cab"><button type="button" class="imprimir" onclick="window.print()">Imprimir</button><span class="pq">As sessões 3 a 7 entram quando estiverem prontas.</span></p>'
             + lados
             + '<p class="saidas-sec"><a href="../">Voltar a Ideias</a><a href="../docente/">Para o docente →</a></p>')
    corpo = LL.nq(corpo)
    return (cabeca(base, 'Guião | Ideias | Laboratório | Lente', 'O guião em papel das sessões de Ideias, no Laboratório: frente e verso por sessão (piloto).')
            + f'<body class="ideias guiao"><a class="c-sr salta" href="#conteudo">Saltar para o conteúdo</a><main id="conteudo">{corpo}</main></body></html>\n')


def tabela_grelha(g):
    soma = sum(p for _, p in g['grelha'])
    assert soma == 20, (g['produto'], soma)
    linhas = ''.join(f'<tr><td>{e(c)}</td><td class="num">{p}</td></tr>' for c, p in g['grelha'])
    return (f'<div class="tabela"><table><caption class="c-sr">Grelha indicativa: {e(g["produto"])}</caption><thead><tr><th scope="col">Critério</th><th scope="col" class="num">Pontos</th></tr></thead>'
            f'<tbody>{linhas}</tbody><tfoot><tr><th scope="row">Total (indicativo)</th><td class="num">20</td></tr></tfoot></table></div>')


def video_de(d):
    for c in d['cartoes']:
        h = c.get('html') or ''
        m = re.search(r'data-yt="([^"]+)"', h)
        if m:
            # 31/10/2026: na lição, o rótulo do botão vem num só <span> (revisão do diretor de arte); no guia, sem esse invólucro
            botao = re.sub(r'^<span>(.*)</span>$', r'\1', re.search(r'data-yt-abrir>(.*?)</button>', h).group(1))
            return {'id': m.group(1), 'botao': botao.replace('Ver: ', '', 1),
                    'cred': re.search(r'<p class="yt-cred">(.*?)</p>', h).group(1).replace(' O vídeo só se liga ao YouTube quando tocas no botão.', ''),
                    'tarefa': re.search(r'<p class="pergunta-c">(.*?)</p>', h).group(1)}
    return None


# 01/11/2026 (método): a coluna diz «Passo» (o método já está apresentado à cabeça do guia), e não «Passo de Young»
SEQ_COLS = ['N.º', 'Sessão', 'Pergunta', 'Passo', 'Porta e peça', 'Estado']
# 01/11/2026 (método): «Porque seguimos um método», à cabeça do guia do docente. As sessões de cada passo vêm do quadro SESSOES
# (passo 1: sessões 1 a 3; passo 2: 3 e 4; passo 3: 4 e a semana até à 5; passo 4: 5; passo 5: 6; a 7 junta os cinco).
GUIA_METODO = [
 ('Juntar material', 'o específico, do problema concreto, e o geral, de toda a vida (sessões 1 a 3).'),
 ('Trabalhar o material', 'virar os factos de todos os lados e juntá-los, à procura de relações (sessões 3 e 4).'),
 ('Largar', 'esquecer o problema e fazer outra coisa (sessão 4 e a semana até à 5, de propósito).'),
 ('A ideia aparece', 'quando menos se espera, depois de largado o problema (sessão 5).'),
 ('Dar forma e pôr à prova', 'adaptar a ideia ao uso e levá-la a quem a pode criticar (sessão 6; a 7 junta os cinco passos).'),
]


def pagina_guia(L):
    base = '../../../'
    seq = ''
    for s in SESSOES:
        rota, peca, _u = s['peca']
        porta = next(n for p, n, _a, _u2 in PORTAS if p == s['porta'])
        estado = 'Pronta (piloto)' if s['n'] in L else 'Em preparação'
        # 01/11/2026 (correção 3): cada célula leva o nome da coluna (data-r), que a ficha mostra abaixo de 640 px
        cel = [(SEQ_COLS[0], str(s['n']), ' class="num"'), (SEQ_COLS[1], e(s['titulo']), ''), (SEQ_COLS[2], e(s['pergunta']), ''),
               (SEQ_COLS[3], e(s['passo']), ''), (SEQ_COLS[4], f'{porta}, «{e(rota)}», <i>{e(peca)}</i>', ''), (SEQ_COLS[5], estado, '')]
        seq += '<tr role="row">' + ''.join(f'<td role="cell"{c} data-r="{r}">{v}</td>' for r, v, c in cel) + '</tr>'
    indice = '<li><a href="#metodo">Porque seguimos um método</a></li><li><a href="#antes">Antes de começar</a></li><li><a href="#sequencia">A sequência</a></li>' + ''.join(
        f'<li><a href="#s{s["n"]}">Sessão {s["n"]}: {e(s["titulo"])}</a></li>' for s in SESSOES if s['n'] in L)
    corpo = (migalhas(base, [('Lente', LENTE), ('Laboratório', '../../'), ('Ideias', '../'), ('Guia do docente', '')])
             + '<header class="abre"><p class="rotulo">Ideias, piloto</p><h1>Guia do docente</h1>'
             '<p class="lead">As sessões prontas em pormenor (tempos, materiais, o que fica escrito e a grelha /20 indicativa) e, antes delas, o quadro das sete sessões.</p>'
             '<p class="info">Piloto escondido dos motores de busca, sem ligação a partir do mapa, das portas nem da entrada do Laboratório, até o docente o ver.</p></header>'
             f'<nav class="indice-nav" aria-label="Neste guia"><ul class="indice">{indice}</ul></nav>'
             # 01/11/2026 (método): o guia abre com a razão do método, como o apresentar na primeira aula e onde o nome volta
             '<section class="sessao" id="metodo"><h2>Porque seguimos um método</h2>'
             '<p class="pg">O percurso adota como espinha <i>A Technique for Producing Ideas</i> (1940), o livro de poucas páginas em que o publicitário norte-americano James Webb Young descreve como se chega a uma ideia. Não é o único método; escolhemo-lo por ser simples e claro, por fazer sentido e por ajudar de facto. O objetivo é que os alunos o aprendam aqui, passo a passo, e depois o usem por conta própria.</p>'
             '<ol class="passos-g">' + ''.join(f'<li><b>{n}</b>: {e(t)}</li>' for n, t in GUIA_METODO) + '</ol>'
             '<p class="pg"><b>Na primeira aula.</b> Cinco minutos, logo a seguir ao «Abre»: no cartão 2 da sessão 1, o docente escreve os cinco passos no quadro, numerados, marca o primeiro e lê a frase do livro que o cartão cita. Nas sessões seguintes, basta voltar a escrever os cinco e marcar o do dia: o primeiro cartão de cada sessão faz o mesmo.</p>'
             '<p class="pg"><b>Onde o nome volta.</b> Os cartões apresentam Young uma vez, na sessão 1, e voltam a nomeá-lo só na passagem de um passo para o outro (no fim da sessão 2, para o passo 2) e na fonte das citações. No resto, pedem o passo sem dizer quem o manda: juntar material, olhar até ao fundo, largar o problema. Na aula, o docente pode fazer o mesmo.</p></section>'
             '<section class="sessao" id="antes"><h2>Antes de começar</h2>'
             '<p class="pg"><b>O fio.</b> Cada aluno dá os cinco passos do método (juntar material, trabalhá-lo, largá-lo, deixar a ideia aparecer, dar-lhe forma e pô-la à prova) com uma ideia sua: uma peça curta que faça alguém olhar de outra maneira para um lugar a cinco minutos da escola. A forma escolhe-se na sessão 5.</p>'
             '<p class="pg"><b>O material.</b> Cada aluno decide como guarda e combina o que junta, desde que funcione: cartões (o livro aconselha cartões brancos de 12,5 por 7,5 centímetros, um assunto por cartão, que acabam por encher uma caixa), um caderno, o telemóvel, um envelope ou um mural. O guia propõe formas, não impõe uma. Nos textos do aluno diz-se «notas» e «onde guardas o material», para não se confundir com os cartões da lição.</p>'
             '<p class="pg"><b>Ler como um detetive.</b> Interpretar é investigar. Em todas as sessões voltam quatro categorias: <b>facto</b> (vê-se), <b>inferência</b> (junta factos), <b>hipótese</b> (espera provas) e <b>pergunta</b> (fica por investigar). Sherlock Holmes é a testemunha que volta, e quem o traz é o autor do método: cita-o duas vezes no livro.</p>'
             '<p class="pg"><b>Cada sessão</b> tem 180 minutos, com uma pausa: cartões durante cerca de 50 minutos, um «Na aula» de 70 minutos com a pausa, cartões durante cerca de 25 minutos e o «Para levar». A lição abre-se no ecrã de cada aluno ou projeta-se (a projeção começa no primeiro cartão e não grava nada neste aparelho).</p>'
             '<p class="pg"><b>As saídas</b> são só à volta da escola, em aula, com o docente e sem autorização especial. Ninguém fotografa caras; pessoas, só de longe. São opcionais: há sempre outra forma de fazer o mesmo (da janela, numa fotografia de rua, no caminho de casa para a escola).</p>'
             '<p class="indicativa">Avaliação indicativa: orienta o trabalho e não é para usar a sério (decisão 17 do docente). Em cada critério há três níveis, salvo quando o critério diz outros: 0 pontos (não aparece), metade (aparece, incompleto ou sem razão) e todos (como está descrito).</p></section>'
             '<section class="sessao" id="sequencia"><h2>A sequência</h2>'
             '<p class="pg">Os passos 1 e 2 do método levam a Ver; os passos 2 e 3, a Treinar; os passos 4 e 5, a Criar. Cada sessão leva a uma peça concreta da sua porta. A semana entre a sessão 4 e a 5 é, de propósito, a incubação.</p>'
             '<div class="tabela"><table class="seq" role="table"><thead role="rowgroup"><tr role="row">'
             + ''.join('<th role="columnheader" scope="col"' + (' class="num"' if k == 0 else '') + f'>{c}</th>' for k, c in enumerate(SEQ_COLS)) + '</tr></thead>'
             f'<tbody role="rowgroup">{seq}</tbody></table></div></section>')
    for s in SESSOES:
        if s['n'] not in L:
            continue
        # 01/11/2026 (correção 3): sem aspas iguais às da f-string dentro das chavetas (o Python 3.11 do CI não as aceita)
        d, g = L[s['n']], GUIA[s['n']]
        aula = next(c for c in d['cartoes'] if c.get('rot') == 'Na aula')
        img = next(c for c in d['cartoes'] if '<img' in (c.get('html') or ''))
        fig = re.search(r'<figcaption>(.*?)</figcaption>', img['html']).group(1)
        v = video_de(d)
        n_liga = next((i for i, c in enumerate(d['cartoes'], 1) if c.get('liga')), 0)
        tempos = ''.join(f'<tr><td class="num">{e(m)}</td><td>{e(t)}</td></tr>' for m, t in g['tempos'])
        # 01/11/2026 (correção 5, revisor de pt-PT): sem «(a lição inteira)», que fazia crer que o cartão 7 só traz um excerto (o
        # leitor do cartão mostra o vídeo inteiro, sem início nem fim)
        if v:
            yt = (f'<p class="pg">{v["botao"]}. {g.get("video_cred", v["cred"])} <a href="https://www.youtube.com/watch?v={e(v["id"])}">Abrir no YouTube</a>.</p>'
                  f'<p class="pg"><b>Tarefa.</b> {v["tarefa"]}</p>'
                  # 01/11/2026 (método): o número do cartão com a ligação ao resumo sai da lição (era «cartão 8»; com o cartão «O
                  # método», é o 9)
                  f'<p class="pg"><b>Sem vídeo.</b> O docente lê o resumo oficial da lição (a ligação aparece no retorno do cartão {n_liga}) e a turma faz a mesma tarefa diante do quadro de La Tour.</p>')
        else:
            yt = '<p class="pg">Nenhum, de propósito: o centro da sessão é um texto lido devagar e um lugar visto ao vivo.</p>'
        corpo += (f'<section class="sessao pronta" id="s{s["n"]}"><p class="rotulo">Sessão {s["n"]}</p><h2>{e(s["titulo"])}</h2>'
                  f'<p class="pg"><b>A pergunta.</b> {pergunta_abre(d)} <b>O passo.</b> {e(s["passo"])}. <b>A porta.</b> {next(n for q, n, _a, _u in PORTAS if q == s["porta"])}, «{e(s["peca"][0])}», <a href="../../{s["peca"][2]}"><i>{e(s["peca"][1])}</i></a>.</p>'
                  f'<p class="pg"><b>O que ensina.</b> {e(g["ensina"])}</p>'
                  f'<p class="acoes-s"><a class="botao-s" href="../sessao-{s["n"]:02d}/">Abrir a sessão</a><a class="botao-s" href="../sessao-{s["n"]:02d}/?projetar=1">Projetar</a><a class="botao-s" href="../guiao/#g{s["n"]}f">O guião</a></p>'
                  f'<p class="pg"><b>Antes da aula.</b> {e(g["antes"])}</p>'
                  '<h3>O que o aluno lê no cartão «Na aula»</h3>'
                  f'<div class="caixa">{aula["html"]}</div>'
                  '<h3>Tempos (180 minutos)</h3>'
                  f'<div class="tabela"><table><thead><tr><th scope="col" class="num">Minutos</th><th scope="col">O que se faz</th></tr></thead><tbody>{tempos}</tbody></table></div>'
                  '<h3>Materiais</h3><ul>' + ''.join(f'<li>{e(m)}</li>' for m in g['materiais']) + '</ul>'
                  f'<h3>O que fica escrito</h3><p class="pg">{e(g["escrito"])}</p>'
                  f'<h3>Imagem</h3><p class="pg">{fig}</p>'
                  f'<h3>Vídeo</h3>{yt}'
                  f'<h3>Grelha /20 indicativa: {e(g["produto"])}</h3>' + tabela_grelha(g)
                  + '<h3>Notas</h3><ul>' + ''.join(f'<li>{it(x)}</li>' for x in g['notas']) + '</ul>'
                  + '<h3>Ligações</h3><ul class="ligacoes">' + ''.join(f'<li><a href="{e(u)}">{it(t)}</a></li>' for t, u in g['ligacoes']) + '</ul>'
                  f'<h3>Fontes da lição</h3><p class="pg fontes">{it(d["fontes"])}</p></section>')
    corpo += '<p class="saidas-sec"><a href="../">Voltar a Ideias</a><a href="../guiao/">O guião →</a></p>'
    corpo = LL.nq(corpo)
    return (cabeca(base, 'Guia do docente | Ideias | Laboratório | Lente', 'Guia do docente das sessões de Ideias, no Laboratório: tempos, materiais, o que fica escrito e grelhas (piloto).')
            + f'<body class="ideias guia"><a class="c-sr salta" href="#conteudo">Saltar para o conteúdo</a><main id="conteudo">{corpo}</main></body></html>\n')


# ── Biblioteca ──────────────────────────────────────────────────────────────────────────────────────────────────────────
# O molde é o das páginas em português da Biblioteca (biblioteca/orta-benjui/, gerada nas fontes por
# _interno/modelo/biblioteca.mjs): o mesmo <head>, a mesma barra, o cabeçalho, a linha da fonte, o texto, «Li este texto»
# (chave epi-biblioteca) e «Voltar à Biblioteca». Não leva «Onde este texto se usa»: o coração ainda é piloto.
# os dois blocos <style> do molde, copiados de biblioteca/orta-benjui/index.html a 31/10/2026 (03ef772)
BIB_ESTILOS = '''<style>:root{--tinta:#000;--papel:#fff;--papel2:#faf8f2;--suave:#444;--fundo:#f3f2ee;--mostarda:#d9a520;--vermelho:#c8232c;--certo:#1b7f3b;--errado:#c8232c;--certo-fundo:#e2f3e8;--errado-fundo:#fbe5e3;--c-cinza:#d6d4ce;--apagado:#b9b6ae;--linha:#000;--agua:#ebebeb;--d1:8px;--d2:20px;--d3:40px;--col:min(680px,100%);--serif:Georgia,"Times New Roman",serif;--sans:Arial,Helvetica,sans-serif;--cartaz:"Bebas Neue","Arial Narrow","Arial Black",Arial,sans-serif;--maq:"Special Elite","Courier New",monospace}
@media (prefers-color-scheme:dark){:root{--tinta:#ecebe5;--papel:#121210;--papel2:#1a1a17;--suave:#b3b1aa;--fundo:#1d1d1a;--mostarda:#e0b23a;--vermelho:#e4555c;--certo:#7fd9bb;--errado:#e4555c;--certo-fundo:#163d30;--errado-fundo:#4a1f1f;--c-cinza:#3d3c38;--apagado:#5a5853;--linha:#ecebe5;--agua:#222220}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--fundo);color:var(--tinta);font:16px/1.5 var(--sans)}
a{color:inherit}img,svg{max-width:100%}
.pg{width:100%;max-width:calc(var(--col) + 32px);margin:0 auto;padding:0 16px 64px}
.pg-larga{width:100%;max-width:1200px;margin-left:auto;margin-right:auto}
.ler,.pg .ler p,.p-cartao p{font-family:var(--serif);font-size:1.02rem;line-height:1.55}
.p-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--tinta);outline-offset:2px}
[hidden]{display:none!important}
.p-cab{padding:14px 0 4px;margin:0 0 var(--d2)}
.p-etiqueta{font:700 .72rem/1.2 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--suave);margin:0 0 6px}
.p-etiqueta a{color:inherit;text-decoration:none;display:inline-flex;align-items:center;min-height:44px;margin:-15px 0}.p-etiqueta a:hover{color:var(--tinta);text-decoration:underline}
.p-cab h1{font:400 2.3rem/.95 var(--cartaz);letter-spacing:.02em;text-transform:none;margin:0;padding:0}.p-cab h1::after{display:none}
.p-sub{font:italic 1.15rem/1.3 var(--serif);margin:.35rem 0 0}
.p-lead{font-size:.95rem;line-height:1.45;margin:.6rem 0 0;max-width:36em}
.p-cartao{position:relative;background:var(--papel);color:var(--tinta);border:0;padding:14px 16px;margin:0 0 var(--d1)}
.p-rot{font:700 .7rem/1.2 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--suave);margin:0 0 var(--d1)}
.p-tit{font:700 1.05rem/1.25 var(--sans);margin:0 0 2px}
.p-nota{font-size:.88rem;color:var(--suave);margin:4px 0 0}
.p-cartao a{color:var(--tinta);font-weight:700}
.p-feito{box-shadow:inset 4px 0 0 var(--mostarda)}
.p-atual{box-shadow:inset 4px 0 0 var(--vermelho)}
.c-prim,.c-sec{font:700 1rem/1.2 Arial;min-height:48px;margin:0;cursor:pointer;border-radius:0;display:inline-flex;align-items:center;justify-content:center;gap:6px;text-decoration:none;box-sizing:border-box}
.c-prim{background:var(--tinta,#000);color:var(--papel,#fff);border:0;padding:0 22px}
.c-prim:disabled{background:var(--c-cinza);color:var(--suave,#444);cursor:default}
.c-sec{background:none;color:var(--tinta,#000);border:0;padding:0 6px;font-weight:400;text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:1px}
.c-sec.c-seta{text-decoration:none;font-size:1.25rem;min-width:44px;padding:0}
.c-prim[data-seguinte]::after,.c-prim[data-confirmar]::after,.c-prim.c-vai::after{content:"→"}
.bib{max-width:680px;margin:0 auto;padding:0 16px 56px}
.bib-fonte{font:.88rem/1.5 var(--sans,Arial);color:var(--suave);border-top:1px solid var(--tinta);border-bottom:1px solid var(--tinta);padding:10px 0;margin:0 0 24px}.bib-fonte a{color:var(--tinta)}.bib-fonte b{color:var(--tinta)}
.bib-texto{font:1.12rem/1.65 var(--serif,Georgia)}.bib-texto p{margin:0 0 1em;text-wrap:pretty;hyphens:auto}.bib-texto p.versos{margin:0 0 1.2em;hyphens:none}.bib-texto p.didascalia{font-style:italic;color:var(--suave)}
.bib-texto h2{font:700 1.05rem/1.3 var(--sans,Arial);letter-spacing:.06em;text-transform:uppercase;margin:1.8em 0 .8em}
.bib-lido{margin:32px 0 0;padding:16px 0 0;border-top:2px solid var(--tinta);display:flex;flex-wrap:wrap;align-items:center;gap:12px}
.bib-lido button{min-height:48px;padding:0 18px;font:700 .95rem/1 var(--sans,Arial);border:2px solid var(--tinta);background:var(--tinta);color:var(--papel);cursor:pointer}.bib-lido button[aria-pressed="true"]{background:transparent;color:var(--tinta)}
.bib-lido a.bib-orig{display:inline-flex;align-items:center;min-height:48px;padding:0 18px;font:700 .95rem/1 var(--sans,Arial);border:2px solid var(--tinta);background:var(--tinta);color:var(--papel);text-decoration:none}.bib-lido a.bib-orig:focus-visible{outline:3px solid var(--tinta);outline-offset:3px}.bib-passagem{font:.9rem/1.5 var(--sans,Arial);color:var(--suave)}
.bib-lido button:focus-visible{outline:3px solid var(--tinta);outline-offset:3px}.bib-lido small{font:.85rem/1.4 var(--sans,Arial);color:var(--suave)}
.bib-usos{margin:24px 0 0}.bib-usos h2{font:700 .72rem/1.2 var(--sans,Arial);letter-spacing:.14em;text-transform:uppercase;color:var(--suave);margin:0 0 8px}.bib-usos ul{list-style:none;margin:0;padding:0}.bib-usos li{padding:8px 0;border-top:1px solid var(--c-cinza,#ddd)}.bib-usos a{color:var(--tinta)}
.marca-sec{display:block;font:700 clamp(2.4rem,8vw,4rem)/.95 var(--sans,Arial);letter-spacing:-.04em;text-transform:lowercase;color:var(--tinta);margin:0 0 12px}.marca-sec i{font-style:normal;color:var(--mostarda,#d9a520)}.p-etiqueta a{color:var(--tinta)}</style><style id="mg-css">.migalhas{background:#000;color:#fff;font:700 14px/1.25 Arial,Helvetica,sans-serif;margin:0;padding:0 16px;position:relative;z-index:1}.migalhas ol{list-style:none;display:flex;flex-wrap:wrap;align-items:center;gap:0 2px;margin:0 auto;padding:0;max-width:680px}.migalhas li{display:flex;align-items:center;margin:0;padding:0}.migalhas li+li::before{content:"›";padding:0 8px 0 6px;opacity:.6;font-weight:400}.migalhas,.migalhas ol,.migalhas li,.migalhas a{border:0;box-shadow:none;background-image:none}.migalhas a{color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 2px}.migalhas a:hover,.migalhas a:focus-visible{text-decoration:underline;text-underline-offset:3px}.migalhas a:focus-visible{outline:3px solid #fff;outline-offset:2px}.migalhas [aria-current]{font-weight:400;opacity:.85;min-height:44px;display:inline-flex;align-items:center;max-width:62vw;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.mg-casa{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linejoin:round}@media print{.migalhas{display:none}}</style>'''


def pagina_biblioteca():
    css = BIB_ESTILOS
    texto = (f'<p>{e(YOUNG_EXCERTO[0])}</p><p class="corte" aria-label="Corte no texto">[…]</p>'
             + ''.join(f'<p>{e(p)}</p>' for p in YOUNG_EXCERTO[1:]))
    titulo = 'Uma Técnica para Produzir Ideias (excerto)'
    return ('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{titulo} · Biblioteca · Lente</title>'
            '<meta name="description" content="James Webb Young, Uma Técnica para Produzir Ideias (1940): os dois princípios em que assenta o livro, num excerto em tradução nossa.">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Special+Elite&display=swap" rel="stylesheet">'
            + css +
            # 01/11/2026 (correção 2, diretor de arte): o botão do tema acosta à barra (como nas páginas de «Ideias», sistema 6.1)
            # em vez de flutuar por cima da coluna de texto (tapava «cada», «conhecimento», «uma», «lei» a 320 e 360 px). Só nesta
            # página: o molde da família está em _interno/modelo/biblioteca.mjs, nas fontes (decisão 44, barra comum).
            # 01/11/2026 (correção 3, diretor de arte): também só nesta página (o molde comum não muda neste pedido): a etiqueta
            # a 13 px (era 11,52), «Voltar à Biblioteca» com 44 px de alvo (era 113 × 16), o texto com cerca de 71 carateres por
            # linha e entrelinha de 1,55 (eram 80 e 1,65 a partir de 1024 px), a abertura alinhada à esquerda e com a mesma medida
            # (era justificada, a 81 carateres) e o corte escrito «[…]», sem o espaçamento que o mostrava como «[ … ]». A regra
            # comum do texto corrido (assets/appearance.css) justifica .p-cab > p.p-lead com um seletor :is() muito específico:
            # aqui só !important o vence, e só nesta página
            '<style>.bib-texto p.corte{text-align:center;color:var(--suave)}'
            '.migalhas{display:flex;align-items:flex-start}.migalhas ol{flex:1 1 auto;min-width:0}.migalhas li{min-width:0}'
            '.migalhas [aria-current]{max-width:min(62vw,100%)}.migalhas>[data-appearance-control]{margin-left:12px}'
            '.p-cab .p-etiqueta{font-size:.8125rem}.bib-fonte>a[href$="/biblioteca/"]{display:inline-flex;align-items:center;min-height:44px}'
            '.bib .bib-texto{max-width:32em;line-height:1.55}.p-cab .p-lead{text-align:start!important;max-width:32em}</style>'
            '<link rel="stylesheet" href="../../assets/appearance.css?v=20261025-universal-1"><script src="../../assets/appearance.js?v=20261025-universal-1"></script></head>'
            f'<body data-texto="{BIB_ID}"><nav class="migalhas" aria-label="Onde estás"><ol><li><a href="{LENTE}"><svg viewBox="0 0 16 16" aria-hidden="true" class="mg-casa"><path d="M2 8.2 8 2.6l6 5.6M4 7v7h3v-4h2v4h3V7"/></svg>Lente</a></li>'
            f'<li><a href="{LENTE}biblioteca/">Biblioteca</a></li><li><span aria-current="page">{titulo}</span></li></ol><span data-appearance-control></span></nav><main class="bib">\n'
            f'<header class="p-cab"><p class="p-etiqueta"><a href="{LENTE}">Lente</a> · <a href="{LENTE}biblioteca/">Biblioteca</a></p><h1>{titulo}</h1>'
            '<p class="p-sub">James Webb Young, 1940, português (tradução nossa), 1 min de leitura</p>'
            '<p class="p-lead">Um livro curto de um publicitário norte-americano, que descreve em cinco passos como se chega a uma ideia. Aqui ficam os dois princípios em que assenta; o primeiro retoma uma ideia do sociólogo italiano Vilfredo Pareto, que o livro cita antes.</p></header>\n'
            '<p class="bib-fonte"><b>Fonte:</b> James Webb Young, <i lang="en">A Technique for Producing Ideas</i>, Advertising Publications, 1940; edição de 1960. '
            'Capítulo «Combinação de Elementos Antigos». Excerto, com um corte assinalado. Tradução nossa.</p>\n'
            f'<article class="bib-texto" lang="pt-PT">{texto}</article>\n'
            '<p class="bib-passagem">James Webb Young, <i>Uma Técnica para Produzir Ideias</i> (<i lang="en">A Technique for Producing Ideas</i>), Advertising Publications, 1940; edição de 1960. Tradução nossa.</p>\n'
            '<div class="bib-lido"><button type="button" data-lido aria-pressed="false">Li este texto</button><small>Fica só no teu aparelho. Conta na Biblioteca como texto lido.</small></div>\n'
            f'<div class="bib-lido"><a class="bib-orig" href="{YOUNG_REGISTO}" target="_blank" rel="noopener">Abrir o registo do livro</a><small>Impressão de 1944, no Internet Archive, só em empréstimo controlado (com conta gratuita). Abre noutro separador.</small></div>\n'
            f'<p class="bib-fonte" style="margin-top:24px;border-bottom:0"><a href="{LENTE}biblioteca/">Voltar à Biblioteca</a></p>\n'
            '</main><script>(function(){var K="epi-biblioteca",id=document.body.getAttribute("data-texto"),b=document.querySelector("[data-lido]");if(!b)return;\n'
            'function ler(){try{return JSON.parse(localStorage.getItem(K)||"null")||{}}catch(x){return{}}}\n'
            'function pinta(){var P=ler();var f=!!(P.feitas&&P.feitas[id]);b.setAttribute("aria-pressed",f?"true":"false");b.textContent=f?"Lido ✓ (tocar para desfazer)":"Li este texto"}\n'
            'b.addEventListener("click",function(){var P=ler();P.feitas=P.feitas||{};if(P.feitas[id])delete P.feitas[id];else P.feitas[id]=1;try{localStorage.setItem(K,JSON.stringify(P))}catch(x){}pinta()});pinta()})();</script>'
            '<script defer src="../../assets/projection-launcher.js?v=20261019.4" data-site="lente"></script></body></html>\n')


# A linha na lista da Biblioteca (biblioteca/index.html): no fim de «Em português», com o estado lido de epi-biblioteca
# (EPI_MISSOES). A função é idempotente: aplicada à lista já acertada, não muda nada.
BIB_LINHA = (f'<a class="missao p-cartao sem-img" style="--k:15" href="{BIB_ID}/" data-id="{BIB_ID}"><span class="r">Ensaio</span>'
             '<span class="t">Uma Técnica para Produzir Ideias (excerto)</span><span class="s">James Webb Young, 1940, português (tradução nossa).&nbsp;·&nbsp;1&nbsp;min</span><span class="a"></span></a>')
# 01/11/2026 (correção 4, verificador de factos): com o Young em «Em português», o rodapé da lista dizia que todos os textos em
# português estão em domínio público e que só o cabeçalho e a nota são nossos; o excerto de Young é tradução nossa e não está
# em domínio público (decisão 31: o original, com muita probabilidade, sim; a tradução, não). A frase vem do molde comum
# (_interno/modelo/biblioteca.mjs, nas fontes; tarefa 150, «rodapé dos excertos»): a troca é idempotente e fica aqui até o molde
# a trazer.
RODAPE_ANTES = ('Os textos em português estão em domínio público; as transcrições vêm do Project Gutenberg, da Wikisource e do Internet '
                'Archive, identificadas em cada página. Os textos em leitura ótica (OCR) mantêm a grafia e os erros da digitalização. Nada '
                'se corrige: o que é nosso é o cabeçalho e a nota.')
RODAPE_DEPOIS = ('Os textos em português estão em domínio público, exceto o excerto de Young, em tradução nossa; as transcrições vêm do '
                 'Project Gutenberg, da Wikisource e do Internet Archive, identificadas em cada página. Os textos em leitura ótica (OCR) '
                 'mantêm a grafia e os erros da digitalização. Nada se corrige: o que é nosso é o cabeçalho, a nota e, no excerto de '
                 'Young, a tradução.')
BIB_ANTES = 'data-id="reporterx-reporterxizar-1930"><span class="r">Nota editorial</span><span class="t">Reporterxizar</span><span class="s">Reinaldo Ferreira (Repórter X), 1930, português.&nbsp;·&nbsp;3&nbsp;min</span><span class="a"></span></a>'


# 31/10/2026 (revisão do diretor de arte): na lista, nenhum texto sozinho na última fila da grelha («Em português» passou a
# 16 textos e «Noutras línguas» já tinha 19): 3 colunas a partir de 960 px, com o último a toda a largura quando fica
# sozinho, e 2 colunas de 700 a 959 px (o último a toda a largura numa lista ímpar). Só nesta página (assets/index-layout.css serve outros índices).
ESTILO_LISTA = ('<style id="ideias-lista">@media (min-width:960px){body.indice-amplo .missoes{grid-template-columns:repeat(3,minmax(0,1fr))}'
                'body.indice-amplo .missoes>.missao:last-child:nth-child(3n+1){grid-column:1/-1}}'
                '@media (min-width:700px) and (max-width:959px){body.indice-amplo .missoes{grid-template-columns:repeat(2,minmax(0,1fr))}'
                'body.indice-amplo .missoes>.missao:last-child:nth-child(2n+1){grid-column:1/-1}}'
                '@media (max-width:699px){body.indice-amplo .missoes{grid-template-columns:minmax(0,1fr)}}</style>')
LINHA_RE = re.compile(r'<a class="missao p-cartao sem-img" style="--k:(\d+)" href="' + BIB_ID + r'/" data-id="' + BIB_ID + r'">.*?</a>')


def lista_biblioteca(s):
    if f'data-id="{BIB_ID}"' not in s:
        assert s.count(BIB_ANTES) == 1, 'a linha de «Reporterxizar» mudou na lista da Biblioteca'
        i = s.index(BIB_ANTES) + len(BIB_ANTES)
        resto = re.sub(r'style="--k:(\d+)"', lambda m: f'style="--k:{int(m.group(1)) + 1}"', s[i:])
        s = s[:i] + BIB_LINHA + resto
        assert s.count('<b data-feitas>0</b> de 15 textos lidos') == 1
        s = s.replace('<b data-feitas>0</b> de 15 textos lidos', '<b data-feitas>0</b> de 16 textos lidos')
        a = '{"id":"reporterx-reporterxizar-1930"}'
        assert s.count(a) == 1
        s = s.replace(a, a + ',{"id":"' + BIB_ID + '"}')
    # 31/10/2026: a linha já escrita acerta-se ao texto atual de BIB_LINHA (revisão de pt-PT), com o mesmo --k
    m = LINHA_RE.search(s)
    assert m and len(LINHA_RE.findall(s)) == 1, 'a linha do Young na lista da Biblioteca'
    s = s[:m.start()] + BIB_LINHA.replace('style="--k:15"', f'style="--k:{m.group(1)}"') + s[m.end():]
    if 'id="ideias-lista"' not in s:
        assert s.count('</head>') == 1
        s = s.replace('</head>', ESTILO_LISTA + '</head>')
    else:
        s = re.sub(r'<style id="ideias-lista">.*?</style>', lambda _m: ESTILO_LISTA, s, count=1, flags=re.S)
    if RODAPE_ANTES in s:
        s = s.replace(RODAPE_ANTES, RODAPE_DEPOIS)
    assert s.count(RODAPE_DEPOIS) == 1, 'o rodapé da lista da Biblioteca'
    return s


def regras(nome, s):
    """As regras da casa no texto visível (as <title> levam «|» ou «·» como as outras páginas; ficam de fora)."""
    corpo = re.sub(r'<(script|style|title)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    if nome.startswith('biblioteca/'):
        # a etiqueta «Lente · Biblioteca» é a do molde das páginas da Biblioteca (navegação, não frase)
        corpo = re.sub(r'<p class="p-etiqueta">.*?</p>', ' ', corpo, flags=re.S)
    txt = LL.visivel(corpo)
    erros = [f'{nome}: «{m.group(0)}» em …{txt[max(0, m.start() - 40):m.end() + 40]}…' for m in LL.PROIBIDAS.finditer(txt)]
    erros += [f'{nome}: «{m.group(0)}» (usa «Qual das…» ou «Que…»)' for m in LL.QUAL_NOME.finditer(txt)]
    if '"' in re.sub(r'<[^>]+>', '', corpo):
        erros.append(f'{nome}: aspas direitas no texto visível')
    return erros


def paginas():
    L = licoes()
    return {PASTA + 'index.html': pagina_entrada(L), PASTA + 'guiao/index.html': pagina_guiao(L),
            PASTA + 'docente/index.html': pagina_guia(L), f'biblioteca/{BIB_ID}/index.html': pagina_biblioteca()}


def main(argv):
    verificar = '--verificar' in argv
    falhou = False
    alvo_lista = ROOT / 'biblioteca/index.html'
    for rel, s in list(paginas().items()) + [('biblioteca/index.html', lista_biblioteca(alvo_lista.read_text('utf-8')))]:
        erros = regras(rel, s) if rel != 'biblioteca/index.html' else []
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
