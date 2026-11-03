"""02/11/2026: os cinco passos do método, partilhados pelas sessões e pela entrada."""
PASSOS = ['Juntar material', 'Trabalhar o material', 'Largar', 'A ideia aparece', 'Dar forma e pôr à prova']


def passos(hoje):
    return ('<ol class="passos-m" aria-label="Os cinco passos do método">'
            + ''.join(f'<li class="hoje" aria-current="step"><b>{n}</b> {t} <span class="hoje-t">hoje</span></li>' if n in hoje
                      else f'<li><b>{n}</b> {t}</li>' for n, t in enumerate(PASSOS, 1)) + '</ol>')



# 02/11/2026: decisões 97 e 112. Os mesmos três critérios, sem nota, nos cartões e nos documentos.
CRITERIOS = {
    1: ['Os dez factos são verificáveis, sem opinião, um por nota.',
        'As três inferências apoiam-se em dois factos cada. A pergunta a que o lugar não responde fica registada.',
        'Um colega confirma ou desmente os factos; outra pessoa confere os degraus.'],
    2: ['As quinze notas distinguem observação de inferência e cobrem as três categorias.',
        'A linha permite reconhecer o teu «cocheiro»; se não, é revista depois da prova.',
        'As duas versões do conselho estão comparadas: o que mudou e o que ficou.'],
}


def esta_bom(n):
    from html import escape
    criterios = CRITERIOS[n]
    assert len(criterios) == 3
    return '<div class="esta-bom"><p><b>Está bom quando…</b></p><ul>' + ''.join('<li>' + escape(c) + '</li>' for c in criterios) + '</ul></div>'


def para_caixa(texto):
    from html import escape
    return '<aside class="para-caixa"><p><b>Para a tua caixa</b></p><p>' + escape(texto) + '</p></aside>'
