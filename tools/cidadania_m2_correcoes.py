"""Correções verificáveis dos «Riscos» do plano do M2 (docs/pedagogia/plano-cidadania-m2.md), 28/10/2026.

Cada correção troca um texto exato por outro, numa página já publicada. É idempotente: se o texto novo já lá
está e o antigo não, não faz nada; se nenhum dos dois aparece, para com erro (a página mudou e a correção tem
de ser revista à mão). tools/generate_cidadania_m2.py aplica-as; tests/test_videos_escolhidos.py aplica-as
também ao lado de origin/main antes de comparar, para que só estas mudanças passem.

Fontes conferidas nesta sessão:
- Ver para fazer: o vídeo de Joana Vasconcelos tem o identificador «arte» em ver-para-fazer/catalogo.json e
  vive em ver-para-fazer/v62/; a página ver-para-fazer/ não tem nenhum elemento com id="arte".
- curl, 28/10/2026: .../pt/cidadania/ferramentas/m2-aula-01-feed/ responde com a página «mudou de endereço»;
  .../lente/cidadania/ferramentas/m2-aula-01-feed/ responde com a ferramenta.
- Wikimedia Commons: The Laughing Audience (National Gallery of Art, dedicação CC0); Declaração de 1789
  (Jean-Jacques Le Barbier, cerca de 1789, Musée Carnavalet, P809, fotografia CC0 do Paris Musées);
  chaleira da AEG (Christos Vittoratos, CC BY-SA 3.0); máquina de Jacquard (David Monniaux, 2006).
- Library of Congress: a estereoscopia «Statue of the Duke of Terceira, Lisbon, Portugal», H. C. White Co.,
  1907, n.º 11420, é o item 2021640877 («No known restrictions on publication»); o item 2021640870, para onde
  as páginas ligavam, é «The arch, Praca do Commercio».
- JSTOR: Nagel, «What Is It Like to Be a Bat?», já ligado na Ética, lição 2 (jstor.org/stable/2183914).
"""

LOC_ANTIGO = 'https://www.loc.gov/item/2021640870/'
LOC = 'https://www.loc.gov/item/2021640877/'
ALT_LISBOA = 'Fotografia antiga: a estátua do Duque da Terceira sobre o pedestal, numa praça de Lisboa, com homens de chapéu à volta.'
FEED_PT = 'https://pedrohfernandes-klk.github.io/pt/cidadania/ferramentas/m2-aula-01-feed/'
FEED = 'https://pedrohfernandes-klk.github.io/lente/cidadania/ferramentas/m2-aula-01-feed/'

