"""02/11/2026: decisão 115, sem pontos também nas peças com motor incorporado.
Transformação idempotente e limitada à apresentação; respostas e registos conservados.
"""
import re


def aplicar(s):
    if 'EPIJogo.montar(' not in s or 'assets/licoes/jogo.js' in s:
        return s
    # As duas versões existentes diferem só no suporte de semPontos dos treinos.
    if 'var soLer=!nFazer();' in s:
        s = s.replace('var soLer=!nFazer();', 'var soLer=!nFazer()||cfg.semPontos;')
        s = s.replace('pontos:ganho?"+"+ganho+" pontos":""', 'pontos:ganho&&!cfg.semPontos?"+"+ganho+" pontos":""')
        s = s.replace('Lido até ao fim.</p>', "'+(cfg.semPontos?\"Atividade feita.\":\"Lido até ao fim.\")+'</p>", 1)
        inicio = s.index('if(st.lida&&cfg.mostrarAnterior!==false)')
        a = s.index('</span></p><p class="grande">', inicio)
        b = s.index("'+(cfg.depois?", a)
        antigo = s[a+len('</span></p>'):b]
        s = s[:a] + "</span></p>'+(cfg.semPontos?'<p>Atividade feita.</p>':'" + antigo + "')+" + s[b+2:]
    if 'cfg.semPontos' not in s or 'var soLer=!nFazer()||cfg.semPontos;' not in s:
        raise ValueError('Motor incorporado desconhecido: não alterar sem revisão')
    # A opção fica junto da chamada, sem reconstruir o banco de cartões.
    s = re.sub(r'EPIJogo\.montar\(\{(?!semPontos:true,)', 'EPIJogo.montar({semPontos:true,', s)
    s = s.replace('t:"Mais uma pista <small>(passa a valer 20)</small>"', 't:cfg.semPontos?"Mais uma pista":"Mais uma pista <small>(passa a valer 20)</small>"')
    s = s.replace('bp.innerHTML="Mais uma pista <small>(passa a valer 10)</small>"', 'bp.innerHTML=cfg.semPontos?"Mais uma pista":"Mais uma pista <small>(passa a valer 10)</small>"')
    # A projeção começa do início e não grava nem chama o registo antigo no fim.
    proj = '/[?&]projetar=1(&|$)/.test(location.search)||window.self!==window.top'
    if 'function montar(cfg){\n var PROJ=' not in s:
        s = s.replace('function montar(cfg){', 'function montar(cfg){\n var PROJ=' + proj + ';', 1)
    s = s.replace('var st=ler(K)||{};', 'var st=(PROJ?null:ler(K))||{};')
    s = s.replace('function gravar(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(x){}}',
                  'function gravar(k,v){if(' + proj + ')return;try{localStorage.setItem(k,JSON.stringify(v))}catch(x){}}')
    s = s.replace('if(cfg.fim&&!soErrados)cfg.fim(st)', 'if(cfg.fim&&!soErrados&&!PROJ)cfg.fim(st)')
    return s
