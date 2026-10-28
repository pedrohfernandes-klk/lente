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

Revisão de 28/10/2026 (quatro revisores; tudo aberto e conferido nesta sessão):
- ver-para-fazer/v62/ é um vídeo «Em revisão» (entrevista de 1 minuto sobre «Plug-in», no MAAT): a ligação do passo 00
  sai, em vez de passar para lá (o passo já tem o vídeo opcional «Arte ou design?»).
- gutenberg.org/ebooks/74223 é um número de 1886 do Chambers's Journal, não as notas de Lovelace; a transcrição
  Fourmilab (já usada em gigantes/lovelace e investigar/passo-04) abre o «Sketch» com as «Notes by the Translator».
- A gravura de Racknitz (Commons, Racknitz_-_The_Turk_3.jpg, 1789) desenha em corte o homem escondido no armário: o
  texto alternativo que só falava de engrenagens estava errado.
- Haeckel, Chiroptera (Commons, Haeckel_Chiroptera.jpg): Kunstformen der Natur, 1904, prancha 67; PD-old-100.
- Library of Congress, item 2021640877: «H. C. White & Co., publisher»; no cartão, «Copyright 1907 by J. J. Killelea & Co.».
"""
from cidadania_m2_molde import ALT_TURCO, LISBOA_1907

LOC_ANTIGO = 'https://www.loc.gov/item/2021640870/'
LOC = 'https://www.loc.gov/item/2021640877/'
ALT_LISBOA = 'Fotografia antiga: a estátua do Duque da Terceira sobre o pedestal, numa praça de Lisboa, com homens de chapéu à volta.'
FEED_PT = 'https://pedrohfernandes-klk.github.io/pt/cidadania/ferramentas/m2-aula-01-feed/'
FEED = 'https://pedrohfernandes-klk.github.io/lente/cidadania/ferramentas/m2-aula-01-feed/'
CC_BY_SA = 'https://creativecommons.org/licenses/by-sa/3.0'
LOVELACE_ERRADA = '<a href=\\"https://www.gutenberg.org/ebooks/74223\\">Ada Lovelace, notas de 1843 (tradução do memorando de Menabrea), Project Gutenberg</a>'
LOVELACE = '<a href=\\"https://www.fourmilab.ch/babbage/sketch.html\\">Ada Lovelace, notas de 1843 (tradução do memorando de Menabrea), transcrição Fourmilab</a>'

# (página, texto antigo, texto novo, risco do plano)
CORRECOES = [
    # 1. Âncora partida no passo 00. 28/10/2026: o vídeo que a âncora queria (v62) está «em revisão» e fora do
    #    contexto do passo; a ligação sai (o passo já tem «Arte ou design?»). Texto vazio: remove-se.
    ('cidadania/m2/passo-00/index.html', '<p class=\\"fonte\\"><a href=\\"https://pedrohfernandes-klk.github.io/lente/ver-para-fazer/#arte\\">Ver Joana Vasconcelos e comparar arte, tecnologia e lugar →</a></p>', '', 1),
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
     'alt=\\"' + ALT_TURCO + '\\"', 4),
    # 4. 28/10/2026: o texto alternativo do Turco omitia o homem escondido, que é o que a gravura mostra.
    ('cidadania/m2/passo-04/index.html', 'alt=\\"Gravura de um autómato vestido à turca sentado a uma mesa de xadrez, com as portas do armário abertas a mostrar engrenagens.\\"',
     'alt=\\"' + ALT_TURCO + '\\"', 4),
    ('cidadania/m2/imagens/index.html', 'alt="Gravura de um autómato vestido à turca sentado a uma mesa de xadrez, com as portas do armário abertas a mostrar engrenagens."',
     'alt="' + ALT_TURCO + '"', 4),
    ('cidadania/m2/imagens/index.html', 'Dentro da caixa escondia-se um jogador humano.', 'Dentro da caixa escondia-se uma pessoa.', 4),
    # 3. 28/10/2026: a página tem também imagens com licença livre (CC BY-SA 3.0), e a licença leva a sua ligação.
    ('cidadania/m2/imagens/index.html', '<p class="p-sub">Domínio público: a imagem também é uma fonte</p>',
     '<p class="p-sub">Domínio público e licenças livres: a imagem também é uma fonte</p>', 3),
    ('cidadania/m2/imagens/index.html', 'Autoria no registo: David Monniaux. Direitos no registo: CC BY-SA 3.0.',
     'Autoria no registo: David Monniaux. Direitos no registo: <a href="' + CC_BY_SA + '" rel="license">CC BY-SA 3.0</a>.', 3),
    # 4. 28/10/2026: no passo 04, o texto alternativo de B («A mesma fotografia antiga, com o pedestal vazio») dizia
    #    a quem usa leitor de ecrã qual era a cópia; os dois passam a descrever só o que se vê, como na sessão 05.
    ('cidadania/m2/passo-04/index.html', '"alt": "Fotografia antiga: a estátua do Duque da Terceira sobre o pedestal, homens de chapéu à volta.", "rotulo": "A"',
     '"alt": "' + LISBOA_1907['a']['alt'] + '", "rotulo": "A"', 4),
    ('cidadania/m2/passo-04/index.html', '"alt": "A mesma fotografia antiga, com o pedestal vazio.", "rotulo": "B"',
     '"alt": "' + LISBOA_1907['b']['alt'] + '", "rotulo": "B"', 4),
    # 3. 28/10/2026: as notas de Lovelace (o n.º 74223 do Project Gutenberg é outro livro).
    ('cidadania/m2/passo-01/index.html', LOVELACE_ERRADA, LOVELACE, 3),
    ('cidadania/m2/passo-07/index.html', LOVELACE_ERRADA, LOVELACE, 3),
    # 5. Nagel: o registo legal no JSTOR, no lugar de uma cópia de legalidade incerta.
    ('cidadania/m2/aulas/04/index.html', '<a href="https://faculty.fiu.edu/~harveyb/What%20is%20it%20like%20to%20be%20a%20bat.htm">Nagel: texto de 1974, em inglês</a>',
     '<a href="https://www.jstor.org/stable/2183914">Nagel: o ensaio de 1974 no JSTOR, em inglês</a>', 5),
    # 28/10/2026 (confirmação final): o cartaz do Cabaret Voltaire diz «Allabendlich (mit Ausnahme von Freitag)»;
    #    a tradução passa a dizer a exceção da sexta-feira.
    ('cidadania/m2/imagens/index.html', '«todas as noites, música, conferências e recitações»',
     '«todas as noites (exceto à sexta-feira), música, conferências e recitações»', 1),
    ('cidadania/m2/passo-08/index.html', '«todas as noites, música, conferências e recitações»',
     '«todas as noites (exceto à sexta-feira), música, conferências e recitações»', 1),
    # 28/10/2026 (pendentes do #65): «jogador» sai também do passo 04 e da revisão, como saiu da página das imagens;
    #    o Turco escondia uma pessoa (a gravura de Racknitz mostra-a em corte).
    ('cidadania/m2/passo-04/index.html', 'escondia um jogador humano', 'escondia uma pessoa', 1),
    ('cidadania/m2/passo-04/index.html', 'Dentro da caixa escondia-se um jogador humano.', 'Dentro da caixa escondia-se uma pessoa.', 1),
    ('cidadania/m2/passo-04/index.html', 'um jogador humano movia as peças', 'uma pessoa movia as peças', 1),
    ('cidadania/m2/passo-04/index.html', 'para concluir que havia um jogador escondido', 'para concluir que havia alguém escondido', 1),
    ('cidadania/m2/passo-04/index.html', 'porque um jogador escondido movia as peças', 'porque uma pessoa escondida movia as peças', 1),
    ('cidadania/m2/passo-04/index.html', 'mas não revelava o jogador escondido', 'mas não revelava a pessoa escondida', 1),
    ('cidadania/m2/revisao/index.html', 'porque um jogador escondido movia as peças', 'porque uma pessoa escondida movia as peças', 1),
    # 28/10/2026 (pendentes do #65): na definição de «Suposição», o infinitivo concorda com «tu».
    ('cidadania/m2/glossario/index.html', 'O que achas que aconteceu sem o poder confirmar.', 'O que achas que aconteceu, sem o poderes confirmar.', 1),
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
           ('cabaret', 'Cartaz da abertura do Cabaret Voltaire'), ('lovelace', 'Ada Lovelace, retrato'), ('haeckel', 'Ernst Haeckel, Chiroptera')]
CHALEIRA = ('<figure class="fig-cid"><img src="../../../img/cidadania/behrens.webp" alt="Fotografia: três chaleiras elétricas de metal martelado, de três tamanhos, com pegas de vime e tampas com puxador, sobre fundo neutro." width="1100" height="756" loading="lazy">'
            '<figcaption>Chaleira elétrica, Peter Behrens para a AEG, 1909. As chaleiras combinavam três formas, três acabamentos e três tamanhos: a imagem abre o passo zero e a sessão 01.<br>'
            'Autoria no registo: Christos Vittoratos. Direitos no registo: <a href="' + CC_BY_SA + '" rel="license">CC BY-SA 3.0</a>. Consulta: 2026-10-28.<br><a href="https://commons.wikimedia.org/wiki/File:Behrens-aeg-wasserkocher.jpg">Consultar a proveniência e a declaração de direitos</a></figcaption></figure>')
LISBOA = ('<figure class="fig-cid"><img src="../../../img/cidadania/duque-1907.webp" alt="' + ALT_LISBOA + '" width="1100" height="825" loading="lazy">'
          '<figcaption>Estátua do Duque da Terceira, Lisboa, 1907: o original das duas fotografias do passo 04, num recorte de uma das metades da estereoscopia. Uma das duas versões do passo 04 foi alterada por nós para o exercício.<br>'
          'Autoria no registo: H. C. White &amp; Co., como editora; estereoscopia n.º 11420, com «Copyright 1907 by J. J. Killelea &amp; Co.» no cartão. Direitos no registo: sem restrições conhecidas de publicação (domínio público). Consulta: 2026-10-28.<br><a href="' + LOC + '">Consultar a proveniência e a declaração de direitos</a></figcaption></figure>')
HAECKEL = ('<figure class="fig-cid"><img src="../../../img/ter-juizo/haeckel-chiroptera.webp" alt="Gravura a preto e branco: no alto, um morcego de asas abertas; à volta e por baixo, cabeças de morcegos de várias espécies, com orelhas enormes e pregas de pele no nariz." loading="lazy">'
           '<figcaption>Ernst Haeckel, Chiroptera, em Kunstformen der Natur, 1904, prancha 67: cabeças de morcegos de várias espécies, desenhadas com todo o pormenor. A imagem abre a sessão 04: o que se sabe de um animal só por o ver, e o que nenhum desenho mostra.<br>'
           'Autoria no registo: Ernst Haeckel. Direitos no registo: domínio público. Consulta: 2026-10-28.<br><a href="https://commons.wikimedia.org/wiki/File:Haeckel_Chiroptera.jpg">Consultar a proveniência e a declaração de direitos</a></figcaption></figure>')


def imagens(ler, write):
    """Riscos 3 e 4: as imagens do M2 ganham âncoras para as sessões e as fotografias que faltavam (a chaleira, Lisboa
    1907 e, desde 28/10/2026, a gravura de Haeckel da sessão 04)."""
    p = 'cidadania/m2/imagens/index.html'
    s = ler(p)
    if 'behrens.webp' not in s:
        s = s.replace('<figure class="fig-cid">', CHALEIRA + '<figure class="fig-cid">', 1)
    if 'duque-1907.webp' not in s:
        i = s.index('<figcaption>Honoré Daumier, litografia')
        j = s.rindex('<figure class="fig-cid">', 0, i)
        s = s[:j] + LISBOA + s[j:]
    if 'haeckel-chiroptera.webp' not in s:  # 28/10/2026: a imagem da sessão 04, antes do Turco (a da 05)
        i = s.index('<figcaption>O Turco, o autómato')
        j = s.rindex('<figure class="fig-cid"', 0, i)
        s = s[:j] + HAECKEL + s[j:]
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
    # 28/10/2026: «Verificação lateral», como o título de Como se investiga, passo 8, e como as sessões dizem.
    ('Transparência', 'Verificação lateral', 'Sair da página para ver, noutras fontes, quem a fez, quem paga e o que dizem os outros, antes de ler o conteúdo.', 'Abrir outro separador e procurar o nome do sítio antes de acreditar no que diz.', 'investigar/passo-08/', 'Abrir Como se investiga, passo 8'),
    ('Recurso', 'Sinal', 'O dado que uma regra usa para ordenar ou selecionar.', 'Na versão 2 do feed de papel, o sinal são os segundos em cada cartão.', 'cidadania/m2/cid-m2-a-regra-do-feed/', 'Voltar ao caso «A regra do feed»'),
    ('Verificação lateral', 'Viragem', 'O momento do guião em que o público percebe a regra.', 'Numa peça em que só avança quem é aplaudido, a viragem é o momento em que o público olha para trás e percebe a regra.', 'cidadania/m2/passo-06/', 'Voltar ao passo 06'),
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