# (página, texto antigo, texto novo, risco do plano)
CORRECOES = [
    # 1. Âncora partida no passo 00.
    ('cidadania/m2/passo-00/index.html', 'https://pedrohfernandes-klk.github.io/lente/ver-para-fazer/#arte', 'https://pedrohfernandes-klk.github.io/lente/ver-para-fazer/v62/', 1),
    # 2. A ferramenta vive no Lente, não no sítio de Português.
    ('cidadania/m2/passo-01/index.html', FEED_PT, FEED, 2),
    ('cidadania/m2/passo-03/index.html', FEED_PT, FEED, 2),
    ('cidadania/m2/passo-06/index.html', FEED_PT, FEED, 2),
    ('cidadania/m2/cid-m2-preco-minuto/index.html', FEED_PT, FEED, 2),
    # 3. Créditos: Hogarth (domínio público, ficheiro CC0), nos dois sítios onde aparece.
    ('cidadania/m2/passo-03/index.html', 'William Hogarth. Domínio público no registo de origem (<a href=\\"https://commons.wikimedia.org/wiki/File:William_Hogarth,_The_Laughing_Audience,_1733,_NGA_30455.jpg\\">Wikimedia Commons</a>), consulta de 2026-10-15.',
     'William Hogarth. Domínio público; ficheiro dedicado ao domínio público (CC0) pela National Gallery of Art, no registo de origem (<a href=\\"https://commons.wikimedia.org/wiki/File:William_Hogarth,_The_Laughing_Audience,_1733,_NGA_30455.jpg\\">Wikimedia Commons</a>), consulta de 2026-10-28.', 3),
    ('cidadania/m2/imagens/index.html', 'Autoria no registo: William Hogarth. Direitos no registo: CC0. Consulta: 2026-10-15.',
     'Autoria no registo: William Hogarth. Direitos no registo: domínio público; ficheiro dedicado ao domínio público (CC0) pela National Gallery of Art. Consulta: 2026-10-28.', 3),
    # 3. Créditos: a Declaração de 1789 é de Le Barbier, no registo e no texto.
    ('cidadania/m2/passo-02/index.html', 'autor desconhecido. Domínio público no registo de origem (<a href=\\"https://commons.wikimedia.org/wiki/File:Declaration_of_the_Rights_of_Man_and_of_the_Citizen_in_1789.jpg\\">Wikimedia Commons</a>), consulta de 2026-10-15.',
     'Jean-Jacques-François Le Barbier, cerca de 1789, Musée Carnavalet. Domínio público; fotografia dedicada ao domínio público (CC0) pelo Paris Musées, no registo de origem (<a href=\\"https://commons.wikimedia.org/wiki/File:Declaration_of_the_Rights_of_Man_and_of_the_Citizen_in_1789.jpg\\">Wikimedia Commons</a>), consulta de 2026-10-28.', 3),
    ('cidadania/m2/imagens/index.html', 'Autoria no registo: autor desconhecido. Direitos no registo: Public domain. Consulta: 2026-10-15.',
     'Autoria no registo: Jean-Jacques-François Le Barbier, cerca de 1789, Musée Carnavalet. Direitos no registo: domínio público; fotografia dedicada ao domínio público (CC0) pelo Paris Musées. Consulta: 2026-10-28.', 3),
    # 3. Créditos: a chaleira também é CC BY-SA 3.0 (o rodapé do índice só falava do Jacquard).
    ('cidadania/m2/index.html', 'exceto a fotografia da máquina de Jacquard (David Monniaux, CC BY-SA 3.0)',
     'exceto as fotografias da chaleira da AEG (Christos Vittoratos, CC BY-SA 3.0) e da máquina de Jacquard (David Monniaux, CC BY-SA 3.0)', 3),
    # 3. Créditos: a máquina de Jacquard no exercício longo 1 ficava sem autor.
    ('cidadania/m2/cid-m2-preco-minuto/index.html', '<span class=\\"fr-cred\\">CC BY-SA 3.0. <a href=\\"https://commons.wikimedia.org/wiki/File:Jacquard_loom_p1040320.jpg\\"',
     '<span class=\\"fr-cred\\">David Monniaux, 2006. CC BY-SA 3.0. <a href=\\"https://commons.wikimedia.org/wiki/File:Jacquard_loom_p1040320.jpg\\"', 3),
    # 3. Créditos: Lisboa 1907. O passo 04 ganha o crédito; o registo certo da Library of Congress.
    ('cidadania/m2/passo-04/index.html', 'quem publicou isto, e porquê."',
     'quem publicou isto, e porquê. A fotografia original: estátua do Duque da Terceira, Lisboa, 1907, estereoscopia n.º 11420 da H. C. White Co., Library of Congress, domínio público. A versão B foi alterada por nós."', 3),
    ('investigar/passo-08/index.html', 'H. C. White Co. (estereoscopia). Domínio público. <a href=\\"' + LOC_ANTIGO + '\\"',
     'H. C. White Co., estereoscopia n.º 11420, 1907. Library of Congress, domínio público. <a href=\\"' + LOC + '\\"', 3),
    ('etica/index.html', 'H. C. White Co. (estereoscopia). Domínio público. <a href=\\"' + LOC_ANTIGO + '\\"',
     'H. C. White Co., estereoscopia n.º 11420, 1907. Library of Congress, domínio público. <a href=\\"' + LOC + '\\"', 3),
    # 4. Texto alternativo em inglês.
    ('investigar/passo-08/index.html', 'alt=\\"Statue of the Duke of Terceira, Lisbon, Portugal, 1907 (Library of Congress)\\"', 'alt=\\"' + ALT_LISBOA + '\\"', 4),
    ('etica/index.html', 'alt=\\"Statue of the Duke of Terceira, Lisbon, Portugal, 1907 (Library of Congress)\\"', 'alt=\\"' + ALT_LISBOA + '\\"', 4),
    ('etica/index.html', 'alt=\\"Statue of the Duke of Terceira, Lisbon, Portugal, 1907 (Library of Congress), versão alterada para o exercício: a estátua foi retirada do pedestal\\"',
     'alt=\\"A mesma fotografia antiga, alterada para o exercício: o pedestal está vazio.\\"', 4),
    ('cidadania/m2/cid-m2-preco-minuto/index.html', 'alt=\\"Jacquard machine for endless paper cards (Verdol system), Musée des arts et métiers, Paris. Photograph by David Monniaux, 2006.\\"',
     'alt=\\"Fotografia de uma máquina de Jacquard num museu: um mecanismo negro sobre pés torneados, com uma tira larga de papel perfurado a descer pela frente.\\"', 4),
    ('cidadania/m2/cid-m2-dentro-da-caixa/index.html', 'alt=\\"From book that tried to explain the illusions behind the Kempelen chess playing automaton (known as The Turk) after making reconstructions of the device.\\"',
     'alt=\\"Gravura de um autómato vestido à turca sentado a uma mesa de xadrez, com as portas do armário abertas a mostrar engrenagens.\\"', 4),
    # 5. Nagel: o registo legal no JSTOR, no lugar de uma cópia de legalidade incerta.
    ('cidadania/m2/aulas/04/index.html', '<a href="https://faculty.fiu.edu/~harveyb/What%20is%20it%20like%20to%20be%20a%20bat.htm">Nagel: texto de 1974, em inglês</a>',
     '<a href="https://www.jstor.org/stable/2183914">Nagel: o ensaio de 1974 no JSTOR, em inglês</a>', 5),
]


