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
import html, importlib.util, json, pathlib, re, sys

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
 '01': {
  'dominio': 'Direitos Humanos: a Declaração Universal, a Convenção sobre os Direitos da Criança e a Constituição.',
  'ensina': 'Situar casos da escola em artigos concretos e distinguir uma declaração, um tratado e a Constituição.',
  'antes': 'Antes de abrir a lição: o Ponto de partida, em papel, sem ajuda e sem consulta (10 a 15 minutos). Os cartões de fazer ensinam as respostas das perguntas 1 e 2; por isso o Ponto vem primeiro, ainda que o cartão «Na aula» o lembre mais tarde.',
  'passos': [
   (5, 'Pôr a planta da escola na parede e dar a regra: uma situação por post-it, descrita sem adjetivos e sem nomes de colegas, com o número do artigo.'),
   (20, 'Em grupos de três, quatro a seis post-its: situações reais ou possíveis, no sítio da planta onde acontecem.'),
   (10, 'Pausa.'),
   (15, 'Volta à parede: cada grupo lê dois post-its; a turma confirma o artigo ou propõe outro.'),
   (10, 'Onde dois direitos chocam, o grupo desenha uma seta entre os post-its e escreve qual pesa mais naquele caso.'),
   (5, 'Fotografar o mapa (volta na sessão 10) e recolher os Pontos de partida.'),
  ],
  'materiais': ['Ponto de partida impresso, um por aluno (ligação abaixo).', 'Planta da escola em A3, ou desenhada no quadro.', 'Post-its de duas cores e marcadores.', 'Os artigos da sessão, projetados: Declaração, 1.º, 2.º, 12.º, 19.º, 20.º e 26.º; Convenção, 12.º; Constituição, 16.º, 26.º, 34.º e 37.º.'],
  'escrito': 'O Ponto de partida de cada aluno, com o código e sem o nome; dois post-its por grupo, com a situação e o artigo; a fotografia do mapa.',
  'projeto': ('Apresentação', '#pergunta-resposta', 'Nos últimos cinco minutos, apresentar a Pergunta Humana: um teatro-documento de 5 a 8 minutos, feito a partir de uma pergunta do grupo, que se escolhe na sessão 03.'),
  'produto': 'Mapa de direitos (por grupo)',
  'grelha': [('Situações descritas sem adjetivos nem nomes de colegas', 4), ('Artigo certo para cada situação', 5), ('Um choque de direitos identificado e pesado no caso', 4), ('Variedade de sítios e de direitos (espaço, regras, redes, turma)', 3), ('Leitura à turma e resposta às perguntas', 4)],
  'notas': ['Se a turma se dividir no «Decide», não se fecha a discussão: a posição volta no «Para levar».', 'Ninguém escreve sobre um colega identificável; uma situação vivida conta-se como possível.', 'Grelha desta sessão: proposta da equipa (o plano não a tinha), para o docente rever.'],
 },
 '02': {
  'dominio': 'Direitos Humanos (imagem, reserva da vida privada, consentimento); Media.',
  'ensina': 'Separar filmar, guardar e publicar, e ver que o consentimento vale para um uso.',
  'passos': [
   (5, 'Grupos de três. Cada grupo recebe as quatro situações num envelope, com a informação nova dobrada à parte.'),
   (25, 'Uma situação de cada vez, cerca de 6 minutos cada: decidir, ler o efeito, abrir a informação nova e rever. Alguém do grupo regista a decisão do início e a revista.'),
   (10, 'Pausa.'),
   (20, 'O pedido de consentimento para as entrevistas da Pergunta Humana, nas quatro partes: para quê, que uso, onde fica e até quando, como se retira.'),
   (5, 'Dois grupos leem o pedido em voz alta; a turma diz o que falta.'),
  ],
  'materiais': ['As quatro situações em papel: o ensaio da Marta; uma fotografia de rua com uma pessoa reconhecível em primeiro plano; uma captura de ecrã de uma conversa privada; a entrevista do projeto. Cada uma com o efeito da decisão e uma informação nova (por exemplo: a pessoa da fotografia de rua é menor).', 'O modelo do pedido de consentimento, em quatro partes.', 'Código Civil, artigo 79.º, projetado.'],
  'escrito': 'O pedido de consentimento do grupo e a decisão revista de uma das situações.',
  'projeto': ('Ética das entrevistas', '', 'O pedido de consentimento entra no dossiê da Pergunta Humana; a página do projeto diz o que fazer com menores (autorização do encarregado de educação), com o anonimato e com quem desiste.'),
  'produto': 'Pedido de consentimento',
  'grelha': [('Finalidade dita em palavras simples', 4), ('Uso, sítio e prazo', 4), ('Direito a recusar e a retirar, com contacto', 4), ('Cuidado com terceiros e com menores (encarregado de educação)', 4), ('Decisão revista de uma situação, com o artigo certo', 4)],
  'notas': ['Ninguém é filmado na aula; nenhum vídeo real de alunos entra nas situações.', 'O vídeo é um excerto (0 a 47 s) de uma conferência do TED, candidato provisório: a decisão 18 manda perguntar ao docente quando não há escolha clara.', 'No cartão da fotografia de rua, a leitura do artigo 79.º, n.º 2 («enquadrada na de lugares públicos») é interpretação nossa: o docente confirma.', 'No cartão dos fins didáticos, a leitura do artigo 79.º, n.º 2 (finalidades didáticas, com o limite do n.º 3) também é para o docente confirmar: a escola precisa de base legal para publicar a imagem de uma aluna.', 'O excerto refere imagens sexuais falsificadas (entre os 25 e os 34 s): ver antes e decidir se se mostra.'],
 },
 '03': {
  'dominio': 'Direitos Humanos (igualdade e não discriminação, igualdade de género, deficiência); Pluralismo.',
  'ensina': 'Ver que uma regra igual para todos pode ter efeitos desiguais e que ouvir quem é afetado faz parte da solução.',
  'passos': [
   (5, 'Grupos de quatro. Cada pessoa tira uma carta (o Rui, a organização, quem orienta a mostra, quem só pode ir à sexta-feira); cada grupo recebe cinco unidades.'),
   (15, 'Cada pessoa defende a sua carta durante dois minutos; o grupo gasta as cinco unidades: mudar de sala custa três, texto para quem acompanha por escrito custa uma, transmitir custa uma.'),
   (5, 'O docente lê a informação nova (por exemplo: a sala do rés do chão tem menos lugares) e o grupo revê.'),
   (10, 'Pausa.'),
   (10, 'A proposta à direção, em cinco linhas: barreira, quem afeta, medida, custo, quem foi ouvido.'),
   (20, 'A pergunta do grupo para a Pergunta Humana: cada grupo escolhe e delimita a sua, investigável na escola e no bairro até ao fim do módulo.'),
  ],
  'materiais': ['Cartas de perspetiva, quatro por grupo.', 'Cinco unidades por grupo (clipes ou papéis) e a tabela dos custos.', 'O modelo da proposta à direção.', 'A secção «Uma boa pergunta» da página do projeto.'],
  'escrito': 'A proposta à direção em cinco linhas e a pergunta do grupo.',
  'projeto': ('A pergunta', '#fases', 'Nos últimos 20 minutos do «Na aula», cada grupo escolhe e delimita a pergunta do grupo para a Pergunta Humana.'),
  'produto': 'Proposta à direção e pergunta',
  'grelha': [('Barreira descrita sem juízo', 4), ('Quem é afetado e foi ouvido', 4), ('Medida possível, com custo dentro do orçamento', 4), ('Fundamento com o artigo certo', 4), ('Pergunta do grupo delimitada e investigável', 4)],
  'notas': ['Enquadramento da imagem, antes de a projetar (decisão 30): em vários estados do sul dos Estados Unidos, a segregação racial era imposta por lei no tempo desta fotografia (1943).', 'Se houver na turma alguém com deficiência, não se usa como exemplo: as cartas são personagens.', 'A Convenção sobre os Direitos das Pessoas com Deficiência, o Decreto-Lei n.º 163/2006 e a Lei n.º 46/2006 ficam fora dos cartões até se confirmarem no Diário da República.'],
 },
 '04': {
  'dominio': 'Direitos Humanos (liberdade de expressão, bom nome); Democracia (discurso de ódio); Media (fontes, verificação).',
  'ensina': 'Separar opinião, sátira e acusação de facto, e verificar antes de repetir.',
  'passos': [
   (5, 'Grupos de três. Cada grupo recebe as três afirmações reais e as três publicações inventadas sobre a escola.'),
   (25, 'Verificar cada afirmação: origem (quem, onde, quando), duas fontes independentes e veredicto (verdadeiro, falso, enganador ou sem prova). Leitura lateral: abrir outros separadores antes de ler a página até ao fim.'),
   (10, 'Pausa.'),
   (15, 'As três publicações: manter, corrigir ou retirar, com o artigo (Constituição, 37.º e 26.º; Convenção, 13.º).'),
   (10, 'O registo de fontes do grupo para a Pergunta Humana: duas fontes da pergunta do grupo, com o que é preciso para as reencontrar.'),
  ],
  'materiais': ['As três afirmações reais: o docente escolhe-as e confirma-as num verificador de factos antes da aula (não vêm prontas aqui).', 'Três publicações inventadas sobre a escola: uma crítica, uma sátira e uma acusação sem prova.', 'O registo de verificação: origem, fonte 1, fonte 2, porque são independentes, veredicto.', 'Um computador ou telemóvel por grupo.'],
  'escrito': 'O registo de verificação das três afirmações (é o laboratório de verificação do módulo) e o registo de fontes do grupo.',
  'projeto': ('As fontes', '#metodo', 'O registo de fontes, localizável, e a leitura lateral; o laboratório de verificação do módulo faz-se nesta sessão.'),
  'produto': 'Laboratório de verificação',
  'grelha': [('Origem identificada (quem, onde, quando)', 4), ('Duas fontes independentes e porque o são', 5), ('Veredicto proporcional à prova', 4), ('Decisão sobre as três publicações, com o artigo', 4), ('Registo localizável', 3)],
  'notas': ['Casos reais só os que o docente escolhe e confirma (decisão 12).', 'Na imagem, o cartão diz só o que está impresso na página de 1834; a atribuição a Daumier e a história do julgamento de Philipon ficam por confirmar na Gallica.', 'A Convenção Europeia dos Direitos Humanos (artigo 10.º) e o Código Penal (artigo 240.º) ficam fora dos cartões até se confirmarem.'],
 },
 '05': {
  'dominio': 'Direitos Humanos (reserva da vida privada, proteção de dados); Democracia (limites a quem vigia); Media.',
  'ensina': 'Pesar segurança e privacidade e saber o que a lei deixa fazer numa escola.',
  'passos': [
   (5, 'Grupos de três. Cada grupo recebe o formulário inventado da visita de estudo.'),
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
  'notas': ['Saída só à volta da escola, em aula, sem autorização especial (decisão 10). Quem não pode sair regista as câmaras e os avisos visíveis do portão.', 'Imagem: a planta de Willey Reveley não se conseguiu descarregar (o servidor respondeu 429 três vezes e não se insistiu); entrou a página de título da edição de 1791.', 'O Regulamento Geral sobre a Proteção de Dados (artigos 5.º e 8.º) fica fora dos cartões até se confirmar no EUR-Lex.'],
 },
 '06': {
  'dominio': 'Democracia e Instituições Políticas (regras coletivas, ética e integridade, conflito de interesses); Direitos Humanos (igualdade).',
  'ensina': 'Comparar critérios de repartir, separar o resultado dos limites e ver o que muda quando quem decide ganha com a decisão.',
  'passos': [
   (5, 'O problema no quadro: seis turnos de filmagem para três grupos. Listar os critérios: igualdade, necessidade, ordem de inscrição, sorteio, outro.'),
   (10, 'Cada grupo escolhe a regra e escreve-a numa frase, sem saber o lugar que lhe vai calhar.'),
   (5, 'Cada grupo tira uma carta com o lugar (A, B ou C) e a situação desse lugar (por exemplo: o grupo C perdeu um turno porque o material não chegou).'),
   (10, 'Aplicar a regra. Quem perde apresenta a objeção em dois minutos; o grupo responde ou revê.'),
   (10, 'Pausa.'),
   (25, 'A mesma pergunta para o teatro-documento: como se repartem as falas e o tempo de cena. A regra do grupo e o primeiro esboço do guião (quem fala, quanto tempo, com que fonte).'),
  ],
  'materiais': ['Cartas A, B e C, com a situação de cada lugar.', 'O quadro dos seis turnos.', 'Papel para o esboço do guião.'],
  'escrito': 'A regra final, quem perde com ela e porque a aceitaria mesmo assim; a regra do grupo para as falas, com o primeiro esboço do guião.',
  'projeto': ('O guião, em esboço', '#metodo', 'A regra do grupo para repartir falas e tempo de cena e o primeiro esboço do guião entram no dossiê.'),
  'produto': 'Regra e esboço',
  'grelha': [('Regra clara e aplicável', 4), ('Quem perde e porquê, dito do ponto de vista de quem perde', 4), ('Objeção respondida', 4), ('Conflito de interesses reconhecido', 4), ('Regra das falas do grupo', 4)],
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
  'notas': ['Nenhum aluno faz de vítima: a colega do caso não entra em cena.', 'Imagem: a fotografia dos óstracos de Temístocles não se conseguiu descarregar (429 e bloqueio do Flickr, sem insistir); entrou uma litografia de Daumier do Metropolitan Museum of Art (CC0).', 'A Lei n.º 51/2012 (Estatuto do Aluno e Ética Escolar) fica fora dos cartões até se confirmar no Diário da República.'],
 },
 '08': {
  'dominio': 'Democracia e Instituições Políticas (órgãos de soberania, autarquias, União Europeia, eleições, petição, Provedor de Justiça).',
  'ensina': 'Distinguir quem faz as leis, quem governa, quem julga e quem decide o que se faz na rua, e escrever um pedido com destinatário e fundamento.',
  'passos': [
   (5, 'Grupos de três. As regras da volta (em aula, com o docente, sem fotografar pessoas nem matrículas) e a grelha das seis coisas.'),
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
   (5, 'Emparelhar grupos (A observa B, B observa A) e entregar a grelha de três colunas.'),
   (15, 'O grupo A mostra o ensaio (5 a 8 minutos) e recebe as notas: o que se ouviu, de quem é a voz, de que fonte vem, que voz falta.'),
   (10, 'Pausa.'),
   (15, 'O grupo B mostra o ensaio e recebe as notas.'),
   (10, 'Cada grupo decide duas mudanças, uma delas para incluir uma voz que ainda não estava. Cada grupo prepara também uma objeção para outro grupo, para a sessão 10.'),
  ],
  'materiais': ['Cartões de posição para «O outro lado» (a regra do português nos intervalos e outras posições do módulo).', 'A grelha de observação em três colunas.', 'Um relógio visível.'],
  'escrito': 'As notas dadas ao outro grupo e duas mudanças decididas pelo grupo.',
  'projeto': ('O ensaio', '#av-teatro', 'O ensaio cruzado do teatro-documento, com a voz de quem discorda e a fonte de cada fala.'),
  'produto': 'Ensaio',
  'grelha': [('Voz que discorda presente e com fonte', 4), ('Ligação reconhecível às fontes', 4), ('Duração dentro dos 5 a 8 minutos', 3), ('Notas concretas ao outro grupo', 4), ('Duas mudanças decididas e justificadas', 5)],
  # 31/10/2026 (verificação final, decisão 39): a fotografia da Library of Congress saiu e a nota «Para rever» também.
  'notas': ['No exemplo de estereótipo, ninguém nomeia colegas.', 'Imagem: a fotografia prevista no plano, _Pipers_, tirada na ilha de Ellis por Augustus Sherman, não se descarregou (o servidor recusou os pedidos e a Biblioteca Pública de Nova Iorque bloqueia robôs). A da Library of Congress (LC-D6-87) também saiu: a biblioteca não diz quem a tirou nem a declara em domínio público.', 'A fotografia nova é de Lewis Hine, _Immigrant Family in the Baggage Room of Ellis Island_ (1905), do Museum of Fine Arts, Houston, domínio público segundo o Wikimedia Commons. O título não diz de onde vem a família: o cartão fala de imigrantes, não de um país.', 'A Declaração Universal (artigos 2.º e 18.º) e a Resolução do Conselho de Ministros n.º 127/2025 ficam fora dos cartões até se confirmarem.'],
 },
 '10': {
  'dominio': 'Direitos Humanos e Democracia e Instituições Políticas (síntese do módulo); Media (fontes). Ponto de chegada.',
  'ensina': 'Defender uma resposta com fontes e responder a uma objeção.',
  'antes': 'Antes de abrir a lição: o Ponto de chegada, em papel, sem ajuda e sem consulta (10 a 15 minutos), com as mesmas 10 perguntas do Ponto de partida. Os cartões de recuperação vêm depois, para não ensinarem as respostas antes.',
  'passos': [
   (5, 'A ordem das apresentações e as regras da defesa: uma pergunta do público e a objeção preparada por outro grupo na sessão 09.'),
   (30, 'As primeiras apresentações: 5 a 8 minutos cada, seguidos de três minutos de defesa.'),
   (10, 'Pausa.'),
   (25, 'As restantes apresentações. Com mais de cinco grupos, as que faltam passam para os 25 minutos finais, antes dos últimos cartões.'),
   (5, 'A autoavaliação «Vi, Situei, Fiz», em três linhas, e o mapa de direitos da sessão 01 revisto: o que mudou.'),
  ],
  'materiais': ['O Ponto de chegada impresso, um por aluno (ligação abaixo).', 'A ordem das apresentações e as objeções preparadas na sessão 09.', 'Um relógio visível.', 'A fotografia do mapa de direitos da sessão 01.'],
  'escrito': 'O Ponto de chegada, a autoavaliação «Vi, Situei, Fiz» e o mapa de direitos revisto.',
  'projeto': ('A apresentação e a defesa', '#av-teatro', 'A apresentação pública do teatro-documento e a defesa das escolhas do grupo.'),
  'produto': 'Apresentação e defesa',
  'grelha': [('Guião e cena fundamentados na investigação', 5), ('Ligação reconhecível às fontes', 4), ('Duração de 5 a 8 minutos e clareza', 3), ('Defesa: resposta à objeção com fonte e limite', 5), ('Contributo de cada pessoa identificado', 3)],
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
 '.cid-piloto .marca{font:400 1rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;letter-spacing:.06em;margin:0 0 4px}'
 '.cid-piloto h1{font:700 clamp(2.4rem,9vw,3.6rem)/.95 Arial,Helvetica,sans-serif;margin:0 0 10px;letter-spacing:-.05em}'
 '.cid-piloto h1,.cid-piloto h2,.cid-piloto h3{text-wrap:balance}'
 '.cid-piloto a{color:inherit;text-underline-offset:.15em}'
 '.cid-piloto h2{font:700 1.25rem/1.25 Arial,Helvetica,sans-serif;margin:32px 0 10px}'
 '.cid-piloto h3{font:700 1rem/1.3 Arial,Helvetica,sans-serif;margin:20px 0 6px}'
 '.cid-piloto .lead{font-size:1.05rem;margin:0 0 18px;max-width:38em}'
 '.cid-piloto .aviso-piloto{font-size:.9rem;color:var(--suave);margin:0 0 18px}'
 # 31/10/2026 (terceira correção, diretor de arte): na página do módulo, a linha do piloto passa para o rodapé (sistema, 6.10).
 '.cid-piloto ol.sessoes+.aviso-piloto{margin:24px 0 0}.cid-piloto .aviso-piloto+footer.mais{margin-top:16px}'
 '.cid-piloto section.proximo{background:var(--tinta);color:var(--papel);padding:14px 16px 16px;margin:4px 0 12px}'
 '.cid-piloto .proximo .kicker{font:700 .8125rem/1.2 Arial,Helvetica,sans-serif;letter-spacing:.12em;text-transform:uppercase;margin:0 0 6px}'
 '.cid-piloto .proximo .prox-n{font:400 2.6rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;margin:0}'
 '.cid-piloto .proximo .prox-t{font:700 1.15rem/1.25 Arial,Helvetica,sans-serif;margin:2px 0 12px}'
 '.cid-piloto a.continuar{display:inline-block;background:var(--papel);color:var(--tinta);text-decoration:none;font-weight:700;padding:12px 18px;border:3px solid var(--papel);margin:0}'
 '.cid-piloto a.continuar:focus-visible,.cid-piloto .sessoes a:focus-visible{outline:3px solid var(--tinta);outline-offset:3px}'
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
 '.cid-piloto ol.sessoes .perg{grid-column:2;color:var(--suave);font-size:.95rem;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}'
 '@media (max-width:599px){.cid-piloto ol.sessoes .perg{display:none}}'
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
 '.cid-piloto li.feita .n::after{content:"";display:block;width:1.6rem;height:4px;background:var(--acento);margin-top:4px}'
 '.cid-piloto footer.mais{margin-top:28px;display:flex;flex-wrap:wrap;gap:8px 20px}'
 '.cid-piloto footer.mais a{color:inherit;font-weight:700}'
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


def pagina_modulo(S):
    base = '../../../'
    linhas = ''
    for s in S:
        linhas += (f'<li data-chave="{e(s["chave"])}" data-versao="{e(s["versao"])}" data-n="{s["n"]}" data-titulo="{e(s["titulo"])}" data-pergunta="{e(LL.visivel(s["pergunta"]))}">'
                   f'<a href="../m1-s{s["n"]}/"><span class="n" aria-hidden="true">{s["n"]}</span>'
                   # 31/10/2026 (verificação final, decisão da equipa): o estado vai na linha do título; a pergunta só aparece
                   # na linha acima de 600 px, numa linha com reticências (abaixo, só a da próxima sessão, na região «A seguir»).
                   f'<span class="tit"><strong><span class="c-sr">Sessão {s["n"]}: </span>{e(s["titulo"])}</strong> <span class="estado" data-estado></span></span>'
                   f'<span class="perg">{s["pergunta"]}</span></a></li>')
    js = ('(function(){"use strict";var L=[].slice.call(document.querySelectorAll("[data-chave]")),feitas=0,prox=null;'
          'L.forEach(function(li){var st=null;try{st=JSON.parse(localStorage.getItem(li.getAttribute("data-chave"))||"null")}catch(x){st=null}'
          'var ok=!!(st&&st.lida&&st.versao===li.getAttribute("data-versao"));var el=li.querySelector("[data-estado]");'
          # 31/10/2026 (revisão do diretor de arte): a sessão feita diz «Feita dd/mm» (o motor grava t=Date.now() no fim); a
          # próxima por fazer leva «A seguir» e o filete vermelho; «por fazer» não se escreve.
          'var dd=function(n){return(n<10?"0":"")+n};'
          'if(ok){feitas++;li.classList.add("feita");var d=typeof st.t==="number"?new Date(st.t):null;el.textContent="Feita"+(d&&!isNaN(d)?" "+dd(d.getDate())+"/"+dd(d.getMonth()+1):"")}'
          'else if(!prox){prox=li;li.classList.add("seguir");el.textContent="A seguir"}});'
          'var b=document.querySelector("[data-continuar]"),c=document.querySelector("[data-contagem]"),pn=document.querySelector("[data-prox-n]"),pt=document.querySelector("[data-prox-t]"),pk=document.querySelector("[data-prox-k]"),pq=document.querySelector("[data-prox-q]");'
          'if(c)c.textContent=feitas+" de "+L.length+" sessões feitas";'
          'if(b&&feitas){if(prox){b.href=prox.querySelector("a").getAttribute("href");b.textContent="Continuar: Sessão "+prox.getAttribute("data-n")+", "+prox.getAttribute("data-titulo")+"\\u00a0→";if(pn)pn.textContent=prox.getAttribute("data-n");if(pt)pt.textContent=prox.getAttribute("data-titulo");if(pq)pq.textContent=prox.getAttribute("data-pergunta")}'
          'else{b.textContent="As 10 sessões estão feitas. Rever a sessão 01\\u00a0→";if(pk)pk.textContent="Módulo feito"}}})();')
    corpo = (migalhas(base, [('Lente', LENTE), ('Cidadania', LENTE + 'cidadania/'), ('Módulo 1 (piloto)', '')])
             + '<header><p class="marca">Cidadania, módulo 1</p><h1>Ser-se humano</h1>'
             '<p class="lead">Direitos humanos, democracia e instituições políticas, em 10 sessões de 180 minutos. Cada sessão é uma lição em cartões, com uma parte na aula.</p>'
             '</header>'
             f'<section class="proximo" aria-label="A seguir"><p class="kicker" data-prox-k>A seguir</p>'
             f'<p class="prox-n" data-prox-n>01</p><p class="prox-t" data-prox-t>{e(S[0]["titulo"])}</p><p class="prox-q" data-prox-q>{S[0]["pergunta"]}</p>'
             f'<a class="continuar" data-continuar href="../m1-s01/">Começar: Sessão 01, {e(S[0]["titulo"])} →</a></section>'
             f'<p class="contagem" data-contagem>0 de {len(S)} sessões feitas</p>'
             f'<ol class="sessoes">{linhas}</ol>'
             # 31/10/2026 (terceira correção, diretor de arte): a linha do piloto vai para o rodapé (sistema, 6.10); no cabeçalho,
             # empurrava a primeira ação para fora do primeiro ecrã a 320 px.
             '<p class="aviso-piloto">Piloto em revisão. O que fazes fica só neste aparelho.</p>'
             '<footer class="mais"><a href="docente/">Guia do docente</a></footer>')
    return (cabeca(base, 'Módulo 1 (piloto) · Cidadania · Lente', 'Cidadania, módulo 1, Ser-se humano: as 10 sessões em piloto.')
            + '<body class="cid-piloto"><style>.c-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}</style>'
            + f'<main id="conteudo">{corpo}</main><script>{js}</script></body></html>\n')


def tabela_grelha(g):
    soma = sum(p for _, p in g['grelha'])
    assert soma == 20, (g['produto'], soma)
    linhas = ''.join(f'<tr><td>{e(c)}</td><td class="num">{p}</td></tr>' for c, p in g['grelha'])
    return (f'<div class="tabela"><table><caption class="c-sr">Grelha indicativa: {e(g["produto"])}</caption><thead><tr><th scope="col">Critério</th><th scope="col" class="num">Pontos</th></tr></thead>'
            f'<tbody>{linhas}</tbody><tfoot><tr><th scope="row">Total (indicativo)</th><td class="num">20</td></tr></tfoot></table></div>')


def yt_link(s):
    u = 'https://www.youtube.com/watch?v=' + s['yt']
    return u + (f'&t={s["yt_ini"]}s' if s['yt_ini'] and s['yt_ini'] != '0' else '')


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
             '<section><h2>Antes de começar</h2>'
             '<p class="pg">Cada sessão tem 180 minutos, com uma pausa. A lição em cartões abre-se no ecrã de cada aluno ou projeta-se para a turma (ligação «Projetar» em cada sessão: a projeção começa no primeiro cartão e não grava nada neste aparelho).</p>'
             + tempos +
             '<p class="pg">O <a href="../ponto/">Ponto de partida e de chegada</a> tem as mesmas 10 perguntas, para imprimir. Faz-se no início da sessão 01 e no início da sessão 10; a chave e a cotação estão no fim deste guia, e não nas páginas dos alunos.</p>'
             '<p class="pg">As saídas das sessões 05 e 08 são só à volta da escola, em aula, com o docente e sem autorização especial. Não se fotografam pessoas nem matrículas.</p>'
             '<h2>Avaliação</h2>'
             '<p class="indicativa">Avaliação indicativa: orienta o trabalho e não é para usar a sério (decisão 17; Portaria n.º 235-A/2018, artigo 27.º, n.º 8).</p>'
             '<p class="pg">Cada sessão tem uma grelha /20 do produto da sessão. Em cada critério há três níveis: 0 pontos (não aparece), metade dos pontos (aparece, mas incompleto ou sem razão) e todos os pontos (como está descrito). A correspondência com os quatro instrumentos da <a href="../../../projeto/">Pergunta Humana</a> também é indicativa:</p>'
             + instr + '</section>'
             f'<nav aria-label="Sessões"><h2>As 10 sessões</h2><ul class="indice">{indice}</ul></nav>')
    for s in S:
        g = GUIA[s['n']]
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
                  f'<div class="caixa">{s["aula"]["html"]}</div>'
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
              '<p><a href="../ponto/">Abrir o Ponto para imprimir</a></p>'
              '<div class="tabela"><table><thead><tr><th scope="col" class="num">N.º</th><th scope="col">Pergunta</th><th scope="col">Chave ou cotação</th><th scope="col" class="num">Pontos</th><th scope="col">Sessão</th></tr></thead>'
              f'<tbody>{chave}</tbody></table></div></section>'
              '<footer class="mais"><a href="../">Voltar ao módulo</a><a href="../../../projeto/">Pergunta Humana</a></footer>')
    return (cabeca(base, 'Guia do docente, módulo 1 (piloto) · Cidadania · Lente', 'Guia do docente das 10 sessões do módulo 1 de Cidadania em piloto.')
            + '<body class="cid-piloto guia"><style>.c-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}</style>'
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
    return {MODULO + 'index.html': pagina_modulo(S), MODULO + 'docente/index.html': pagina_guia(S), MODULO + 'ponto/index.html': pagina_ponto()}


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
