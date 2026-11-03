"""03/11/2026: integração das quatro sessões revistas, sem substituir arquivos.

O índice abre as lições reais. As sessões e os pilotos anteriores conservam
endereços, ficheiros e chaves. O gerador principal aplica esta camada no fim.
"""
from pathlib import Path
import html
import json
import re
import licoes_lente as L

ROOT = Path(__file__).resolve().parents[1]
e = html.escape

def bancos():
    return [json.loads(p.read_text('utf-8')) for p in sorted((ROOT/'tools/cidadania-interativas').glob('*.json'))]

def titulo(d):
    return d['titulo'].split(': ', 1)[-1]

def instalar_indice(s):
    # Um destino por sessão; não duplicar o catálogo nem apagar as outras seis.
    for n,d in enumerate(bancos(),1):
        ident=f'{n:02}'
        pattern=r'(<li class="c10-card" data-session-card="'+ident+r'">)(.*?)(</li>)'
        def cartao(m):
            corpo=m[2]
            corpo=re.sub(r'href="[^"]+"', 'href="licoes/'+ident+'/"', corpo, count=1)
            corpo=re.sub(r'<h3>.*?</h3>', '<h3>'+e(titulo(d))+'</h3>', corpo)
            corpo=re.sub(r'<span class="c10-topic">.*?</span>', '<span class="c10-topic">Sessão interativa</span>', corpo)
            corpo=re.sub(r'<span class="c10-card-q">.*?</span>', '<span class="c10-card-q">Observar, experimentar e concluir.</span>', corpo)
            return m[1]+corpo+m[3]
        s,count=re.subn(pattern,cartao,s,flags=re.S)
        assert count==1, 'cartão ausente ou duplicado: '+ident
    s=re.sub(r'<a class="c10-action" href="[^"]+" data-continue>.*?</a>', '<a class="c10-action" href="licoes/01/" data-continue>Começar na sessão 01</a>',s)
    s=s.replace('assets/cidadania-m1-sessoes.js?v=20261027-molde-2','assets/cidadania-interativas-indice.js?v=20261103-1')
    if 'data-interativas-fontes' not in s:
        s=s.replace('<footer class="c10-support">','<footer class="c10-support"><a data-interativas-fontes href="licoes/docente/">Guia das sessões interativas 01 a 04</a><a href="licoes/guiao/">Registo breve em papel</a>')
    return s

def pagina_guia(docente):
    partes=[]
    for n,d in enumerate(bancos(),1):
        final=d['cartoes'][-1]['html']
        texto=('<p>Materiais antes das perguntas. Vinte cartões, catorze atividades de cinco tipos. Apoiar a leitura dos materiais e pedir uma prova para cada conclusão; não exigir escrita extensa durante os exercícios.</p>'
               '<p>A duração depende do uso em turma e não está aferida.</p>'
               '<h3>Fontes e limites</h3><p>'+L.esc_it(d['fontes'])+'</p><details open><summary>Materiais da sessão</summary>'+''.join('<h3>'+e(c.get('titulo',c.get('rot','Ler')))+'</h3>'+c['html'] for c in d['cartoes'][:-1] if c['t']=='ler')+'</details>' if docente else '')
        partes.append('<section id="sessao-'+f'{n:02}'+'"><h2>'+e(d['titulo'])+'</h2><a href="../'+f'{n:02}'+'/">Abrir a sessão</a>'+texto+final+'<div class="linhas" aria-label="Espaço para o registo em papel"><hr><hr><hr></div></section>')
    nome='Guia das sessões interativas' if docente else 'Registo breve em papel'
    return ('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+nome+' | Humanos | Lente</title>'
            '<link rel="stylesheet" href="../../../../assets/appearance.css"><script src="../../../../assets/appearance.js"></script>'
            '<style>body{font:18px/1.55 Arial,sans-serif;background:var(--papel,#fff);color:var(--tinta,#111);margin:0}main{max-width:72ch;margin:auto;padding:24px;overflow-wrap:anywhere}a{color:inherit;display:inline-block;min-height:44px}img{max-width:100%;height:auto}summary{cursor:pointer;min-height:44px}section{border-top:1px solid;padding:24px 0}h1{font-size:2rem;line-height:1.15}h2{font-size:1.5rem;line-height:1.2}.linhas hr{margin:36px 0;border:0;border-bottom:1px solid}.credito{font-size:1rem}@media print{nav,section>a{display:none}section{break-before:page;border:0}.linhas hr{margin:30px 0}body{font-size:12pt}main{padding:0}}</style></head><body><main><nav><a href="../../">Humanos</a></nav><h1>'+nome+'</h1><p>Sessões 01 a 04. Os casos e simulações estão identificados nos materiais. As sessões 05 a 10 mantêm o formato anterior.</p>'+''.join(partes)+'</main></body></html>\n')

def gerar():
    for d in bancos():
        erros=L.validar(d)
        if erros:raise ValueError(d['id']+': '+str(erros))
        p=ROOT/d['saida'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(L.pagina(d).encode('utf-8'))
    p=ROOT/'cidadania/m1/index.html';p.write_bytes(instalar_indice(p.read_text('utf-8')).encode('utf-8'))
    for docente,pasta in [(True,'docente'),(False,'guiao')]:
        p=ROOT/'cidadania/m1/licoes'/pasta/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(pagina_guia(docente).encode('utf-8'))

if __name__=='__main__':
    gerar()
    print('Quatro sessões reais, índice, guia e registo em papel gerados; versões anteriores preservadas.')