def aplicar(texto, pagina, rigoroso=True):
    """Aplica a «texto» (o conteúdo de «pagina») as correções dessa página. Devolve o texto corrigido."""
    for p, antes, depois, _ in CORRECOES:
        if p != pagina:
            continue
        if antes in texto:
            texto = texto.replace(antes, depois)
        elif depois not in texto and rigoroso:
            raise ValueError(pagina + ': nem o texto antigo nem o novo; rever a correção ' + antes[:60])
    return texto


def paginas():
    return sorted({p for p, *_ in CORRECOES})


LENTE = 'https://pedrohfernandes-klk.github.io/lente/'

# As imagens do M2 e a sua origem: âncoras para as sessões, e as duas fotografias que faltavam.
ANCORAS = [('chaleira', 'Chaleira elétrica, Peter Behrens'), ('declaracao', 'Declaração dos Direitos do Homem e do Cidadão, 1789'),
           ('hogarth', 'William Hogarth, The Laughing Audience'), ('turco', 'O Turco, o autómato'), ('lisboa-1907', 'Estátua do Duque da Terceira'),
           ('daumier', 'Honoré Daumier, litografia'), ('goya', 'Francisco de Goya, Caprichos'), ('jacquard', 'Uma máquina de Jacquard'),
           ('cabaret', 'Cartaz da abertura do Cabaret Voltaire'), ('lovelace', 'Ada Lovelace, retrato')]
CHALEIRA = ('<figure class="fig-cid"><img src="../../../img/cidadania/behrens.webp" alt="Fotografia: três chaleiras elétricas de metal martelado, de três tamanhos, com pegas de vime e tampas com puxador, sobre fundo neutro." width="1100" height="756" loading="lazy">'
            '<figcaption>Chaleira elétrica, Peter Behrens para a AEG, 1909. As chaleiras combinavam três formas, três acabamentos e três tamanhos: a imagem abre o passo zero e a sessão 01.<br>'
            'Autoria no registo: Christos Vittoratos. Direitos no registo: CC BY-SA 3.0. Consulta: 2026-10-28.<br><a href="https://commons.wikimedia.org/wiki/File:Behrens-aeg-wasserkocher.jpg">Consultar a proveniência e a declaração de direitos</a></figcaption></figure>')
LISBOA = ('<figure class="fig-cid"><img src="../../../img/cidadania/duque-1907.webp" alt="' + ALT_LISBOA + '" width="1100" height="825" loading="lazy">'
          '<figcaption>Estátua do Duque da Terceira, Lisboa, 1907: o original das duas fotografias do passo 04, num recorte de uma das metades da estereoscopia. A versão B, com o pedestal vazio, foi alterada por nós para o exercício.<br>'
          'Autoria no registo: H. C. White Co., estereoscopia n.º 11420. Direitos no registo: sem restrições conhecidas de publicação (domínio público). Consulta: 2026-10-28.<br><a href="' + LOC + '">Consultar a proveniência e a declaração de direitos</a></figcaption></figure>')


def imagens(ler, write):
    """Riscos 3 e 4: as imagens do M2 ganham âncoras para as sessões e as duas fotografias que faltavam."""
    p = 'cidadania/m2/imagens/index.html'
    s = ler(p)
    if 'behrens.webp' not in s:
        s = s.replace('<figure class="fig-cid">', CHALEIRA + '<figure class="fig-cid">', 1)
    if 'duque-1907.webp' not in s:
        i = s.index('<figcaption>Honoré Daumier, litografia')
        j = s.rindex('<figure class="fig-cid">', 0, i)
        s = s[:j] + LISBOA + s[j:]
    for ancora, legenda in ANCORAS:
        if 'id="' + ancora + '"' in s:
            continue
        i = s.index('<figcaption>' + legenda)
        j = s.rindex('<figure class="fig-cid">', 0, i)
        s = s[:j] + '<figure class="fig-cid" id="' + ancora + '">' + s[j + len('<figure class="fig-cid">'):]
    write(p, s)


# Palavras explicadas: os seis termos que faltavam ao glossário do M2 (definições dos casos e passos publicados).
TERMOS = [
    ('Conceito', 'Contexto', 'Os elementos que ajudam a compreender a função e a circulação de um conteúdo.', 'Oito segundos de uma peça de teatro, sem a cena completa, parecem uma ameaça.', 'cidadania/m2/cid-m2-o-contexto-em-falta/', 'Voltar ao caso «O contexto em falta»'),
    ('Contexto', 'Critério', 'O objetivo ou a regra que orienta uma decisão.', 'Ordenar os conteúdos pelo tempo médio ou pelas avaliações positivas.', 'cidadania/m2/cid-m2-a-regra-do-feed/', 'Voltar ao caso «A regra do feed»'),
    ('Incitamento ao ódio', 'Independência', 'Duas fontes são independentes quando uma não se limita a repetir a origem da outra.', 'Um blogue que cita uma notícia não é uma segunda confirmação.', 'cidadania/m2/cid-m2-o-rasto-da-afirmacao/', 'Voltar ao caso «O rasto da afirmação»'),
    ('Independência', 'Leitura lateral', 'Sair da página para ver, noutras fontes, quem a fez, quem paga e o que dizem os outros, antes de ler o conteúdo.', 'Abrir outro separador e procurar o nome do sítio antes de acreditar no que diz.', 'investigar/passo-08/', 'Abrir Como se investiga, passo 8'),
    ('Recurso', 'Sinal', 'O dado que uma regra usa para ordenar ou selecionar.', 'Na versão 2 do feed de papel, o sinal são os segundos em cada cartão.', 'cidadania/m2/cid-m2-a-regra-do-feed/', 'Voltar ao caso «A regra do feed»'),
    ('Transparência', 'Viragem', 'O momento do guião em que o público percebe a regra.', 'Entrada, regras, viragem, saída: a viragem vem antes da saída.', 'cidadania/m2/passo-06/', 'Voltar ao passo 06'),
]


def glossario(ler, write):
    """Risco 7: os seis termos em falta no glossário do M2."""
    from html import escape as e
    p = 'cidadania/m2/glossario/index.html'
    s = ler(p)
    for depois_de, termo, definicao, exemplo, alvo, volta in TERMOS:
        if '<dt>' + termo + '</dt>' in s:
            continue
        i = s.index('<div class="termo"><dt>' + depois_de + '</dt>')
        j = s.index('</div>', s.index('</dd>', i)) + len('</div>')
        novo = '<div class="termo"><dt>' + e(termo) + '</dt><dd>' + e(definicao) + '<span class="exemplo">Por exemplo: ' + e(exemplo) + '</span><span class="exemplo"><a href="' + LENTE + alvo + '">' + e(volta) + '</a></span></dd></div>'
        s = s[:j] + novo + s[j:]
    write(p, s)


def aplicar_tudo(ler, write):
    """Todas as correções: os textos exatos, as imagens e o glossário. «ler(caminho)» e «write(caminho, texto)»."""
    for pagina in paginas():
        write(pagina, aplicar(ler(pagina), pagina))
    imagens(ler, write)
    glossario(ler, write)
